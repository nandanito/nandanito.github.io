---
layout: post
title: "The question my coding agent couldn't answer"
excerpt: "Agents act, agents remember, but the standard agent stack rarely lets you reconstruct what the agent actually believed when it acted. This is a problem worth a name."
modified: 2026-05-24
category: writing
tags: [AI Agents, Trust, Memory, Post-Mortem, Lodestar, Epistemic Governance, Research]
author: nandan
comments: false
share: false
---

A few months ago I was watching a coding agent work through a small
refactor on one of my side projects. It deleted a file I cared about,
re-created a stripped-down version of it three steps later, then
confidently reported success. The tests passed because the deletion
had taken the test for that file with it.

I rolled back, and then I sat with the question that bothered me more
than the bug:

*What did the agent think it was doing?*

Not "what did it do" — I had a complete log of tool calls. Not "what
were the inputs" — I had the prompt, the diff context, the file tree.
What I wanted was the **belief state** the agent held the moment it
chose to delete that file — not its private consciousness, but the
claims it was treating as true enough to act on. Did it think the
file was dead code? Did it think it had moved the file's contents
elsewhere? Did it have a plan that included "and now re-create the
parts we need" that just didn't survive the next context shift? Was there a
chain of reasoning where each step was locally sensible and the
catastrophe was emergent?

I had no way to find out. Not because I had bad tools — I had OTel
traces, conversation transcripts, prompt logs, memory snapshots from
the agent's memory store. I had **more telemetry than I could read**.

I had no record of belief.

---

## The gap I started seeing everywhere

Once I noticed this gap, I couldn't stop noticing it.

Every agentic system I touched had the same shape. There was a
**runtime** — the thing that picked tools and called them. There was
a **memory store** — mem0, Letta, Zep, a vector database, whatever
the team had reached for that quarter. There was **observability** —
spans, traces, prompts, completions, sometimes structured logs.
Three layers, each excellent at its own job, and rarely speaking the
language I needed.

If I asked the runtime "what did you do," it answered with a tool
trace. If I asked the memory store "what did you know," it answered
with a vector retrieval. If I asked observability "what happened in
the call," it answered with timing, tokens, model parameters.

None of them could cleanly answer "what did you **believe**, why did
you believe it, and what evidence supported that belief at the moment
of action."

This isn't a minor gap. The five questions I find myself wanting to
answer about any non-trivial agent run are:

1. **What did the agent observe**, as raw evidence, distinct from what
   it concluded?
2. **What claims did the agent extract** from those observations, and
   how strongly were those claims supported?
3. **Which claims became actionable beliefs**, and under what authority
   were they promoted from "the model said this" to "the agent now
   acts as if this is true"?
4. **Which beliefs informed which decisions**, and when those beliefs
   were contradicted later, did the agent revise downstream
   decisions or did the corrections stay orphaned?
5. **Did the outcome of the action match the agent's prior claims
   about what would happen** — or did we discover the gap only by
   running the test suite?

Standard observability can address fragments of this — actions,
inputs, traces, sometimes outcomes. What usually falls through is the
promotion step: the moment when a claim becomes something the agent
is willing to act on.

The agent that deleted my file produced a perfectly clean OTel trace.
I could see the tool call, the response, the next tool call, all the
way through. But somewhere in that trace there was a moment where the
agent crossed a threshold from "I'm exploring this codebase" to "I
believe this file is dead code," and the trace recorded only the
*action that followed* the crossing, not the crossing itself.

<figure>
  <img src="/images/posts/the-question-my-coding-agent-couldnt-answer/agent-stack.svg"  
       alt="Four horizontal lanes showing the layers of a current agent stack. Runtime captures tool calls and responses; Memory captures retrieved context and embeddings; Observability captures traces, spans, metrics, evals, and logs. A fourth lane below, drawn in dashed red and marked with a question mark, labels what is missing: an epistemic state or trust layer that would record claims, evidence, beliefs, decisions, and revisions." />
  <figcaption>Fig. 1 · The agent stack today. Three lanes — runtime, memory, observability — each excellent at its own job. A fourth layer is missing: the one that would record what the agent took to be true.</figcaption>
</figure>

---

## Why this is harder than it looks

The first response I get when I describe this gap is usually: "Just
log the LLM's reasoning. Have it think out loud. Capture the chain of
thought."

This is the wrong shape of solution and I want to be specific about
why.

