---
title: 在负载均衡下使用DT
author: 谭显英
date: '2020-10-05'
slug: use-dt-behind-a-load-balancer
categories:
  - cn
tags:
  - tech
  - programming
  - R
  - load balancer
  - DT
---

过去这两年，陆陆续续一直有用户抱怨DT在负载均衡(load balancer)下使用不了，老是报错，比如[rstudio/DT#849](https://github.com/rstudio/DT/issues/849)和[rstudio/DT#642](https://github.com/rstudio/DT/issues/642)。

关于“负载均衡”，我其实之前并没使用过，只是出于兴趣大概了解了下基本的原理。它就是一种类似于反向代理的东西，可以把客户发来的请求，按一定规则合理地分配给背后不同的服务器去处理。

不过我技术方面的直觉还成，一看是Ajax相关的错误，立马就联想到一种可能：在服务器模式(server-side processing mode)下，DT会在shiny中注册一个数据对象，其可以处理浏览器发来的数据请求 —— 这一切发生在服务器A上。然而，浏览器发出的Ajax请求却被“负载均衡”引导至了服务器B，从而导致了错误。解决这个问题的办法，就是得通过某种设置，让“负载均衡”能够将当前会话的请求都引流至同一个服务器上。大概搜索了下，这个设置有个专有术语叫做粘滞会话(sticky session)。于是乎，我就回答了用户，希望他们尝试使用粘滞会话去解决此问题。

可是事与愿违，用户要么从此杳无音讯，个别反馈的却说“试了不行”。如此这般多了，我就有点怀疑自己的判断了，毕竟我也没实地部署过负载均衡——前两年折腾shinyproxy时有过这个打算，但我们公司那几十号人一台机器完全够用了——万一真的是哪里弄了个Bug呢？再加上Docker虚拟化的技术现在很成熟了，我也勉强算是会用吧，心想要不搞个基于Docker Swarm的负载均衡验证下。正好，[@richardtc](https://github.com/richardtc)提到他也是用Docker Swarm部署的，用的是[Traefik](https://traefik.io/)做负载均衡，而且还分享了部分相关的配置文件，这激起了我的热情，正好晚上有空，抡起袖子就上了。

（Traefik在我“肤浅”的看来，其实和[Nginx](https://www.nginx.com/)类似，但前者的优势在于其对Docker支持更到位一些，比如可以直接在Docker配置文件的服务labels里面写，而且能够实时监测到新生成的容器等，相对来讲更容易配置和管理。根据我过往“浅薄”的使用经验，Nginx配置的东西太多了，而且新生成容器后，老是需要reload下Nginx服务才行。)

一番搜索和鼓捣后，在参照[Yihui Fan](https://www.databentobox.com/authors/yihui-fan/) 的 [Effectively Deploying and Scaling Shiny Apps with ShinyProxy, Traefik and Docker Swarm](https://www.databentobox.com/2020/05/31/shinyproxy-with-docker-swarm/#optional-deploying-r-shiny-apps-without-shinyproxy)基础上，最后完成了[“DT在负载均衡下使用”的“可重复化”栗子](https://github.com/shrektan/DT-load-balancer)。运气不错，最初的猜测是正确的，如果用户**“正确地在负载均衡中启用了粘滞会话”**，那么DT是能够正常工作的。

那为什么会有用户声称自己配置了粘滞会话还是不行呢？一种可能的原因是，有时候用户认为自己启用了，但实际上没有。比如，我在鼓捣的时候就发现，在没有使用HTTPS的情况下，使用secured cookie实际上是不行的（@richardtc应该就是犯了这个错误）。系统虽然没有报错，但是浏览器压根就不会在普通HTTP中传输这个cookie，所以，Traefik只能把每一个请求都当做不同的会话来处理了……

所以，以后再有用户抱怨均衡负载和DT（其实shiny的下载功能也类似）不能共存时，我就可以理直气壮地说“请在均衡负载中开启粘滞会话，如果还不行，那么就是你的粘滞会话没有开启成功”。
