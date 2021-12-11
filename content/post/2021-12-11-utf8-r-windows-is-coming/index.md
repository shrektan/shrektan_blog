---
title: 使用UTF8作为默认编码的Window R快来了
author: 谭显英
date: '2021-12-11'
slug: utf8-r-windows-is-coming
categories:
  - cn
tags:
  - encoding
  - complaint
editor_options: 
  markdown: 
    wrap: 72
---

2021年12月8日，晚上21点56分（北京时间），Tomas Kalibera
在R-dev邮件列表上发了封邮件，通知Windows平台上的R用户们，在4.2版本后，（终于）就能使用UTF-8作为native
Encoding，可以和其他平台的R用户一样，保证读进来的字符默认都是UTF-8编码的了。

我同Windows的字符问题战斗了整整10年------准确来说，是被折磨得多，偶尔有反抗。看到这一天的到来，我还是很开心的------虽然我个人以后只会用mac和linux来处理程序了，但我想其他同事、其他Windows上的R用户，他们的时间将还是会被省掉不少的。

不过，能够使用UTF-8作为native编码方便的主要还是包的开发者。因为数据一旦进来就是UTF-8，那么开发者就不用再费心思去打各种补丁处理字符编码问题了（非UTF-8编码环境下，各种字符编码都可能不经意的混入到你的字符向量里面，当淤泥中的一束莲花可真难）。

然而，对于用户来讲，他还是会面临：读取的csv格式可能是GBK的，UTF-8的csv格式Excel直接打开是一堆乱码，数据库的编码配置仍然让人头痛......
但至少一旦读对了，和包相关的字符串错误的可能性还是会少很多了。

真心感谢CRAN Core Member的努力，尤其是Tomas
Kalibera，他为推动这个事情肯定耗费了超多的精力。

正是有你们这些无私奉献的神人，R的社区才这么生气勃勃，世界才一天天更美好。

## 邮件全文

> Please note an update concerning the support of UTF-8 as native
> encoding on Windows, which may at this point be of interest
> particularly to developers of packages with native code and to R users
> using R-devel (the development version of R) on Windows:
>
> <https://developer.r-project.org/Blog/public/2021/12/07/upcoming-changes-in-r-4.2-on-windows/>
>
> The key part is that CRAN will switch the incoming checks of R
> packages on Windows to a new toolchain targeting UCRT on Monday,
> December 13.
>
> It may take up to several days for all systems to synchronize and
> during this time, it may be difficult to build R-devel on Windows from
> source or to install packages. After the switch, the snapshot R-devel
> builds and binary package builds provided by CRAN will be built using
> the new toolchain for UCRT. These new builds will use UTF-8 as the
> native encoding on recent Windows.
>
> These builds will be incompatible with the previous builds for MSVCRT
> and installed/binary packages will be incompatible as well. The
> recommended/simplest course of action for R-devel users is to
> uninstall the old build of R-devel, RTools, delete the old package
> libraries, and then install the new versions.
>
> Checks of CRAN packages with the new toolchain have been running since
> March with results available on CRAN pages. By now, most packages are
> working, but some packages using native (C, C++, Fortran) code still
> have to be updated. The Winbuilder service and R-hub support the new
> toolchain, there is also support/example for using github actions. The
> builds of R-devel and CRAN (and recommended binary packages) with the
> new toolchain are available regularly since March.
>
> I've created patches for CRAN (and required Bioconductor packages)
> which are installed automatically at package installation time by R.
> This feature will be also in R-devel after the switch and will be used
> temporarily to give package authors more time to fix their packages.
> Uwe Ligges, other CRAN team members and I have also been in touch with
> some package authors, providing advice how to fix their packages, when
> the issues required more explanation. I am prepared to help the
> remaining authors as well if needed.
>
> Please see the blog post and materials linked from there for more
> details and feel free to ask questions.
