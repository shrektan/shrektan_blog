---
title: 兜兜转转，还是 data.table
author: 谭显英
date: '2026-04-04'
slug: data-table-is-the-best
originalLang: zh
categories:
  - 技术
tags:
  - R
  - tech
---

![data.table 的方括号语法](cover.jpg)

dplyr、Pandas、Polars——这些年主流的 DataFrame 工具我都认真用过。兜兜转转，我现在觉得 data.table 还是综合最好用的数据分析工具，没有之一。

R 有 R 的好，Python 有 Python 的好，这个不用争。但就 DataFrame 操作本身——筛选、变换、分组、合并——这才是数据分析的日常。我这里只聊这件事。

数据分析为什么围绕 DataFrame？因为二维表是人肉眼能理解的极限。Excel 是二维的，CSV 是二维的，SQL 结果也是二维的。更高维度的数据，最终都得拍平成二维才能被人消化。你用的 DataFrame 工具好不好，直接决定了工作效率。

### `DT[i, j, by]` —— 表达力的根源

data.table 的语法就一个形式：`DT[i, j, by]`——在哪些行（i）上，做什么运算（j），按什么分组（by）。初看觉得奇怪，但这个设计是"天才"级的（感谢作者 Matt Dowle）。

关键在于，**i、j、by 是在同一个表达式里协作的，不是流水线上的独立步骤**。这和 dplyr 的 `filter() %>% mutate() %>% group_by()` 管道、Pandas 的链式调用、Polars 的 `filter().with_columns().group_by()` 有本质区别。管道式语法把条件筛选和后续操作拆成了独立的环节，看起来好像每一步都很清楚，但一旦操作之间有耦合——比如"只改某些行""在筛选后的子集上做分组计算"——就会变得别扭。

先看一个最基本的例子：**把满足条件的行原地更新**。

**data.table：**
```r
DT[age > 30, salary := salary * 1.1]
```

一行。筛出 `age > 30` 的行，把它们的 `salary` 乘 1.1，原地修改，不复制整列。

**dplyr：**
```r
DF <- DF %>% mutate(salary = if_else(age > 30, salary * 1.1, salary))
```

没有"只改某些行"的概念。必须对整列写条件表达式，`if_else` 里还得手动写一遍 `salary` 作为 else 分支。

**Pandas：**
```python
df.loc[df["age"] > 30, "salary"] *= 1.1
```

还算简洁，但列名全是字符串，没有 autocomplete。

**Polars：**
```python
df = df.with_columns(
    pl.when(pl.col("age") > 30)
    .then(pl.col("salary") * 1.1)
    .otherwise(pl.col("salary"))
    .alias("salary")
)
```

Polars 根本不支持原地修改某几行——你必须对整列做 `when/otherwise`，然后替换掉整个 column。五行代码，表达了一行的意思。

这不是 edge case，这是数据分析里最常见的操作之一。

### 当 i、j、by 结合在一起

上面的例子还算简单。真正拉开差距的，是 i、j、by 三者结合的场景。

比如：**在活跃用户中，按地区计算每个人的收入占比，并写回原表**。

**data.table：**
```r
DT[status == "active", pct := salary / sum(salary), by = region]
```

一行做了三件事：筛选活跃用户（i），计算每人薪资占该地区活跃用户总薪资的比例（j），按地区分组（by），结果原地写回。而且 `sum(salary)` 只在活跃用户中计算——因为 i 的筛选在 by 分组之前就生效了。

**dplyr：**
```r
DF <- DF %>%
  group_by(region) %>%
  mutate(pct = if_else(
    status == "active",
    salary / sum(salary[status == "active"]),
    NA_real_
  )) %>%
  ungroup()
```

因为 dplyr 的 `mutate` 作用于所有行，你无法说"只在 active 的行上做这个运算"。所以 `sum(salary)` 如果不加条件，算的是整个地区（包括不活跃的）的总薪资——跟 data.table 的语义不同。你得在 `sum()` 里再嵌套一层筛选条件。整体需要五行加嵌套逻辑。

**Polars：**
```python
active = df.filter(pl.col("status") == "active")
active = active.with_columns(
    (pl.col("salary") / pl.col("salary").sum())
    .over("region")
    .alias("pct")
)
df = df.join(active.select("id", "pct"), on="id", how="left")
```

Polars 需要先筛选出子集，在子集上做窗口计算，再 join 回原表。三步，而且需要一个 id 列来做 join。

这就是管道式语法的代价——**filter 和 mutate 是分离的，你没法说"只在符合条件的行上做计算并写回"**。data.table 把 where（i）和 what（j）放在同一个表达式里，这种设计让很多常见操作只需一行就能精确表达。

