---
id: "pin-and-track"
title: "Pin dependencies, track upgrades deliberately"
status: "Active"
created: "2026-07-23"
last_reviewed: "2026-07-23"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- dependencies
- infrastructure
---

# Pin Dependencies, Track Upgrades Deliberately

## Tenet

**Description**: Third-party dependencies — Decap CMS, Jekyll gems, GitHub Actions — can and do introduce breaking changes. The commit history records three separate occasions where a dependency change broke the site: a Ruby Gemfile constraint, a Liquid syntax incompatibility with GitHub Pages, and Decap CMS 3.15.0 crashing the editor on the day of release. Each required reactive firefighting that interrupted editorial work.

The correct response is not to avoid upgrades — outdated dependencies carry their own risks — but to make upgrades deliberate rather than automatic. Version pins should be explicit, each pin should be documented with the reason it was introduced, and the path to unpinning should be tracked in the backlog. Floating version ranges (`^3.0.0`, `latest`) are convenient until they are not.

**Quote**: *"Convenience ranges are bets against the future. Pin with intent, upgrade with evidence."*

**Examples**:
- `admin/index.html` pinned to `decap-cms@3.14.1` with an inline comment explaining why and linking to the tracking issue
- `backlog/infrastructure/2026-07-23_unpin-decap-cms-3-14-1.md` recording the acceptance criteria for when to unpin
- `Gemfile.lock` committing exact gem versions so Jekyll builds are reproducible

**Counter-examples**:
- Using `decap-cms@^3.0.0` which auto-upgraded to 3.15.0 on the day of its release, crashing the CMS for all editors
- Applying a dependency upgrade without checking whether the CMS editor still functions
- Pinning a version without recording why, leaving future developers unable to judge whether it is still necessary
