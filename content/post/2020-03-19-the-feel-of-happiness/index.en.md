---
title: The Feel of Happiness
author: Xianying Tan
date: '2020-03-19'
slug: the-feel-of-happiness
originalLang: zh
categories:
  - Random Thoughts
tags:
  - life
  - thinking
  - personal
---

In the blink of an eye, I'm already approaching forty, yet my sense of happiness keeps fading, and negative emotions surface from time to time.

# Work

I still remember my early days at work. I pulled all-nighters constantly, but I often felt genuinely happy. The reason was simple: a newly established company, severely understaffed, with mountains of miscellaneous tasks waiting to be done. It was exhausting, but my supervisors and colleagues felt like they were all pulling in the same direction, working together wholeheartedly to get things done. Perhaps because I happened to be a jack-of-all-trades, I could deliver decent results on tasks regardless of whether they were in my wheelhouse. The recognition from supervisors and colleagues, combined with constantly pushing my own boundaries, gave a young man in his early twenties a real sense of accomplishment and joy.

Among all that miscellaneous work, I could always find commonalities and shared patterns. My innate "laziness" drove me to hand off everything repetitive to computers -- not only to make life easier, but also to minimize errors. At the very least, once a bug was fixed in code, the same mistake wouldn't happen again, whereas manual work offered no such guarantee. Gradually, I built up an elaborate system of programs that could handle all sorts of data analysis needs in the asset management industry. I thought this would eventually free me from the mundane tasks, allowing me to devote my time and energy to things I considered more meaningful and important.

How naive I was.

The demands from the life insurance parent company kept growing. The shareholders wanted more. The regulators wanted more. The clients wanted more. The "jack-of-all-trades" became the "king of miscellaneous tasks" -- it seemed like any work involving data, portfolio analysis, or anything others couldn't handle would end up on our desks. The more we delivered, the more came our way. Nobody cared how much effort or dedication it took; all they could see was "you seem to handle it so effortlessly."

Sometimes I think about it myself and find it absurd. Who else works like this?

- Not only maintaining the entire investment management analytics system, but constantly adding new features as business needs evolved (in early 2019, to fix persistent frontend lag issues, I even picked up some Java and the Spring framework and modified the open-source ShinyProxy);
- Basic information for 200+ portfolios and 1,000+ securities was essentially maintained by us -- both automated imports and manual entries;
- Several internal R packages -- for shared utilities like database connections, investment performance analysis, quantitative multi-factor stock models, and mutual funds -- were mostly developed and maintained by us;
- All sorts of ad-hoc requests from regulators and clients: if a script existed, we'd run it, paste the results into an email, and send it off; if not, we'd write one on the spot (and don't assume these ad-hoc requests were rare -- in 2019 alone, we wrote 110 new scripts!);
- Board reports, portfolio reports, risk control reports, client reports -- anything related to investment data had to come through us;
- On top of that, maintaining stock multi-factor portfolio rebalancing (I no longer had any energy to improve it), and we also had to place orders for index futures hedging, monitor execution, and write all kinds of reports related to futures processes;
- When the company first applied for a derivatives license, we had to write most of the application report and sort out the entire workflow;
- Even opening futures accounts and applying for hedging quotas somehow fell on us -- sometimes I really felt...
- In 2014, when our company launched offshore business, the system wasn't ready yet, so they had me (not IT) build an offshore trading management system covering order placement, risk control, and settlement (that's when I first encountered Shiny and DT). Proudly, it ran for nearly two years without a single error;
- In 2015, I mentored a junior colleague in risk control to develop a risk metrics calculation system. After she left, nobody else could maintain it, and sometimes we had to step in;
- By late 2016, I finally had a window to dive into quantitative multi-factor work. To solve some systemic issues, I spent lunch breaks and late nights studying numerous C++ materials until I felt I had a solid grasp of it. I committed to building a complete factor model system in C++ and R that I was quite proud of -- only for the entire quantitative multi-factor strategy space to slump after 2017, making it impossible for a firm like ours to launch any products;
- Sales colleagues constantly had all kinds of data requests: tender documents, performance summaries;
- Various ad-hoc assignments from management, all kinds of PowerPoint presentations -- none of them simple;
- IPO subscription calculations now also required our involvement, plus roadshow attendance;
- WeChat messages from colleagues at the life insurance companies or our own firm, constantly asking questions -- not just wanting data and reports, but needing explanations of the "why" behind the numbers;
- ...