再看一个更典型的：**按证券代码匹配，日期落在某个区间内，对匹配到的行做聚合**（non-equi join + grouped aggregation）。

**data.table：**
```r
B[, 交易总额 := A[B, .(sum(交易金额)),
  by = .EACHI,
  on = c("证券代码", "日期>=起始日期", "日期<=终止日期")]$V1
]
```

join 条件、聚合逻辑、赋值，一个表达式搞定。

同样的事用 Pandas 做，你得先 `merge`，再筛选日期范围，再 `groupby` 聚合，再 `map` 回去，少说六七行加上一堆中间变量。Polars 可以用 `join_where`，但也远没有这么紧凑。

这种表达密度的根源是 R 的 NSE（Non-Standard Evaluation）。在 `DT[...]` 内部，列名就是变量，任意 R 表达式都能自由组合。这不是 API 设计巧妙的问题，是语言层面的能力差异。

### Key——被忽视的基础设施

data.table 有一个很基本但很重要的概念：Key。

```r
setkey(DT, 证券代码, 日期)
DT["A"]                              # 按 key 做二分查找
DT[.("A", as.Date("2024-01-01"))]    # 多列 key 查找
A[B, on = "证券代码"]                 # join 自动利用 key
```

Key 就像 SQL 里的主键和索引。声明之后，data.table 对数据做物理排序，后续查询和 join 走二分查找，性能从 O(n) 变成 O(log n)。更重要的是，**Key 声明了你对数据的语义理解**——哪些列唯一标识一行，数据按什么排列。

Pandas 曾经有 `index` 的概念，设计初衷类似，但用起来让人困惑——到底什么时候该 `reset_index()`，什么时候不该，社区自己都在吵。现在基本上大家都不太用了。

Polars 和 dplyr 干脆没有这个概念。每次 join 都得手动指定 on 列，无法声明"这张表的主键是什么"。看起来简化了心智模型，但丧失了一层重要的语义信息。

我自己的习惯是，拿到一张表就先 `setkey()`——这既是性能优化，也是告诉自己（和读代码的人）这张表的逻辑结构。

### 速度和 SQL 转换

速度也是 data.table 的强项，benchmark 上常年名列前茅。但对大多数分析场景，速度是次要的。

Polars 现在很火，主打速度。但我实际用下来，觉得它太繁琐了。上面那些例子就很典型——条件更新不支持原地修改，分组后回写需要 join，`pl.col("x")` 写得人手酸。速度快有什么用，如果写起来这么费劲？

至于 dplyr 能转 SQL 之类的卖点，说实话有多少人在生产中真正用到了？能转的都是简单查询，简单查询直接写 SQL 有什么难的。复杂查询那些跨语言转换的 edge case 根本处理不了，那都是些美好的幻想。

### 缺一个类型系统

上面说了那么多好话，但所有 DataFrame 工具——包括 data.table——都有一个共同的、根本性的缺陷：**没有类型系统**。

这里说的不只是列名能不能 autocomplete。我说的是一整套静态保障：这个 DataFrame 有哪些列，每列是什么类型，做了一步运算之后列会怎么变化，两列能不能参与某个运算。这些信息，目前没有任何 DataFrame 工具能在写代码的时候告诉你。多打了一个字符，少了一个下划线，列名拼错了，把 character 列拿去做算术了——全都要等运行时才会爆。

这意味着什么？意味着你的代码里必然存在大量"编程错误"——不是逻辑上想错了，纯粹是手误、拼写、类型不匹配这些本可以在写代码时就消灭的问题。

TypeScript 和 Rust 已经证明了一件事：好的类型系统能让你**写完代码通过编译，就基本确信在计算机层面是对的**。剩下的只可能是逻辑错误——你的业务理解有误，而不是你打错了一个列名。这两类错误的性质完全不同，前者需要思考，后者纯属浪费时间。

在 AI 辅助编程的时代，这个问题更加致命。AI 生成的代码不可能 100% 正确，但如果有类型系统兜底，linter 和编译器就能自动拦住大部分低级错误。没有这层保障，AI 写出来的 DataFrame 代码你不跑一遍根本不知道对不对——而且跑了也未必知道，因为有些错误只在特定数据分布下才会暴露。

我之前在[聊 R Shiny 的文章](https://shrektan.com/post/2025/05/05/from-r-shiny-to-fastapi-react/)里也说过，R 缺乏静态分析是它最大的工程短板。data.table 的表达力恰恰来源于 R 的动态性，而动态性天然和类型系统矛盾。但我不觉得这是死结。

我在琢磨能不能自己写一个 package 来做这件事——哪怕牺牲一些表达灵活性，换来列名和类型的可追踪。类似 type annotation 的机制，在 data.table 里能不能搞出来？不确定可行性，但我觉得这是 data.table 最值得突破的方向。
