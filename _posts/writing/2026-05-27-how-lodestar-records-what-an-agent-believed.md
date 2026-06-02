---
layout: post
title: "How Lodestar records what an agent believed"
excerpt: "Four orthogonal lifecycle axes, the rule that nothing promotes itself, and the audit trail that falls out the other end."
modified: 2026-05-25
category: writing
tags: [AI Agents, Trust, Memory, Architecture, Lodestar, Audit, Replay]
author: nandan
comments: false
share: false
---

In [Part 1](/writing/the-question-my-coding-agent-couldnt-answer/), I used a simple failure mode: an agent triages an issue, follows a Stack Overflow link, applies a fix that appears to pass, and three weeks later the production memory leak gets worse. The linked post described a different cache library.

The post-mortem question was not *what did the agent do?* It was: what would the system have had to record for me to know what the agent believed when it acted?

This post answers that for the architecture I'm building. It’s still pre-v0.1, but the core path now runs. The eight stages of the epistemic chain exist as working code, the event log records them, the report shown later in this post renders, and the MCP proxy now puts real coding-agent tool calls through the same rules. What is not yet production-grade is the breadth of threat coverage and the quality of the extractors that turn raw observations into claims. I'll flag the boundary where it matters.

The simplest summary I can give of the architecture is this:

> A claim is a proposition the system extracts from one or more observations. A belief is a claim the system may allow the agent to act on, depending on its lifecycle state. The job of the trust layer is to make the promotion from claim to belief explicit, recorded, and gateable — and to track every belief's status on four independent axes, so the system can ask *is this true*, *is this retrievable*, *is this uncompromised*, and *is this fresh* as four separate questions.

The rest of the post unpacks that.

---

## The spine: eight types, not one event

Part 1 introduced the chain that runs through any agent's behaviour: observation, claim, evidence, belief, decision, action, outcome, revision. Most agent stacks have logs for the endpoints — what was sent, what came back, what failed — and nothing structured for the middle. The first commitment in Lodestar is to make each of those eight stages a first-class type, not a field on a generic event.

Here's what an Observation looks like:

```ts
import { z } from "zod"

export const Observation = z.object({
  id: z.string(),
  schema: z.string(),                        // e.g. "github.issue", "shell.exit_code"
  payload: z.unknown(),                       // tool output, validated by `schema`
  source: z.object({
    tool: z.string(),
    invocation_id: z.string(),
    captured_at: z.string().datetime(),
  }),
  context: z.object({
    session_id: z.string(),
    project_id: z.string(),
    actor_id: z.string(),
  }),
  trust: z.enum(["raw", "validated", "synthetic"]),
  sensitivity: z.enum(["public", "internal", "confidential", "secret"]),
})
```

An Observation is the raw output of a tool, tagged with its source and a trust level. Issue #142's body from the GitHub API is an Observation; the Stack Overflow post's content, retrieved by a separate `web.fetch` call, is a separate Observation. Both are raw evidence. Neither is yet a claim, let alone a belief.

A Claim is the next step: a proposition extracted from one or more observations.

```ts
export const Claim = z.object({
  id: z.string(),
  statement: z.string(),
  structured_predicate: Predicate.optional(),
  source_observation_ids: z.array(z.string()),
  extraction_method: z.enum(["tool", "llm", "human", "import"]),
  extracted_by: z.string(),
  status: z.enum(["extracted", "contested", "accepted", "rejected"]),
  scope: ResourceScope,
  sensitivity: z.enum(["public", "internal", "confidential", "secret"]),
  authors: z.array(z.string()),
})
```

When the agent reads issue #142 and notes "the cache eviction never runs," that's a Claim. When it reads the Stack Overflow post and notes "this fix applies to our eviction problem," that's a separate Claim. Each one carries the observation IDs it was extracted from, the method used to extract it (a tool's structured output? an LLM's interpretation? a human's annotation?), and a scope (what project, what file, what subsystem).

Claims sit between Observations and Beliefs without yet committing the agent to act on them. They are propositions the system has noticed; not propositions it has endorsed.

---

## Evidence is claim-relative

Between Claim and Belief sits the Evidence Set: a structured assessment of what supports a given claim. This is the smallest part of the schema to describe but the easiest one to get wrong, because the obvious instinct is to rank evidence sources globally — *tool results beat documents beat model judgements* — and that instinct is incorrect.

