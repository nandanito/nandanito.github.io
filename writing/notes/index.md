---
layout: page
title: Notes
excerpt: "Shorter informal pieces — paper reading notes, conference reflections, project-status updates."
modified: 2026-05-31
permalink: /writing/notes/
---

Shorter, lower-overhead pieces: paper reading notes, conference reflections, and project-status updates from [QMI Lab](/research/qmi-lab/) and [AstroLLM](/research/astrollm/). Long-form essays live at [/writing/](/writing/).

Subscribe via the [notes feed](/writing/notes/feed.xml).

{% assign notes_posts = site.categories.notes | sort: 'date' | reverse %}

{% if notes_posts.size > 0 %}
<ul class="writing-list">
{% for post in notes_posts %}
  <li class="writing-entry">
    <h2 class="writing-entry-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p class="writing-entry-meta">
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
      {%- assign words = post.content | number_of_words -%}
      {%- assign minutes = words | divided_by: site.words_per_minute | at_least: 1 -%}
      &nbsp;·&nbsp;{{ minutes }} min read
      {% if post.tags %}&nbsp;·&nbsp;{{ post.tags | slice: 0, 3 | join: ' · ' }}{% endif %}
    </p>
    {% if post.excerpt %}
    <p class="writing-entry-excerpt">{{ post.excerpt | strip_html | strip_newlines | truncate: 280 }}</p>
    {% endif %}
  </li>
{% endfor %}
</ul>
{% else %}
<p>The first notes arrive shortly.</p>
{% endif %}
