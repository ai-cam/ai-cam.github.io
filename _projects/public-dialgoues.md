---
layout: projects-single
title: AI Public Dialogues
excerpt: "A new ai@cam report sets out the guardrails needed to increase
  democratic control over hte use of AI in public services in the UK. "
category:
  - policy
image: /assets/uploads/154937-ouy119-839-copy.jpg
researchers:
  - neil-lawrence
  - jessica-montgomery
---

A new ai@cam report sets out the guardrails needed to increase democratic control over hte use of AI in public services in the UK.

<section class="block block--bg-pink block__posts">
  <div class="container">
    <div class="posts__intro">
      <h2 class="section-heading section-heading--left">Related Content</h2>
    </div>
    <div class="posts__grid">
      {% assign combined_entries = '' | split: '' %}
      
      {% comment %}Collect all posts and news with dialogue category{% endcomment %}
      {% for post in site.posts %}
        {% if post.categories contains "dialogue" %}
          {% assign combined_entries = combined_entries | push: post %}
        {% endif %}
      {% endfor %}
      
      {% for news in site.news %}
        {% if news.categories contains "dialogue" %}
          {% assign combined_entries = combined_entries | push: news %}
        {% endif %}
      {% endfor %}
      
      {% comment %}Sort combined entries by date{% endcomment %}
      {% assign sorted_entries = combined_entries | sort: 'date' | reverse %}
      
      {% assign count_check = false %}
      {% for item in sorted_entries limit:4 %}
        {% if item.url == page.url %}
          {% assign count_check = true %}
        {% endif %}
      {% endfor %}
      
      {% if count_check == false %}
        {% for entry in sorted_entries limit:4 %}
          <a class="posts__item" href="{{ entry.url }}">
            <div class="posts__item-thumbnail">
              {% if entry.image != nil %}
                <img src="{{ entry.image }}">
              {% else %}
                <img alt="" src="../assets/images/placeholder-1.jpg" />
              {% endif %}
            </div>
            <div class="posts__item-content">
              <span class="category">{{ entry.categories | replace: "-", " " | replace: "[", "" | replace: "]", "" | replace: '"', "" }}</span>
              <h3>{{ entry.title }}</h3>
              <span class="button button--simple">Read more</span>
            </div>
          </a>
        {% endfor %}
      {% else %}
        {% for entry in sorted_entries limit:4 %}
          {% if entry.url != page.url %}
            <a class="posts__item" href="{{ entry.url }}">
              <div class="posts__item-thumbnail">
                {% if entry.image != nil %}
                  <img src="{{ entry.image }}">
                {% else %}
                  <img alt="" src="../assets/images/placeholder-1.jpg" />
                {% endif %}
              </div>
              <div class="posts__item-content">
                <span class="category">{{ entry.categories | replace: "-", " " | replace: "[", "" | replace: "]", "" | replace: '"', "" }}</span>
                <h3>{{ entry.title }}</h3>
                <span class="button button--simple">Read more</span>
              </div>
            </a>
          {% endif %}
        {% endfor %}
      {% endif %}
    </div>
  </div>
</section>
