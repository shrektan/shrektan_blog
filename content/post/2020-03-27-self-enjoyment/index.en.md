---
title: Self-Indulgence
author: Xianying Tan
date: '2020-03-27'
slug: self-enjoyment
originalLang: zh
categories:
  - 生活
tags:
  - life
---

A couple of days ago, I received a file shared in a WeChat group about data issues found in the C-ROSS Phase II pilot market risk filings across various insurance companies. I counted them up — a staggering 125 companies had data problems of one kind or another, with nearly every mid-to-large insurer prominently on the list. Yet I couldn't help but feel a quiet smugness: my company was not among them.

Having all sorts of issues is perfectly normal, though. That Excel file has so many cells. For each row of assets, you have to figure out how to classify them, which risk category they fall into, and each risk category requires different information. The number of possible combinations is simply overwhelming. Oh, and if an asset needs to be looked through, that single row of data multiplies into many rows. And if the underlying sub-account also contains assets that need to be looked through, well, it keeps multiplying...

With so many different pieces of information to collect and so many different relationships to handle, I honestly cannot imagine how painful it must be to do all of this manually in Excel. Not to mention that every time you refresh that Excel model, it freezes for several seconds.

Given this massive amount of manual work, how can anyone guarantee the correctness of the results? (As a mid-sized company, our total data volume alone is 3,000 rows by 80 columns — granted, only a fraction of that is actual data, but that's still a lot.) If you switch to a different reporting date, do you have to go through all that suffering again? If you switch dates, might the bugs you already fixed come back? Actually, even without changing the date, running it again would probably yield different results.

The only way out of this sea of suffering is to master the art of "reproducible reporting":

1. Clarify the relationships between data; manually collected data should be entered directly as CSV files.
1. Describe the data relationships and calculations in code.
1. Use Git for version control — keeping a full history of all changes to data and code.

Then just hit one button to generate an Excel file, copy and paste it into the regulator's template, and you're done. How satisfying is that?
