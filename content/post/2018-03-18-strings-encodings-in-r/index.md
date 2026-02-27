---
title: R中的字符编码
subtitle: Strings、Encodings in R
author: Xianying Tan
date: '2018-03-18'
slug: strings-encodings-in-r
originalLang: zh
categories:
tags:
  - R
  - programming
  - encoding
  - data.table
---

费了不少功夫，不出意外，总算是彻底解决了`data.table`中文支持的问题（[PR#2678](https://github.com/Rdatatable/data.table/pull/2678)、[PR#2566](https://github.com/Rdatatable/data.table/pull/2566))、 [PR#3451](https://github.com/Rdatatable/data.table/pull/3451)、 [PR#3849](https://github.com/Rdatatable/data.table/pull/3849)、 [PR#3850](https://github.com/Rdatatable/data.table/pull/3850)。散乱地写下些学习到的点，供以后参考：

### 学习笔记

- R对象在C环境下统一为`SEXP`类型(读音为S,EXP(external pointer)，不是SEX P)；
- R里面字符串的实施细节用到了字符串池([The CHARSXP cache](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#The-CHARSXP-cache))来提高效率;
- 对于字符串的排序，`data.table`和base R里面的radix sort巧妙地使用了SEXP一个基本废弃的属性[`truelength`](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#DOCF3)。更具体地说，把`The CHARSXP cache`当做一个哈希表(key -> value)，并将值储存在`truelength属性`中；
- R字符在C level下，能够保存的Encoding属性只有三种：`Latin-1`, `ASCII` 和 `UTF-8`，参见[此段最后一行](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#Rest-of-header)和[R Internals - Encodings for CHARSXPs](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#Encodings-for-CHARSXPs)；
- R中使用到`SEXP`时，一定要注意思考垃圾回收有没有可能回收这个变量。垃圾回收导致的bug非常难以查找，[data.table issue#2674](https://github.com/Rdatatable/data.table/issues/2674)前前后后花了差不多6个小时才解决。标准的查虫流程为“发现异常、找到最小可重复的代码、定位问题、解决问题”，然而垃圾回收的触发是不可控的，因此要想复现此类bug非常困难；
- 字符串的比较有两种方式，一是直接比较背后的编码(可以用`charToRaw()`查看），二是统一转换为UTF-8编码后再比较；
- 如何判断一个CHARSXP是不是ASCII, UTF8可参考：
    - [R-source/util.c](https://github.com/wch/r-source/blob/44d54d6f848468a7353d99cc9be0255105185975/src/main/util.c#L1834)
    - [data.table/data.table.h](https://github.com/Rdatatable/data.table/blob/bb3ba9a39be1ee8386b86909e045947898cb0935/src/data.table.h#L50)
- 在R的C Routine中将字符转为UTF-8编码：`mkCharCE(translateCharUTF8(s), CE_UTF8)`；
- Debug往往需要把相关变量值打印出来，然而R的C Routine中支持的`Rprintf()`只能打印本地编码的字符，因此必须先将字符串用`translateChar`转换后才能成功打印，如`Rprintf("%s", translateChar(value))`，否则只会得到空白。  

> [Character-encoding-issues](https://cran.r-project.org/doc/manuals/r-release/R-exts.html#Character-encoding-issues): However, if they need to be interpreted as characters or output at C level then it would normally be correct to ensure that they are converted to the encoding of the current locale: this can be done by accessing the data in the CHARSXP by translateChar rather than by CHAR. 


### 其他

- `enc2utf8()`对于长字符串是需要耗费一定时间的，而且没有特别好的办法来处理；
- 建议尽量在R的层面把所有`非ASCII字符`转换为`UTF-8`编码后再统一处理；
- Windows下Encoding的问题让人头疼，一个重要原因是主流平台中只有Windows下的默认字符编码不是UTF-8，而且不同语言下的默认编码都不一样。我遇到的`data.table`编码问题，只有在语言为中文的windows下才能复现（当然其他语言也可以，不过就得把例子换成相应的语言）。这就是为什么我在2016年提交的bug[#1826](https://github.com/Rdatatable/data.table/issues/1826)两年无人理睬，因为要么其他人要么不使用windows，即使使用windows也不是中文环境。理解到这一点，我便意识到这个问题只有靠自己了，这就是费这么大劲研究这个的原因（实在忍不了又没人帮忙）。

    **更新：** 这论断有些不当。正如前文所言，R里的编码可以保存`latin1`，那么把问题改成用`latin1`编码便可以在任何电脑上复现了！栗子：[`data.table`的测试](https://github.com/Rdatatable/data.table/pull/2678/commits/8e04d53496432f66c1f1655e1aa0ab1d8f01c70a)。
- 解决这个问题后，[Mattdowle](https://github.com/mattdowle)邀请我加入了[Rdatatable Team](https://github.com/Rdatatable)，希望自己能帮助`data.table`把对中文（或其他语言）的支持做得更好。


### 主要可供参考的资料

- [Writing R Externtions](https://cran.r-project.org/doc/manuals/r-release/R-ints.html)
- [R Internals](https://cran.r-project.org/doc/manuals/r-release/R-exts.html)
- [R source code](https://github.com/wch/r-source)
- [Hadley's R-internals](https://github.com/hadley/r-internals)
