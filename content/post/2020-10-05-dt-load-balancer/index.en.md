---
title: Using DT Behind a Load Balancer
author: Xianying Tan
date: '2020-10-05'
slug: use-dt-behind-a-load-balancer
originalLang: zh
categories:
  - Tech
tags:
  - tech
  - programming
  - R
  - load balancer
  - DT
---

Over the past two years, users have been intermittently complaining that DT doesn't work behind a load balancer, constantly throwing errors, such as [rstudio/DT#849](https://github.com/rstudio/DT/issues/849) and [rstudio/DT#642](https://github.com/rstudio/DT/issues/642).

Regarding "load balancing," I actually hadn't used it before and only had a rough understanding of the basic principles out of interest. It's essentially something similar to a reverse proxy that distributes incoming client requests to different backend servers according to certain rules.

However, my technical intuition served me well. As soon as I saw it was an Ajax-related error, I immediately thought of a possibility: in server-side processing mode, DT registers a data object within Shiny that can handle data requests from the browser -- all of this happens on server A. However, the Ajax request sent by the browser gets routed by the load balancer to server B, which causes the error. The solution would be to configure the load balancer so that all requests from the current session are directed to the same server. After a quick search, I found that this setting has a specific term: sticky session. So I replied to the users, hoping they would try using sticky sessions to resolve the issue.

Unfortunately, things didn't go as planned. Users either went silent after that, and the few who did follow up said "I tried it and it didn't work." After this happened enough times, I started doubting my own judgment. After all, I had never actually deployed a load balancer myself -- I had planned to when I was tinkering with ShinyProxy a couple of years ago, but a single machine was more than enough for the dozens of people at our company -- what if there really was a bug somewhere? On top of that, Docker virtualization technology is quite mature now, and I can more or less use it, so I thought why not set up a Docker Swarm-based load balancer to verify. Conveniently, [@richardtc](https://github.com/richardtc) mentioned that he also deployed with Docker Swarm, using [Traefik](https://traefik.io/) as the load balancer, and even shared some of the related configuration files. That sparked my enthusiasm. I happened to have a free evening, so I rolled up my sleeves and got to work.

(In my "superficial" view, Traefik is actually similar to [Nginx](https://www.nginx.com/), but Traefik's advantage lies in its better Docker support. For example, you can write configurations directly in the service labels of the Docker Compose file, and it can detect newly created containers in real time, making it relatively easier to configure and manage. Based on my "shallow" past experience, Nginx has too many configuration options, and after creating new containers, you always need to reload the Nginx service.)

After some searching and tinkering, building upon [Yihui Fan](https://www.databentobox.com/authors/yihui-fan/)'s [Effectively Deploying and Scaling Shiny Apps with ShinyProxy, Traefik and Docker Swarm](https://www.databentobox.com/2020/05/31/shinyproxy-with-docker-swarm/#optional-deploying-r-shiny-apps-without-shinyproxy), I finally created a [reproducible example for "using DT behind a load balancer"](https://github.com/shrektan/DT-load-balancer). Luckily, my initial guess was correct: if users **"correctly enable sticky sessions in the load balancer"**, DT works just fine.

So why did some users claim that they had configured sticky sessions and it still didn't work? One possible reason is that sometimes users think they've enabled it, but they actually haven't. For example, while tinkering with it, I discovered that using a secured cookie doesn't actually work when HTTPS is not being used (@richardtc likely made this exact mistake). The system doesn't throw an error, but the browser simply won't transmit that cookie over plain HTTP. As a result, Traefik can only treat every request as a different session...

So from now on, whenever users complain that load balancing and DT (and Shiny's download functionality, which has a similar issue) can't coexist, I can confidently say: "Please enable sticky sessions in your load balancer. If it still doesn't work, then your sticky sessions haven't been enabled successfully."

### Related Resources

- [Effectively Deploying and Scaling Shiny Apps with ShinyProxy, Traefik and Docker Swarm](https://www.databentobox.com/2020/05/31/shinyproxy-with-docker-swarm/#optional-deploying-r-shiny-apps-without-shinyproxy)

- [shrektan/DT-load-balancer](https://github.com/shrektan/DT-load-balancer)

- [Quick Start - Traefik](https://doc.traefik.io/traefik/getting-started/quick-start/)

- [Docker Swarm](https://docs.docker.com/engine/swarm/)