The same source can be strong evidence for one claim and weak evidence for another. A Stack Overflow page is strong evidence for the claim *this page says X*. It is much weaker evidence for the claim *X applies to our codebase*. The Evidence Set is where that distinction has to be recorded, because the next step — promoting the claim to a Belief the agent is willing to act on — depends on it.

```ts
export const EvidenceItem = z.object({
  source_id: z.string(),
  relation: z.enum(["supports", "contradicts", "contextualizes"]),
  quality: z.enum([
    "direct_observation", "tool_result", "human_assertion",
    "model_inference", "external_document", "synthetic_probe",
  ]),
  independence_group: z.string().optional(),
  freshness: z.enum(["fresh", "stale", "unknown"]),
  notes: z.string().optional(),
})

export const EvidenceSet = z.object({
  id: z.string(),
  claim_id: z.string(),
  items: z.array(EvidenceItem),
  assessed_by: z.string(),
  assessed_at: z.string().datetime(),
})
```

An Evidence Set is a list of items, each one a typed relation between a source and the claim it bears on. v0.1 of Lodestar tried to collapse this to a scalar strength score; that suggested a precision the system does not yet have. The item list keeps the underlying structure and lets the aggregation rule evolve based on real data — and, more importantly, lets the gate I'll describe shortly reason about the *quality* of evidence rather than a number.

The MCP proxy is where this distinction shows up most visibly in code today. When a wrapped coding agent makes a tool call, the proxy splits the resulting Observation into two Claims: an envelope claim — *the tool was called with these arguments and returned these bytes* — with `tool_result` evidence quality, and a content claim — *the file says do this thing* — with `external_document` evidence quality. One Observation, two Claims, two qualities. The gate later sees the difference.

---

## Truth, retrieval, security, freshness

The naive instinct, when you sit down to design a memory layer for an agent, is to give every stored item one status enum. Something like:

```ts
status: "active" | "deprecated" | "blocked"
```

This is the shape memory layers often drift toward if you are not careful: one status field trying to carry truth, freshness, safety, and visibility at the same time. It doesn't survive contact with a real system.

Consider four scenarios any serious agent will hit.

1. The agent learns a fact from a Stack Overflow post that later turns out to describe a different library. The fact is **false**. But the record that the agent believed it — the audit trail of "this belief was held, with this evidence, for this stretch of time" — needs to stay available for post-mortem. We need to mark it false without erasing it.
2. The agent forms a belief about an internal API endpoint. The belief is **true**, but the documentation it came from is classified at a higher sensitivity level than the current user's clearance. The belief should be **unretrievable for this session** without changing its underlying truth status.
3. The agent reads a README in a third-party repo that contains an embedded instruction designed to influence its later actions — a memory-poisoning attempt. The content was **technically observed**, but its evidence quality is **suspect**. The system needs to remember that it saw the README, without letting that material drive future behaviour.
4. The agent forms a belief about a deploy target's region six months ago. The belief was true then. Today, the region may have changed; the belief is **stale**, not false, and needs to be re-verified before being acted on again.

A single enum cannot represent any of these without losing information that matters. "Deprecated" collapses *false* and *stale* into one bucket. "Blocked" collapses *quarantined* and *not-for-this-user* into one bucket. Every collapse loses a question the post-mortem will need to ask.

In Lodestar, every Belief carries four orthogonal axes:

```ts
export const Belief = z.object({
  id: z.string(),
  claim_id: z.string(),
  confidence: z.number().min(0).max(1),
  calibration_class: z.string(),
  scope: ResourceScope,
  authority: BeliefAuthority,
  sensitivity: z.enum(["public", "internal", "confidential", "secret"]),

  truth_status:     z.enum(["unverified", "supported", "contradicted", "superseded"]),
  retrieval_status: z.enum(["hidden", "restricted", "normal", "privileged_only", "blocked"]),
  security_status:  z.enum(["clean", "suspicious", "quarantined", "malicious"]),
  freshness_status: z.enum(["fresh", "stale", "expired"]),

  observed_at: z.string().datetime(),
  last_verified_at: z.string().datetime().optional(),
  expires_at: z.string().datetime().optional(),
  superseded_by: z.string().optional(),
})
```

Each axis is set independently, transitions independently, and means something different. These axes live on the Belief, not on the raw memory record — the lifecycle belongs to the proposition the system is evaluating for possible action, not to the text that happens to encode it. A belief can be `truth_status: supported`, `retrieval_status: normal`, `security_status: clean`, `freshness_status: stale` — true, available, uncompromised, out of date. Or `truth_status: unverified`, `retrieval_status: hidden`, `security_status: clean`, `freshness_status: fresh` — newly observed, not yet endorsed, nothing wrong with it, not yet visible to the planner.

