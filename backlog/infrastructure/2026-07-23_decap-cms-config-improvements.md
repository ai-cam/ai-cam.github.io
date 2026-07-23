---
id: "2026-07-23_decap-cms-config-improvements"
title: "Decap CMS config — medium-priority UX improvements"
status: "Proposed"
priority: "Medium"
created: "2026-07-23"
last_updated: "2026-07-23"
category: "infrastructure"
related_cips: []
owner: ""
dependencies: []
tags:
- backlog
- decap-cms
- ux
---

# Task: Decap CMS config — medium-priority improvements

## Description

A review of `admin/config.yml` identified several improvements that would make
the CMS more usable for editors and reduce the risk of content errors. The
quick-win bugs (broken slug templates, `related_title` required) were fixed on
2026-07-23. This task tracks the remaining medium-priority work.

## Acceptance Criteria

- [ ] `preview_path` added to folder collections (Events, News, Reports, Policies,
      Blog Posts, Projects, Team Members, People) so editors can click through
      to the live page before publishing
- [ ] `summary` templates updated to include dates, e.g. `"{{title}} — {{event_date}}"` for Events and `"{{title}} — {{date}}"` for News, so list views are easier to navigate
- [ ] `abstract` field in Reports changed from `widget: "text"` to
      `widget: "markdown"` to match how it is actually used in existing content
- [ ] Field order in Events improved: `event_date`, `event_end_date`, `time`,
      `location`, and `organizers` moved above `event_content` so editors do
      not have to scroll past the markdown editor to set basic metadata
- [ ] Redundant `multiple: false` removed from all `relation` widgets (~20
      occurrences) to reduce config noise

## Implementation Notes

All changes are confined to `admin/config.yml`. No Jekyll templates or existing
content files are affected.

The larger change — auto-generating slugs from titles to eliminate the class of
URL conflict fixed on 2026-07-23 — would require a migration plan for existing
content and is tracked separately if pursued.

## Related

- Fix commit: `082c321` (slug conflict on chia-conference event)
- Bug fix commit: applied 2026-07-23 (broken slug templates, `related_title`)

## Progress Updates

### 2026-07-23
Task created following a config review. Quick-win bugs already fixed.
