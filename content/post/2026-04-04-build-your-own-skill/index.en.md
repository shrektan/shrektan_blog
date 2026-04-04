---
title: "Build Your Own Skill"
author: Xianying Tan
date: '2026-04-04'
slug: build-your-own-skill
originalLang: zh
categories:
  - Thoughts
tags:
  - thinking
  - tech
---

Garry Tan's [gstack](https://github.com/garrytan/gstack) has been everywhere lately — nearly 20,000 stars on GitHub, trending #1 on Product Hunt, discussed all over the place. Using this set of Skills, he averaged 10,000 lines of code and 100 pull requests per week over a 50-day stretch.

I installed it. Used it seriously for a while. Then deleted all of it.

Not because it was bad. There are genuinely useful ideas in gstack. The `/plan-ceo-review` Skill, for example, has the AI evaluate a feature from a CEO and product perspective — I found that valuable, since I tend to think in product terms rather than pure engineering. But after using it for a while, I realized the judgment framework behind it was Garry Tan's — his experience, the kinds of projects he's been exposed to, his decision-making preferences. It felt somewhat old-school, and didn't quite match how I think.

What I needed wasn't to copy his CEO review wholesale, but to reshape it into my own version.

That realization made me rethink what a Skill should actually be.

### Skills Are About How You Work, Not What You Know

A lot of people — myself included, at first — treat Skills as a way to "feed knowledge to the AI." Stuff in domain expertise, best practices, technical specs, make the AI more professional at its job.

But after spending time with this approach, I think it's more nuanced than that.

AI doesn't lack knowledge. Large models are trained on an enormously broad corpus, Web Search gives them real-time access to the latest information, and project context provides specific code and architectural details. The vast majority of "knowledge" you can think of, AI can already access on its own. Stuffing knowledge into a Skill not only eats up precious context window, but that knowledge tends to be either too broad to be useful or too narrow to be generalizable.

What a Skill should really do is describe how you approach your work — how you break down a task, how you make decisions, what to do first and what comes later, when to pause and rethink. Not "what is it" (knowledge), but "how to do it" (process).

Take blog writing as an example. AI knows Markdown syntax, knows Hugo's front matter format, knows a good article should have clear structure. That's all knowledge — no Skill needed. But "how to collaborate with me on a blog post" — first understand my raw material and intent, confirm the structure, draft, generate images, iterate — that's my way of working. That's what a Skill should capture.

### Everyone Works Differently

Once you see this, a natural corollary follows: **other people's Skills are worth studying, but unlikely to work for you out of the box.**

This isn't a quality issue. It's a fit issue. Everyone understands "how to work" differently. Some people plan before they code; others adjust as they go. Some write tests first; others get the main flow working and backfill tests later. Some reviewers focus on architectural consistency; others zero in on edge cases and error handling.

![Customizing your own tools](cover.jpg)

Back to the gstack example. I think the CEO review concept is excellent — stepping back to ask whether something is worth building from a product and business angle before diving into implementation. Many people with pure engineering backgrounds lack this perspective. But the specific evaluation criteria, the questions asked, the focal points in Garry Tan's Skill all carry his own experience and preferences baked in. I needed to extract the core idea and reorganize it around my own judgment framework.

So the question isn't whether gstack is good or bad. It's that **it reflects Garry Tan's way of working.** Your role is different, your projects are different, your thinking habits are different. Using his approach directly is like wearing someone else's shoes — not that the shoes are bad, but your feet are shaped differently.

### The Cost Is Low Enough to Go Personal

We used to rely on generic tools because customization was expensive. A SaaS product serving tens of thousands of users can only target the lowest common denominator — nobody's needs are fully met, but everyone makes do.

But the cost of customizing a Skill is essentially zero. It's a Markdown file. A few hundred lines describing how you work. No code to write, no architecture to design, no database to maintain. Change a line, save, and it takes effect in the next conversation.

Which means there's really no reason not to customize.

When the cost is low enough, "generic" stops being an advantage and becomes a compromise. A Skill that precisely matches how you think — even if it's rough and unpolished — will serve you better than a beautifully crafted Skill that wasn't designed for you.

### Find Your Own Iteration Loop

My advice isn't to start from scratch. Building a Skill from nothing is inefficient and risks reinventing the wheel in a vacuum. Here's what I do:

1. **Browse first** — Look around GitHub, community forums, see if there are Skills related to what you need. gstack, other open-source Skill collections, whatever.
2. **Try it, then ask why** — Use it for a while. Notice which parts feel smooth and which feel awkward. Pay special attention: what design choices make the smooth parts work? What assumptions make the awkward parts chafe?
3. **Reshape it to fit** — Fix the awkward parts, fill in what's missing. Nobody understands your way of working better than you do.
4. **Keep iterating** — Improve a little each time you use it. A Skill isn't a finished document. It should evolve alongside how you work.

This loop is what matters. Not finding the "right" Skill and sticking with it forever, but continuously iterating on how you approach your work.

### How You Work Is Your Most Unique Asset

Knowledge is shared — the same technical docs, the same books, everyone reads the same material. The knowledge AI can access is even more universal.

But how you work is yours alone. It's the distillation of your experience, preferences, judgment criteria, and working rhythm. It's what distinguishes you from everyone else, and it's where you can keep compounding your effectiveness.

Building your own Skill is really about making your way of working explicit. And once you've made it explicit, you don't just help AI collaborate with you better — you also gain a clearer understanding of how you actually work.

That's the investment I think is most worth making.
