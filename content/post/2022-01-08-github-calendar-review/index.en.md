---
title: GitHub Calendar
subtitle: Some Memories
author: Xianying Tan
date: '2022-01-08'
slug: github-calendar
originalLang: zh
categories:
  - 随想
tags:
  - reflection
---

# Why

Today, while replying to a comment from my friend Yihui, I suddenly realized that since I started hanging around GitHub in mid-2015, I'd never gone this long without writing code — which tells you just how rough 2021 was. So I pulled up my GitHub contribution calendars[^1] from these years for a little retrospective, as a keepsake.

[^1]: Some of these contributions are from my open-source involvement, but a large portion came from work and lives in private repositories.

# 2015

![](images/%E6%88%AA%E5%B1%8F2022-01-08%2000.54.21.png)

I started my internship in 2012 and discovered a deep, genuine love for coding. From Excel to VBA to VB.NET to R, from writing simple scripts to solve problems to systematically learning coding standards, studying R packages, and reading professional books and documentation. In mid-2015, I went to Greece for my honeymoon. On the flight there, I started writing my first R package (for internal company use). The 10-plus-hour flight felt like nothing.

In the second half of the year, I began deploying an open-source Shiny Server on a virtual machine, and built an overseas investment trading management system (Shiny + DT) that handled order placement, risk control approvals, clearing and settlement, position management, and more — which is why I know every operational aspect of asset management so well.

# 2016

![](images/%E6%88%AA%E5%B1%8F2022-01-08%2000.54.37.png)

2016 kicked off with two circuit breakers in the stock market. The entire year was an endless stream of reports. Mid-year brought more upheaval — I was sent to Trieste, Italy, to Generali's European investment company headquarters for two weeks of training, and coding frequency dropped noticeably. In the second half, the market rebounded and my reporting workload eased up a bit — back to coding and optimizing daily workflows.

But the year wasn't without results. Early on, I replaced all the system interfaces originally written in VB.NET with Shiny. By year-end, frustrated by the countless inefficiencies in daily work, I wrote a new R package. It automatically synced data from the database daily, transformed it into a convenient format on disk, and provided unified, fast-access functions through the package to meet work needs.

This was my first attempt at high-level abstraction after my coding skills had matured, and I began developing some initial intuitions about I/O, data usage patterns, and architecture.

Throughout this year, I was sporadically studying C++ materials. Why learn C++? Because as a non-professional programmer, I always carried a sense of insecurity — feeling clueless about the lower-level workings of computers. Also, I'd been doing a lot of multi-factor model work those two years. In certain data processing scenarios, I keenly felt that R could handle the vast majority of my needs. But for specific cases — non-vectorizable operations, fine-grained data manipulation, organizing and managing large codebases — combining a static language with R as a dynamic language was the ideal approach. And since C++ is compatible with C, it integrates seamlessly with R, and it's fast — I figured I'd need that capability someday, so I started learning.

