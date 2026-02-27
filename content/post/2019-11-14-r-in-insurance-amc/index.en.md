---
title: Practical Applications of R in Insurance Asset Management
subtitle: Talk at the "Insurance Company Economic Capital Seminar"
author: Xianying Tan
date: '2019-11-14'
slug: r-in-insurance-amc
originalLang: zh
categories:
  - Tech
tags:
  - finance
  - sharing
  - note
---

# Background

In mid-October, at the invitation of a former professor, I went back to my department to share some applications of R in insurance asset management, primarily to introduce what R can do. Since I'm not great at impromptu speaking, I prepared a written script in advance. I spent several days carefully preparing it, so I've lightly organized and shared it here.

# R Can Play an Important Role in Every Stage of Data Modeling

## "Reproducibility" Is Crucial for Both Research and Work Efficiency

- Research is about constant trial and error, and work involves continuous repetition and improvement. "Codification" can greatly enhance the ability to make things reproducible;
- Compared to expressing ideas through natural language, code forces us to specify every detail clearly and precisely—otherwise we get incorrect results;
- Code is the model and computational logic. Given the same data and the same execution environment, it is guaranteed to produce the same results. Feed it new data, and it automatically produces new results;
- Real-world work is about continuously building new workflows to address new problems. If a new workflow can be codified, machines can be relied upon to repeat the same tasks, ensuring both accuracy and speed—thus improving work efficiency;
- Code is text, so every improvement to a model can be faithfully recorded (thanks to version control software like Git), and even if a change turns out to be wrong, it can be easily reverted.

## Steps of Data Modeling / Data Analysis

Data analysis work, at a high level, can be summarized in three steps: **Data Preparation (Input) -> Data Modeling (Modeling) -> Data Output (Output)**. Of course, this is an iterative process—after obtaining results, we need to examine and analyze them, then adjust the data and model accordingly, repeating the cycle. After nearly 30 years of development, R has built a powerful software ecosystem that provides solid support for every stage of data analysis.

## Data Preparation

Data preparation is the process of reading raw data from various sources, preprocessing it, and transforming it into structured data suitable for modeling.

### Characteristics of Financial Industry Data — Diverse Data Sources and Relatively Large Data Volumes

In terms of asset classes, standardized products like equities and bonds can be obtained from third-party data providers, while non-standardized products like debt investment plans and trusts can only be recorded manually. Wind provides more comprehensive information for domestic assets, while Bloomberg is the go-to for overseas assets. Some data can only be obtained through web scraping...

R provides a fairly complete set of tools for accessing data from various channels. For example, text data such as CSV can be read with `data.table::fread()` or `readr`, Excel data with readxl, Wind data with WindR, Bloomberg data with Rblp, and databases—whether SQL Server, Oracle, Access, MySQL, or SQLite—all have excellent support. Web scraping is of course supported as well.

### The Complexity of the Real World Creates Complex Raw Data, Which in Turn Creates Complex Data Processing

In real-world data analysis work, it is no exaggeration to say that 90% of the time is spent "cleaning" and "integrating" data—especially in the financial industry. Since data is never perfect and always has various "quirks," data preprocessing is the process of understanding these quirks to integrate and transform the data into the structure required by the model. The inherent complexity of the data means the processing can be extremely complex, requiring ideal data processing tools to have the following characteristics:

- **Strong interactivity:** R is a "working environment" with excellent interactivity—you can execute a command and immediately see the result, preview statistical characteristics of data in the same window, and benefit from strong visualization capabilities;
- **Strong expressive power:** R is a language developed by "statisticians," designed from the start to serve data analysis. It has the ability to express user intent accurately in a concise form;
- **Fast computation speed:** High-level abstraction and computation speed often conflict, but R has a native ability to interface with other languages, which addresses this issue well.

Furthermore, for large datasets, processing speed becomes particularly important. Thanks to R being a language developed by "statisticians," R's data processing tools are arguably "the best on the planet." Here's a simple example: most financial data is closely tied to time—time-series panel data. Suppose I have table A with securities held by a portfolio on different dates, and table B with some information (e.g., prices) for all securities on different dates. Now I need to find the "latest available price" for each security in table A as of its corresponding date. How would you do this? R's data.table package lets you accomplish this in a single line: `B[A, roll = TRUE, on = .(CODE, DATE)]`, and it executes extremely fast (even if table B has tens of millions of rows, it can typically complete within 1 second).

## Model Building

