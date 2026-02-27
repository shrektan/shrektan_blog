---
title: MS SQLServer 中特殊的 Unicode 字符 \uff0d
author: 谭显英
date: '2019-05-06'
slug: the-special-unicode-character-uff0d-in-ms-sqlserver
originalLang: en
categories:
  - 技术
tags:
  - complaint
  - tech
---


现在是北京时间凌晨 01:57，我还没睡，拜这个“伟大”的 Unicode 字符 `\uff0d` 所赐。它的官方名称是 "FULLWIDTH HYPHEN-MINUS"（打印出来是 `－`，和 `-` 长得非常像）。

为什么我要称它为“伟大”的“特殊” Unicode 字符？

MS SQLServer（至少我使用的 2014 版本）会把 `\uff0d(－)` 当作 `-`（普通减号）来识别。

什么意思呢？假设你创建了这样一张表：

```sql
CREATE TABLE table_test (
COL1 as nvarchar(10),
CONSTRAINT pk_test PRIMARY KEY (COL1)
);
```

当你插入值 `a-b`（其中 `-` 是普通减号）之后，令人惊讶的事情就会发生：

```sql
insert into table_test values('a－b');
```

这条语句一定会报错，提示违反了主键约束。相信我，我已经尝试了各种方法，包括添加所谓的 Unicode 前缀 `'N'`、使用 `'a'+ nchar(65293)+'b'` 等等——全都失败了。

更奇怪的是，MS SQLServer 在存储时实际上区分了它们。也就是说，如果我删除主键约束后再把两个值都插入表中，可以清楚地看到这两条记录是不同的，一个是 `-`（普通减号），另一个是 `－`（那个“伟大”的 `\uff0d`）。

至今还没有搜到原因……先用变通方案绕过去吧……真的真的不想在这种问题上再浪费宝贵的时间了…… :cry:

---

**更新 (@2020-04-02)**：这两个字符之间的关系有可能类似于大小写的关系，考虑到 MS SQLServer 在比较字符串时默认忽略大小写。不过，这只是我未经验证的猜测。
