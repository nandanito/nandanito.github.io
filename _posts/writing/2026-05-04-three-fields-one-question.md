---
layout: post
title: "Three fields, one question"
excerpt: "A notebook for working out loud across machine intelligence, quantum computing, and the digital-asset infrastructure those two fields are starting to reshape. Why I write here, and what is coming."
modified: 2026-05-04
category: writing
tags: [Project Notes, Cross-Domain, Intro]
author: nandan
comments: false
share: false
---

I started in physics. I'm still in physics, really, even when the surface labels have changed. The fastest way I know to introduce someone to the way I think is to say I've been a curious child for forty-something years and have not yet found a reason to stop.

<!--more-->

The work I do, and the work I write about here, is the working-out-loud of that curiosity — together with whatever I owe back to the people, the institutions, and the natural world that have made it possible for me to keep asking.

This notebook covers three fields.

**Machine intelligence**, mostly through the lens of how language models, retrieval systems, and learned representations encode — or fail to encode — the structure of the world they are trained on.

**Quantum computing**, with emphasis on near-term hybrid quantum-classical methods, honest benchmarking against strong classical baselines, and the longer-horizon question of whether quantum representations let us model systems whose dynamics classical methods can only approximate.

**Digital assets and the financial infrastructure those assets run on** — the field I currently work in professionally. This is where information becomes institutional state: balances, ownership, identity, collateral, settlement, and risk signals have to be represented correctly enough that banks, asset managers, regulators, and counterparties can act on them. Money has always been a social technology for transmitting knowledge about value and obligation. Digital-asset infrastructure makes that transmission programmable, auditable, and fragile in new ways.

These three fields do not sound related. To most readers, they are not. The reason I write across all three is that they share a single question I keep coming back to, in different vocabulary each time. The question is: **how does information become knowledge?**

In machine learning, the question is how a Transformer or a retrieval-augmented system turns a corpus of text into a representation that can answer questions about it — and whether what is learned is closer to structured competence or closer to compressed statistics. In quantum computing, the question is whether some classes of physical systems can only have their information faithfully represented on quantum substrates, and what that means for the world models we might eventually want to build. In digital assets, the question becomes practical and institutional: how do financial systems decide what is true — who owns what, who may transfer it, when settlement is final, and which risks are visible soon enough to matter? But it is the same question underneath. Information, structure, signal, knowledge — that is the thread. That thread has an older name: cybernetics, the line of thought about communication, feedback, and control. It will show up here more than once.

The honest version of my background runs physics → software → quantum, with each chapter overlapping the next rather than replacing it. Diplom Physik at Göttingen, then DFG-funded doctoral research in stellar astrophysics with observations at European Southern Observatory facilities in Chile, then a decade of software engineering in industry — financial infrastructure, decentralized identity, distributed ledger systems, and most recently digital-asset platforms inside banks and capital-markets institutions. The reinforcement-learning work I did as a research assistant at the Max Planck Institute for Dynamics and Self-Organization in 2002, controlling artificial-muscle systems through Q-learning agents that operated on Lagrangian-mechanics simulations, sat at an intersection — reinforcement learning and physics-based simulation — that the field would later have proper names for. It did not feel that way at the time. It mostly felt like work no one was particularly interested in, which is, I now understand, what most useful work feels like before it has a name.

I write because curiosity has a half-life if it is not shared, and because the people who taught me — formally and informally — invested time they could not recover in someone who could only repay them forward. The next people reading this are the ones I owe.

So that is what this notebook is for.

## What is coming next, in order

The two posts immediately following this one are introductions to the two projects I am currently most engaged with outside the day job.

**AstroLLM** is an open-source language-model project for astronomy and astrophysics — retrieval-grounded against NASA ADS, SIMBAD, and the NASA Exoplanet Archive, evaluated against research-workflow tasks rather than knowledge recall. The post explains why it exists, where it is, and what is coming.

**QMI Lab** is an independent research lab studying intelligence, learning, and representation across classical and quantum computation. Three pillars at three time horizons, one question underneath. The post lays out the principles and the current research.

After those two come the first technical pieces. **A post on quantum-safe digital-asset custody** — the most concrete cross-field question I can write right now, because the timeline on post-quantum migration for institutional custody appears to have compressed, and the engineering choices made in the next two years will determine how fast banks and asset managers can actually migrate. **A post on honest baselines for quantum machine learning** — the methodology question the QML literature is finally catching up with, and the standard I want every QMI Lab claim measured against.

After that, I expect the notebook to move between retrospective pieces — the 2002 Max Planck reinforcement-learning project is the one I owe myself first — evaluation notes on AstroLLM and on world-model methodology more broadly, and research reports as the work produces something worth showing.

The voice in everything that follows is the same voice that wrote this paragraph. Curious first, careful second, generous about what I do not yet know, allergic to claims I have not paid for. That is the rule of the house.

If you read something here that you want to pull on, the contact channels at the bottom of the site are live. I would rather hear that I got something wrong than have people quietly file it under things-I-disagree-with-but-will-not-mention. The point of writing in public is that the public answers back.