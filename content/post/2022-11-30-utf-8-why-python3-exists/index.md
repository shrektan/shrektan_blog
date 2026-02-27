---
title: UTF-8万岁
subtitle: 读《Why Python3 Exists》有感
author: 谭显英
date: '2022-11-30'
slug: utf-8-why-python3-exists
originalLang: zh
categories:
  - 技术
tags:
  - encoding
  - Python
---

这次参加R会议的talk还挺有收获，一是吐槽了下字符编码(Encoding)的各种恶心事，二是勾起了我学习下Python的兴趣。

最近几日都在鼓捣Python，的确有很多好用的地方，目前粗略地总结了下：
1. 语言自身工程性强：语言自带的基础类型（如dict、set和tuple）更丰富，偏软件工程的标准库也更丰富得多，对于工程支持是原生的
1. 用户基数大：带来更多大厂的支持，如大量机器学习的库、详实的文档还有更多的“同行”
1. 原生Unicode字符：爱了爱了

当然R也有很多自己的优点，比如对于数据框的支持、作图、meta programming、更为方便的帮助系统等，以后我再熟悉些了，写个总结吧。语言这东西真就像小马过河，只有自己试了才知道。

---
偏题了

---

本来是冲着好奇，想去了解下为什么Python3和Python2如此地泾渭分明，而不是循序渐进的过渡。[《Why Python3 exists》](https://snarky.ca/why-python-3-exists/)这篇文章着实让我有些惊讶，原来Python3和Python2无法缓慢过渡的最重要的原因之一，就是因为Python2里面的字符串存在多种选择，`str`, `bytes`和`unicode`，导致了无数的bug和问题。

文章也提到，虽然Python2.0提供了unicode的类型，但是开发者可能因为“没注意”“懒”“要追求极致计算效率”等各种原因不去使用它，进而导致无止境的复杂…

这不就和我之前遇到的经历一样吗？

幸运的是，随着R4.2.0对于Win10原生UTF-8的支持，也许R的世界里能有朝一日看到这只奇异生物的灭绝。

（本来是临时起兴，发到统计之都论坛上，没想到写了这么多，干脆搬到博客里了，哈哈）