(One thing I'm proud of: no matter how busy I was, I never stopped learning and growing. In 2015, I passed all three levels of the CFA exams. In the fall of 2018, I committed to waking up at 4 AM to study and do math problems, and passed the SOA advanced-level Quantitative Finance and Investment exam -- pretty impressive, right, still solving stochastic process problems after all those years in the workforce. Of course, I've forgotten it all by now T.T. On the computing side, I've read tons of books and written even more code, and I genuinely strive for improvement every single time -- which, at its core, still comes from "laziness." I simply cannot stand doing the same thing twice.)

"We"... in truth, most of the time it was just me, alone. As if knowing how to code somehow meant the work didn't count as work.

Take a recent example. Last month, working on the "Solvency II Pilot Testing" project, the regulator sent nine technical documents, with the market risk section alone running 44 pages, packed with countless details. To complete this test, we also had to familiarize ourselves with the Phase I documentation (17 files). There was no time during the day, so it had to be done at night. I think my efficiency was already pretty high, but the sheer volume of details was overwhelming -- after producing the results, I still needed to compare each one against the Phase I results to identify discrepancies and rule out human error. For this, I pulled five consecutive all-nighters.

Many people probably don't realize that I might be one of the employees who stays up the latest at the company -- pulling 10 to 20 all-nighters a year -- for all sorts of reasons: management's excruciatingly high standards for PowerPoint decks (racking my brain), too many people asking for things during the day leaving zero time for real work so nights became the only option, the annual party video (yes, I single-handedly produced those for several years), and occasionally being in such a productive flow state that I'd push through to finish a major project in one go...

Is it hard? Yes. But is it worth it? Hard to say.

Such an enormous project, completed silently and without fanfare. Management didn't need to assign or coordinate it; they barely even needed to know about it.

Over these years, I seem to have done a lot of work, and perhaps I genuinely have, helping colleagues and the company solve problems. My supervisors and colleagues have always recognized me personally, and I'm grateful for that. Perhaps everyone knows that certain problems can be solved by coming to me. But as for what exactly I do or have done, I doubt anyone could clearly articulate it -- because my work is simply too "miscellaneous."

From my internship in July 2012 to now, it's been nearly eight years. I'm a seasoned veteran at this point, so why am I still this busy? No wait -- why is my work still this "miscellaneous"?

Much of this miscellaneous work matters to the company but does little for one's personal career development. Sure, I'm well-versed in many aspects of asset management -- trading, risk control, settlement, finance, operations -- I know all the links reasonably well. But so what? Who puts "jack-of-all-trades" in a job description? Besides, much of the work, especially regulatory data submissions, holds zero interest for me because literally nobody cares about the output. So why go through all that effort? Yes, our company's investment analytics system and database are excellent, but how many people in this industry truly understand the value of "accurate data + reproducibility"?

I don't think I'm someone who shies away from hard work or tedious tasks, but the meaningfulness of work matters deeply to me. Piles of tedious, exhausting work that goes unrecognized can sometimes leave me feeling utterly drained.

# Life

In 2019, I accomplished many major life milestones -- finished renovating and moved into our small apartment, our adorable baby was born, and we even sorted out the household registration before the baby arrived. I should feel happy about all this, and I truly do.

Am I demanding about my lifestyle? Yes and no. During my internship, I lived in a 5-square-meter partitioned room with plywood walls and got used to it after a year. I don't have many needs -- give me some black tea, a computer, books, and a phone, and I can spend a whole day contentedly. But I still hope for a slightly better life.

Yet sometimes I feel deeply frustrated. Why is it that with both of us earning decent incomes, no extravagant spending habits, and years of working, we still can't scrape together a down payment for a small two-bedroom apartment out by the eastern 5.5th Ring Road? After doing the math, we'd need to save diligently for several more years just to upgrade to a small two-bedroom, at which point all those years of savings would go straight to real estate. Setting the apartment aside -- how about a car? One of my few hobbies. Forget the license plate lottery; even the new energy vehicle queue won't come through until the year after next at the earliest.

I give up.

# In Closing

Maybe it's just that work has been overwhelmingly busy lately -- working from home somehow feels busier than going to the office. I'm exhausted, so here I am, venting.

A good night's sleep, and it'll be a brand new day.
