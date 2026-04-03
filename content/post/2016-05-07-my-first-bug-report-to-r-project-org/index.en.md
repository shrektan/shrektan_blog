---
title: My first bug report to r-project.org
author: Xianying Tan
date: '2016-05-07'
slug: my-first-bug-report-to-r-project-org
originalLang: en
categories:
  - Tech
tags:
  - R
  - programming
---


One of the most headache problems in R (maybe in all programming) is the `Encoding` issue, especially on Windows. Even the veterans in the R-Core team can't survive.

In the new version of R 3.3.0, there's an upgrade related to `match(x, table)` ( [#PR16491](https://bugs.r-project.org/show_bug.cgi?id=16491)). However, it leads to unconsistent behaviors when `x` and `table` contains non-ascii characters. So I filed my first [bug report](https://bugs.r-project.org/show_bug.cgi?id=16885) to the [bugs.r-project.org](https://bugs.r-project.org/).


What a wonderful world it would be, had all the characters been encoded in `UTF-8`.
