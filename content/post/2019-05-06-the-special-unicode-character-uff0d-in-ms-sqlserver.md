---
title: The special unicode character \uff0d in MS SQLServer
author: Xianying Tan
date: '2019-05-06'
slug: the-special-unicode-character-uff0d-in-ms-sqlserver
categories:
  - complaint
  - tech
tags:
  - complaint
---


It's currently 01:57 a.m in Beijing. I'm still awake, thanks to the "great" unicode `\uff0d`, whose official name is "FULLWIDTH HYPHEN-MINUS" (the print of the character is `－`, very similiar to `-`).

Why I'm calling it the "great" "special" unicode?

MS SQLServer (at least for the version I use - 2014) somehow recongizes `\uff0d(－)` as if it was `-` (the normal minus sign).

What do I mean? Let's say you have a table created like this:

```sql
CREATE TABLE table_test (
COL1 as nvarchar(10),
CONSTRAINT pk_test PRIMARY KEY (COL1)
);
```

After you insert the value `a-b` where `-` is the normal minus sign, the suprising thing will happen: 

```sql
insert into table_test values('a－b');
```

will always result in an error saying it violates the primary key constraints. Trust me I've tried various ways including adding a so-called unicode prefix `'N'`, using `'a'+ nchar(65293)+'b'`, etc - all of them failed.

What's even strange is that MS SQLServer stores them differently. It means if I delete the primary key constraints then insert the two values into the table. I can see the two records are clearly different, one is `-` (the normal minus) and the other is `－`(the great `\uff0d`).

Haven't googled the cause yet... For now just use a workaround and let it go... Really really don't want to waste the precious time on this kind of issues any more... :cry:
