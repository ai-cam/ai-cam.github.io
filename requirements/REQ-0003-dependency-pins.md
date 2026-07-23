---
id: "0003"
title: "All site-critical dependencies must be version-pinned with documented upgrade paths"
status: "Proposed"
priority: "Medium"
created: "2026-07-23"
last_updated: "2026-07-23"
related_tenets: ["pin-and-track", "editorial-continuity"]
stakeholders: ["Neil Lawrence", "Elinor Pegler"]
tags:
- requirements
- dependencies
- infrastructure
---

# REQ-0003: All site-critical dependencies must be version-pinned with documented upgrade paths

## Description

Three separate dependency-related outages appear in the commit history: a Ruby Gemfile version constraint, a Liquid syntax incompatibility introduced by a GitHub Pages update, and Decap CMS 3.15.0 crashing the editor on release day. Each required reactive intervention. Floating version ranges (`^3.0.0`, `latest`) trade short-term convenience for unpredictable breakage.

Site-critical dependencies are those whose failure prevents either the site from building or editors from publishing.

**Why this matters**: Tenets `pin-and-track` and `editorial-continuity` — floating ranges are bets against the future; a broken dependency is a broken CMS.

**Who benefits**: Elinor Pegler (no unexpected CMS outages), developers (predictable build environments).

## Acceptance Criteria

- [ ] `admin/index.html` specifies an exact Decap CMS version (not a range)
- [ ] `Gemfile.lock` is committed and kept up to date so Jekyll builds are reproducible
- [ ] Any version pin introduced to resolve an incident is accompanied by a backlog task recording when and how to unpin
- [ ] GitHub Actions workflow files reference pinned versions of actions (e.g., `actions/checkout@v4`, not `actions/checkout@latest`)

## References

- **Related Tenets**: pin-and-track, editorial-continuity
- **Incident**: Decap CMS 3.15.0, 2026-07-23
- **Backlog**: 2026-07-23_unpin-decap-cms-3-14-1

## Progress Updates

### 2026-07-23
Requirement created following the Decap CMS 3.15.0 incident. Decap pinned as immediate fix. GitHub Actions versions not yet audited.
