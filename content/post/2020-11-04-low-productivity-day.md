---
title: 低效的一天
subtitle: “杀毒软件”和“字符编码”的折腾
author: 谭显英
date: '2020-11-04'
slug: low-productivity-day
categories:
  - cn
tags:
  - complaint
  - encoding
---

最近手头事特别多，但今天特别低效，两件事：**“杀毒软件”**和**“Windows下的字符编码”**。

# 杀毒软件

我们公司安全策略是所有Windows机器必须要安装两个软件：[趋势科技](https://www.trendmicro.com)还有[LANDESK](https://www.ivanti.com.cn/company/history/landesk)。前者是防病毒软件，后者为了防止员工使用网盘等非允许软件的控制程序。

的确，公司的网络安全非常重要，安装安全软件情有可原，但是，这造成了一个局面，就是**我们公司的电脑运行环境，对数据分析、程序开发类的工作非常不友好**。因为，上面提到的这两个大哥，会对你电脑任何文件操作（哪怕你是在用户的临时文件夹里面）、任何程序（趋势的白名单审查非常繁琐冗长，而且不时升级）的执行都进行一遍又一遍地查杀。

然而，R还有Git天然就需要进行大量的磁盘文件访问或修改，这就导致虽然公司电脑硬件配置非常好，但是我们[在RStudio下的工作，不时出现各种恼人的卡顿](https://github.com/rstudio/rstudio/issues/5335)。尤其是Git，每次进行刷新时，就卡得像幻灯片一样（因为Git本来就是用大量小文件进行数据存储的），一度达到几乎不可使用的程度（对的，那个趋势总是在不停升级，一会快一会慢，非常令人崩溃）。还有C++代码的编写，由于RStudio IDE需要运行Clang对语法进行检查或者是提供自动补全的功能，然后就导致了Clang和杀毒软件抢夺对源文件控制权的局面，导致经常性地无法保存文件，必须得手动执行下restart r session后才能保存 :joy: 。

不时的卡顿够让人烦心的了，但我还能勉强忍受（谁叫我是“忍者”呢？）。今天早上开始，一旦我运行`R CMD build`进行R包的编译，升级了的趋势就会把Rterm.exe认为是恶意加密软件，直接进行强制删除。赶紧找IT同事和趋势厂家商量，说他们不只有全球范围内（需要审批1个月）的白名单，现在可以设置本地白名单了。于是，索性将R、RStudio、Git等所有相关的exe文件加入IT后台的信任程序路径中。似乎起了作用。但是，从下午开始，RStudio IDE中一旦执行reprex的shiny addin，立马把RStudio文件夹下的rsession.exe也查杀删除了——虽然，上午我们就已经把这个文件加入到了信任名单中。

奇葩吧？赶紧问趋势厂家，说要排查下问题，明天给答复。希望明天能有个好点的解决方案。

# Windows下的字符编码

## 背景

本人自认为是R字符编码问题的“砖家”了，没想到今天还是意想不到地吃了一个亏。最近，让小朋友做一个科创板和创业板注册制下各家机构新股报价入围率的Shiny App（源数据整理好后，大概100多万行的产品报价信息，包含大量中文）。小朋友做得不错，唯一的问题是每次查询非常的慢（大概需要15秒）。我表示非常不解，100多万行的数据这么简单的查询应该是“瞬间”出来结果才对，为何如此之慢？

## 排查

经过一系列定位，排查到类似下面的这个语句上（`tbl`就是我上面提到的源数据，是一个data.table的对象）：

```r
tbl[SECTOR %in% input$sector & DATE >= as.Date("2020-10-01") & DATE <= as.Date("2020-11-01")]
```

我退出Shiny，然后直接在Console里把`input$sector`用“科创板”文字替换掉执行，果然瞬间(0.01s)便完毕了。但是，我设置`browser()`在Shiny App中，暂停后运行，这个语句却需要15秒左右。这让我感到十分崩溃，心想，难道是我对于Shiny的`input`不了解吗？难道是`input$sector`这个语句和data.table发生了某种冲突？最令我崩溃的是，我一旦改写为下面的语句后，语句执行速度立马恢复成预期状态：

```r
tbl2 <- tbl[SECTOR %in% input$sector]
tbl2[DATE >= as.Date("2020-10-01") & DATE <= as.Date("2020-11-01")]
```

## 根源

经过了一系列的折腾和试验后，终于排查出了问题的根源：

1. Shiny里的`input$sector`是UTF-8编码，而`tbl`里的`SECTOR`列却是native encoding。R里面`%in%`左右两侧的字符编码不一致的时候，尤其是有一列字符特别长的时候，执行速度会非常非常慢，原因应该是R对两列字符都进行了重新编码。我感觉这是R的一个问题，因为不论长的一列是native或UTF-8编码，速度都会特别慢。但按理说，R只需要对短的那一列字符进行重编码即可，没必要对两边都重编码。于是乎，我晚上在[R-bugzilla上提交了个报告](https://bugs.r-project.org/bugzilla/show_bug.cgi?id=17965)。

1. 为什么改成了两个语句执行了就变快了呢？原因是data.table对于单独的`%in%`查询语句会进行优化，并没有使用base R里的`%in%`代码。但是，按照我的理解，对于非单独的`%in%`查询语句，data.table理应也进行优化才对，不知何故，没有能够触发优化的逻辑。于是乎，[在data.table上也提交了一份报告](https://github.com/Rdatatable/data.table/issues/4799)。

## 喜讯

之前我就注意到了Tomas Kalibera写的这两篇文章：[《UTF-8 support on Windows》](https://developer.r-project.org/Blog/public/2020/05/02/utf-8-support-on-windows)和[《UTF-8 build of R and CRAN packages》](https://developer.r-project.org/Blog/public/2020/07/30/windows/utf-8-build-of-r-and-cran-packages/)。但我以为这只是一个小小的试验，离最终R能提供一个“在Windows10下使用UTF-8左右native encoding的版本”，还有好长的路要走。

好消息是，参照Tomas Kalibera在R-bugzilla上给我的[回复](https://bugs.r-project.org/bugzilla/show_bug.cgi?id=17960#c3)，以及我注意到[《UTF-8 build of R and CRAN packages》](https://developer.r-project.org/Blog/public/2020/07/30/windows/utf-8-build-of-r-and-cran-packages/)进行了更新，补充了相关的编译工具链、编译好的R和所有CRAN/BIOC package的文件，我感觉到，**距离Windows下用UTF-8的R的那个日子，已经不太远了**。

## 另，为什么现在才开始准备“在Windows下用UTF-8作为默认编码的R版本”？

根据[《UTF-8 build of R and CRAN packages》](https://developer.r-project.org/Blog/public/2020/07/30/windows/utf-8-build-of-r-and-cran-packages/)的说法，原因是Windows 10（2019.11后的版本），才开始支持程序使用UTF-8作为native encoding同操作系统进行交互（不过我简单搜了下，似乎没有找到微软官方的这一宣布）：

> Windows 10 (November 2019 release and newer) allows applications to use UTF-8 as their native encoding when interfacing both with the C library (needs to be UCRT) and with the operating system. This new Windows feature, present in Unix systems for many years, finally allows R on Windows to work reliably with all Unicode characters.

> Applications that already worked reliably with all Unicode characters on Windows before used proprietary Windows API and wide-character strings, which required implementing and maintaining a lot of Windows-specific code. R did not go that route completely, except for RGui and particularly Windows-specific code interfacing with the file system / operating system (in some cases on Windows this is also needed for other reasons than character encoding). Today, Windows can’t even encode all Unicode characters using one wide character (wide characters are 16-bit, UTF16-LE is used, and hence two wide characters are needed to represent some Unicode characters), so the old Windows way to support Unicode in addition does not seem to have any technical advantage. The new way, via UTF-8, will instead allow to eventually phase out some Windows-specific code from R.

# 末了

真希望在Mac或者Linux下工作，这些杀毒软件神马的、字符编码神马的东东，请离我远一点，我已经受够了 :angry: 。
