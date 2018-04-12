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

If you defined the `opts` inside of an R package and didn't export it, you would find that your code works great under `devtools::load_all()` but fails ruthlessly after the package being built and reloaded, reporting _can't find `opts`_. 

I can't find any documentation about this. Apparently, the defaults are evaluated at the time the function being called rather than being binded to the function at the time of defining.

**Simply do not use anything other than literals as the default values.** :joy:	
