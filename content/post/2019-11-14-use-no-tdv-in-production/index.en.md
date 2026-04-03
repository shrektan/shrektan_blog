---
title: Don't Use Tidyverse in Production
author: Xianying Tan
date: '2019-11-14'
slug: use-no-tdv-in-production
originalLang: zh
categories:
  - 技术
tags:
  - R
  - complaint
  - programming
---

Every time I systematically upgrade R packages, my biggest concern is the tidyverse-related code, because from time to time there are all kinds of "break the existing code" upgrades that give me headaches. Sure enough, previously valid code threw an error once again:

### This code now errors (but it didn't before)

```r
dplyr::mutate_at(data.frame(a = 1), "a", .funs = list(~as.character))
```

### You have to change it to the following

```r
dplyr::mutate_at(data.frame(a = 1), "a", .funs = list(as.character))
```

or

```r
dplyr::mutate_at(data.frame(a = 1), "a", .funs = list(~as.character(.)))
```

I started using dplyr around January 2014. It is somewhat closer to SQL, which makes it friendlier for beginners, and it is indeed significantly more efficient than the base R functions. On top of that, I was once "brainwashed" by the fantasy that *"you can operate on databases directly using dplyr syntax -- thus avoiding writing SQL statements yourself"*, and for a period of one to two years I used tidyverse extensively (mainly dplyr, really).

Gradually, I realized that the biggest problem with tidyverse is that it is not "mature" enough -- every so often there would be "destructive" upgrades. Yet it is a data manipulation tool that gets used many times in virtually every script, making every such change extremely painful and tedious.

Furthermore, while dplyr can operate on databases using the same syntax -- and I don't deny that this is quite useful in itself -- "truly avoiding writing SQL yourself" is indeed just a fantasy. The reason is that every language has rich details that must be precisely controlled when dealing with real-world problems. However, the details of different languages can never be perfectly aligned, meaning many things expressible in R are hard to express directly in SQL, and vice versa. Using dplyr to operate on databases is only viable for research; once it is actually used in production, you will inevitably encounter many "corner cases" -- for example, `dplyr::filter(FIELD %in% character(0L))` simply cannot generate a reliable SQL statement that returns a data frame with zero rows. Dealing with these corner cases is endlessly annoying, and you eventually realize that if you had just written SQL from the start, none of these troubles would have existed.

Also, I have started abandoning the habit of endlessly chaining pipes with `%>%`. At first, this approach did feel really clear. However, real-world datasets are nowhere near as simple as the examples -- the various transformations and processing steps are very complex. Introducing a reasonable number of well-named intermediate variables is what actually improves code readability. Moreover, once a bug appears, debugging piped code is truly inconvenient. Of course, pipes do have their advantages -- for example, I still use them frequently in Shiny-related code.

Finally, tidyverse now depends on too many packages, which leads to another problem: when an error occurs, it is very difficult to get a clear error message. Sometimes even after `traceback()` you still can't figure out where the problem actually lies.

Beyond these issues, although dplyr's syntax design is relatively easy to pick up, it also makes dplyr unsuitable for handling time-series data common in the finance industry, and unable to achieve optimal performance. data.table, on the other hand, is different -- its syntax is even more concise than dplyr's, which allows it to express richer intent within a single function call, making certain time-series operations more convenient and more efficient. Most importantly, data.table is exceptionally stable -- which is closely related to it having nearly zero dependencies. I personally made up my mind at the beginning of 2016 to stop using tidyverse entirely, switching fully to data.table and gradually rewriting some existing scripts. But with limited time and energy and far too many scripts, I was unable to fully complete this plan, which is the source of today's pain.

(Of course I know I could just not upgrade, but the relationships between tidyverse packages are very complex -- for example, if you upgrade rlang, you might have to use the new dplyr or things won't work. Besides, not upgrading only delays the problem rather than solving it, doesn't it?)

Although I only gave examples about dplyr, tidyr, rlang, and dbplyr have all had their share of backward-incompatible changes. Actually, I personally very much welcome upgrades, and I don't mind occasionally having to adjust source code. However, when a function as extremely common as `dplyr::mutate()` -- one that gets used many times in a single script -- frequently requires adjusting production code, I really don't dare use it anymore. Those who enjoy tinkering are welcome to tinker on their own.

In summary, setting aside whether tidyverse's design or syntax is good or bad, it is simply not mature enough for me, and I strongly advise against using it in production environments.
