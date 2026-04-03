---
title: 忍无可忍的Encoding
subtitle: 浪费了多少宝贵的时间？！
author: 谭显英
date: '2018-05-07'
slug: cant-bear-with-encoding-any-longer
originalLang: zh
categories:
  - 技术
tags:
  - complaint
  - note
  - tech
  - R
  - encoding
---

### RSQLServer包正式退役了

[RSQLServer](https://github.com/imanuelcostigan/RSQLServer)于2018年4月10日[正式退役(Archive)](https://cran.r-project.org/package=RSQLServer)，作者建议用[r-dbi/odbc](https://github.com/r-dbi/odbc)代替。

> This package is archived as there is now an excellent, much better supported package [odbc](https://github.com/r-dbi/odbc).

### 切换到odbc包


作为一个长期混迹于Github的码农，很早前便注意到odbc这个包了。的确，odbc更快更轻（不需要安装Java），也在积极开发中。而RSQLServer则有点缺乏维护，加上之前引入了dplyr的一些功能，不时会引起冲突，我便一直手痒想切换过去。虽然做了一些比较和测试，基本没看出问题，但却暗暗担心会遇到些意想不到的毛病。

不过既然早晚都要切换，宜早不宜迟。记得 _"The Pragmatic Programmer"_ 有句很经典的论断：

> Refactor Early, Refactor Often. 

### 坑

果然，没多久就发现有些脚本的结果有些奇怪了。排查了半天后，终于发现了问题：_odbc并没有像RODBC或者RJDBC一样，预先把SQL字符编码转换成和数据库一致的字符编码。_ 坑爹的是，我很少会在SQL中用中文，正好那个别的中文虽然转换成了垃圾字符但并不会报错，只是返回的结果不一样 :rage:。

早上在Github上提交了报告[r-dbi/odbc#179](https://github.com/r-dbi/odbc/issues/179)，感觉强制将SQL转换成和数据库的字符编码应该可行（`RODBC::odbcQuery()`就是这么做的），但考虑到我实在不是数据库专家，还是不提交PR献丑了，留给作者[Jim Hester](https://github.com/jimhester)解决吧…

### 浪费时间

计算机的世界里，字符编码Encoding真是奇葩得不行，尤其是在windows上（哦，我们也别忘了另外一个奇葩：时区Timezone）。回想起这些年码农的日子，在这两个奇葩上耗费了无数的宝贵时间，列举一些我印象比较深刻的：

* GB2312编码的文件不小心用UTF-8编码打开了，编辑然后保存了 —— 那会儿还不会用版本控制；

* 从数据库上读取`data.frame`里面的日期字段，用`as.Date()`立马会少一天 —— 因为`as.Date()`里的参数`tz`默认是`"UTC"`；

* Linux上读取Oracle数据库一堆乱码 —— 需要设置Oracle的语言环境变量；

* Windows储存的数据拿到Linux下变身为一堆乱码（储存的字符用的是GB2312编码，Linux下面只有UTF-8才能正常显示）；

* LaTeX上写中文，包括在PDF浏览器上能够正确显示中文的书签 —— 只有XeLaTeX能救你；

* ggplot2的图在pdf中显示中文 —— 必须要把图形中相关字体设置成pdf可用的字体，而且Warning似乎永远都消除不掉；

* 我隐约记得base包里的`gsub()`（也可能是其他某个函数）不支持UTF-8编码的输入（好像现在已经修复了）；

* `roxygen2`和`devtools`在windows上对中文的支持 —— [r-lib/roxygen2#532](https://github.com/r-lib/roxygen2/pull/532)、[r-lib/devtools#1378](https://github.com/r-lib/devtools/pull/1378)

* `data.table`在1.9.7版本中引入的八哥 —— 参见我[前一篇日志](/post/2018/03/18/strings-encodings-in-r/)，来来回回折磨了我快两年；

* R版本3.3.0引入的八哥，导致`match()`函数对于不同字符编码结果不一致 —— 我[第一篇日志](/post/2016/05/07/my-first-bug-report-to-r-project-org/)写的就是这个；

* R里的数据库链接，有的返回的是UTF-8编码的字符，而有的则返回本地编码字符，总之你只能试了才知道；

* 公司的MS SQL Server使用GB2312储存数据，UTF-8来源的某些数据储存进去后变成乱码；

* R默认产生的时间是不带时区属性的(比如`attr(Sys.time(), "tzone")`返回`NULL`)，这种时间储存后换一个机器读取有可能就会遇到问题，比如你们两的时区不一致；

* 各种数据储存格式对于编码的支持，比如[wesm/feather#335](https://github.com/wesm/feather/issues/335)、[fstpackage/fst#114](https://github.com/fstpackage/fst/issues/144)；

* 各种htmlwidgets对中文的支持 —— 现在这方面问题似乎越来越少了；

* ROracle包必须要把SQL用UTF-8编码才行；

* ...


恐怕大家都多多少少被这些问题折磨过，可折腾来折腾去，究竟有多少意义？最悲哀的是，无论之前踩了再多坑，后面却有更多坑等着你 :joy:。

###  (嘚瑟下我提交PR修复的问题)

* [r-lib/roxygen2#532](https://github.com/r-lib/roxygen2/pull/532)：roxygen2会使用DESCRIPTION里的Encoding字段，之前总是使用native encoding，在Windows下带来很多问题

* [rstudio/rmarkdown#841](https://github.com/rstudio/rmarkdown/pull/841)：很早之前yaml对UTF-8支持不太友好，rmarkdown不得不在内部对yaml读取进行一些更改，但是忘记了除了最后的内容外，列表的名称也可能是UTF-8编码的

* [Rdatatable/data.table#2566](https://github.com/Rdatatable/data.table/pull/2566))、 [Rdatatable/data.table#3451](https://github.com/Rdatatable/data.table/pull/3451)、 [Rdatatable/data.table#3849](https://github.com/Rdatatable/data.table/pull/3849)：解决了data.table在处理包含非ASCII字符的排序、查询和崩溃问题——专研了好一会，而且data.table的C代码挺复杂的，能搞定这些我真的挺得意的，哈哈

* [rstudio/plumber#312](https://github.com/rstudio/plumber/pull/312)、[rstudio/plumber#314](https://github.com/rstudio/plumber/pull/314/files)：plumber能够支持读取UTF-8的源文件以及处理包含UTF-8的JSON信息

* [Rblp/Rblpapi#278](https://github.com/Rblp/Rblpapi/pull/278)：Rblpapi会可以调用彭博API，但是对于返回的结果没有进行UTF-8标识，导致乱码

* [r-dbi/RSQLite#276](https://github.com/r-dbi/RSQLite/pull/276)：RSQLite没有对返回的列头标识UTF-8编码，导致显示乱码

* [openanalytics/containerproxy#15](https://github.com/openanalytics/containerproxy/pull/15)：shinyproxy在向influxdb传送用户信息时没有把编码从Java默认的UTF-16装换成UTF-8，导致包含中文字符时，数据库收到的信息是乱码

* [Rdatatable/data.table#3850](https://github.com/Rdatatable/data.table/pull/3850)：`data.table::setnames()`无法正确对中文列头重命名

* [r-dbi/odbc#294](https://github.com/r-dbi/odbc/pull/294)：`odbc`包返回的时区强制为UTC导致用户使用非常困惑和不方便

* [r-dbi/odbc#295](https://github.com/r-dbi/odbc/pull/295)：`odbc`包返回的日期值是数据库存储的日期减1天

* [rstudio/rstudioapi#158](https://github.com/rstudio/rstudioapi/pull/158)：Windows下，rstudioapi在选择了包含中文的文件后，显示为乱码

* [rstudio/htmltools#157](https://github.com/rstudio/htmltools/pull/157)：Windows下rmarkdown在遇到emoji的字符串后，后续的htmlwidgets对象无法显示

* [Rdatatable/data.table#4785](https://github.com/Rdatatable/data.table/pull/4785)：`data.table::fwrite()`可以通过设置encoding来写UTF-8编码的CSV文件

* [ycphs/openxlsx#118](https://github.com/ycphs/openxlsx/pull/118): openxlsx是一个可以创建/修改/读取Excel表格的包，强大而且好用。但是，当批注中包含中文或表单名称包含中文时，就会报错。读了一遍它里面R和C++相关的代码，把所有的地方都改成了UTF-8进出（因为xlsx格式本来就是UTF-8编码的）。应该差不多能彻底解决中文支持的问题了吧（不排除还有漏网之鱼）？

### 未来

按照Tomas Kalibera这两篇文章的说法，Windows10（2019.11后的版本）开始允许应用使用UTF-8编码和操作系统进行交互了。所以，将R和相关包的编译工具改为[UCRT](https://devblogs.microsoft.com/cppblog/introducing-the-universal-crt/)后，Windows下Encoding的大部分问题可能就在根源上得以解决。不过，文章中并没有明确R未来的计划安排，但我们至少看到了一丝的希望。

- [Windows/UTF-8 Build of R and CRAN Packages, Tomas Kalibera](https://developer.r-project.org/Blog/public/2020/07/30/windows/utf-8-build-of-r-and-cran-packages/)

- [UTF-8 Support on Windows, Tomas Kalibera](https://developer.r-project.org/Blog/public/2020/05/02/utf-8-support-on-windows/)

- [R-dev/WindowsBuilds/winutf8](https://svn.r-project.org/R-dev-web/trunk/WindowsBuilds/winutf8/winutf8.html)
