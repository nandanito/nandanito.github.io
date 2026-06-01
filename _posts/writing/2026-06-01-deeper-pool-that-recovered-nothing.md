---
layout: post
title: The deeper pool that recovered nothing
excerpt: When the corpus grew, the relevant papers stayed in the candidate pool but the fused ranking stopped surfacing them. I deepened the pool from 50 to 500 candidates per arm; the candidate union reached a perfect 1.000 and the fused top-10 did not change by a single query.
modified: 2026-06-01
category: notes
permalink: /writing/notes/deeper-pool-that-recovered-nothing/
tags: [AstroLLM, Retrieval, Evaluation, Fusion]
author: nandan
comments: false
share: false
---

[The last note](/writing/notes/widening-that-lowered-every-score/) ended on a question: when the corpus grew, the relevant papers were still in the candidate pool, but the fused ranking had stopped surfacing them — was that recall lost, or just sitting below a pool fixed too shallow? A deeper pool was the cheap thing to try, so I swept it: 50, 100, 200, 500 candidates per arm, on the same frozen index, everything else held fixed. It recovered nothing where it mattered: the fused top-10 did not move by a single query, even as the candidate union climbed from 0.948 to a perfect 1.000.

<!--more-->

## What I changed

This is the mirror image of the widening experiment. There I changed the corpus and held the method fixed; here I change one number — the per-arm candidate pool depth — and hold the corpus, the embedding, the index, and the fusion code fixed. No re-ingest, no re-embed, no re-index: the 2,500-abstract index from the last note is queried as-is at four depths. The metrics are the ones from [the first note](/writing/notes/label-review-that-lowered-my-score/).

Two guards matter. The harness refuses to write results unless pool 50 reproduces the last note's numbers exactly, so the pipeline cannot have drifted. And the scored cutoff — top-10 and top-50 — is held fixed while the pool varies, so "fused top-50 recall at pool 200" is measurable; that decoupling is the whole point. I also folded in the deferred reporting split, separating named targets, scored as recall, from topical ones, reported as coverage — by a rule committed before any of these numbers existed.

## What depth bought

Across all 29 queries:

| pool | candidate union | fused top-10 | fused top-50 |
|---|---|---|---|
| 50  | 0.948 | 0.592 | 0.793 |
| 100 | 0.966 | 0.592 | 0.862 |
| 200 | 0.966 | 0.592 | 0.828 |
| 500 | 1.000 | 0.592 | 0.845 |

The union — what the two arms find between them — rises with depth, as it must: a deeper pool admits more candidates. The fused top-10 is the flat column. It is 0.592 at every depth; not one query's top-10 changes between pool 50 and pool 500. The fused top-50 barely moves, and not even monotonically — it rises at pool 100, then falls back at 200. So the gap between what the candidate set contains and what the fusion surfaces does not close as the pool deepens. At pool 500 the candidate set holds every labelled paper, and the fused top-50 still leaves the same 0.155 it left at pool 50. The only real gain is the small fused top-50 bump at pool 100; past that, depth buys nothing.

## Why deeper didn't help

The last note asked whether sweeping the pool would recover the lost recall or merely relocate the question. It relocated it. The candidates are present; the fusion demotes them. A gold paper sitting mid-rank in both arms earns only small reciprocal-rank terms from RRF and lands below the cut no matter how many candidates are admitted around it.

At pool 500, seven queries have their relevant paper in the candidate set yet missing from the fused top-50. One is the WASP-96b paper that lexical alone surfaced in [the ablation note](/writing/notes/headline-that-was-within-noise/) — still in the pool, still left out. Several of the others sit in *both* arms' top-500 and are demoted anyway, the cleanest version of the problem: no single-arm blindness to blame. The complementarity counts do shift with depth — papers once exclusive to one arm migrate into both as the pool grows — but that redistribution does nothing for what fusion surfaces. The candidate set and the ranking are decoupled, and it is the ranking that binds.

## The arm edges didn't move either

I had a second prediction: as the pool deepened and fusion mattered less, the margins between arms would compress. They did not compress; they did not move at all. The dense−hybrid and lexical−hybrid Recall@10 margins, with their bootstrap intervals and leave-one-out checks, are identical at every depth.[^ci] The fragile edge from the last note stays fragile — hybrid over dense survives dropping 25 of 29 queries and collapses on any of the same four — and the robust one stays robust: hybrid over lexical survives all 29. Those margins live in the top-10 fused ranking, which a deeper pool did not touch.

## The lever

So the lever is not the pool. Against the frozen labels, the candidate set is already saturated — a perfect 1.000 for the named queries at every depth, and 1.000 across all 29 by pool 500. What decides whether a user sees the relevant paper in the top ten is RRF's ordering, which a deeper pool did not change at the top-10. The intervention that can turn candidate recall into top-k recall is a second stage that reranks the candidates a fixed pool already holds — the cross-encoder reranker I flagged as the next hypothesis in the first note. Whether it actually recovers the demoted papers is the next experiment, not a foregone conclusion.

If I stay on RRF in the meantime, the sweep sets an operating point: pool 100, which captures the one recoverable piece of fused recall — a query or two — at about 157 candidates per query. Pool 200 and 500 fuse three to seven hundred candidates and buy nothing, sometimes less. That is the whole return on a deeper pool, and the case for not spending the next week on a bigger net. The papers the labels call relevant are already in the net; the next thing worth building is the stage that reads them.

[^ci]: Paired-difference bootstrap, 10,000 resamples, seed 20260531; leave-one-out drops each query in turn and refits the interval to check it still excludes zero.