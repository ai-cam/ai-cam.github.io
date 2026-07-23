---
id: "0001"
title: "The CMS must be available and functional for non-technical editors at all times"
status: "Proposed"
priority: "High"
created: "2026-07-23"
last_updated: "2026-07-23"
related_tenets: ["editorial-continuity", "two-interfaces-one-truth"]
stakeholders: ["Elinor Pegler", "Communications team"]
tags:
- requirements
- cms
- editorial
---

# REQ-0001: The CMS must be available and functional for non-technical editors at all times

## Description

Elinor Pegler (communications lead) and the wider editorial team publish all content through Decap CMS. They cannot use GitHub directly. When the CMS is broken — whether due to a dependency update, a configuration error, or an infrastructure change — they have no fallback and cannot publish. This is the highest-priority failure mode in the repository.

**Why this matters**: Tenet `editorial-continuity` — the website exists to publish content, and 88% of commits in this repository are editorial operations through the CMS.

**Who benefits**: Elinor Pegler, the communications team, and anyone relying on timely publication of events, news, reports, and calls.

## Acceptance Criteria

- [ ] An editor can log in to `/admin/` and create, edit, and publish any content type without developer assistance
- [ ] A CMS outage (any state in which an editor cannot publish) is detected and resolved within one working day
- [ ] Dependency updates to Decap CMS are tested against the live editor before being applied
- [ ] The Decap CMS version is pinned in `admin/index.html` and any change to that pin is recorded in the backlog with a rationale

## Notes

The July 2026 incident (Decap 3.15.0) demonstrated that a floating version range (`^3.0.0`) can cause an immediate outage on the day a new upstream release ships. The acceptance criteria above requires pinning as a structural control.

## References

- **Related Tenets**: editorial-continuity, two-interfaces-one-truth
- **Incident**: Decap CMS 3.15.0 crash, 2026-07-23, GitHub issue #29

## Progress Updates

### 2026-07-23
Requirement created following the 3.15.0 incident. Decap pinned to 3.14.1 as immediate fix. Backlog task created for deliberate unpin when upstream fixes the regression.
