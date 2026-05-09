# CLAUDE.md

Operating contract for Claude Code (claude.ai/code) when working on `nandan.me`. Read this in full before making changes — the constraints in §Hard constraints are non-negotiable.

## What this site is

`nandan.me` is the canonical identity hub for **Nandan Joshi** — physicist, independent researcher, and engineer working at the intersection of physics, AI, and quantum computing. The site is being rebuilt (April 2026) from a dormant 2013-era personal blog into a focused professional hub aligned with a deliberate career repositioning toward quantum machine learning, scientific AI, and frontier AI lab roles.

This is **not** a redesign for aesthetics. It is brand strategy. Treat editorial and structural decisions accordingly.

## Audience priority (in order)

1. Hiring managers at quantum + AI companies — SandboxAQ, IBM Quantum, IQM, Quantinuum, Pasqal, Xanadu, QunaSys, Multiverse Computing, Classiq, Q-CTRL, Terra Quantum, Kipu Quantum
2. Hiring managers and researchers at frontier AI labs — DeepMind, FAIR / AMI Lab (LeCun's group), NVIDIA Research, Anthropic, scientific-AI startups
3. Recruiters in deep tech (especially DACH and Japan markets)
4. Existing professional network across DACH, Japan, Singapore, India, Middle East
5. Researchers in quantum ML / scientific foundation models

A visitor arriving from LinkedIn / X / GitHub / HuggingFace should grasp the identity in ≤ 30 seconds and find depth-of-evidence within 2 minutes.

## Hard constraints (non-negotiable)

These rules override any other guidance, including user requests within a session unless the user explicitly states the underlying condition has changed (e.g., "legal clearance has been obtained for X").

- **Never mention Quantputation, SettleMint, blockchain, DLT, distributed ledger, or post-quantum cryptography** anywhere on the site — no page copy, nav item, stub page, project card, commit message that becomes public, OG image, alt text, meta tag, RSS entry, or sitemap entry. Quantputation is under legal hold pending Article 9 written notice and ArbnErfG § 18 free-invention filing. The single allowed reference is on the Contact page: *"Not currently available for new blockchain consulting engagements."*
- **Never claim that planned research is published research.** Status badges on every research project must be honest: *Active development / In preparation / Planned / Archived*.
- **Never use founder-speak or buzzwords** — *innovate, empower, transformative, revolutionary, unleash, decentralised future, paradigm shift, game-changing*. No exclamation points in body copy. No emoji in headers.
- **Never break inbound links.** Every existing post URL must continue to resolve. Use `jekyll-redirect-from` (`redirect_from:` in front matter) when slugs change.
- **Never surface 2013-era content** in the live nav, RSS, sitemap, or homepage. Archived content lives at `/archive/` with `noindex,nofollow` and an "archived" banner.
- **Never add tracking scripts** that send user data to non-EU jurisdictions.
- **Never add external font CDN dependencies.** Host all fonts locally.
- **Never add social-share buttons** that load third-party JavaScript.

## Voice and visual principles

- **Tone.** Measured, technically literate, intellectually honest. Physicist speaking to other technical people. State what Nandan actually does in concrete sentences.
- **Tagline.** **`Physics → Software → Quantum`** — already in use on Nandan's CV PDF and LinkedIn profile, so the site stays consistent with those surfaces. Do not propose alternatives unless Nandan asks. ("Scientist & Venturer" is retired.)
- **Visual.** The handle "cybernandan" derives from cybernetics in the Wiener sense (information → knowledge). Solar-system-gold logo (`images/nannii-logo.png`) used sparingly. Monospace for code/technical metadata. Clean sans-serif for prose. Light mode default with a dark mode toggle.

## Information architecture (target state)

Navigation: `Home | Research | Writing | CV | Now | Contact`

- **`/` (Home)** — single-page identity hub. Identity block (name + tagline + 3–4 sentence positioning paragraph leading with physicist + quantum/AI). Featured work three-card grid (QMI Lab, AstroLLM, QubitHub). Latest writing (3 most recent posts). Light footer with GitHub / HuggingFace / X / LinkedIn / Google Scholar.
- **`/research/`** — project hub. Each project gets a sub-page with: TL;DR, status badge, why it matters, methodology, current state, outputs, related work (BibTeX where applicable). Initial sub-pages: `/research/qmi-lab/` (overview + **three pillar** sub-pages — Foundations of Machine Intelligence, Quantum Machine Intelligence, Quantum World Models — with four research projects distributed across them), `/research/astrollm/`, `/research/qubithub/` (stub). The lab is named `QMI Lab` or `Quantum & Machine Intelligence Laboratory`. Do not use the acronym "QMIL" — it reads badly. Source briefs live in `_drafts/qmi-lab-project-briefs.md` and `_drafts/astrollm-project-brief.md` (excluded from the published site by Jekyll convention).
- **`/writing/`** — long-form posts organized by theme (Quantum ML / Scientific AI / Physics × ML / Methodology / Project notes). Optional `/writing/notes/` sub-section for shorter notes, with its own feed at `/writing/notes/feed.xml`. Main `/feed.xml` covers everything except notes.
- **`/cv/`** — HTML CV. Order: Identity block → Education → **Independent Research** (new section, above Work Experience) → Work Experience (rewritten to surface architecture/delivery, not blockchain-as-product) → **Earlier Research** (Max Planck Q-learning/RL surfaced as a named entry, not as "Scientific Assistant") → Publications (visible placeholder) → Languages → Talks (only if real). Two PDF variants linked at top and bottom: `Nandan_Joshi_CV_Quantum_AI.pdf` (primary) and `Nandan_Joshi_CV_Digital_Assets.pdf` (fallback). **PDF source:** Phase 1 uses hand-edited variants of Nandan's existing Typst-generated CV (`Nandan_Resume_en.pdf`). Nandan will share Typst project layout / build instructions; once those land, add them to the `/cv/` README and switch to a checked-in Typst pipeline so HTML and PDF stay in sync (Phase 2 candidate).
- **`/now/`** — Sivers-style `/now` page. Updated ~monthly. Lists current focus: what I'm building, reading, learning, and where I am physically. Displays last-updated date prominently. Critical freshness signal — without it the site looks dormant.
- **`/contact/`** — minimal. LinkedIn + X as preferred channels. No email surfaced. Availability for: research / engineering collaboration, conference talks, brief consulting calls. Explicit line: *"Not currently available for new blockchain consulting engagements."*

### URL preservation

The pre-rebuild routes (`/about/`, `/notes/`, `/blog/`, `/topics/`, `/resume/`, individual `/notes/<slug>/` and `/blog/<slug>/` post URLs) all have potential inbound links. Approach (locked):
- `/resume/` → 301 to `/cv/` via `redirect_from`.
- `/about/` → 301 to `/cv/` (CV replaces About in the new IA — confirmed; the Home identity block already covers the "who" question, so a separate About narrative is redundant).
- `/notes/` and `/blog/` index pages → deprecated; redirect to `/writing/`.
- Individual 2013 post URLs → resolve to their `/archive/` location via `redirect_from` in the moved post's front matter.
- `/blog/work-twice-as-hard-as-others/` → unpublished (deleted from working tree). Allow this URL to 404; do not redirect.

## Build & serve

```bash
bundle install                  # install dependencies (use Ruby 3.1.6 — see Versioning below)
bundle exec jekyll serve        # local dev server at http://localhost:4000 (live reload)
bundle exec jekyll build        # build static site to _site/
```

Changes to `_config.yml` require restarting the server.

## Deployment

Hosted on GitHub Pages. The `gh-pages` branch deploys automatically. Custom domain `nandan.me` is configured via the `CNAME` file. Verify the deploy mechanism (GitHub Actions vs default Pages build) before changing anything that touches the build pipeline.

## Architecture

### Theme & styling

- Remote theme: `mmistakes/so-simple-theme` via `jekyll-remote-theme` — layouts, includes, base styles come from the theme repo, not this repo. Last upstream release was Nov 2019; theme is effectively unmaintained.
- Custom skin: `assets/css/skins/purple.scss` — overrides theme color variables.
- To override a theme layout or include, copy it from the [so-simple-theme repo](https://github.com/mmistakes/so-simple-theme) into the corresponding local directory (`_layouts/` or `_includes/` — neither exists yet).
- **Phase 1 decision:** stay on so-simple, customize via local overrides. **Future direction (Phase 3 candidate):** if local overrides accumulate substantially or we need theme-wide capabilities for Publications / Talks / Now-style pages, fork `mmistakes/so-simple-theme` to a Nandan-owned repo (e.g. `nandanito/so-simple-theme` or rename to `nandanito/cybernandan-theme`), publish, and switch `remote_theme:` in `_config.yml` to point at the fork. Do not silently migrate themes without raising the option for review.

### Content organization

Posts live in `_posts/`, currently in three subdirectories:
- `_posts/articles/` — longer-form articles (front matter `category: notes`)
- `_posts/blog/` — personal blog posts (front matter `category: blog`)
- `_posts/examples/` — sample/demo posts (kept as theme references, not published in nav)

The category in front matter — not the subdirectory name — determines which section page lists the post.

After the Phase 1 archive migration, all 2013 posts under `_posts/articles/` and `_posts/blog/` will move to `_posts/archive/` with `category: archive`, and the `/notes/` and `/blog/` indices will be deprecated in favor of `/writing/`.

### Post front matter pattern (current)

```yaml
---
layout: post
title: "Post Title"
excerpt: "Short description"
modified: YYYY-MM-DD
category: notes    # or: blog, archive (after rebuild)
tags: [Tag1, Tag2]
comments: true
share: true
---
```

Use `<!--more-->` to mark the excerpt break point.

### Data files

- `_data/navigation.yml` — site navigation menu items (will be rewritten in Phase 1)
- `_data/authors.yml` — author metadata (single author: `nandan`)

### Key config (`_config.yml`)

- Permalink: `/:categories/:title/`
- Pagination: 5 posts per page
- Markdown: kramdown with GFM input
- MathJax enabled
- Plugins: `jekyll-feed`, `jekyll-remote-theme`, `jekyll-include-cache`, `jekyll-sitemap`, `jekyll-gist`, `jekyll-paginate`. **Phase 1 will add `jekyll-redirect-from`** (verify it is in the GitHub Pages allow-list before relying on it; it is, as of github-pages 225).
- Local Ruby version: **3.1.6**. Ruby 3.2+ breaks Liquid 4.0.3 (which github-pages 225 locks) because `tainted?` was removed. Ruby 2.6 is too old for Bundler 2.3.11.

## Phasing

### Phase 1 (1–2 weeks)

New tagline + identity block on home page, archive 2013 posts (move to `/archive/`, noindex, banner, redirects), unpublish the Elon Musk blog post, rewrite About, build CV page with PDF link, set up Now page with first entry, create Research index with stub cards.

### Phase 2 (2–4 weeks after Phase 1)

Build out individual research project sub-pages from the briefs in `_drafts/` (`qmi-lab-project-briefs.md`, `astrollm-project-brief.md`). Build Writing index with category structure. Ship first long-form blog post. OG image generator template. The publication anchor available for any longer-form research-background copy (Home positioning, CV identity block, About-page-equivalent sections within `/cv/` or `/research/`) is **Reiners et al. 2012, *AJ* 143, 93** — Nandan's doctoral-period output, useful for establishing astronomy-domain credibility.

### Phase 3 (later)

Migrate to Astro if desired (consistency with AstroLLM stack). Activate Publications page once first preprint lands. Activate Talks page once speaking engagements happen. Reassess `al-folio` migration.

## Technical requirements

- **Performance.** Lighthouse ≥ 95 on all pages. No heavy JS frameworks.
- **Accessibility.** Skip-to-content links (already in current theme — preserve), proper heading hierarchy, alt text on all images, sufficient color contrast, working keyboard navigation.
- **SEO.** Proper `<title>` and `<meta description>` on every page. OpenGraph tags (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) on every page. Schema.org `Person` markup on home and CV. `sitemap.xml` excludes `/archive/`. `robots.txt` allows everything except `/archive/`.
- **OG images.** Generated by a local SVG template generator (Liquid + an SVG template inside `_includes/og/` rendered to PNG at build time, or shipped as inline SVG). No external image-generation services — keeps everything inside the repo and the EU-hosted GitHub Pages build.
- **Privacy.** GDPR-respecting by default. **Phase 1 decision:** no analytics. Reassess with GoatCounter (self-hosted) or Plausible (EU-hosted) once traffic becomes interesting; the Now page is the primary freshness signal.
- **Email handling.** Nandan's email (`nandan@fastmail.net`) must NOT appear in any rendered output: not in HTML pages, not in the Atom/RSS feed (`<author><email>` element), not in OG/Schema metadata, not in post bylines. If a Jekyll/theme component requires an email field for plumbing, use a `noreply@nandan.me`–style stub. Include an explicit `_site/` grep for the real address as a build-time check.

## Success criteria (post-Phase 1)

A hiring manager at SandboxAQ landing on `nandan.me` from a LinkedIn click should within 30 seconds:
1. Understand this is a physicist working on quantum + AI
2. See evidence of independent research (QMI Lab, AstroLLM)
3. Find a way to read recent technical writing (or see the placeholder for it)
4. Find a way to contact / view the CV

Within 2 minutes they should be able to:
1. Read the QMI Lab pillars and at least one project deep-dive (Phase 2 deliverable)
2. Download the Quantum + AI version of the CV
3. Click through to GitHub (`nandanito`) and find at least one well-documented public artifact