For most people, the reason they use R is that some "new" statistical method has a ready-made package available in R. So another key feature of R is that it has **a large number of ready-made statistical and econometric tools available, and their quality is generally high**. This is thanks to R's popularity among statisticians and CRAN—the official R package repository—which enforces strict quality control.

Model building requires statistical tools, but not all tasks are R's strong suit. For example, R is an interpreted dynamic language, and its operating principles and design philosophy make it suitable for vectorizable scientific statistical computations. For certain specific detailed problems, languages that are more "computer-sciency" like C/C++ may be more appropriate. Similarly, for machine learning and especially deep learning, Python-related libraries and ready-made code tend to be more abundant. **R is a programming language with the ability to glue together other languages**, making it easy to call functions and code written in C/C++/Python.

In practical work, different tasks are interrelated rather than completely independent. This means that mechanisms for sharing functions and models are very important. For example, many tasks require reading data from the company database. We want every script to be able to easily establish a database connection, rather than copying and pasting a large block of configuration code—which is neither elegant nor maintainable. Because any specific model, workflow, or function must be continuously iterated and updated as business practices evolve. **R has a very complete and powerful extension mechanism—the package system—that makes it very convenient to codify and share model code.** Through this mechanism, the iterative updating of tools or knowledge can be well integrated with actual workflows. For instance, after fixing a bug or adding new functionality, other colleagues only need to update the package to automatically get the new code.

Additionally, **R has excellent backward compatibility and cross-platform capabilities**. Company models are often used for many years. We want to upgrade R versions and package versions to take advantage of the latest language features, while also wanting our previously written code to continue running without various bugs. R places great emphasis on backward compatibility—code written perhaps 20 years ago can still run perfectly today. As business grows more complex, previously written code may need to be applied to scenarios that were not originally planned for, such as Linux servers. R's excellent cross-platform capabilities allow you to switch platforms directly without additional adjustments.

Finally, it is worth mentioning **R's open-source nature and its healthy community environment**. The open-source nature ensures that for any specific computational function, we can analyze its source code whenever we want—there are no "black boxes." More importantly, open source means more people can easily participate in R's evolution, which means new technologies, methods, and tools can be quickly incorporated into R. A healthy community environment means that when searching for answers to specific technical questions, we can quickly find results and even receive help from R users around the world—which is extremely important for beginners. Additionally, **R's package documentation system is very comprehensive—many packages have extensive and detailed help documents and tutorials, making it easier to get started**.

## Output

**R has powerful plotting capabilities**. Quite a few people may have started using R precisely because they needed to make plots. ggplot2 is a very well-known package based on "The Grammar of Graphics," establishing a systematic relationship between data and graphics that makes it easy to create various visualizations that would be difficult with other tools.

Beyond traditional static graphics, **in recent years R has built a solid ecosystem around web technologies, and many JavaScript visualization libraries can be easily called and rendered using R**. For example, Baidu's echarts library can be used to display various dynamic visualizations, but probably only computer science students would know how to use it directly, and it is quite disconnected from the data analysis workflow. In R, you can simply execute one line of code to convert "data" into beautiful echarts dynamic visualizations, without worrying about the underlying technical details.

**R is one of the languages with the best support for "literate programming," and one of the earliest to support this feature, making automated reporting much easier.** In practice, the routine updating of many reports does not involve structural changes—they simply regenerate based on new data following the original template. "Literate programming" refers to writing reports that combine prose with programming code. When the document is executed, the code sections are automatically converted to their corresponding values, achieving both automated report updates and a tighter connection between text and data. knitr/rmarkdown/blogdown/bookdown make automated reports, personal blogs, and even book writing very simple.

Beautiful and intuitive interactive model interfaces allow us to better and faster understand data, understand models, and discover patterns. Perhaps when reading a report we always wonder "what would the result look like if I changed this parameter?" But we studied actuarial science and statistics, not computer science—and building complex interactive systems requires non-trivial engineering effort. **Shiny is a truly magical tool in the R world—it allows someone without IT skills to easily build an interactive web application to showcase their models**.

## Summary

R has powerful data analysis expressive power, rich data processing tools, excellent interactivity between human and machine and between programming languages, outstanding extensibility, and a healthy software ecosystem. These qualities make it one of the most suitable languages for data analysis and modeling.

# Application Examples in Insurance Asset Management Companies

## Insurance Asset Management Portfolio Analysis System

The data in insurance asset management is extremely complex, for the following reasons:

