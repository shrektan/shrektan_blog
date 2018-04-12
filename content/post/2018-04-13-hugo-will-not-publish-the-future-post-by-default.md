---
title: Hugo will not publish the "future" post by default
author: Xianying Tan
date: '2018-04-12'
slug: hugo-will-not-publish-the-future-post-by-default
categories:
  - programming
  - tech
tags:
  - web
  - material
---

It's annoying. 

I live in China. I have just finished a post for my blog. The current time (Asia/Shanghai) is `2018/04/13 02:52`. However, the Netlify server is in USA and the local time is 12 hours earlier, `2018/04/12 14:52` (assuming NYC). 

So I can preview my blog with my new writing article on my computer. However, I can't see it after pushing it to Netlify server.

_What's happened? Do I do something wrong?_ I was asking myself... Until I saw [this](http://gohugo.io/content-management/front-matter/):

> `publishDate`  
if in the future, content will not be rendered unless the `--buildFuture` flag is passed to hugo.

So changed my post date from 2018/04/13 to 2018/04/12 and it works.

Great :rage: !
