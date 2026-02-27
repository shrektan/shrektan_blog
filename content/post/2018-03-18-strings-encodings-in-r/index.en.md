---
title: String Encodings in R
subtitle: Strings、Encodings in R
author: Xianying Tan
date: '2018-03-18'
slug: strings-encodings-in-r
originalLang: zh
categories:
  - 技术
tags:
  - R
  - programming
  - encoding
  - data.table
---

After quite a bit of effort, I finally managed to thoroughly fix the Chinese support issues in `data.table` ([PR#2678](https://github.com/Rdatatable/data.table/pull/2678), [PR#2566](https://github.com/Rdatatable/data.table/pull/2566)), [PR#3451](https://github.com/Rdatatable/data.table/pull/3451), [PR#3849](https://github.com/Rdatatable/data.table/pull/3849), [PR#3850](https://github.com/Rdatatable/data.table/pull/3850). Here are some scattered notes on what I learned along the way, for future reference:

### Learning Notes

- R objects are uniformly represented as the `SEXP` type at the C level (pronounced S-EXP, as in "external pointer", not "SEX P");
- The implementation details of strings in R use a string pool ([The CHARSXP cache](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#The-CHARSXP-cache)) for efficiency;
- For string sorting, both `data.table` and base R's radix sort cleverly use a largely deprecated SEXP attribute called [`truelength`](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#DOCF3). More specifically, they treat `The CHARSXP cache` as a hash table (key -> value) and store the values in the `truelength` attribute;
- At the C level, R character strings can only store three types of Encoding attributes: `Latin-1`, `ASCII`, and `UTF-8`. See [the last line of this section](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#Rest-of-header) and [R Internals - Encodings for CHARSXPs](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#Encodings-for-CHARSXPs);
- When using `SEXP` in R, you must always carefully consider whether the garbage collector might reclaim the variable. Bugs caused by garbage collection are extremely hard to track down — [data.table issue#2674](https://github.com/Rdatatable/data.table/issues/2674) took roughly 6 hours to resolve. The standard debugging workflow is "notice the anomaly, find the minimal reproducible code, locate the problem, fix it". However, since garbage collection triggers are unpredictable, reproducing such bugs is very difficult;
- There are two ways to compare strings: one is to directly compare the underlying byte representation (which you can inspect with `charToRaw()`), and the other is to convert both strings to UTF-8 encoding first and then compare;
- To determine whether a CHARSXP is ASCII or UTF-8, see:
    - [R-source/util.c](https://github.com/wch/r-source/blob/44d54d6f848468a7353d99cc9be0255105185975/src/main/util.c#L1834)
    - [data.table/data.table.h](https://github.com/Rdatatable/data.table/blob/bb3ba9a39be1ee8386b86909e045947898cb0935/src/data.table.h#L50)
- To convert a character string to UTF-8 encoding in R's C routines: `mkCharCE(translateCharUTF8(s), CE_UTF8)`;
- Debugging often requires printing variable values, but `Rprintf()` in R's C routines can only print characters in the native encoding. Therefore, you must first convert the string using `translateChar` before printing, e.g., `Rprintf("%s", translateChar(value))` — otherwise you will get blank output.

> [Character-encoding-issues](https://cran.r-project.org/doc/manuals/r-release/R-exts.html#Character-encoding-issues): However, if they need to be interpreted as characters or output at C level then it would normally be correct to ensure that they are converted to the encoding of the current locale: this can be done by accessing the data in the CHARSXP by translateChar rather than by CHAR.


### Other Notes

- `enc2utf8()` takes a noticeable amount of time for long strings, and there is no particularly good workaround;
- It is recommended to convert all `non-ASCII characters` to `UTF-8` encoding at the R level before proceeding with any processing;
- Encoding issues on Windows are a real headache. A key reason is that among mainstream platforms, only Windows does not use UTF-8 as the default character encoding, and different language locales have different default encodings. The `data.table` encoding issues I encountered could only be reproduced on Windows with a Chinese locale (of course other language locales would work too, but you would need to adjust the examples accordingly). This is why the bug I reported in 2016, [#1826](https://github.com/Rdatatable/data.table/issues/1826), was ignored for two years — other people either did not use Windows, or if they did, they were not using a Chinese locale. Once I realized this, I understood that I was the only one who could fix this problem, which is why I invested so much effort into studying it (I simply could not stand it any longer, and no one was going to help).

    **Update:** This assertion is somewhat inaccurate. As mentioned earlier, R can store `latin1` encodings, so by reformulating the problem using `latin1` encoding, the issue can be reproduced on any computer! Example: [`data.table`'s tests](https://github.com/Rdatatable/data.table/pull/2678/commits/8e04d53496432f66c1f1655e1aa0ab1d8f01c70a).
- After fixing this issue, [Mattdowle](https://github.com/mattdowle) invited me to join the [Rdatatable Team](https://github.com/Rdatatable). I hope I can help `data.table` improve its support for Chinese (and other languages).


### Key References

- [Writing R Extensions](https://cran.r-project.org/doc/manuals/r-release/R-ints.html)
- [R Internals](https://cran.r-project.org/doc/manuals/r-release/R-exts.html)
- [R source code](https://github.com/wch/r-source)
- [Hadley's R-internals](https://github.com/hadley/r-internals)