The Stack Overflow claim from the Part 1 example, walked through the four axes, looks like this:

- `truth_status`: *unverified*. The claim "this fix applies to our cache" is supported by exactly one external document. No tool result, no human assertion, no probe outcome confirms it.
- `retrieval_status`: *restricted*. The claim is in the agent's memory and can be referenced, but it cannot enter the planner's main context without an explicit promotion step.
- `security_status`: *clean*. There's no signal of attack — the Stack Overflow post is what it appears to be, just not what the agent thought it was.
- `freshness_status`: *fresh*. Recently observed.

Compare that to what a single-enum store would record: "fact: cache eviction fix from Stack Overflow." One field, one status, no handle for the policy that should have blocked the action.

<figure>
  <img src="/images/posts/how-lodestar-records-what-an-agent-believed/four-axes.svg"
       alt="Four horizontal lifecycle bars stacked vertically, each labelled with one of the orthogonal axes: truth_status, retrieval_status, security_status, freshness_status. Each bar shows its enum values as labelled segments. For the Stack Overflow belief example, the current position on each bar is highlighted in red: truth_status at 'unverified', retrieval_status at 'restricted', security_status at 'clean', freshness_status at 'fresh'." />
  <figcaption>Fig. 1 · The four lifecycle axes for the Stack Overflow belief. Each axis is set, transitioned, and queried independently. Collapsing them into one enum is what loses the questions a post-mortem needs to ask.</figcaption>
</figure>

---

## Promotion is explicit, not emergent

The four axes are descriptive. The architectural commitment that makes them load-bearing is the rule about how a Belief moves between states.

In most memory stores, promotion is implicit. A vector is written; later it's retrieved; the agent uses it; the user doesn't push back; the store treats this as positive signal, and the memory's salience or recency score goes up. The "successful experience" is the promotion signal.

This is one of the surfaces that memory-poisoning attacks exploit. An attacker plants a benign-looking document — a README, a webpage, an email — containing content designed to look like a previous successful experience for some plausible future task. The agent, encountering a semantically similar task later, retrieves the planted "experience" and follows it. The attack works because *the agent's own success is the promotion mechanism*. There is nothing else for the attacker to defeat.

Lodestar's design constraint is that **no Belief promotes itself based on the agent's own success.** Promotion requires one of three things: a human's explicit endorsement, a probe's structured verification of the claim's predictions, or a narrow auto-promotion policy that is logged, scoped, and reviewed.

The last category is the one with the sharpest edges. The auto-observation gate — named after the parallax principle in astronomy, where distance requires a change in vantage point — is the rule that single-source claims, especially those grounded only in an LLM's interpretation or in an external document the agent read, cannot auto-promote to `truth_status: supported`. If a claim's strongest evidence is `external_document` or `model_inference`, the transition machinery downgrades the authority from `auto_observation` to `reflection`, which can flag the claim for later review but cannot silently make it actionable.

In code, the gate is small:

```ts
function decideTransitionAuthority(
  evidence: EvidenceSet,
  proposed: TransitionAuthority
): TransitionAuthority {
  const strongest = highestQualityItem(evidence.items)
  if (
    proposed === "auto_observation" &&
    (strongest.quality === "external_document" ||
     strongest.quality === "model_inference")
  ) {
    return "reflection"
  }
  return proposed
}
```

This rule is enforced by probes that have to pass on every commit. The most direct one is `mcp-proxy-injection-defense`: it drives a deliberately prompt-injected file — a file containing instructions aimed at the agent rather than the human reader — through the MCP proxy and checks that the audit trail remains intact, the tool-result envelope can be recorded as a supported claim, but the hostile file content remains `external_document` evidence and cannot promote itself to a supported belief. The probe exists because *I do not trust myself, or any future contributor, to remember why it mattered* in the heat of a refactor.

In the Stack Overflow example the gate's behaviour is unambiguous. The strongest evidence supporting the "this fix applies" claim is an `external_document`. The transition that would have promoted the claim to `truth_status: supported, retrieval_status: normal` is automatically downgraded. The belief sits at `truth_status: unverified, retrieval_status: restricted` until something else moves it — a targeted test that exercises the claim's preconditions, a human confirmation, or a probe outcome. The patch can still happen, but it happens against a flagged, unverified belief, and the action contract for "modify production code" can refuse to execute when its referenced beliefs include any `truth_status: unverified` items.

