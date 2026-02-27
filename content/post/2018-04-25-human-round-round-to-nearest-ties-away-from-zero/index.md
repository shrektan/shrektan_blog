---
title: '"人类的四舍五入"——最近偶数舍入 vs 四舍五入'
author: 谭显英
date: '2018-04-25'
slug: human-round-round-to-nearest-ties-away-from-zero
originalLang: en
categories:
  - 技术
tags:
  - R
  - programming
  - note
---

你有没有注意到，在 R 中 `base::round(2.5)` 和 `base::round(1.5)` 的返回值都是 `2`？是不是觉得很奇怪？至少我在学校里只学过一种舍入规则，就是"四舍五入"。意思是小数部分达到五就进位，四则舍去。


通过阅读 `base::round()` 的[文档](https://www.rdocumentation.org/packages/base/versions/3.5.0/topics/Round)，我们可以了解到有一个叫做 _"IEEE 754"_ 的标准，而 `base::round()` 使用的舍入规则叫做 _"go to the even digit"_（银行家舍入法，即向最近的偶数舍入）。

> Note that for rounding off a 5, the IEC 60559 standard (see also 'IEEE 754') is expected to be used, 'go to the even digit'.


搜索 _"IEEE 754"_ 会找到[维基百科页面](https://en.wikipedia.org/wiki/IEEE_754#Rounding_rules)，其中列出了五种舍入规则。_"To nearest, ties away from zero"_（四舍五入）正是我们所熟悉的那一种。遗憾的是，由于未知原因，`base::round()` 选择了第一种规则 _"to nearest, ties to even"_（银行家舍入）。

|模式 / 示例值                    | 11.5| 12.5|−11.5 |−12.5 |
|:-------------------------------|----:|----:|-----:|-----:|
|to nearest, ties to even        |   12|   12|−12.0 |−12.0 |
|to nearest, ties away from zero |   12|   13|−12.0 |−13.0 |
|toward 0                        |   11|   12|−11.0 |−12.0 |
|toward +∞                       |   12|   13|−11.0 |−12.0 |
|toward −∞                       |   11|   12|−12.0 |−13.0 |


总之，剩下唯一重要的问题就是：_如何在 R 中实现 `human_round()`？_ 虽然大多数情况下用户不会注意到这种"奇怪"的舍入规则，但我可以想象，一旦被问到就很难解释清楚。所以我们最好有一个解决方案。下面来分享一下。

## R 版本（推荐）

这里的原理是，[计算机只能以有限精度表示小数](https://en.wikipedia.org/wiki/Double-precision_floating-point_format)，也就是说，如果两个数的差小于某个常数，我们就可以认为它们相等。通常我们选择 `.Machine$double.eps^0.5` 作为这个常数（为什么是这个数？我是从 [`dplyr::near()`](https://www.rdocumentation.org/packages/dplyr/versions/0.7.3/topics/near) 那里偷来的 :P）。

```r
human_round_r <- function(x, digits = 0) {
  eps <- .Machine$double.eps^0.5
  flag_pos <- !is.na(x) & (x > 0)
  x[flag_pos] <- x[flag_pos] + eps
  flag_neg <- !is.na(x) & (x < 0)
  x[flag_neg] <- x[flag_neg] - eps
  round(x, digits = digits)
}
human_round_r(c(2.5, 1.5, -1.5, -2.5, 1.5 - .Machine$double.eps^0.5))
```

```text
[1]  3  2 -2 -3  2
```

没错，对于像 `1.5 - .Machine$double.eps^0.5` 这样的极端情况，它可能不会如预期那样工作，但在实际应用中遇到一个恰好等于这个值的数的概率接近于零。而且，基于上面提到的精度问题，我认为 `1.5 - .Machine$double.eps^0.5` 和 `1.5` 本质上是一样的。不过，如果你坚持要一个"完美"的版本，请使用下面的 Rcpp 版本。

## Rcpp 版本

这个版本利用了 C++ 中的 `std::round()` 使用的正是[我们熟悉的舍入规则](http://en.cppreference.com/w/cpp/numeric/math/round)这一特点。

```r
Rcpp::cppFunction("
NumericVector human_round_cpp(const NumericVector x, const int digits = 0)
{
  const double multiplier = std::pow(10, digits);
  NumericVector y(x.size());
  std::transform(x.begin(), x.end(), y.begin(),
                 [multiplier](const double x) {
                   if (!R_FINITE(x)) return x;
                   return std::round(x * multiplier) / multiplier;
                 });
  return y;
}")
human_round_cpp(c(2.5, 1.5, -1.5, -2.5, 1.5 - .Machine$double.eps^0.5))
```

```text
[1]  3  2 -2 -3  1
```
