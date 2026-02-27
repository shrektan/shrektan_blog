---
title: Rust and R on Mac M1的一个注意事项
subtitle: 关于R、C++、Rust的流水账一篇
author: 谭显英
date: '2021-12-11'
slug: rust-and-r-on-mac-m1
originalLang: zh
categories:
tags:
  - note
  - programming
  - Rust
---

最近看到一个R包叫[rextendr](https://extendr.github.io/rextendr/)，能比较方便地把[Rust语言](https://www.rust-lang.org)和R语言粘起来。Rust语言我关注也比较久了，最近几年各大厂都开始使用，说明这个语言的确尤其过人之处，更重要的是使用的人多了就表明它变得成熟稳定而且配套的工具文档都丰富了起来。作为一个非专业的码农，我就不要去踩坑了，选择大神们走通的路就好。

之所以想用Rust呢，是因为我的工作中的确有少些使用C++的场景。比如有时候会需要静态语言特性，因为部分模型比较复杂，用R这种动态语言容易出错，而且数据的各种问题在过程中都可能发生，我需要很清晰地提示出来。再比如，做一些量化回测的时候既要对于很多细节能够进行控制，还要对计算效率要求比较高。这个时候用C++处理一部分计算的内容，的确会很好。

但是，我的确不太喜欢C++。一方面是坑太多，时时刻刻必须提醒自己要使用一个子集，不然就没法收拾。另一方面，上手难度很大，而团队同事程序基础好点的，也就勉强能改，因为要写好写对，需要记住的东西太多，对于头脑负担很大，结果就全变成我一个维护。最后，就是那些segfaults的点太难debug，编译能查出来的错误虽然是天书，但熟悉了也能看懂。最麻烦的就是，某个地方不小心写越界了，而这个路径还只有非常偶然的机会才触发，但一触发就崩。debug这种问题真心吐血------所以更不敢让别的同事写了。

Rust就很好地解决了很多问题，一方面代码再也不像看天书一般，很多C++的新特性（40年坑的结晶）都被移植了过去。另一方面，它是一门新语言，不需要考虑那么多历史遗留问题，而且主打的特性就是------效率和可维护性------这对我的场景来说非常合适。最后，它能很好地和C语言对接上，所以也就能很好地和R融合。

最近两天晚上抽空读了读[Rust的文档](https://doc.rust-lang.org/book/title-page.html)，感觉还挺好上手的（毕竟就是一个C++子集外加一些升级），很想试试和R这边交互的感觉。于是乎就试了试rextendr的包示例，执行`rextendr::document()`。

然后问题就来了：之前给我一直感觉很好的Rust，突然像疯了一样，吐了一大堆乱七八糟的字符，最后报错说无法load。感到很慌张------咋坑还这么多呢，难道又要让我去鼓捣那些编译的flag设定么------一顿瞎搜和检索无果后，就耐着性子看了看那堆字符，发现一个"嫌疑人"：

```
ignoring file /Library/Frameworks/R.framework/Versions/4.1/Resources/lib/libR.dylib, 
building for macOS-arm64 but attempting to link with file built for macOS-x86_64
```

联想到，那一大对乱七八糟的字符不就是在吐槽很多R本身的symbol找不到么，而找不到的原因是，我这电脑是arm64架构，但是libR.dylib是x86_64架构------“嫌疑人”更可疑了。

于是又联想到，上个月实在没有忍住新macbook pro的诱惑（M1芯片效率真的很高，14寸的和16寸电脑性能一样，而且电池状态下可以坚持很久），但是转移过来之后我并没有重装R------所以R还是用的Intel的架构下编译的版本。然而，Rust新编译的文件必然又会是arm64下的版本，所以就有了这个无法link的错误。

所以，从CRAN上重新下了一个[ARM64的R版本](https://mirrors.tuna.tsinghua.edu.cn/CRAN/)------搞定。

### 附：把Cargo的镜像更改为国内源的步骤（不然很卡）[^1]

编辑 ~/.cargo/config 文件（如果没有这个文件，那么你就自己创建一个），添加以下内容即可：

```toml
[source.crates-io]
replace-with = 'tuna'
[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```

[^1]: 来源：[Rust crates.io 索引镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/crates.io-index.git/)