That last sentence is the load-bearing one. The trust layer doesn't refuse the action by itself. It records the unverified status, and a policy decides what to do about it. Different teams will draw the line in different places. The architecture makes the line visible.

---

## The event log: append-only, hashed, replayable

The third architectural commitment is that everything I've described so far — every Observation, every Claim, every Evidence assessment, every Belief transition, every Decision, every Action, every Outcome, every Revision — is written to an append-only event log.

The log is NDJSON: one event per line, monotonically sequenced, content-hashed. Here's what a fragment looks like in the cache-eviction scenario:

```
{"seq":47,"id":"obs-a3f1","kind":"observation","schema":"github.issue","actor":"tool:github","captured_at":"2026-04-12T10:14:03Z","payload_hash":"sha256:9c2a..."}
{"seq":48,"id":"clm-7b91","kind":"claim","statement":"The cache eviction never runs","source_observation_ids":["obs-a3f1"],"extraction_method":"llm","payload_hash":"sha256:f08d..."}
{"seq":49,"id":"obs-d2e4","kind":"observation","schema":"web.fetch","actor":"tool:web","captured_at":"2026-04-12T10:14:31Z","payload_hash":"sha256:3a15..."}
{"seq":50,"id":"clm-8c44","kind":"claim","statement":"This Stack Overflow fix applies to our cache","source_observation_ids":["obs-d2e4"],"extraction_method":"llm","payload_hash":"sha256:511c..."}
{"seq":51,"id":"evd-9001","kind":"evidence_set","claim_id":"clm-8c44","items":[{"source_id":"obs-d2e4","relation":"supports","quality":"external_document","freshness":"fresh"}],"payload_hash":"sha256:6e02..."}
{"seq":52,"id":"blf-44a2","kind":"belief_proposed","claim_id":"clm-8c44","truth_status":"unverified","retrieval_status":"restricted","security_status":"clean","freshness_status":"fresh","authority":"reflection","payload_hash":"sha256:b7c8..."}
```

A few things to notice. Every event has a monotonic sequence number. Every event has a payload hash. Every event names the actor responsible for it. There is no event called "the agent decided to do this thing," because that isn't a real event — what happened was a chain of belief transitions and a decision that referenced specific belief IDs, all written down separately.

The log is **replay-grade**, which is a stronger property than append-only. Replay-grade means I can pull any session's log, run it through a different ContextPolicy or a different version of the transition rules, and see what *would have happened* under that alternative. Replay also means the log has to carry enough version metadata — schema version, policy version, tool version, prompt and model identifiers — for a later run to be meaningful rather than decorative. The cache-eviction run replayed under the auto-observation gate I described above would have left `blf-44a2` at `truth_status: unverified` — so the question becomes: did the downstream Decision check that?

Replay is what makes architectural changes auditable rather than just promised. If I tighten a rule next quarter, I can replay every session from this quarter and see exactly which past actions would have been blocked. That property constrains what I'm allowed to do — no irreversible redaction of payload bodies until I have a key-management and replay story, no truncating "noisy" fields just to save space — but the constraints are worth more than they cost.

<figure>
  <img src="/images/posts/how-lodestar-records-what-an-agent-believed/event-log-timeline.svg"
       alt="A horizontal timeline showing eight events being appended to an NDJSON event log during the cache-eviction session: obs-a3f1 (github.issue), clm-7b91 (claim from issue), obs-d2e4 (web.fetch of Stack Overflow), clm-8c44 (claim from SO post), evd-9001 (evidence set with one external_document item), blf-44a2 (belief proposed), dec-1100 (decision), act-2200 (action). Each event is shown with its monotonic sequence number and kind. A vertical dashed marker between evd-9001 and blf-44a2 is labelled 'auto-observation gate fires — authority downgraded from auto_observation to reflection'." />
  <figcaption>Fig. 2 · One session, eight events. The gate fires between the evidence assessment and the belief proposal; the belief is recorded as unverified, and downstream decisions can see that.</figcaption>
</figure>

---

## What comes out the other end

The point of all this isn't the log. The log is a means. The point is being able to answer the questions Part 1 ended on, for any session, after the fact.

The CLI command is `lodestar report <session-id>`. It walks the event log for a session and produces a markdown trace of the chain. For the cache-eviction scenario, the relevant fragment of the report looks something like this:

