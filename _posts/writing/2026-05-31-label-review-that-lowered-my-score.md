---
layout: post
title: "The label review that lowered my score"
excerpt: "A retrieval pilot over 500 real exoplanet papers scored Recall@10 in the low 0.8s; reviewing my own relevance labels pulled it down to 0.69. The drop is the part worth trusting."
modified: 2026-05-31
category: notes
permalink: /writing/notes/:title/
tags: [AstroLLM, Retrieval, Evaluation]
author: nandan
comments: false
share: false
---

The first pass at my retrieval pilot scored Recall@10 = 0.812 over sixteen graded queries, against 500 real exoplanet-atmosphere abstracts. Then I reviewed the relevance labels those scores were measured against, and the figure fell to 0.690 across twenty-nine queries. The drop is the part of the exercise I trust.

<!--more-->

## What the pilot does

AstroLLM is meant to cite real papers instead of inventing them, which makes retrieval the grounding layer: given an astronomy question, return the abstracts most likely to answer it. The pilot corpus is 500 abstracts from NASA ADS — the query `abs:"exoplanet atmosphere"`, 2018 onward, 500 of 4,845 matches. Two engines run in parallel and are then fused: a dense vector search (BGE-small, 384 dimensions, in pgvector) that matches on meaning, and a lexical BM25 index (SQLite FTS5) that matches on words. Reciprocal-rank fusion[^rrf] merges their two ranked lists. I grade the merged list with Recall@10[^recall] and MRR[^mrr].

## Why the number moved down

Three things happened in the review, and only the first was flattering. Re-reading query 06, I found I'd labelled a transmission-spectrum paper relevant to a question about dayside thermal emission — a different observable. Removing it pushed the headline up to 0.844. Had I stopped there, the review would have "confirmed" a score better than the one I started with, which is exactly the kind of review to distrust.

Continuing honestly pulled it back. I graded the conceptual queries I'd skipped on the first pass, and I stopped rounding away real misses: query 11 (WASP-121b) has no correct paper in its top ten, which is a 0.00 and belongs in the denominator. Twenty-nine of thirty queries ended up scored — one had no correct paper anywhere in the corpus — and the corpus-wide figure settled at Recall@10 0.690 and MRR 0.623.

## Labels track relevance, not rank

The rule I held to: a label records whether a paper answers the query, not whether the ranker found it. Query 08's top fused result — ranked first by the system — got marked irrelevant, because the abstract did not address what was asked. Queries 03, 05, and 18 stayed at 0.50, genuine partial misses I could have rationalised away. One correction went the other way: I'd overlooked that a sodium-detection paper was a valid second answer for query 07, which raised its reciprocal rank from 0.17 to 1.00. Corrections in both directions, judged from the abstract, never from where the ranker had placed it.

## Where it is actually weak

Split by query type, the result that matters shows up. On named-target queries — a specific planet, a specific measurement — Recall@10 is 0.794. On broad known-item queries — topic-shaped questions whose answer key is one or two landmark papers — it is 0.542. Lexical search is good with identifiers like WASP-39b; dense search handles paraphrase; the current hybrid first-stage baseline is weaker on topic-shaped questions with no single string to match. A cross-encoder reranker is the next hypothesis for closing that gap, because it reads the query and abstract together instead of scoring them apart.

Two caveats keep me honest about the 0.542. There are only twelve broad known-item queries and seventeen named-target ones — small on both sides. And because those answer keys are landmark papers rather than exhaustive topical relevance, 0.542 is the optimistic reading; true topical recall is likely worse. The corpus is 500 abstracts, too: an earlier 14-document synthetic fixture scored a perfect 1.000/1.000, which only demonstrates that a number without a real, confusable corpus is theatre.

Before building the reranker, though, I wanted to know whether hybrid fusion was even the right first-stage baseline. So I ran an ablation, switching each engine off in turn to see what it contributed. That is the [next note](/writing/notes/headline-that-was-within-noise/).

[^recall]: Recall@10 — of the papers labelled relevant for a query, the fraction that land in the top ten results, averaged over queries. With a single target paper per query it reduces to whether the right paper made the top ten.
[^mrr]: MRR, mean reciprocal rank — 1 ÷ (rank of the first relevant hit), averaged over queries: first place scores 1.0, third place 0.33, not found 0. It rewards ranking the answer high rather than merely surfacing it.
[^rrf]: Reciprocal-rank fusion — combine two ranked lists using only each document's rank in each, scoring 1 ÷ (60 + rank) and summing. Because it ignores the raw similarity scores, it needs no normalisation between the dense and lexical engines.