This was when I gradually built confidence in my coding abilities. I realized I could read C++ books and documentation on technical minutiae during subway rides, meals, and before bed (I read all of Scott Meyers' books several times over) without feeling tired. That's when it hit me: genuine passion is the best talent you can have.

It was also when I developed the concept that different tools suit different scenarios, and I began consciously paying attention to the applicable contexts and trade-offs of various technologies. Of course, I quickly realized C++ is an enormously complex language — mastering all of it in a short time was impossible — so I eventually focused only on the C++11 paradigm, which was perfectly suited for my use cases.

# 2017-2018

![](images/%E6%88%AA%E5%B1%8F2022-01-08%2000.54.45.png)

![](images/%E6%88%AA%E5%B1%8F2022-01-08%2000.54.55.png)

My assistant had grown capable enough to handle most of the portfolio management work (the miscellaneous-affairs club), so I wanted to focus on quantitative investing. From prior experience, I knew I needed a standardized, fast backtesting model and a factor management system. I had a quant assistant by then too. So from the second half of 2017, the two of us poured our energy into building the multi-factor quant infrastructure.

From this point on, I developed deeper thinking about how to organize code for large-scale models and how to store data.

But good times don't last. The 2017 style rotation and 2018 market crash made quant work extremely difficult. Mid-2018, I went to Japan for vacation — only to have a 6.1 magnitude earthquake hit that night. My wife was terrified and insisted we go home... After returning, I discovered that my portfolio management assistant had resigned...

So the entire second half of 2018 was spent filling the vacancy left by my assistant. A market crash meant endless reports, and the second half was consumed by just keeping up. I never got to devote myself fully to quant work again after that.

Early 2018, the Shiny Server on the VM couldn't handle concurrency and was getting increasingly sluggish. I spent some time researching the open-source ShinyProxy and decided to migrate the entire Shiny Server architecture to a ShinyProxy-based deployment. Thanks to my C++ learning experience, I found I could handle learning a bit of Java and Spring Framework to customize ShinyProxy.

Also in January, I received an email from Yihui inviting me to co-maintain the DT package — the beginning of my real open-source developer journey. Encouraged by Yihui, I attempted to once and for all fix the Chinese character bug in data.table that had plagued me for over two years — something I'm still proud of to this day.

# 2019

![](images/%E6%88%AA%E5%B1%8F2022-01-08%2000.55.03.png)

In March, a new portfolio management assistant finally joined. But after the merger of CIRC and CBRC, regulatory data requirements skyrocketed. Between that and training the new assistant, there was basically no time for anything else.

However, since the quant assistant was still around, and we noticed that the top-performing private quant funds were using deep learning for high-turnover strategies (T+0 was out of the question for institutional investors like us), we started exploring this approach from late 2018 into early 2019. Then my former boss left to accompany his child to school in New York — another round of chaos (serving a new boss). The quant assistant got assigned to various reporting tasks... and soon enough, feeling this wasn't going anywhere, he resigned too... Great.

Mid-2019, the STAR Market launched its first batch of IPOs under the registration system, and suddenly IPO subscription became incredibly profitable again. In October, a private fund approached us about a FoF IPO subscription product. That's when I started discovering I had a knack for product design — creatively combining regulatory requirements, client needs, and investment objectives.

# 2020

![](images/%E6%88%AA%E5%B1%8F2022-01-08%2000.55.12.png)

Our little one was born at the end of 2019, and life got busy. In February 2020, during the C-ROSS Phase II testing, I was working from home during the pandemic — designing IPO subscription product proposals, running calculations, and doing roadshows during the day, then reading documents, writing code, and verifying results at night. Five consecutive all-nighters later, I had turned the maddeningly complex C-ROSS Phase II work into an automated model. That's why we were virtually the only company where regulators found no reporting errors.

But the tragedy of my work situation was: so what? Almost nobody at the company knew — and even if they did, they wouldn't care — that I'd single-handedly handled the entire C-ROSS Phase II implementation, and done it well.

This was when I started feeling a mix of weariness and doubt about my work.

Of course, 2020 was also a year of rich harvests. The IPO subscription products our department spearheaded ended up selling around 10 billion yuan (hedged IPO, secondary-market IPO, structured IPO products, and more). To manage futures hedging across a dozen-plus products, I optimized every step of the trading workflow.

In October 2020, the company implemented the so-called "dual network separation" — separating the office network from the trading network to meet regulatory requirements. This involved a series of data center and network changes. But due to historical reasons, our asset management company shared part of the network infrastructure with the life insurance company, creating a ridiculous problem: the network speed from the office to the server room was painfully slow and would intermittently drop. My programs pulled large amounts of data from databases, causing frequent errors. So I spent a month migrating most programs to the data center servers (bypassing the slow network). Furthermore, since the data center couldn't connect to the internet, and my system was massive enough that some parts needed internet access...

Through a series of maneuvers, I managed to make it look like everything was running locally when in fact a large portion ran on the servers, with the entire user experience identical to before. I also added automatic retry logic for database connections when network errors were detected. And since much of the work still had to be done locally, I needed data transferred to my machine for interactive tasks. To solve this, I built both an in-memory caching mechanism and a disk-based caching mechanism.

Early that year, I also realized that my previous approach of dumping data locally worked well for quant analysis with large datasets, but was overkill for portfolio management where data volumes were more modest. Maintaining a local data backup was a hassle, and data synchronization was a nightmare. Meanwhile, I had developed a much deeper understanding of the portfolio management data tables and their design. So I tackled both fronts: systematically restructured the table schemas and wrote a new package that skipped local storage entirely, instead computing directly via SQL queries plus caching. This way, the data from this package was always correct, always up-to-date, and blazingly fast.

This work was genuinely difficult — managing portfolios across 200+ products worth over 200 billion yuan, with enormously complex data in constant daily use. I had to carry out this entire migration in whatever scraps of time I could find, without disrupting business operations, while ensuring complete data consistency. I'm quite satisfied with how I performed.

But the problem remained: so what? Nobody knows. Because this kind of work is like Bian Que — treating the disease before it manifests. People only notice firefighting. They never see the places that never catch fire.

Through this year of ordeals, I developed a much deeper understanding of system maintainability and architectural design.

# 2021

The first few months were normal work plus handover. After joining the new company in June, I barely touched code.

Not until late October could I finally catch my breath and start setting up the portfolio management database. Since the new company had no legacy baggage, the original system's complexity could be dramatically reduced. I essentially rebuilt the entire data layer of the old system in about two weeks (including time for configuring machines and deploying RStudio Teams). Now, adding a new field or modifying a view could be done through YAML configuration files — no more fiddling around in the PL/SQL interface. The added benefit was that data dictionaries and such were auto-generated. Best of all, this standardized approach meant I could delegate data maintenance work (like entering masses of non-standardized securities information) to IT colleagues, and just pull data from them.

![](images/%E6%88%AA%E5%B1%8F2022-01-08%2000.55.20.png)

# Epilogue

These past two years, I've increasingly felt a clear conflict between myself and this environment. I'm willing to provide professional knowledge consulting, design system architecture — these are things I'm good at and where I can create the most value for a company. But in a corporate setting, you're inevitably sucked into endless meetings, endless administrative tasks, with massive amounts of energy wasted. This feeling is especially acute when time is short and work is plentiful. Because as long as I'm at my desk, a constant stream of people comes to ask me all sorts of questions. So the time I actually have for focused work is already limited — waste another hour or two in meetings, and I can barely stand it.

I've also come to deeply appreciate that for creative work, I need to enter a state of [mental flow](https://en.wikipedia.org/wiki/Flow_(psychology)). Fragmented time simply doesn't work — it can only be used for administrative tasks. But isn't my value precisely in creative work? In doing things others can't? In systematically improving efficiency?

Yet in a corporate setting, that's just not possible. Even when you do improve efficiency, it gets swallowed by more work and more demands, or the surplus time gets wasted on yet more internal politics and busywork.
