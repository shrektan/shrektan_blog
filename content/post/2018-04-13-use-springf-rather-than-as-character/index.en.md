---
title: Use sprintf() rather than as.character()
subtitle: when you need to convert a number to a string sophisticatedly in R
author: Xianying Tan
date: '2018-04-12'
slug: use-sprintf-rather-than-as-character
originalLang: en
categories:
tags:
  - R
  - programming
  - note
---

Converting a number to a string is easy. In many cases, you don't even need to call the converting functions explicitly. However, when it comes to sophisticatedly control the output, you may find `as.character()` is not enough and `sprintf()` is the cure. I'll give some real world use cases to demostrate.

### Case 1: Always display 2 digits for a number

For example, if the investment return in a report displays `1%`, it's natural to ask whether the real number is `1.00%` or `1.xx%`. Here `sprintf("%0.2f", x)` can help.

```r
as.character(c(0.1, 1.0))
# [1] "0.1" "1"  
sprintf("%0.2f", c(0.1, 1.0))
# [1] "0.10" "1.00"
sprintf("%0.2f%%", c(0.001, 0.01) * 100) # even nicer use double `%` to escape 
# [1] "0.10%" "1.00%"
```

### Case 2: Display an integer as `000000`

For example, you need to convert some integers to the stock codes of China A shares. Use `sprintf("%06d", x)`.

```r
as.character(0:3)
#> [1] "0" "1" "2" "3"
sprintf("%06d", 0:3)
#> [1] "000000" "000001" "000002" "000003"
```

### Case 3: You don't want the scientific formating for a large number. 

Use `sprintf("%d")` or `sprintf("%.0f")`. 

```r
x <- c(1e+05, 1e+06, 1e+07)
as.character(x)
#> [1] "1e+05" "1e+06" "1e+07"
sprintf("%d", x)
#> [1] "100000"   "1000000"  "10000000"
sprintf("%.0f", x)
#> [1] "100000"   "1000000"  "10000000"
sprintf("%s", x) # see the explaination below
#> [1] "1e+05" "1e+06" "1e+07"
```

The letter `s` is used to denote the string type. The reason of `sprintf("%s", 1e5)` works is that R will convert the number `1e5` to the string `"1e5"` silently before pass it to the `sprintf()` C rountine. So `sprintf("%s", x)` is kind of identical to `as.character(x)`.

`sprintf()` is powerful although it's a bit of confusing to learn. See `help("sprintf")` for more info.

**UPDATE** If you need to print numbers like `1,900.00`, you may find `prettyNum()` or `format()` helpful.
