---
title: 自我陶醉
author: 谭显英
date: '2020-03-27'
slug: self-enjoyment
categories:
  - cn
tags:
  - life
---

前两天，收到微信群里发的文件，是关于各家公司偿二代二期测试市场风险填报数据问题的情况。统计了下，有各种数据问题的保险公司真不少，竟然有125家，几乎所有中大型的保险公司都赫然在列。但又心中窃喜，暗自嘚瑟，我司不在名单之中。

有各种问题是正常的，那个Excel文件那么多单元格，每行资产究竟如何划分，划分之后应该归于什么风险，不同的风险又需要不同的信息。一套排列组合下来，情况实在太多。哦，对了，如果资产还需要穿透的话，那这一行数据就会变成很多行，如果这子账户的资产又包含需要穿透的，那就还需要继续变多…

涉及到如此多的不同信息的收集、如此多的不同关系的处理，我实在难以想象用Excel去手工处理是有多么地“困难”。更别说那个Excel模型每一次刷新都需要卡顿好几秒种。

这海量的手工操作，请问如何保证结果的正确性（作为一家中型公司，总数据量就有3000行* 80列之多——当然只有一小半是有效数据，但这也不少）？如果换了个日期，是不是所有的“苦”又得重来一遍？如果换了个日期，所有修复的错误是不是可能还会错？哦不对，即使不换日期同样做一遍结果估计都会不一样。

要想脱离“苦海”，就只能修炼“可重复化报告”大法：

1. 理清数据之间的关系，手工收集的数据直接用csv形式录入
1. 把数据关系和计算用代码形式描述
1. 使用Git进行版本控制——记录数据和代码的所有历史修改

最后直接一键输出成一个Excel文件，复制粘贴到监管给的模板上就好了，岂不爽乎？
