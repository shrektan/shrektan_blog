---
title: non-ASCII {.tabset} headers in Rmarkdown
author: Xianying Tan
date: '2018-04-21'
slug: non-ascii-tabset-headers-in-rmarkdown
categories:
  - en
tags:
  - R
  - note
  - programming
  - tech  
---

Generally, the rmarkdown package supports non-ASCII strings very well, e.g., the link on the table of content works even for pure non-ASCII headers. However, I was bitten when using non-ASCII headers with [the nice tabbed sections feature](https://rmarkdown.rstudio.com/html_document_format.html#tabbed_sections) recently. Luckily, I found the solution [rstudio/rmarkdown#1149](https://github.com/rstudio/rmarkdown/issues/1149) quickly, which I'd like to share to you.

The problem is that if the headers below `{.tabset}` contain non-ASCII characters, the produced html page may not display the tabbed sections or the tabbed sections display the wrong content (e.g., always display the content of the tab1). Here's a simple example (stolen from [rstudio/rmarkdown#1149](https://github.com/rstudio/rmarkdown/issues/1149)) :


```md
---
title: 你好世界
output: html_document
---

# 标题 {.tabset}

## 标签一

I'm tab1.

## 标签二

I'm tab2.
```

<img src="/post/2018-04-21-non-ascii-tabset-headers-in-rmarkdown_files/not-working.png" alt="non-ascii-tabset-not-working" height="500px"/>

There're two simple solutions to fix it:

1. Add an ASCII id mannuall,
1. Or, remove the `ascii_identifiers` extention by adding `md_extensions: -ascii_identifiers` to the YAML header of your rmarkdown file (not sure if there's any side-effects because I don't know why it's enabled by default).

### Solution 1

```md
---
title: 你好世界
output: html_document
---

# 标题 {.tabset}

## 标签一 {#tab1}

I'm tab1.

## 标签二 {#tab2}

I'm tab2.
```

### Solution 2

```md
---
title: 你好世界
output:
  html_document:
    md_extensions: -ascii_identifiers
---

# 标题 {.tabset}

## 标签一

I'm tab1.

## 标签二

I'm tab2.
```

<img src="/post/2018-04-21-non-ascii-tabset-headers-in-rmarkdown_files/working.png" alt="non-ascii-tabset-working" height="500px"/>

# Reference

[rstudio/rmarkdown#1149](https://github.com/rstudio/rmarkdown/issues/1149)
