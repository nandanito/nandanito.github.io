# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal blog for Nandan Joshi (nandan.me), a Jekyll-based static site hosted on GitHub Pages. Uses the **So Simple** remote theme (`mmistakes/so-simple-theme`) fetched via `jekyll-remote-theme`. The site has been largely dormant since ~2014.

## Build & Serve Commands

```bash
bundle install                  # Install dependencies
bundle exec jekyll serve        # Local dev server at http://localhost:4000 (live reload)
bundle exec jekyll build        # Build static site to _site/
```

Note: Changes to `_config.yml` require restarting the server.

## Deployment

Hosted on GitHub Pages. The `gh-pages` branch deploys automatically. The custom domain `nandan.me` is configured via the `CNAME` file.

## Architecture

### Theme & Styling
- Remote theme: `mmistakes/so-simple-theme` — layouts, includes, and base styles come from the theme repo, not this repo
- Custom skin: `assets/css/skins/purple.scss` — overrides theme color variables (black/white/purple palette)
- To override a theme layout or include, copy it from the [so-simple-theme repo](https://github.com/mmistakes/so-simple-theme) into the corresponding local directory

### Content Organization
Posts live in `_posts/` and are categorized into subdirectories:
- `_posts/articles/` — longer-form articles (category: `notes`)
- `_posts/blog/` — personal blog posts (category: `blog`)
- `_posts/examples/` — sample/demo posts from the theme

**Important:** The category in front matter determines which section page displays the post, not the subdirectory name. Articles use `category: notes`, blog posts use `category: blog`.

### Post Front Matter Pattern
```yaml
---
layout: post
title: "Post Title"
excerpt: "Short description"
modified: YYYY-MM-DD
category: notes    # or: blog
tags: [Tag1, Tag2]
comments: true
share: true
---
```

Use `<!--more-->` to mark the excerpt break point in post content.

### Section Pages
Each section (`/about/`, `/notes/`, `/blog/`, `/topics/`, `/search/`) has its own `index.md` that uses Liquid templates to list posts filtered by category or tag. Navigation is defined in `_data/navigation.yml`.

### Data Files
- `_data/navigation.yml` — site navigation menu items
- `_data/authors.yml` — author metadata (currently single author: `nandan`)

### Key Config Details (`_config.yml`)
- Permalink structure: `/:categories/:title/`
- Pagination: 5 posts per page
- Markdown: kramdown with GFM input
- MathJax enabled
- Plugins: jekyll-feed, jekyll-remote-theme, jekyll-include-cache, jekyll-sitemap, jekyll-gist, jekyll-paginate

### Versioning
Pinned to `github-pages ~> 225` which locks Jekyll at 3.9.0. This is an older Jekyll version — be aware of API differences if consulting current Jekyll docs.
