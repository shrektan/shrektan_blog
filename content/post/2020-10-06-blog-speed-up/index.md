---
title: 博客提速小记
subtitle: 拿来主义
author: 谭显英
date: '2020-10-06'
slug: blog-speed-up
originalLang: zh
categories:
tags:
  - blogdown
  - personal
  - tech
---

刚刚用手机登录了下自己的网站，发现连接速度超级慢。用浏览器查看了下资源载入消耗的时间，发现了两个“罪魁祸首”：

1. yihui.name/js/center-img.js和yihui.name/js/math-code.js : 不知为何，最近半年来在天朝访问益辉兄的网站速度极慢，这相关资源的加载必然也就永无尽头，而且还是非异步的。于是乎，在益辉兄网站的[Github仓库](https://github.com/yihui/yihui.org)里扒出来了[源文件](https://github.com/yihui/yihui.org/tree/be87d74a0cf5ac8bf54fa14cd00dd6ba3b674be0/static/js)，替换之。

1. disqus的js文件 : Disqus被墙是很早的事了，其实可以换一个别的，但是我想也没必要。猛然想起年初看益辉兄的博客，Disqus而且出现了“大陆地区无法访问Disqus”的字样，而且显示速度还挺快。当时还以为是Disqus的脚本更新了，现在转念一想，应该是益辉兄又鼓捣了什么秘密武器。于是继续祭出搜索大法，顺利发现了[秘诀](https://github.com/yihui/yihui.org/blob/be87d74a0cf5ac8bf54fa14cd00dd6ba3b674be0/layouts/partials/disqus.html)，复制粘贴之。

在天朝访问本小侠网站的速度总算变得“嗖嗖嗖”的了，开森。
