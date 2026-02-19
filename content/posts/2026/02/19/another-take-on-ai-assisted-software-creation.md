---
title: "Another take on AI assisted software creation"
date: 2026-02-19T21:50:58+01:00
draft: false
cover:
  image: https://oschvr.s3.us-west-2.amazonaws.com/2026/02/19_bois_de_la_cambre.jpg
tags:
  - ai
  - llm
categories:
  - programming
description: "Of course I need to put my opinion on the matter out there."
---

If you're asking, yes I use `claude code` and yes I've used it for my actual professional paid work. And no nothing has broken beyond repair.

I started exploring AI/LLM use for software engineering and programming tasks about a year ago, and as a data privacy paranoid, I still remember the immense feeling of risk I experienced. 

I mean... existentially... you were surrendering your data, your code, your intellectual property to a massive statistical machine that would use it to get fed, become bigger and thus perpetuate itself.

That is a phase is, very likely, past us... Now, the modern AI machine, is difficult to ignore.

And I feel like this is especially true if you're like me, working in the technology industry, as an engineer.

See, when I want to actually focus on some higher level system implementation, design a full end to end workflow, or actually go deep in an investigation, leveraging AI to do some of the grunt work, has been a delight.

> One thing to note here, and something I am completely open for advice or suggestion is that I am purposely an dumb AI user, in like I'm not really following up all the minutiae, benchmarks,  model releases... I just type `claude` in my terminal, select the piece of code I'm working on, or simply ask a specific request with some additional context and that's it.

I never know if I'm using Claude Sonnet 4.5 or Opus 4.6. I tend to ignore this and I just pay Mr Anthropic 20 USD a month for the privilege of not thinking about this (the default configs). It's been like this for about 3 months now, and I have not hit any limits. 

As I said, a **dumb AI user**

**Personal**

For personal stuff, experiments and such, is just great. 
Just now, before I started this entry, I asked mr `claude` if **it** could help me create a simple _WYSIWYG_markdown editor with "drag/drop" support that uploads pictures to my blob storage (AWS S3) without me running `aws s3 cp ...`

![wysiwyg.png](https://oschvr.s3.us-west-2.amazonaws.com/2026/02/19_wysiwyg.png)

I had to ask for a couple changes, some nice to haves and I did read what it produced... and voila ! Everything is local and works wonderfully.

**Work**

Now in terms of using AI to assist on my work, I always start from an accountability perspective, that is, in the end, it is **me**, the human that will push the `Merge` or `Deploy` button, so it is **me** who will get called when anything is not working or on fire.

With that in mind, I always always use my experience, knowledge and intuition to contest whatever the output is. Sometimes is easy to detect the deviation of the initial request (hallucination), sometimes the wording is incredibly convincing. 

When I feel like my knowledge on the matter can be complemented with what the LLM is suggesting, I do the simple following (what anyone sane would/should do anyway):

1. Commit current progress with a distinctive commit message
2. Push my changes remotely
3. Checkout to a new branch
4. Triple check (**Very important**) I don't have any live connection to prod (or even staging). Think of an open SSH session, or a `current-context` for K8s
5. Open `claude` code in my VSCode fork (either Cursor of VSCodium) and make sure [Claude for VSCode](https://code.claude.com/docs/en/vs-code) is installed
6. Narrow down the piece of code (by selecting) or files I want to work with
7. Request (prompt) a suggestion for a solution with as much context as possible
8. Assess responses and let it drive (in creating and updating stuff)
9. Test and validate (**Very important**)
10. Should the solution be expanded or reconsidered, go to 6 and change the request

I know it might sound like a long process but it's the safest approach I've found for myself for when you don't want to have any nasty surprise in production.

At this point I recognise that this approach is only possible to me because I have sufficient experience (>15y in front of the screen!) to recognise some patterns. 

And if Mr Anthropic ramped the price 10x ? I think I'll stop paying immediately, rely on the good old brain.

But what will the kids do ?
