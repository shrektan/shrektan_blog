---
title: Strings, Encodings in R
author: Xianying Tan
date: '2018-03-18'
slug: strings-encodings-in-r
categories:
  - programming
tags:
  - R
---

费了不少功夫，不出意外，总算是彻底解决了`data.table`中文支持的问题（[PR#2678](https://github.com/Rdatatable/data.table/pull/2678)，[PR#2566](https://github.com/Rdatatable/data.table/pull/2566))。散乱地写下些学习到的点，供以后参考：

### 学习笔记

- R对象在C环境下统一为`SEXP`类型(读音为S,EXP(external pointer)，不是SEX P)；
- R里面字符串的实施细节用到了字符串池([The CHARSXP cache](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#The-CHARSXP-cache))来提高效率;
- 对于字符串的排序，`data.table`和base R里面的radix sort巧妙地使用了SEXP一个基本废弃的属性[`truelength`](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#DOCF3)；
- R字符在C level下，能够保存的Encoding属性只有三种：`Latin-1`, `ASCII` 和 `UTF-8`，参见[此段最后一行](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#Rest-of-header)和[R Internals - Encodings for CHARSXPs](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#Encodings-for-CHARSXPs)；
- R中使用到`SEXP`时，一定要注意思考垃圾回收有没有可能回收这个变量。垃圾回收导致的bug非常难以查找，[data.table issue#2674](https://github.com/Rdatatable/data.table/issues/2674)前前后后花了差不多6个小时才解决。标准的查虫流程为“发现异常、找到最小可重复的代码、定位问题、解决问题”，然而垃圾回收的触发是不可控的，因此要想复现此类bug非常困难。

### 其他：

- `enc2utf8()`对于长字符串是需要耗费一定时间的，而且没有特别好的办法来处理；
- 建议尽量在R的层面把所有`非ASCII字符`转换为`UTF-8`编码后再统一处理；

### 主要可供参考的资料：

- [Writing R Externtions](https://cran.r-project.org/doc/manuals/r-release/R-ints.html)
- [R Internals](https://cran.r-project.org/doc/manuals/r-release/R-exts.html)
- [R source code](https://github.com/wch/r-source)