Chain-of-thought logs can be useful, but they are not the same as the
agent's belief state. They may include rationalisation the model
produced in service of an answer or action it had already settled on.
In roughly the way that a politician's explanation of a vote is not
the same as the politician's actual reasons for the vote, the
reasoning trace may be downstream of the decision. [Anthropic's work
on the faithfulness of chain-of-thought reasoning](https://arxiv.org/abs/2307.13702)
found that stated reasoning is not always a reliable account of how
a model reached its answer — sometimes the reasoning trace appears
connected to the answer, sometimes it looks more like post-hoc
narrative. What I want is the structured record that existed *before*
the action: what claim was being treated as true, on what evidence,
and under what authority.

The second response is: "Just dump the agent's memory store. The
memory is the belief state."

This conflates two very different things. A memory store holds
**recalled material** — things the agent retrieved when context
demanded. The act of retrieval doesn't tell you whether the agent
*believed* what it retrieved, treated it as background context, or
ignored it entirely. Worse, most memory stores I've worked with don't
distinguish between "this fact came from a tool output I directly
witnessed" and "this fact came from a document I read, which someone
else wrote, which could have been wrong or hostile." Too often,
everything in the memory store is just text the agent has access to,
without enough distinction between observation, claim, evidence, and
belief.

The third response is: "Just ask the model after the fact what it
was thinking."

This one is the most seductive and the most dangerous. Post-hoc model
introspection is often unreliable: models asked "why did you do X"
produce plausible-sounding answers that may or may not correspond to
the actual computation that led to X. Recent interpretability research
on the faithfulness of chain-of-thought rationales has surfaced enough
examples of this disconnect to make me cautious about treating
self-reports as ground truth. If you want to know what an agent
believed, you probably cannot ask the agent reliably — you have to
have recorded the belief at the time it was formed. That doesn't
mean self-reports are useless; it means they should be treated as
claims requiring evidence, not as evidence by themselves.

The actual gap, the one that requires a new piece of infrastructure
rather than better use of existing pieces, is that **the agent's
journey from observation through claim through belief through
decision to action is, in current agent infrastructure, not written
down as a structured artifact.** It is implicit in the model's
weights and the conversation context, and that is exactly the place
where it cannot be audited.

---

## A worked example of why this matters

Let me put a concrete shape on the cost of this gap.

Suppose I'm using an AI coding assistant to triage a stack of GitHub
issues. The assistant reads issue #142, which describes a memory leak.
The issue body contains the line: *"the cache eviction never runs;
see this Stack Overflow post for the fix."* The Stack Overflow link
is helpfully embedded.

The agent dutifully follows the link, reads the post, finds the
suggested fix, and proposes a patch. The patch passes my eyeballs and
the test suite. I merge it.

Three weeks later, the production memory issue gets worse, not better.
I start digging. The Stack Overflow post turned out to describe a
different cache library entirely; the "fix" the agent applied was
locally sensible but semantically wrong for our codebase.

I want to do a post-mortem. The questions I'd like to answer:

- Did the agent **register** that the Stack Overflow post was about a
  different library? Was that information in its context window?
- Did it consider the possibility and dismiss it? Or did it never
  raise the question?
- At what point did "Stack Overflow says X" become "this is the
  correct fix"? Was there a single step where that promotion
  happened, or did it accumulate?
- Were there other claims in the agent's context that contradicted
  this one? Did the agent see them and not weight them, or did it
  never see them at all?

I cannot answer any of these from a tool trace, a memory dump, or
post-hoc model interrogation. The information I need was never
recorded, because nothing in the stack was set up to record it.

The cost of this isn't measured in this one bug. It's measured in
**my trust in the agent the next time**. Because I can't do a real
post-mortem, I can't isolate what went wrong; because I can't isolate
what went wrong, I can't tell whether it was a one-off or a pattern;
because I can't tell whether it was a pattern, I have to either trust
the agent less across the board or close my eyes and hope. Neither is
a sustainable position once you're using these systems for work that
matters.

There is a chain running through all of this, even when it isn't
named. An observation becomes a claim through interpretation. A
claim counts as evidence only under a warrant — a rule about what
would actually support it. Evidence becomes belief through
inference. Beliefs become decisions through preferences over
values, risks, and goals. Decisions become actions through
commitments, and outcomes should revise the earlier claims and
beliefs. Most agent stacks record the nodes. None of them make
the links auditable.

<figure>
  <img src="/images/posts/the-question-my-coding-agent-couldnt-answer/epistemic-chain.svg"
       alt="A horizontal chain of seven stages — observation, claim, evidence, belief, decision, action, outcome — connected by labeled forward transitions: interpretation, warrant, inference, preference, commitment, consequence. Most forward transitions are drawn in red to mark them as implicit; only inference, commitment, and consequence are slate, marking them as transitions whose rule is usually stated. Two dashed red revision arrows curve back from outcome: one to belief, labeled re-weight; one to claim, labeled rename." />
  <figcaption>Fig. 2 · The epistemic chain. Solid slate marks transitions whose rule is usually stated; red marks the implicit forward links; dashed red marks the revision feedback. Five of eight links are normally implicit.</figcaption>
</figure>

---

## A name for what's missing

I've come to believe that this gap deserves its own name, partly
because naming things makes them tractable and partly because the
people who need to build for this gap are different from the people
building the existing three layers.

The missing piece is **the agent's epistemic state** — the structured
record of what the agent took to be true, why it took it to be true,
and how confidently. The infrastructure that maintains this record I
think of as a **trust layer**: separate from the runtime (which acts),
separate from the memory (which recalls), separate from observability
(which observes), and sitting alongside all three.

The job of a trust layer is roughly:

- Capture every observation as raw evidence, tagged with its source
  and trust level.
- Capture every claim the agent extracts from observations, along
  with which observations support the claim.
- Make the promotion of a claim to an "actionable belief" an explicit,
  recorded step — never an implicit accumulation.
- Track which beliefs informed which decisions, so that when beliefs
  are contradicted later, the downstream decisions can be flagged.
- Compare what the agent claimed would happen against what actually
  happened, so calibration can in principle be measured rather than
  guessed.

This is a different kind of artifact from anything I've seen shipped
in the agent stack today. It is not an observability backend, because
observability systems primarily ingest and evaluate signals from a
running system. A trust layer has to sit closer to the action path:
it shapes whether claims become beliefs and whether beliefs can drive
action. It is not a memory store, because memory stores conflate
retrieval status with truth status. It is not part of the runtime,
because the runtime operates at the granularity of "make this call,
get this response," not "this claim was promoted to an actionable
belief at this step."

It needs to be its own thing. I think it needs to be open-source. I
think it needs to be language-agnostic at the integration boundary —
[the Model Context Protocol](https://modelcontextprotocol.io) is the
most practical first boundary — even though its first reference
implementation will live in one ecosystem. I think it needs to make
the cost of *not* having a trust layer visible enough that people
who build agents start asking the same questions I'm asking, instead
of accepting "more telemetry" as a sufficient answer.

I'm calling the project **Lodestar**. The name comes from the
historical term for a guiding star, the fixed reference point by
which a navigator orients themselves before deciding where to sail.
That maps onto what the trust layer is meant to do for an agent:
fix a reference point in the form of recorded, evidenced beliefs,
so the agent — and the human reviewing it after the fact — has
something to navigate by.

---

## What's next in this series

This is the first post in a short series. Three articles, each one
standing on its own but building on the last.

**Part 1 (this post): The question my coding agent couldn't answer.**
The gap, why it's harder than it looks, and the case for naming the
missing piece.

**Part 2: How Lodestar records what an agent believed.** A walk
through the architecture I'm building to fill the gap — not as a
finished product but as a worked-through sketch with code that runs.
It separates the lifecycle of any remembered information into four
orthogonal axes (truth, retrieval, security, freshness), enforces
explicit transitions between them, and produces an event log that
can be replayed and audited. I'll show the data structures, the
rules for promoting claims to beliefs, and the kind of audit trail
that comes out the other end.

**Part 3: What five rounds of adversarial review taught me about my
own design.** A reflection on the review process I ran on Lodestar's
architecture — pushing the design against a sceptical reviewer
across five rounds, watching what survived, what got rebuilt, and
what I learned about the shape of my own blind spots. I think this
is the part of the work that's most generally useful, because the
discipline of asking another mind "where am I wrong" is portable to
almost any serious technical project, and I want to put the
specifics on record.

Links to parts 2 and 3 will appear here as they go live.

If you want to follow along before then, the project lives at
[qmilab.com/lodestar](https://qmilab.com/lodestar), with code at
[github.com/qmilab/lodestar](https://github.com/qmilab/lodestar).
It is deliberately pre-v0.1 — I want the architectural commitments
to be public *before* they harden into shipped product, while they
are still cheap to revise.

---

*This series is part of the [QMI Lab](https://qmilab.com) research
arc on machine intelligence. The lab's broader thesis is that the
fundamental problem in machine intelligence is the conversion of
information into knowledge; the trust layer I'm sketching here is one
specific lever for that conversion when the system doing it is an
autonomous agent.*

*Lodestar was developed internally under the codename Orrery; if you
came across the project under that name, the renaming history is
documented in the repository.*