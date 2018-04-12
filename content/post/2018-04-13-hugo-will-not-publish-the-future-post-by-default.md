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

It's kind of annoying. I live in China. I have just finished a post for my blog. Current local time (Asia/Shanghai) is 2018/04/13 02:52. However, the Netlify server is in USA and the local time is 12 hours later, 2018/04/12 14:52 (assuming NYC). 

So I can preview my blog with my new writing article on my computer. However, I can't see it after pushing it to Netlify server.

What's happened? Do I do something wrong? I'm asking myself... Until I saw [this](http://gohugo.io/content-management/front-matter/):

> `publishDate`  
if in the future, content will not be rendered unless the `--buildFuture` flag is passed to hugo.

Great :rage: ! 
