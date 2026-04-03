---
title: From R Shiny to FastAPI + React
subtitle: From Human Coding to Vibe Coding
author: Xianying Tan
date: '2025-05-05'
slug: from-r-shiny-to-fastapi-react
originalLang: zh
categories:
  - 技术
tags:
  - Python
  - R
  - Shiny
  - tech
---

![](images/image1.png)

During the May Day holiday, I took a few days of annual leave, originally planning to spend quality time with my kid. To my surprise, starting from the very first morning, my child came down with acute gastroenteritis---days of vomiting, diarrhea, and zero appetite. While caring for the little one, I found some time to explore the FastAPI + React + Tailwind tech stack. **My gut feeling is that, combined with "Vibe Coding" (AI-assisted programming), this stack is better suited for production work environments than R Shiny, even when the use case is primarily data reporting and visualization.**

## The Magic of R Shiny

I started using R Shiny in late 2014, making me one of the earliest adopters. The excitement I felt the first time I used it is still vivid---it was the first web framework I'd encountered that could deliver rich interactivity with such minimal code. It was especially well-suited for internal systems like asset management: mostly multi-dimensional data display with relatively little user input.

It's worth remembering the context. Back then, the data science wave was just getting started again. Python barely had a decent DataFrame library (Pandas had only recently arrived), and interactive data visualization frameworks were virtually nonexistent. Building anything interactive was incredibly clunky---if you went the web route, you had to write mountains of HTML and JS. R Shiny felt like magic: just a few dozen lines of code could produce a beautifully polished web-based data dashboard. From 2015 to 2022, I built several medium-to-large projects with R Shiny at work, primarily around portfolio analytics.

## The Underwhelming Python Shiny

In recent years, RStudio rebranded to Posit and launched Python Shiny, but it never really took off. I tried it a few times and found that the community ecosystem hadn't materialized, and it failed to properly leverage Python's engineering strengths---it felt like an awkward in-between. Ironically, simpler Python frameworks like Dash gained more traction instead. This made me wonder: why couldn't the R Shiny philosophy, which I found so powerful, be replicated successfully in the Python ecosystem? Clearly, limited adoption of the R language alone doesn't explain it.

## The Shortcomings of the Shiny Framework

Through years of working with R Shiny, I gradually came to recognize some inherent limitations of the framework itself. The commonly cited issues---single-threaded execution, production readiness---actually have workable solutions. Especially with high-performance data processing tools like data.table, performance is usually not the bottleneck. However, R Shiny's greatest strength is also its weakness: the concise, flexible expressiveness comes at the cost of engineering rigor, which becomes particularly apparent in medium-to-large projects. Specifically, there are two main drawbacks:

1. Lack of static analysis support (an inherent weakness of the R language)
2. Hidden complexity from the coupled front-end/back-end architecture

Both issues have become even more pronounced in the AI era.

### The Cost of Missing Static Analysis

The lack of static analysis stems from R's fundamentally dynamic nature. Unlike Python, R never gradually adopted a type system. This absence creates problems on several levels in real-world engineering:

**1. Unpredictable function return types**---you have to manually handle countless edge cases, which is especially painful in complex interaction chains.

**2. Excessive cognitive load**---in practice, you typically invest heavily in building a system during the initial phase, then maintain and iterate on it in scattered chunks of time afterward. Even with careful decoupling at design time, the absence of a type system means every change is a leap of faith in terms of impact assessment. Systems need continuous refactoring to evolve, but each refactoring cycle demands that the developer re-familiarize themselves with the entire codebase and reconstruct the mental model---practically impossible in a real work setting. The result is a productivity trap: development starts out agile, but maintenance becomes a slog, and the team eventually resists adding any new features.

**3. A poor fit for the AI era**---in today's world of AI-assisted programming, lacking static analysis may be a fatal flaw. AI coding capabilities are powerful but never 100% correct. Unit tests only catch part of the problem. A solid type system enables static analysis to flag common issues, unlocking more of AI's potential.

I had hoped Python Shiny would address these issues, but as mentioned: its community is far less active than R Shiny's, unable to cover real-world needs (e.g., no powerful table library comparable to DT); static analysis support is weak, with constant linter errors during use; and the design is awkward---neither familiar to R Shiny users nor comfortable for Python developers. It feels like a half-baked product.

### The Hidden Costs of a Coupled Architecture

The problems caused by front-end/back-end coupling are more insidious and represent a fundamental constraint of the Shiny framework. For small display projects, this is perfectly fine---producing beautiful, interactive data presentations with concise code is already impressive. However, many work scenarios demand fine-tuning and granularity control over details.

Shiny's advantage lies in abstracting away front-end details, but in these scenarios that becomes a liability---you either spend significant time digging into the underlying mechanics, or resort to workarounds. Beyond the lack of front-end granularity, the more critical issue is how a coupled architecture undermines the distillation of clean computational models.

The upside of a coupled architecture is a lower barrier to entry and less boilerplate. The downside is that back-end models and business logic inevitably get tangled up with front-end code. This makes it difficult to extract a cleanly separated computational model or achieve true decoupling at the business concept level. What appears to be concise code with seemingly low coupling gradually becomes a significant obstacle as the project evolves. Whether adjusting the UI or modifying business logic, developers must re-navigate the entire project first, creating the same kind of "cognitive overload" problem as the lack of static types. This is likely the key reason why medium-to-large projects lose their ability to evolve and eventually stagnate.

In theory, you could implement front-end/back-end separation within R Shiny, but doing so throws away Shiny's core advantage---at which point there's little reason to use it at all.

## FastAPI + React

This gave me an opportunity to study the design philosophy of REST APIs. Its stateless design is essentially a resource-oriented architecture that achieves low coupling at the system design level, bringing significant benefits to architectural design, computational elasticity, and more. Python's FastAPI framework is quite mature, and combined with Pydantic, it offers excellent static analysis and runtime type guarantees, ensuring type stability for data consumed by the front end.

On the other side, React + Tailwind CSS has been battle-tested and iterated on by countless companies, making it extremely powerful and mature. With AI tools (such as Cursor, Windsurf, etc.), we no longer need to hand-write extensive HTML or memorize arcane CSS properties to design attractive front-end pages. Thanks to the separation of concerns and React's modular nature, the mental overhead of adjusting page content is greatly reduced. Moreover, this architecture forces you to think carefully about what resources and models to expose at the REST API layer. Examining your business model through the lens of resources often yields fresh insights.

Based on my hands-on experience over these few days, this tech path may be a better fit for my current work scenarios. Additionally, our company's Posit Connect platform supports static page and FastAPI deployment quite well, which means I can smoothly transition to the new framework and tooling within my existing workflow.

## Conclusions and Recommendations

R Shiny remains an excellent framework that shines within the R ecosystem. It's well-suited for small-to-medium data display projects, particularly in research-oriented rather than production business settings. Python Shiny, due to design issues and community immaturity, is only recommended for small, informal projects---though you could also consider alternatives like Python Dash, which offer similar capabilities with potentially more active communities (meaning easier problem-solving).

For larger projects, I recommend building the back end with a REST API framework (such as Python FastAPI), using React + Tailwind CSS for the front end, and leveraging AI tools throughout development. This approach delivers polished results quickly while maintaining system maintainability and extensibility.
