---
id: "0002"
title: "Slugs must be valid, unique, and stable after first publication"
status: "Proposed"
priority: "High"
created: "2026-07-23"
last_updated: "2026-07-23"
related_tenets: ["slugs-are-permanent", "two-interfaces-one-truth"]
stakeholders: ["Comms lead", "Neil Lawrence", "Site visitors via shared links"]
tags:
- requirements
- slugs
- content
- urls
---

# REQ-0002: Slugs must be valid, unique, and stable after first publication

## Description

A slug defines the public URL for a piece of content. Invalid slugs (containing spaces or uppercase) cause Jekyll build failures. Duplicate slugs cause URL collisions where one piece of content silently overwrites another in the built site. Changed slugs on published content break any external links or bookmarks to that content.

The commit history shows this is the most persistent error class in the repository, requiring several batch fix campaigns and at least one build-breaking collision.

**Why this matters**: Tenet `slugs-are-permanent` — a bad slug is a broken promise to anyone who shares the link.

**Who benefits**: The comms lead (avoids confusing build errors), site visitors (stable URLs), developers (fewer fix campaigns).

## Acceptance Criteria

- [ ] The CMS slug field displays a hint making clear that only lowercase letters and hyphens are valid (no spaces, no capitals)
- [ ] Jekyll raises a visible conflict warning (and ideally fails the build) when two content files resolve to the same output URL
- [ ] A new content item cannot be saved with a slug that duplicates an existing item in the same collection
- [ ] When a slug must change after publication, a redirect from the old URL to the new URL is added to the repository

## Notes

The immediate fix applied on 2026-07-23 was to improve the CMS hint text and fix the broken slug on `chia-conference-shaping-the-future-of-ai.md`. The longer-term fix — auto-generating slugs from titles to eliminate manual entry — is desirable but requires a migration plan and is tracked in the Decap CMS config improvements backlog task.

## References

- **Related Tenets**: slugs-are-permanent, two-interfaces-one-truth
- **Fix commit**: 082c321 (slug collision fix), b623ef0 (CMS hint text)
- **Historical**: "Fixing some names and slugs" batch campaigns, "slug script triggered" commit

## Progress Updates

### 2026-07-23
Requirement created. Immediate improvements applied to CMS hint text. Slug collision fixed. Auto-generation from title identified as longer-term improvement.
