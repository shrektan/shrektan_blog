---
title: Render Rnw and Email PDF reports in RStudio Connect
author: Xianying Tan
date: '2022-03-30'
slug: render-rnw-and-email-pdf-reports-in-rstudio-connect
originalLang: en
categories:
  - Tech
tags:
  - tech
  - rmarkdown
  - rnw
  - rstudio-connect
---

# Background

RStudio Connect is great. It allows you to deploy Shiny Apps and share RMarkdown reports in minutes with minimal costs. It provides user-access control, app / report's version controls, fixing package version, periodical report generating, alarming you when something wrong, tracing user usage stats, the audit log, etc. With RStudio Connect, a Shiny developer can focus his/her energy on "developing ideas" instead of IT infrastructure setting-up or boring maintenance related works. Moreover, RStudio Connect has a user-friendly UI, so deploying a new content no longer costs an expert (that is me in our company)'s precious time.

RStudio Connect provides a great "framework" on production-ready Shiny and RMarkdown content management. I love "framework". Not only "framework" brings unified operation logic, thus less knowledge to master, but also it restricts the freedom of what users can do. I often find myself grateful on resisted the impulse of "doing more".

However, I do need to do one thing "more". Recently, I need to render Rnw files to PDFs and send out these PDF reports via email, on customized periodicity. I want the report to be generated automatically in RStudio Connect, so that I can use the same user-access control and view the previous reports conveniently.

RStudio Connect can render RMarkdown files to PDF reports. It can send out the email with PDF attachments as well. It can also scheduled the task. Why can't I use the native features? Why do I even need PDF reports, isn't HTML report enough? ... I'm going to continue this article in a Q&A style.

---

# Q&A

## Why do I need PDF reports?

Simple. The clients ask for this. Why do they have to use PDF reports? Convention, people used to it. In addition, PDF reports are beautiful and very easy to be shared. You can anticipate exactly the same beauty no matter what the device is. 

It's not true for HTML reports.


## Why do you have to use `$LaTeX$`?

I must use `$LaTeX$` as our report's style is often highly tailor-made. I'm not a fan of `$LaTeX$` but it solves the problem. It has been used by millions of people over many years. You can always find way to achieve the style you want. Just a matter of how much time it takes you there.

## Can I use RMarkdown to render PDF reports?

Yes, I can use RMarkdown to render (Chinese) PDF, thanks to [`rticles::ctex()`](https://github.com/rstudio/rticles/blob/main/inst/rmarkdown/templates/ctex/skeleton/skeleton.Rmd). The steps are: 

1. Remove the "title" meta in yaml. Otherwise, the default pandoc template makes a title page for me. I never want that.

1. Set the output to `rticles::ctex` so that I can use the `$LaTeX$` package `$ctex$`, which is a must for reports containing Chinese.

1. Set up the `$LaTeX$` options and this is the tricky part. In Rnw files, I can put all those "preamble" codes into one place - the Rnw file. But in RMarkdown, I need to carefully read [the pandoc template](https://github.com/jgm/pandoc/blob/master/data/templates/default.latex), and put some `$LaTeX$` package set-up in the yaml and some in a "preamble" tex file. The tex file is registered by adding the path to "output/rticles::ctex/includes/in_header" in the yaml meta. You can find my sample yaml in the Appendix.

1. For all those inline R code (e.g., `\Sexpr{*R-code*}`), you should replace them with `` `r *R-code*` ``.

## So, why do I choose to use Rnw to render PDF reports?

No strong reasons. If I don't need to write many text, but just running automated reports, I prefer to have all the codes in one place. But in RMarkdown, I need a separate file, the preamble.tex. In addition, since I need to tweak the style a lot, with this pandoc layer, I may not easily tell the cause when something is wrong.

But I do consider to use RMarkdown, if the report contains lots of human-write text. It makes my eyes a lot easier.

## Again, why can't I use RStudio Connect to directly render PDF reports and send out the email?

RStudio Connect can render PDF reports with RMarkdown source files. 

The reason I can't use this feature in this case is not about Rnw: I need to generate two reports with two different parameter (product name) and sending out the two report in one email. However, RStudio Connect can only send out one report in one email.

In addition, the periodicity in RStudio Connect is not flexible enough: It can only set periodicity like once a day (Monday to Friday) at a fixed time. What I need is to send out the report at every trading day - it's slightly different from the working day. 

Yes, I can set a checker in the Rmd file to throw errors when the rendering day is not expected. But it will trigger an annoying false error report.

Finally, it seems that the email receiver can only be the RStudio Connect users but I need to send out the email to clients out of our organization. I also need to separate copy-to receivers from direct receivers, but it's not supported by RStudio Connect. Not to say that custimize the email content seems far more difficult than directly providing HTML email content to `blastula::smtp_send()`.

## Ok, how do I solve this problem?

I had two ideas:

1. Running this task (rendering reports and sending email) in a docker container. Now I can customize everything by writing R code but the drawbacks are:  

    - I need to maintain a docker image with correct R package versions for this report and "future" reports. The truth is, once you open a backdoor, you can never close it.
    - The share of these reports can no longer managed by RStudio Connect. It means I have to set-up all these tedious user-access control, twice.
    - The audit-log, security check?

1. Scheduled a periodical RMarkdown report in RStudio Connect: 

    - Since we can run arbitrage R code in RMarkdown, we can render two Rnw files to two PDF reports.
    - Then we can send out the email by calling `blastula::smtp_send()` with any custimized email content.
    - We can even take advantage of the parameter RMarkdown report by setting the receivers as an RMarkdown parameter. The parameter can be changed interactively in RStudio Connect. Modifying the receiver no longer needs to change the source code.
    - In this report, it renders nothing (just a message) when it's not a trading day. So it won't trigger any alarm email.
    - On trading day, it renders two PDF files. We can use the cool RMarkdown feature, "output files" via calling `rmarkdown::output_metadata$set(rsc_output_files = ...)`. So we can put two links on the HTML report which link to the PDF reports. 
    - If any "real" error happens, I can get a "real" alarm email.
    - The HTML report can be shared to other colleagues, so the whole history of the report can be accessed, easily.
    
Apparently, any rational people would choose option 2. 

I'm rational.

## Anything more?

Life is never easy. Programming is similar to life.

Soon I encountered two errors when running `knitr::rnw2pdf()` inside of a RMarkdown file:

1. We can't simply knitting something else during knitting. This is probably `knitr` uses some common or global variables, e.g., `knitr::opts_current()`. No easy way to solve this issue as long as in a same R session. Luckily, we don't need to. Thanks to `callr::r()`, we can call `knitr::rnw2pdf()` in a different session. Problems solved.

1. `file.rename()` fails to copy the PDF file in the current working directory to the user's temporary directory, on RStudio Connect. Locating this issue is not easy as it works good locally. Frankly speaking, I don't quite understand. But the solution is clear: just keep the PDF file in the current working directory (I shouldn't have tried to move the reports to temporary directory, as they needs to stay in the working directory to be shared as "rsc_output_files"). 

---

# Appendix

## An example yaml meta for RMarkdown to PDF

```yaml
documentclass: ctexart
classoption:
- a4paper
- landscape
hyperrefoptions:
- pdfstartview=FitH
- bookmarks=true
- pdfpagelayout=OneColumn
- bookmarksopen=true
- bookmarksnumbered=false
- CJKbookmarks=true
- colorlinks=true
colorlinks: yes
output:
  rticles::ctex:
    fig_width: 7
    fig_height: 3.5
    latex_engine: xelatex
    includes:
      in_header: resources/preamble.tex
```      
