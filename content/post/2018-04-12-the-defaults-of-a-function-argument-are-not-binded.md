---
title: The defaults of a function argument are not binded
author: Xianying Tan
date: '2018-04-12'
slug: the-defaults-of-a-function-argument-are-not-binded
categories:
  - programming
  - tech
  - note
tags:
  - R
---

When writing a function in R, it's good to provide commonly appropriate default values for the arguments so that the user could call the function conviniently in most cases. However, if you happen to have some functions sharing the same default values, you may be lured to create a variable (e.g., `opts`) and assign those default values to this variable.

The code looks good, runs well, works fine. Until one day, the little `opts` gets redefined somewhere... 

```r
opts <- c("a", "b")
your_fun <- function(x  = opts) { x }
your_fun()
# "a" "b"
opts <- c("b", "c")
your_fun()
# "b" "c"
```

If you defined the `opts` inside of an R package and didn't export it, you would find that your code works great under `devtools::load_all()` but fails ruthlessly after the package being built and reloaded, complaining _can't find `opts`_. 

**UPDATE** Thanks Yihui for pointing out my mistake. It will complain only when you use `match.arg(x)` (by omitting the param `choices`). Except this, normally it should be safe to use inside of a package, because the function will only look up the defaults variable at the environment where it's defined.

I create a simple example to demostrate this. 

```r
test1 <- local({
  opts <- c("a", "b", "c")
  function(x = opts) print(x)
})
test2 <- local({
  opts <- c("a", "b", "c")
  function(x = opts) print(match.arg(x))
})
test3 <- local({
  function(x = c("a", "b", "c")) print(match.arg(x))
})
test1()
#> [1] "a" "b" "c"
test2() # match.arg() will try to find the `opts` in the calling frame so fails
#> Error in eval(formal.args[[as.character(substitute(arg))]]): object 'opts' not found
test3()
#> [1] "a"
opts <- c("d", "e", "f")
test1() # finds `opt` in the envir where test1() gets defined
#> [1] "a" "b" "c"
test2()
#> Error in match.arg(x) : 'arg' must be of length 1 
test2("d") 
#> "d"
```

So here's the suggestion:

- Be attention to use a variable as the default value if the working envir is the same as your function's defining envir, because your variable may get changed unintentionally.
- Normally it's ok to use in a package as the plain default value. However, if you are providing a set of opts with `match.arg()`, you should write it like:  

    ```r
    your_fun <- function(x) {
      x <- match.arg(x, choices = opts)
    }
    ```  
    instead of  
    
    ```r
    your_fun <- function(x = opts) {
      x <- match.arg(x)
    }
    ```
