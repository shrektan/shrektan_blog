---
title: "Can't Bear with Encoding Any Longer"
subtitle: How much precious time has been wasted?!
author: Xianying Tan
date: '2018-05-07'
slug: cant-bear-with-encoding-any-longer
originalLang: zh
categories:
  - Tech
tags:
  - complaint
  - note
  - tech
  - R
  - encoding
---

### The RSQLServer Package Is Officially Retired

[RSQLServer](https://github.com/imanuelcostigan/RSQLServer) was [officially archived](https://cran.r-project.org/package=RSQLServer) on April 10, 2018. The author recommends using [r-dbi/odbc](https://github.com/r-dbi/odbc) as a replacement.

> This package is archived as there is now an excellent, much better supported package [odbc](https://github.com/r-dbi/odbc).

### Switching to the odbc Package

As a developer who has been lurking on GitHub for years, I noticed the odbc package quite early on. Indeed, odbc is faster and lighter (no Java installation required), and is under active development. RSQLServer, on the other hand, had been somewhat lacking in maintenance. On top of that, it introduced some dplyr features that occasionally caused conflicts, so I had been itching to make the switch. Although I ran some comparisons and tests and didn't find obvious issues, I was secretly worried about running into unexpected problems.

But since the switch was inevitable sooner or later, better sooner than later. I recall a classic statement from _"The Pragmatic Programmer"_:

> Refactor Early, Refactor Often.

### The Pitfall

Sure enough, it wasn't long before I noticed some scripts producing odd results. After half a day of debugging, I finally found the problem: _odbc does not pre-convert the SQL string encoding to match the database's encoding, unlike RODBC or RJDBC._ What made it especially frustrating was that I rarely use Chinese characters in SQL. The few Chinese characters that were there got converted to garbled text but didn't throw an error -- they just returned different results :rage:.

That morning I filed a report on GitHub [r-dbi/odbc#179](https://github.com/r-dbi/odbc/issues/179). I thought forcibly converting the SQL to the database's encoding should work (that's what `RODBC::odbcQuery()` does), but given that I'm really not a database expert, I decided not to submit a PR and embarrass myself. I'll leave it to the author [Jim Hester](https://github.com/jimhester) to solve...

### Wasted Time

In the world of computing, character encoding is truly a nightmare, especially on Windows (oh, and let's not forget that other nightmare: timezones). Looking back on my years as a developer, I've wasted countless precious hours on these two issues. Here are some of the more memorable ones:

* Accidentally opened a GB2312-encoded file with UTF-8 encoding, edited it, and saved it -- back when I didn't know how to use version control;

* Reading a date column from a `data.frame` fetched from a database, then using `as.Date()` which immediately gives you a date that's one day off -- because the `tz` parameter in `as.Date()` defaults to `"UTC"`;

* Getting a bunch of garbled text when reading from an Oracle database on Linux -- you need to set Oracle's language environment variable;

* Data stored on Windows turning into garbled text on Linux (the stored strings were in GB2312 encoding, while Linux can only display UTF-8 correctly);

* Writing Chinese in LaTeX, including getting Chinese bookmarks to display correctly in the PDF viewer -- only XeLaTeX can save you;

* Displaying Chinese in ggplot2 plots within a PDF -- you must set the relevant fonts in the plot to fonts available in the PDF, and the warnings seemingly never go away;

* I vaguely recall that `gsub()` from the base package (or maybe some other function) didn't support UTF-8 encoded input (seems to be fixed now);

* `roxygen2` and `devtools` support for Chinese on Windows -- [r-lib/roxygen2#532](https://github.com/r-lib/roxygen2/pull/532), [r-lib/devtools#1378](https://github.com/r-lib/devtools/pull/1378)

* A bug introduced in `data.table` version 1.9.7 -- see my [previous post](/post/2018/03/18/strings-encodings-in-r/), which tormented me on and off for nearly two years;

* A bug introduced in R version 3.3.0, causing the `match()` function to return inconsistent results for different encodings -- my [very first blog post](/post/2016/05/07/my-first-bug-report-to-r-project-org/) was about this;

* Database connections in R: some return UTF-8 encoded strings, others return strings in the native encoding -- you can only find out by trying;

* Our company's MS SQL Server stores data in GB2312. Certain data originating from UTF-8 sources turns into garbled text once stored;

* R generates timestamps without a timezone attribute by default (e.g., `attr(Sys.time(), "tzone")` returns `NULL`). When such a timestamp is saved and read on a different machine, you may run into problems if the two machines are in different timezones;

* Various data storage formats and their encoding support, e.g., [wesm/feather#335](https://github.com/wesm/feather/issues/335), [fstpackage/fst#114](https://github.com/fstpackage/fst/issues/144);

* Various htmlwidgets and their support for Chinese -- these issues seem to be getting rarer nowadays;

* The ROracle package requires SQL to be in UTF-8 encoding;

* ...


I imagine everyone has been tormented by these issues to some extent. But after all the struggling, how much of it was truly meaningful? The saddest part is that no matter how many pitfalls you've fallen into before, there are always more waiting ahead :joy:.

### (A little bragging about PRs I submitted to fix these issues)

* [r-lib/roxygen2#532](https://github.com/r-lib/roxygen2/pull/532): roxygen2 uses the Encoding field in DESCRIPTION, but previously always used native encoding, which caused many problems on Windows

* [rstudio/rmarkdown#841](https://github.com/rstudio/rmarkdown/pull/841): Long ago, yaml didn't handle UTF-8 very well, so rmarkdown had to make some internal changes to yaml reading. But they forgot that in addition to the final content, list names could also be UTF-8 encoded

* [Rdatatable/data.table#2566](https://github.com/Rdatatable/data.table/pull/2566), [Rdatatable/data.table#3451](https://github.com/Rdatatable/data.table/pull/3451), [Rdatatable/data.table#3849](https://github.com/Rdatatable/data.table/pull/3849): Fixed sorting, querying, and crash issues in data.table when dealing with non-ASCII characters -- I spent quite a while digging into these, and data.table's C code is pretty complex. I'm genuinely proud of getting these fixed, haha

* [rstudio/plumber#312](https://github.com/rstudio/plumber/pull/312), [rstudio/plumber#314](https://github.com/rstudio/plumber/pull/314/files): Enabled plumber to read UTF-8 source files and handle JSON containing UTF-8 content

* [Rblp/Rblpapi#278](https://github.com/Rblp/Rblpapi/pull/278): Rblpapi calls the Bloomberg API, but didn't mark the returned results as UTF-8, leading to garbled text

* [r-dbi/RSQLite#276](https://github.com/r-dbi/RSQLite/pull/276): RSQLite didn't mark returned column headers as UTF-8 encoded, resulting in garbled display

* [openanalytics/containerproxy#15](https://github.com/openanalytics/containerproxy/pull/15): ShinyProxy didn't convert encoding from Java's default UTF-16 to UTF-8 when sending user information to InfluxDB, causing garbled text when Chinese characters were involved

* [Rdatatable/data.table#3850](https://github.com/Rdatatable/data.table/pull/3850): `data.table::setnames()` couldn't correctly rename columns with Chinese headers

* [r-dbi/odbc#294](https://github.com/r-dbi/odbc/pull/294): The `odbc` package forced the returned timezone to UTC, which caused confusion and inconvenience for users

* [r-dbi/odbc#295](https://github.com/r-dbi/odbc/pull/295): The `odbc` package returned date values that were one day less than what the database stored

* [rstudio/rstudioapi#158](https://github.com/rstudio/rstudioapi/pull/158): On Windows, rstudioapi displayed garbled text after selecting a file with Chinese characters in its path

* [rstudio/htmltools#157](https://github.com/rstudio/htmltools/pull/157): On Windows, rmarkdown failed to display subsequent htmlwidgets objects after encountering a string with emoji characters

* [Rdatatable/data.table#4785](https://github.com/Rdatatable/data.table/pull/4785): `data.table::fwrite()` can now write UTF-8 encoded CSV files by setting the encoding parameter

* [ycphs/openxlsx#118](https://github.com/ycphs/openxlsx/pull/118): openxlsx is a powerful and user-friendly package for creating/modifying/reading Excel files. However, it would throw errors when comments or sheet names contained Chinese characters. I read through all the relevant R and C++ code and changed everything to use UTF-8 for input and output (since the xlsx format is UTF-8 encoded by nature). This should mostly solve the Chinese support issues once and for all (though there might still be a few edge cases I missed).

### The Future

According to these two articles by Tomas Kalibera, starting from Windows 10 (versions after November 2019), applications are allowed to use UTF-8 encoding to interact with the operating system. Therefore, after switching R and related packages' build tools to [UCRT](https://devblogs.microsoft.com/cppblog/introducing-the-universal-crt/), most encoding issues on Windows could potentially be resolved at the root. The articles don't explicitly lay out R's future roadmap, but at least we can see a glimmer of hope.

- [Windows/UTF-8 Build of R and CRAN Packages, Tomas Kalibera](https://developer.r-project.org/Blog/public/2020/07/30/windows/utf-8-build-of-r-and-cran-packages/)

- [UTF-8 Support on Windows, Tomas Kalibera](https://developer.r-project.org/Blog/public/2020/05/02/utf-8-support-on-windows/)

- [R-dev/WindowsBuilds/winutf8](https://svn.r-project.org/R-dev-web/trunk/WindowsBuilds/winutf8/winutf8.html)
