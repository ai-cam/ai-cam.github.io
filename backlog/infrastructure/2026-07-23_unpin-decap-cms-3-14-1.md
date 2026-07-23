---
id: "2026-07-23_unpin-decap-cms-3-14-1"
title: "Unpin Decap CMS from 3.14.1 once 3.15.x JSX bug is fixed"
status: "Proposed"
priority: "Medium"
created: "2026-07-23"
last_updated: "2026-07-23"
category: "infrastructure"
related_cips: []
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- decap-cms
- dependencies
---

# Task: Unpin Decap CMS from 3.14.1

- **GitHub Issue**: [#29](https://github.com/ai-cam/ai-cam.github.io/issues/29)

## Description

`admin/index.html` is pinned to `decap-cms@3.14.1`. Decap CMS 3.15.0
(released 2026-07-23) introduced a React JSX runtime migration
([PR #7876](https://github.com/decaporg/decap-cms/pull/7876)) that broke the
bundled CDN build, causing React error #130 for anyone opening `/admin/`.
The pin prevents the CMS from auto-upgrading to the broken version.

## Acceptance Criteria

- [ ] Decap CMS has shipped a release that confirms the JSX runtime regression
      is fixed (check [releases](https://github.com/decaporg/decap-cms/releases))
- [ ] `admin/index.html` script tag updated back to `@^3.0.0` (or pinned to
      the fixed version if a further risk is identified)
- [ ] The inline comment in `admin/index.html` referencing this task is removed
- [ ] GitHub issue #29 is closed

## Implementation Notes

File to change: `admin/index.html`

```html
<!-- change this -->
<script src="https://unpkg.com/decap-cms@3.14.1/dist/decap-cms.js"></script>

<!-- back to floating range -->
<script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
```

## Progress Updates

### 2026-07-23
Pinned to 3.14.1 after 3.15.0 broke the CMS. Task created to track the unpin.
