---
title: 在 plumber API 中使用 `base::serialize()`
author: 谭显英
date: '2018-11-14'
slug: use-base-serializer-in-the-plumber-api
originalLang: en
categories:
  - 技术
tags:
  - R
  - web
  - programming
  - sharing
  - tech
---

最近，我需要把服务器上的一个 R 模型分享给使用 R 的同事。我立刻想到了 [Plumber](https://www.rplumber.io)。用 plumber 构建 Web API 非常简单。我很喜欢它用 roxygen 风格来定义 API 的方式，既优雅又易于维护。

通常，Web API 使用 [JSON](http://json.org/) 来表示数据。然而不幸的是，JSON 将对象编码为字符串，这可能导致信息丢失。例如，属性（除了 names 之外）无法被保留。这会带来一些麻烦：

- 用户在解析 JSON 结果后，必须显式地设置回属性，因为在纯 JSON 格式中无法分辨 `["2018-11-15"]` 是一个字符串还是一个日期。或者你不得不将所有属性存储在一个单独的列表中，既繁琐又容易出错。

- 有些问题很难解决，比如你无法在 JSON 中表示一个零行的 dataframe（`jsonlite::toJSON(iris[0,])` 返回 `[]`）。你必须自己处理这类边界情况。

- 将大型 R 对象解析为 JSON 可能非常慢[^1]。

幸运的是，我所有的“客户端”（我的同事们）都是 R 用户，所以我并不真正需要一个通用的 Web API。JSON 只是众多[序列化](https://en.wikipedia.org/wiki/Serialization)对象的方法之一，我并不受它的约束。由于 `base::saveRDS()` 的存在，我知道 R 本身一定提供了一种序列化方法——唯一不确定的是这个方法是否被导出了。幸运的是，稍加搜索便找到了 `base::serialize()` 和 `base::unserialize()`，正是我需要的。

我的解决方案在下面的代码中给出。由于 rds 文件几乎是 R 对象的无损表示（外部指针是例外），使用 `base::serialize()` 作为 plumber API 的自定义序列化器，可以最大限度地减少为 R 用户建立稳定 plumber API 所需的工作量。

开用吧！

[^1]: 创建一个大的 double 向量 `v <- rnorm(1e8)`，在我的电脑上 `system.time(invisible(jsonlite::toJSON(v)))` 耗时 27 秒，而 `system.time(invisible(serialize(v, NULL)))` 不到 4 秒。

## 更新 @2020/03/21

截至撰写本文时，`plumber` 的开发版本已经新增了原生的 `rds` 序列化器。

---

## 示例代码（同时 POST 和返回 R 对象）

- 将所有脚本放在同一个文件夹下。
- 执行 `main.R` 启动 API 服务器。
- 执行 `client.R` 测试 API。

### plumber.R

```r
#* @post /api
#* @serializer rds
function(req) {
  req$robj
}
```

### main.R

（在实际使用中，你可能需要在里面加一个条件判断。一个好的示例是：https://github.com/jcpsantiago/protopretzel/blob/master/R/protobuf_filter.R）

```r
library(plumber)
x <- plumb("plumber.R")
x$filter("robj", function(req) {
  req$rook.input$rewind()
  req$robj <- unserialize(req$rook.input$read())
  plumber::forward()
})
x$run(debug = TRUE, port = 9999)
```

### client.R

```r
out <- httr::POST(
  "http://127.0.0.1:9999/api",
  encode = "raw",
  body = serialize(iris, NULL),
  httr::content_type("application/octet-stream")
)
# 你可能需要先检查 httr::status_code() == 200L
# 或者 is.raw(httr::content(out)) 是否为 TRUE
base::unserialize(httr::content(out))
```
