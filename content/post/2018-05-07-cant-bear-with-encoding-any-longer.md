---
title: 忍无可忍的Encoding
subtitle: 浪费了多少宝贵的时间？！
author: 谭显英
date: '2018-05-07'
slug: cant-bear-with-encoding-any-longer
categories:
  - note
  - tech
tags:
  - complaint
---

### RSQLServer包正式退役了

[RSQLServer](https://github.com/imanuelcostigan/RSQLServer)于2018年4月10日[正式退役(Archive)](https://cran.rstudio.com/web/packages/RSQLServer/index.html)，作者建议用[r-dbi/odbc](https://github.com/r-dbi/odbc)代替。

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

* `roxygen2`和`devtools`在windows上对中文的支持 —— [klutometis/roxygen#532](https://github.com/klutometis/roxygen/pull/532)、[r-lib/devtools#1378](https://github.com/r-lib/devtools/pull/1378)

* `data.table`在1.9.7版本中引入的八哥 —— 参见我[前一篇日志](/post/2018/03/18/strings-encodings-in-r/)，来来回回折磨了我快两年；

* R版本3.3.0引入的八哥，导致`match()`函数对于不同字符编码结果不一致 —— 我[第一篇日志](/post/2016/05/07/my-first-bug-report-to-r-project-org/)写的就是这个；

* R里的数据库链接，有的返回的是UTF-8编码的字符，而有的则返回本地编码字符，总之你只能试了才知道；

* 公司的MS SQL Server使用GB2312储存数据，UTF-8来源的某些数据储存进去后变成乱码；

* R默认产生的时间是不带时区属性的(比如`attr(Sys.time(), "tzone")`返回`NULL`)，这种时间储存后换一个机器读取有可能就会遇到问题，比如你们两的时区不一致；

* 各种数据储存格式对于编码的支持，比如[wesm/feather#335](https://github.com/wesm/feather/issues/335)、[fstpackage/fst#114](https://github.com/fstpackage/fst/issues/144)；

* 各种htmlwidgets对中文的支持 —— 现在这方面问题似乎越来越少了；

* ROracle包必须要把SQL用UTF-8编码才行；

* ……

恐怕大家都多多少少被这些问题折磨过，可折腾来折腾去，究竟有多少意义？最悲哀的是，无论之前踩了再多坑，后面却有更多坑等着你 :joy:。
