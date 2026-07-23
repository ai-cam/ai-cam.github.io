---
id: "automate-editorial-toil"
title: "Automate the editorial toil, not the editorial judgment"
status: "Active"
created: "2026-07-23"
last_reviewed: "2026-07-23"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- automation
- editorial
---

# Automate the Editorial Toil, Not the Editorial Judgment

## Tenet

**Description**: Some content maintenance work is mechanical and error-prone when done by hand: moving past events into the "Past Events" category, updating canonical dates, keeping indexes current. The commit history includes batch "fixing names and slugs" campaigns — evidence that mechanical work deferred becomes a larger correction later. Automation should absorb this class of work so that editorial time is spent on content, not housekeeping.

However, automation must not make editorial decisions. What is published, when it is published, how it is described — these judgments belong to the editorial team. Automation that silently alters content meaning (rather than structure) erodes trust in the system and can cause published errors that are hard to detect. The right boundary: automate state transitions driven by objective facts (a date has passed), never automate content or tone.

**Quote**: *"A computer should notice that the event is in the past. A human should decide what that means for the audience."*

**Examples**:
- `auto-past-categories.yml` moving events whose `event_date` has passed into "Past Events" without human intervention
- `backlog/update_index.py` regenerating the task index automatically on each `whats-next` run
- Slug validation in the CMS config preventing invalid slugs at entry time rather than requiring a fix-up commit later

**Counter-examples**:
- An automation that edits the body text of a published report to update statistics
- Auto-generating social media copy from frontmatter fields and publishing it without editorial review
- Silently deleting content that passes a threshold age without a human decision point
