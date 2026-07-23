---
id: "editorial-continuity"
title: "Editorial continuity comes first"
status: "Active"
created: "2026-07-23"
last_reviewed: "2026-07-23"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- cms
- editorial
---

# Editorial Continuity Comes First

## Tenet

**Description**: The website exists to publish content. When the CMS is broken, the organisation cannot communicate — and communications staff cannot fix it themselves. Any change to infrastructure, dependencies, or configuration must therefore be evaluated first against the question: does this keep Eli able to publish? A crashed CMS is a P1 incident regardless of what caused it. Everything else is secondary.

This tenet is grounded in the numbers: 88% of commits in this repository are content operations initiated through Decap CMS. The technical infrastructure serves those operations; it does not justify itself.

**Quote**: *"If Eli can't publish, we've failed."*

**Examples**:
- Pinning Decap CMS to 3.14.1 within hours of 3.15.0 breaking the editor — restoring publishing before investigating the root cause
- Tracking the Decap version pin in a backlog task and a GitHub issue so the unpin is deliberate, not accidental
- Running `whats-next` after infrastructure changes to confirm no new blocking issues

**Counter-examples**:
- Applying a CMS dependency upgrade on a Friday afternoon without testing the editor
- Fixing a Jekyll build error without checking whether the CMS is still functional after the fix
- Prioritising developer experience improvements over a broken publish workflow
