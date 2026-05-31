# /writing/notes/ — post format

Reference snippet for authoring shorter informal posts under `/writing/notes/`.
Kept in `_drafts/` (unpublished) so the format guidance lives next to the
other brand/content source-of-truth files. Share with Claude Desktop's
"Career & Brand" project when drafting notes.

Last updated: 2026-05-31.

---

## Follow-up: Notes discoverability (Phase 2)

Current state (2026-05-31): Notes are reachable via two clicks from the home
page (`Latest writing → All writing → Notes`) plus a one-click `Notes →`
shortcut in the home page's "Latest writing" footer, and a prominent link
at the top of `/writing/`. Top nav stays at 6 items per the locked IA spec,
so Notes is intentionally not a top-level nav item.

This is workable but not strong. Open options to revisit in Phase 2:

1. **"Recent notes" strip on `/writing/`** — a small section at the top or
   side of the long-form index showing the latest 3 notes with smaller,
   muted type and one-line excerpts. Keeps long-form signal clean while
   raising notes' visibility. **Preferred.**
2. **Sub-nav under Writing** — hover/disclosure menu in the top nav
   exposing "Long-form" and "Notes" as Writing children. Closer to the
   theme's grain, but adds a JS/hover dependency to the otherwise
   plain-anchor nav.
3. **Inline-mix notes into `/writing/`** — single chronological list with
   a "Note" badge on notes entries. Solves discoverability in one move,
   but dilutes the long-form signal that the index is doing for hiring
   managers. **Not preferred.**
4. **Footer "Recent notes" block** — site-wide footer lists 2–3 latest
   notes. Lowest-friction, lowest-prominence. Defensible if (1) feels
   too prominent.

Decide once there are 5–10 notes posts in the bin — the right answer
depends on cadence and average note length.

---

Shorter informal pieces: paper-reading notes, conference reflections,
project-status updates. Separate from long-form essays at `/writing/`.
Goal: ship faster, lower edit overhead, but the same voice and honesty
rules apply.

## File location & naming

- Path: `_posts/writing/YYYY-MM-DD-kebab-case-slug.md`
- Date in filename = publish date (UTC, today or earlier — never future)
- Slug: lowercase, hyphenated, no stop-words at the front
  ("notes-on-x" not "some-notes-on-x")

## Front matter (copy verbatim, fill in)

```yaml
---
layout: post
title: "Short, declarative, no colon-subtitle pattern unless needed"
excerpt: "One or two sentences. Shown in the notes index, the feed, and OG tags. No marketing tone."
modified: YYYY-MM-DD
category: notes
permalink: /writing/notes/:title/
tags: [Two, To, Four, Tags]
author: nandan
comments: false
share: false
---
```

Notes on the fields:

- `category: notes` is what `/writing/notes/feed.xml` picks up. Do not also
  add `writing` — that would surface the note in the long-form index.
- `permalink: /writing/notes/:title/` is required because the default
  permalink in `_config.yml` would otherwise put the post at `/notes/<slug>/`.
- `modified:` = the last meaningful edit date. Equal to the publish date
  on day one.
- Tags: 2–4, Title Case, reused from existing tags where possible.

## Body

- Length envelope: ~150–800 words. If it grows past ~800, it probably
  wants to be a long-form `/writing/` piece.
- Open with the claim or observation in the first 1–2 sentences. No
  throat-clearing ("I've been thinking about…", "Recently I read…").
- Use `<!--more-->` after the lead paragraph to mark the excerpt break.
- Markdown only. Inline links fine. Code blocks fenced with triple
  backticks and a language tag.
- One H2 (`##`) per logical break if the post needs structure; skip
  headings for very short notes.
- No emoji in headings. No exclamation points in body copy.

## Voice (binding — from CLAUDE.md)

- Measured, technically literate, intellectually honest. Physicist
  speaking to other technical people.
- **Never** write "PhD" or "Dr." Use "DFG-funded doctoral research" or
  "DFG Doctoral Research Fellow" if referencing the 2007–2012 period.
  Awarded degree is **Diplom Physik** (Göttingen, 2007).
- **Never** claim planned research is published research. Status badges:
  *Active development / In preparation / Planned / Archived*.
- **Banned phrases:** transformative, empower, unleash, paradigm shift,
  game-changing, boundary-pushing, bold, journey, passionate, thrilled,
  honoured, excited to share, just my two cents, leverage (as a verb),
  innovate, revolutionary, decentralised future.
- **Never** mention Quantputation, QubitHub, or SettleMint product
  internals on this site. (SettleMint is fine in CV/work-history
  context only.)
- Email `nandan@fastmail.net` must not appear anywhere in rendered output.

## Suitable note types

- Paper-reading notes: 1–3 papers, what's interesting, what's wrong,
  what to try next.
- Conference / talk reflections: what was said, what was missed, what
  changed your mind.
- Project status: what shipped this week on QMI Lab / AstroLLM, blockers,
  next step.
- Reading-list snippets: a single idea from a book or post, in your own
  framing.

## Not suitable as a note

- Position statements on identity, research direction, or career →
  long-form `/writing/`.
- Anything you'd cite from a CV → long-form, with proper structure.
- Personal-life posts → not on this site at all.

## Example skeleton

```markdown
---
layout: post
title: "Reading notes: Carleo et al. on neural-network quantum states"
excerpt: "The 2017 RBM ansatz paper, re-read with seven years of hindsight on what generalised and what didn't."
modified: 2026-06-04
category: notes
permalink: /writing/notes/:title/
tags: [Quantum ML, Reading Notes, Variational Methods]
author: nandan
comments: false
share: false
---

The paper's central claim — that a restricted Boltzmann machine can represent ground states of spin Hamiltonians as accurately as established variational ansätze — held up. What didn't hold up was the implicit promise that the architecture would scale.

<!--more-->

## What the paper got right

…

## What seven years showed

…
```
