---
layout: post
title: "The headline that was within noise"
excerpt: "I wrote down three predictions about which retrieval arm would win, then watched the aggregate Recall@10 ranking dissolve into noise at twenty-nine queries. The findings that held up were single queries, not averages."
modified: 2026-05-31
category: notes
permalink: /writing/notes/:title/
tags: [AstroLLM, Retrieval, Evaluation, Ablation]
author: nandan
comments: false
share: false
---

Before running the ablation on my retrieval pilot, I wrote down three predictions about which of the three arms — dense vector search, lexical BM25, or their reciprocal-rank fusion — would retrieve best. Writing them first was the useful part: it stopped me from reading the results as a ranking when the data could not support one.

<!--more-->

## No ranking the data supports

The obvious question — which arm wins Recall@10 — has a numerical answer and no defensible one. Across the same twenty-nine hand-reviewed queries from [the previous note](/writing/notes/label-review-that-lowered-my-score/), where Recall@10, MRR and reciprocal-rank fusion are defined, dense search has the highest Recall@10 at 0.724 and the hybrid the lowest at 0.690. But the paired-difference intervals reported in the ablation all cross zero[^ci]: dense over hybrid is +0.034, with an interval from −0.069 to +0.121. The two metrics do not even agree on direction — the hybrid is lowest on Recall@10 and highest on MRR, and that gap is within noise too. At twenty-nine queries there is no ordering to report.

<figure class="figure">
  <img src="/images/notes/recall-forest-within-noise.svg"
       alt="Forest plot of pairwise Recall@10 differences over 29 queries with 95% bootstrap confidence intervals. Dense minus hybrid is +0.034 and lexical minus hybrid is +0.023; both intervals straddle the zero line.">
  <figcaption>
    Pairwise Recall@10 differences on the 500-abstract pilot, 29 queries, with 95% paired-difference bootstrap intervals (10,000 resamples, seed 20260531). Dense edges hybrid by +0.034 and lexical edges hybrid by +0.023, but every interval crosses zero — at this sample size the aggregate ranking of the three arms is within noise, which is why the decision below rests on the findings that survive it rather than on which arm sits highest.
  </figcaption>
</figure>

My three predictions were that lexical search would beat the hybrid on queries with one strong single-arm answer, that dense would beat lexical on broad topic questions, and that the hybrid would win on average while losing on the tails. The middle one held in direction only — dense edged lexical on the broad queries, 0.625 to 0.583, well inside its interval. The "wins on average" prediction is exactly the averaged claim this sample cannot settle. The first prediction is the one that survived, and it survived as a single query.

## Two results that survive a small sample

First, the depth-ten ranking does not survive to depth fifty. Measured at Recall@50 the order inverts: the hybrid moves from last to first, 0.966, and dense from first to last, 0.897. I am not claiming the hybrid significantly wins at depth — same small sample — but a ranking that flips when you move the cutoff is not one to trust at either cutoff.

Second, and more durable because it does not lean on an average, is query 12. Its landmark paper for WASP-96b sits at rank 4 in lexical search and rank 338 in dense — effectively invisible to the dense arm. Fusion then buries it anyway. Reciprocal-rank fusion at k=60 rewards papers that both arms return: a paper one arm ranks, say, 8th and the other 15th scores about 0.028 (1/68 + 1/75), enough to outrank a paper only one arm rates highly — like the WASP-96b result, about 0.016 from its lexical rank of 4. So for query 12 a paper lexical search alone would have placed fourth never reaches the hybrid's top ten. That one query is the cleanest case for keeping a lexical arm, and a concrete reminder that fusion can bury a paper exactly one arm is sure of.

## What I will actually change

The complementarity is real but thin. Pool the top fifty from each arm and 42 of the 49 relevant documents are found by both; only five are unique to one arm, and of those only query 12 is genuinely blind to the other — the rest sit just past the cutoff, at ranks in the fifties to nineties, reachable rather than missed. Two relevant papers neither arm surfaced at depth fifty at all.

I am keeping the hybrid as the stage-one candidate generator regardless. The job of stage one is to land the relevant papers somewhere in the pool a reranker will read, not to order them perfectly — so the number I should be optimising is candidate-set recall at the pool depth, not Recall@10. Recall@10 was the wrong target for a stage that feeds a second stage; it was measuring the reranker's job before the reranker existed.

This is all still 500 abstracts. The question I am carrying into the corpus-widening work is whether the dense-blind class — papers like query 12's — grows as the corpus grows, or stays a handful of edge cases. That is [the next note](/writing/notes/widening-that-lowered-every-score/).

[^ci]: Each interval comes from ten thousand bootstrap resamples of the per-query scores (seed 20260531). An interval that spans zero means the data are consistent with no difference between the arms.
