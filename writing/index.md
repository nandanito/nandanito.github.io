---
layout: page
title: Writing
excerpt: "Long-form writing on quantum machine learning, scientific AI, and the physics × ML interface."
modified: 2026-05-18
---

Long-form pieces on quantum machine learning, scientific AI, the physics × ML interface, and the methodology questions that show up at all three intersections. Project notes from [QMI Lab](/research/qmi-lab/) and [AstroLLM](/research/astrollm/) land here as they ship.

{% assign writing_posts = site.categories.writing | sort: 'date' | reverse %}

{% if writing_posts.size > 0 %}
<ul class="writing-list">
{% for post in writing_posts %}
  <li class="writing-entry">
    <h2 class="writing-entry-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p class="writing-entry-meta">
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
      {%- assign words = post.content | number_of_words -%}
      {%- assign minutes = words | divided_by: site.words_per_minute | at_least: 1 -%}
      &nbsp;·&nbsp;{{ minutes }} min read
      {% if post.tags %}&nbsp;·&nbsp;{{ post.tags | join: ' · ' }}{% endif %}
    </p>
    {% if post.excerpt %}
    <p class="writing-entry-excerpt">{{ post.excerpt | strip_html | strip_newlines | truncate: 280 }}</p>
    {% endif %}
  </li>
{% endfor %}
</ul>
{% else %}
<p>The first long-form posts arrive in 2026.</p>
{% endif %}

A separate `/writing/notes/` sub-section will host shorter informal pieces — paper reading notes, conference reflections — kept visually distinct from long-form essays.
