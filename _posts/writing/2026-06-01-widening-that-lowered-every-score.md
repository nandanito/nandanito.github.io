---
layout: post
title: The widening that lowered every score
excerpt: I made the corpus five times bigger expecting better coverage. Every score on the same queries got worse, and the gap I had already decided to build on grew wider.
modified: 2026-06-01
category: notes
permalink: /writing/notes/widening-that-lowered-every-score/
tags: [AstroLLM, Retrieval, Evaluation, Corpus]
author: nandan
comments: false
share: false
---

I expected the bigger corpus to help. [Post 2](/writing/notes/headline-that-was-within-noise/) closed on a falsifiable question — as the corpus grows, does the class of papers only one retrieval arm can find grow with it, or stay the singleton I had seen at 500 abstracts? To check, I widened the corpus five times over, held the method fixed, and re-ran the same three arms on the same queries with the same labels. Every score on those queries got worse. One thing did move in the architecture's favour: the gap a second retrieval stage feeds on.

<!--more-->

## What I changed

The pilot drew 500 abstracts from a single ADS phrase query. I kept the query, the 2018 year floor, and the embedding, index, and fusion code all identical, and only took a deeper citation-ranked cut: 2,500 abstracts, with the original 500 preserved as a byte-identical subset. The metrics are the ones defined in [the first note](/writing/notes/label-review-that-lowered-my-score/).

One honest caveat up front: a deeper cut of the same query admits younger, less-cited papers, so corpus *size* and corpus *recency* move together here by construction. The 2,000 new abstracts skew hard towards 2024–2026. This experiment isolates the method, not those two axes from each other.

## What got worse

On the same 29 queries, with the same gold labels, every arm lost recall and rank. Recall@10 fell from 0.724 to 0.529 for dense, 0.713 to 0.437 for lexical, and 0.690 to 0.592 for hybrid; MRR and Recall@50 fell in step. The proximate mechanism is mechanical: 2,000 more papers push the relevant ones deeper, and a candidate pool fixed at 50 is now 2% of the index rather than 10%.

The arm ordering flips. In the pilot, hybrid had the *lowest* Recall@10; on the widened corpus it has the highest on every split and degrades least. Lexical collapses hardest — what you would expect when BM25's OR-of-tokens matching meets five times as many token-matching distractors.

These are honest deltas, because the queries and labels did not change. What I did *not* do is re-review the gold set for the larger corpus, so these are not the widened corpus's final recall — only its recall against the pilot's labels.[^relabel] That relabel is deferred.

## What got better

One thing moved the other way. The premium the pooled candidate set holds over dense alone — the recall a reranker would gain from seeing both arms rather than one — grew from +0.069 to +0.172 at Recall@50. In absolute terms the union barely moved, from 0.966 to 0.948, while each single arm fell much further, towards ~0.78–0.81. The class of papers only one arm catches grew from 5 to 15, in both directions.

So the case for a two-stage design — both arms feeding a later reranker — got stronger, not weaker, as the corpus grew. I want to be precise about how much. Hybrid beating lexical at Recall@10 is robust: the gap survives dropping any single query.[^ci] Hybrid beating *dense* is not — that edge rests on four queries and dissolves if you drop any one of them, so I read it as suggestive only. The durable claim is the pool-level union premium, which does not rest on a handful of top-10 query wins. And the mechanism behind the growth was not the one I had guessed: the single-arm class grew because recent newcomers displace older relevant papers out of one arm's pool, not because new papers arrive that one arm is blind to.

## A premise that broke

I had expected widening to pull two earlier coverage misses into the corpus. It cannot, and not for lack of depth. One target's abstracts never contain the exact phrase the query requires; the other's canonical papers predate the 2018 floor. The whole phrase universe is 6,492 papers, and 2,500 already samples over half of the post-2018 slice. These misses are a query-recall problem, not a corpus-size one, and they need a different lever: widening the query, not the corpus.

## The open question

The pilot had hybrid winning at depth 50; that inversion is gone. Hybrid's fused top-50 now sits at 0.793 while the union it draws from holds 0.948 — the fusion is leaving recall on the table that the candidate set still contains. With the pool fixed at 2% of the index, this experiment cannot say whether that recall is genuinely lost or just sitting below a pool that is now too shallow; the pool was held fixed by design. Whether sweeping it recovers the recall or merely relocates the question is [the next note](/writing/notes/deeper-pool-that-recovered-nothing/).

[^relabel]: Recall is reported only where the relevant set is much smaller than the cutoff; where a named entity matches dozens of in-corpus papers, Recall@k stops measuring ranking and is reported as coverage instead.
[^ci]: 10,000 bootstrap resamples, seed 20260531; "robust" means the 95% paired-difference interval excludes zero under every leave-one-out drop.
