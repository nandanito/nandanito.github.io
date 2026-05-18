---
layout: post
title: "The model I wish I had as a graduate student"
excerpt: "AstroLLM is an open-source, retrieval-grounded language model for astronomy and astrophysics — designed around the workflows researchers actually use rather than the benchmarks frontier models optimize for. Why I started it, where it is, and what is next."
modified: 2026-05-09
category: writing
tags: [AstroLLM, Scientific AI, Domain-Specialized LLMs, Retrieval-Augmented Generation, Astronomy, Project Notes]
author: nandan
comments: false
share: false
---

When I was doing my doctoral research at the Institut für Astrophysik in Göttingen, the work was equal parts physics, code, and bibliography. The IDL pipelines were one thing — those I could write and read. The physics was the reason I was there.

<!--more-->

But the bibliography was where the time disappeared. Tracing a measurement back through three or four papers to find the original calibration; identifying which of two contradictory mass-loss prescriptions a more recent paper had quietly assumed; figuring out whether an object catalogued under one name in SIMBAD was the same as an object referenced under a different name in someone else's spectroscopic survey. The literature was an ocean I learned to swim in, but it cost time I would rather have spent on the physics.

The reason I started AstroLLM is that the ocean has gotten bigger.

NASA ADS now indexes more than 15 million publications. SIMBAD tracks more than 20 million astronomical objects. The NASA Exoplanet Archive lists more than 5,700 confirmed planets, and the discovery rate continues to climb. The next generation of graduate students will face the same swim, with more of it, and no more time. A retrieval-grounded language model that knows how to use those resources — really use them, the way someone who has spent years inside the field would — is a tool I would have wanted very badly fifteen years ago. It is a tool that should exist now.

There has been important work in this direction already. AstroMLab's AstroSage models, released in 8B and 70B variants, demonstrated that domain specialization can match or exceed frontier models on astronomical knowledge benchmarks. That work is real and it earned the territory it claimed. But the AstroSage models operate as isolated Q&A systems. They are not connected to ADS. They cannot look up an object in SIMBAD. They cannot retrieve a paper's actual text, cite it accurately, or tell the user when their training data has gone stale. They do well on benchmarks of astronomical knowledge. They are not designed for the work of astronomical research itself — retrieval, tool use, citation grounding, and stale-data awareness.

AstroLLM is designed for that work.

## What AstroLLM is

AstroLLM is being built as a family of retrieval-grounded language models, based on QLoRA fine-tuning of open Qwen3 base models at the 4B and 8B scale to start. The retrieval architecture is what differentiates it: a three-stage pipeline combining hybrid sparse-and-dense recall with cross-encoder reranking and an astronomy-aware filtering layer that performs SIMBAD alias expansion before any retrieval results reach the model. Every factual claim AstroLLM makes is meant to trace back to a specific paper via an ADS bibcode. When the retrieval comes back weak, the model will be trained to say so rather than confabulate.

## How it is evaluated

This is the part I care about most, because it is where existing astronomy-LLM work has the largest gap. AstroMLab-1 and Astro-QA are good benchmarks of knowledge recall. They do not measure what a domain-specialized model has to do well in order to be useful. AstroLLM has a custom four-track evaluation suite.

*Track one* is grounding and citation accuracy — does the model cite real papers, do those papers say what the model claims, do the bibcodes resolve.

*Track two* is tool routing — when a question requires looking up an object in SIMBAD versus retrieving a paper from ADS versus checking the Exoplanet Archive, does the model route correctly.

*Track three* is abstention under weak retrieval — when nothing useful comes back, does the model decline cleanly or does it hallucinate confidently.

*Track four* is pedagogical quality — does the model adapt its explanation depth for a first-year graduate student versus a senior researcher.

These four tracks are the honest answer to the question: *what would a useful astronomy assistant actually need to do?*

## Where the project is right now

Pre-training. The base-model selection is done. The SFT dataset is in design — five to eight thousand examples spanning literature Q&A, object and property retrieval, citation-grounded summarization, pedagogical explanation, and tool-call formatting. The retrieval pipeline is in development in parallel against pgvector and Pyserini, with SPECTER2 embeddings for scientific document representation. The evaluation suite is partly specified, partly under construction. Nothing has been trained yet. The earliest target for a public beta at [astrollm.org](https://astrollm.org) is Q3 2026.

## Why it has to be open

Models, training data, evaluation benchmarks, retrieval pipelines, the SFT recipe — all of it will be public, on HuggingFace under `astrollm` and on GitHub under the same name. The reason is not ideological. Scientific tools that cannot be inspected are not scientific tools. If a researcher uses AstroLLM to ground a claim in a paper, the chain of evidence has to be traceable end-to-end. That is not negotiable in science, and it should not be negotiable in scientific AI. The closed frontier models are useful and I use them every day. I would not trust them to do citation-grounded astronomy. AstroLLM is the version I want to be able to trust.

## The longer arc

The current focus is what the project plan calls the Core — the 4B and 8B retrieval-grounded models that can serve graduate students and early-career researchers reliably. After Core comes a Nano tier for embedded and edge inference, and an Ultra tier at 70B+ for harder reasoning loads. The multimodal direction is on the agenda but deferred until Core is stable — eventually, AstroLLM should be able to take a spectrum, an image, or a light curve as input, which means bridging the language model to a modality encoder like AION-1. Continuous learning through automated arXiv ingestion is on the agenda too. None of this happens before the Core is real. There is a lot of work between here and a multi-tier multimodal scientific assistant. I am starting with the part that is hardest to do well — the small model that does not lie about citations.

## A note on what this is not

AstroLLM is not a research-replacement tool. It is a research-amplification tool, designed with the assumption that the human asking the question is the scientist and the model is the assistant that helps them swim through the ocean faster. The model will be wrong sometimes, and the evaluation suite is designed to catch the wrong-sometimes cases. When a more capable frontier model exists, AstroLLM should help its users decide when to switch up; when a paper has not been ingested yet, the model should say so rather than fake it.

## Why this post exists

I write about this project for two reasons. The first is that I think domain-specialized scientific LLMs are one of the most interesting near-term applications of language-model technology, and the science has to be done in public. The second is more personal. The graduate student I was at the Institut für Astrophysik would have used this tool. The graduate students who are there now should not have to wait for a frontier lab to remember astronomy exists.

That is why I started it.

You can follow along at [astrollm.org](https://astrollm.org), on [GitHub](https://github.com/astrollm), and on [HuggingFace](https://huggingface.co/astrollm). The next post introduces QMI Lab, the broader research context within which AstroLLM sits as the most empirically-grounded current project.
