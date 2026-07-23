---
id: "slugs-are-permanent"
title: "Slugs are URLs, and URLs are permanent"
status: "Active"
created: "2026-07-23"
last_reviewed: "2026-07-23"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- content
- urls
---

# Slugs are URLs, and URLs are Permanent

## Tenet

**Description**: A slug is not just a filename — it becomes the public URL for a piece of content. Once published and shared (in newsletters, social posts, external links, or search indexes), changing a slug breaks those references permanently unless a redirect is put in place. The commit history shows this is the single most persistent class of error in this repository: multiple batch "fixing names and slugs" campaigns, a dedicated slug-fix script, and the URL conflict that caused a Jekyll build failure in July 2026.

Slug fields must enforce the correct format (lowercase, hyphens, no spaces), must be unique across their collection, and must be treated as immutable after first publication. The CMS must make it easy to get this right the first time, not fix it afterwards.

**Quote**: *"A bad slug is a broken promise to everyone who shares the link."*

**Examples**:
- CMS slug fields showing an explicit hint: "lowercase and hyphens only, no spaces or capitals"
- The auto-past-categories workflow using slugs as stable identifiers that never change when a category is updated
- Checking for slug conflicts in a Jekyll build before deploying

**Counter-examples**:
- Entering `AI for Science Research Showcase` as a slug, creating a URL collision with an existing event (exactly the bug fixed in commit 082c321)
- Renaming an event after it has been published and shared without adding a redirect
- Allowing the CMS to accept uppercase or spaced slugs without warning
