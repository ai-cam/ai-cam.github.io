---
id: "2026-07-24_fix-data-swap-events-people"
title: "Fix 8 content files where title and slug belong to different items"
status: "Proposed"
priority: "Medium"
created: "2026-07-24"
last_updated: "2026-07-24"
category: "bugs"
related_cips: ["0001"]
owner: "comms lead"
dependencies: []
tags:
- backlog
- content
- slugs
- editorial
---

# Task: Fix data-swapped titles in events and people files

## Description

During the CIP-0001 slug audit, 8 content files were found where the `slug`
field matches the filename (and the current live URL) but the `title` field
contains text that belongs to a completely different content item. These are
almost certainly the result of duplicating an existing file in Decap CMS and
not updating the title before saving.

These files were excluded from the automated `redirect_from` migration
(CIP-0001 step 8) because adding a redirect would map one wrong URL to another
wrong URL. Each file needs a human editorial decision before a redirect can be
added.

The 8 affected files and their current mismatch:

| File | Current slug / live URL | Title found (should not be here) |
|------|------------------------|----------------------------------|
| `_events/ai-for-ops-community-meet-up.md` | `/events/ai-for-ops-community-meet-up/` | AI Sciencepreneurship Bootcamp 2026 |
| `_events/ai-for-science-research-showcase.md` | `/events/ai-for-science-research-showcase/` | Cambridge Social Data School |
| `_events/chia-conference-shaping-the-future-of-ai.md` | `/events/chia-conference-shaping-the-future-of-ai/` | AI for Science Research Showcase |
| `_events/the-bennett-institute-for-public-policy-annual-conference.md` | `/events/the-bennett-institute-for-public-policy-annual-conference/` | AI Needs You: an evening with Verity Harding in conversation with Diane Coyle |
| `_events/training-workshop-llm-hands-on-workshop.md` | `/events/training-workshop-llm-hands-on-workshop/` | AI for Ops Community Meet-Up |
| `_events/workshop-ai-time-politics-and-ideologies-of-the-future.md` | `/events/workshop-ai-time-politics-and-ideologies-of-the-future/` | AI for Ops Community Meet-Up 2026 |
| `_people/department-of-computer-science-and-technology.md` | `/people/department-of-computer-science-and-technology/` | Carl Henrik Ek |
| `_people/mihaela-van-der-schaar-1.md` | `/people/mihaela-van-der-schaar-1/` | Sjors Scheres |

## Acceptance Criteria

- [ ] For each file, open it in Decap CMS and check whether the body content
      matches the slug/filename or the title.
- [ ] If the body matches the slug: correct the title to match the content,
      then check whether a `redirect_from` entry is needed.
- [ ] If the body matches the title: the file may need to be moved/renamed; ask
      for technical help.
- [ ] All 8 files have a title that is consistent with the slug and the body
      content.
- [ ] Re-run `python3 scripts/audit-slugs.py` and confirm there are 0 data
      swaps remaining in the REAL MISMATCH section.

## Implementation Notes

The quickest fix for most of these will be to open the file in Decap CMS,
scroll to the title field, and type the correct title. The slug field is now
auto-generated from the title (since CIP-0001 step 6), so the live URL will
not change until the slug field is explicitly removed.

After correcting a title, re-run the audit to confirm the file moves from
REAL MISMATCH to MATCH or MALFORMED (the latter just needs a format cleanup,
which is also automated).

## Related

- CIP: 0001
- Documentation: `cip/cip0001.md`

## Progress Updates

### 2026-07-24

Task created. All 8 files excluded from the automated CIP-0001 redirect
migration. Awaiting editorial review by the comms lead.
