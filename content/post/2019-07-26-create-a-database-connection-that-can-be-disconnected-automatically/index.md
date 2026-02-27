---
title: 创建一个能自动断开的数据库连接
author: 谭显英
date: '2019-07-26'
slug: create-a-database-connection-that-can-be-disconnected-automatically
originalLang: en
categories:
  - 技术
tags:
  - R
  - programming
  - tech
---

数据库连接是一种资源。虽然数据库会自动释放空闲连接，但最好还是自己主动释放。否则，可能会严重影响数据库的性能。

在使用完毕后显式关闭连接是可以的，但太过冗长。而且，这种方式无法保证连接一定会被释放——想象一下，你的代码在关闭连接那行之前就抛出了错误。在 CPP 中，一个好的做法是通过将资源的使用封装到对象中来管理资源，这样只要对象离开作用域，资源就会被释放。这种技术叫做 [RAII（Resource Acquisition Is Initialization，资源获取即初始化）](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r1-manage-resources-automatically-using-resource-handles-and-raii-resource-acquisition-is-initialization)。

我并不热衷于在 R 中使用对象。但 RAII 的思想很简单——在“某个东西”结束时执行一些操作。而那个“某个东西”也可以是一个函数。`on.exit()` 就是那个在当前函数退出时注册表达式的魔法（实际上，它是在调用环境退出时被调用的，所以你也可以使用 `local({...})`）。即使函数抛出错误，该表达式也保证会被执行。因此我们可以把代码改进成这样：

```r
data_a <- local({
  conn <- DBI::dbConnect(...)
  on.exit(DBI::dbDisconnect(conn), add = TRUE)
  DBI::dbGetQuery(...)
})
```

看起来不错，但想象一下，如果你有好几个不同的数据库并且使用很多不同的表，你就不得不一遍又一遍地写那个 `on.exit()`。所以问题就变成了：*如何编写一个包装函数来创建连接，使其在调用帧结束时自动断开*。这意味着我们要在 `parent.frame()` 上注册 `on.exit()`。相信我，这不是一件容易的事……感谢 `withr::defer()`，我们不需要了解背后的复杂性。所以可以简化为：

```r
activate_conn <- function(...) {
  conn <- DBI::dbConnect(...)
  withr::defer(try(DBI::dbDisconnect(conn)), envir = parent.frame(), priority = "last")
  conn
}
data_a <- local({
  DBI::dbGetQuery(activate_conn(...), ...)
})
data_b <- local({
  DBI::dbGetQuery(activate_conn(...), ...)
})
data_c <- local({
  DBI::dbGetQuery(activate_conn(...), ...)
})
```
已经足够好了，不是吗？唯一的问题是 `withr::defer()` 在 `.GlobalEnv` 中不起作用，因为 `.GlobalEnv` 不能被删除，只有在 R 会话结束时才会退出。但有时候在全局环境中用一个连接来测试代码会更方便。我认为 `RODBC` 和 `DBI` 包含了在垃圾回收时释放连接的机制，但我不太确定。所以让我们借助 `reg.finalizer()` 在垃圾回收或 R 会话结束时注册一个终结器函数（今天刚好在 [Twitter](https://twitter.com/henrikbengtsson/status/1154692874816110592?s=20) 上发现了它）。

这就是我们最终的连接器，只要我们不再需要它，它就会自动断开连接！

#### 终结器注册

```r
# use close_fun so that it not only works for DBI but could also be used for RODBC, etc.
reg_conn_finalizer <- function(conn, close_fun, envir) {
  is_parent_global <- identical(.GlobalEnv, envir)
  if (isTRUE(is_parent_global)) {
    env_finalizer <- new.env(parent = emptyenv())
    env_finalizer$conn <- conn
    attr(conn, 'env_finalizer') <- env_finalizer
    reg.finalizer(env_finalizer, function(e) {
      print('global finalizer!')
      try(close_fun(e$conn))
    }, onexit = TRUE)
  } else {
    withr::defer({
      print('local finalizer!')
      try(close_fun(conn))
    }, envir = envir, priority = "last")
  }
  conn
}
```

#### 连接器

```r
# build connection that will be automatically destroyed
activate_conn <- function(...) {
  conn <- DBI::dbConnect(...)
  reg_conn_finalizer(conn, DBI::dbDisconnect, parent.frame())
}
```

#### 来测试一下

##### 局部环境

```r
local({
  invisible(activate_conn(RSQLite::SQLite(), ':memory:'))
})
```

```text
[1] "local finalizer!"
```

##### 全局环境 - 删除对象

```r
conn <- activate_conn(RSQLite::SQLite(), ':memory:')
rm(conn)
invisible(gc())
```

```text
[1] "global finalizer!"
```

##### 全局环境 - R 会话结束

```r
# This chunk will not be evaluated because we don't want the render engine to exit :P
invisible(activate_conn(RSQLite::SQLite(), ':memory:'))
q(save = 'no')
```