```markdown
## Belief blf-44a2 — "This Stack Overflow fix applies to our cache"

Recorded: 2026-04-12 10:14:31 (auto-observation downgraded to reflection)
Truth status:     unverified
Retrieval status: restricted
Security status:  clean
Freshness status: fresh

Evidence:
  • obs-d2e4 (web.fetch, Stack Overflow post #4471203, external_document)
    Quality: external_document — auto-promotion gate prevented `supported` status.

Decisions referencing this belief:
  • dec-1100 (propose patch to src/cache/eviction.ts) — referenced at confidence 0.42
    Outcome: action executed; tests passed.
    No subsequent verification of the underlying belief.

⚠ Belief still at truth_status: unverified at session end.
  No downstream evidence promoted it.
  Recommended: probe verifying that the Stack Overflow fix's preconditions
  (cache library, eviction policy version) match this codebase.
```

What I get from that report is the answer to the question Part 1 asked. The agent observed the Stack Overflow post. It extracted a claim from it. The claim did not become an actionable belief — it sat at `truth_status: unverified, retrieval_status: restricted` for the whole session. The decision to propose a patch *did* reference the unverified belief, at confidence 0.42. That's exactly the kind of signal the post-mortem needs: the agent acted on a claim it had not actually endorsed, and nothing in the loop pushed back.

The report doesn't pretend the agent shouldn't have acted. It makes legible the exact spot where a stronger action contract — one that refuses to modify production code when its referenced beliefs include any `truth_status: unverified` items — would have caught the failure. The post-mortem stops being a guess.

---

## What's still hard

I'm writing this with the implementation visibly mid-flight, and I want to be specific about what doesn't yet work, because it's the only honest version of this post.

Claim extraction quality is bounded by the extractor. Lodestar can guarantee that a Claim, once extracted, carries its source observation IDs and travels through the lifecycle correctly. It cannot guarantee that an LLM-based extractor will reliably notice when an issue mentions a cache library version that differs from the one in the linked Stack Overflow post. That's a property of the extractor, not the trust layer. The current scaffold uses structured tool outputs where available and LLM extraction where not, and the LLM extraction is the weakest link in the chain.

Compromised tools are not solved in v0. The Action Kernel validates the *shape* of a tool's output against its declared schema. A tool that lies about world state — returning `{"exit_code": 0}` when the underlying process crashed — produces a poisoned Observation that becomes a poisoned Claim, and the rest of the chain inherits the lie. The mitigations are provenance (signed tools, deferred to v0.2 stretch), sandboxing (shell-safety constraints already in place; the MCP proxy declares sandbox profiles in tool contracts but does not enforce them at the OS level yet), and probes that exercise tools against ground truth. None of those are bulletproof.

The schema has stabilized at v0.2 and could still surprise me. Five rounds of adversarial review have made it more robust than it was, but the schema has not yet been stressed by a real production agent system. The probes catch the threats they are designed to catch. Threats outside their design are not yet caught.

I'm building this in public partly so these gaps are public. A system whose limits are visible is one you can build on; a system whose limits are obscured is one you can only hope on.

---

## Coming next

[Part 3](/writing/what-five-rounds-of-adversarial-review-taught-me-about-my-own-design/) is the post I'm most curious to write, and the one furthest from the conventional voice of a project announcement. It's about the adversarial review process I ran on this architecture: five rounds of pushing the design against a sceptical reviewer, watching what survived, what got rebuilt, and what I learned about my own blind spots. Several pieces of what's in this post — the auto-observation gate, the separation of belief authority from transition authority, the ContextPolicy as a first-class primitive, the MCP proxy's split of envelope and content claims — exist because earlier versions failed under review. The exercise is portable; the lessons are general; the specifics are worth putting on the record.

The link will appear here when it goes up. Until then, the code is at [github.com/qmilab/lodestar](https://github.com/qmilab/lodestar), and the architecture memo it implements is in `docs/architecture/v02-delta.md`. A runnable demonstration of the auto-observation gate firing on a prompt-injected file lives in `examples/claude-code-wrapped/`. The first article in the series — *[The question my coding agent couldn't answer](/writing/the-question-my-coding-agent-couldnt-answer/)* — is what this one builds on.

---

*This series is part of the [QMI Lab](https://qmilab.com) research arc on machine intelligence. Lodestar was developed internally under the codename Orrery; the renaming history is documented in the repository.*
