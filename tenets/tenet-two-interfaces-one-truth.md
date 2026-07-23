---
id: "two-interfaces-one-truth"
title: "Two interfaces, one source of truth"
status: "Active"
created: "2026-07-23"
last_reviewed: "2026-07-23"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- architecture
- cms
- git
---

# Two Interfaces, One Source of Truth

## Tenet

**Description**: This repository is managed through two very different interfaces: Decap CMS (a browser-based editor designed for non-technical users) and GitHub (a developer-oriented version-control system). Both write to the same Git repository. Neither interface is privileged — changes made through the CMS are equally valid as changes made directly in Git, and vice versa.

This duality creates the central design tension in the repository. Decap CMS abstracts away Git entirely, which makes content editing accessible but hides the structure that Git relies on (slugs, frontmatter, file naming). Direct Git access gives full control but requires technical knowledge that editorial staff do not have. Good decisions in this repository resolve that tension rather than ignore it: infrastructure must be legible to developers, and content workflows must be operable by editors without developer assistance.

**Quote**: *"The CMS and GitHub are two doors into the same room. Both must work."*

**Examples**:
- Backlog tasks written in plain Markdown files, readable in GitHub and manageable without the CMS
- Slug hint text in the CMS config written to prevent errors that would only surface as Jekyll build failures visible only in GitHub
- Automated workflows (GitHub Actions) doing housekeeping work that neither interface handles well (e.g., recategorising past events)

**Counter-examples**:
- Making a structural change to content files through GitHub that breaks the CMS's ability to edit them
- Adding a CMS-only workflow that has no fallback for direct Git edits
- Writing commit messages that only make sense to developers and give no context to someone reviewing through the CMS audit log