1. Asset classes are diverse—public funds, private funds, exchange-traded, OTC, securities, non-standard assets, domestic, overseas, foreign currency, derivatives. Different assets often correspond to different data sources, and even the same asset can have many data dimensions;
1. There are many investment portfolios—the number of parent company accounts plus third-party products often reaches hundreds or even thousands;
1. The asset management industry changes rapidly, constantly encountering new market conditions, new investment products, and new regulatory requirements.

The first step in portfolio management is having a clear understanding of portfolio information. However, integrating information across multiple accounts and multiple asset types is extremely difficult, because it requires deep familiarity with both the integration of different data sources and the business of asset management—and more importantly, it requires continuously meeting new demands arising from constant changes. The inherent complexity of the business makes it impossible for IT departments and software vendors to produce accurate information tables. The common industry practice is to export raw tables from systems, then manually process and verify them, and use these verified position tables to complete subsequent model and metric calculations.

This approach has many drawbacks:

1. Too many manual steps make it both inefficient and error-prone;
1. Markets change rapidly—we need timely information, but this approach makes it difficult to obtain accurate, effective information promptly;
1. Due to the difficulty of replicating source data, systematic portfolio analysis reporting systems become a luxury.

R has strong data integration, processing, and transformation capabilities. Leveraging these, we used R to directly read and parse raw data from accounting/valuation systems, trading systems, and data vendors, building one of the best portfolio foundational databases in the industry. It contains comprehensive multi-dimensional information including positions, trades, profit and loss, cash flows, and derived security information. Because the parsing is fast, it can achieve rapid synchronization with the accounting/valuation system. Furthermore, since the entire parsing process is transparent, the source of every data point can be clearly traced (this is extremely important, because data errors are inevitable—when anomalies appear in an analytical report, you need to clearly know whether it is a data error or a computational logic error).

After solving the accuracy and reproducibility of the core foundational database, we first codified many commonly used analytical functions in the form of R packages, so that other colleagues only need to call these functions when performing related analyses.

Building on this foundation, we established three different approaches for daily work:

1. Script-based: A series of program code to accomplish a specific task. These are typically various data requests from colleagues or clients. When needed, we run the script, which generates an Excel file and opens it automatically—we then paste it into an email or PowerPoint;
1. Automated reports: For routine analytical reports, we create LaTeX or R Markdown templates that run automatically on a daily or weekly basis. The system automatically generates reports and sends them to the relevant recipients' inboxes, or posts them on the company intranet;
1. Shiny-based web applications: As introduced earlier, Shiny helps us rapidly develop specific web-based applications where users can control different options to get the results they want. For information that colleagues frequently need but doesn't fit the report format, we built a system using Shiny (deployed at scale with Docker) that allows querying various information and metrics across different time periods and different portfolios (or combinations of portfolios), along with many handy features—such as automatically converting different departments' work plan Excel files into polished work plan PDFs...

In summary, **using R as our tool, we were able to gradually codify complex and difficult work, break down tasks, and thereby make work simpler and more enjoyable.**

## Equity Multi-Factor Quantitative Strategy Development and Backtesting System

The equity multi-factor framework involves quantifying stock characteristics into data—labeling them—then analyzing and exploring these labels, aiming to discover patterns (models) for constructing quantitative strategies with favorable risk-return profiles. Some characteristics of the data include **relatively large data volumes, rich dimensions, and tedious detail handling**. The most critical aspect of model design is ensuring computational speed and clarity of computational logic while avoiding any possible use of future information. Because future information is unavailable in actual trading, research that incorporates future information typically performs very poorly in real trading.

As mentioned earlier, research is an iterative process, and the speed of iteration partly determines the speed of our research. Since the entire process involves extensive details that cannot be vectorized and must be processed element by element, we ultimately chose C++ as the core computation engine. Let me briefly mention the benefits of using C++: on one hand, when used properly, C++ can achieve extremely fast computation speeds. On the other hand, object-oriented programming is very useful for solving certain problems. For example, if the backtesting model is designed to mirror the real trading environment—that is, the portfolio manager - risk control - trading desk - exchange - clearing model—it makes the model's control over trading details more intuitive and richer. Additionally, using the concept of proxy objects can completely eliminate the possibility of using future data in the computational logic (although future data in terms of data and ideas can never be fully eliminated), while barely affecting computation speed. Thanks to R's excellent support for C and C++, we only need to focus on using C++ for what it does best—computation—while for tasks that C++ is not as good at, such as data input and result output, we can still use R to handle them excellently. This combination improves the overall efficiency of model building while making computation speed and maintainability better.

# Closing

I hope to see more and more people join the R community and apply R to their real-world work and studies.
