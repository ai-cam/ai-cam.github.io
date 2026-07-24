---
id: "2026-07-24_cip0001-post-deploy-monitoring"
title: "CIP-0001 post-deploy monitoring — two-week sign-off"
status: "In Progress"
priority: "Medium"
created: "2026-07-24"
last_updated: "2026-07-24"
category: "infrastructure"
related_cips: ["0001"]
owner: "comms lead"
dependencies: []
tags:
- backlog
- monitoring
- redirects
- slugs
due: "2026-08-07"
---

# Task: CIP-0001 post-deploy monitoring — two-week sign-off

## Description

CIP-0001 (auto-generate slugs from titles) has been implemented and deployed.
The final step is a two-week passive monitoring period to catch any unexpected
404s or broken redirects that did not surface during testing.

The automated `Redirect Health Monitor` GitHub Actions workflow runs every
Monday and Thursday at 07:00 UTC and opens a GitHub issue automatically if
any redirect returns a non-200 status. No manual action is needed unless the
workflow fails.

The sign-off checkpoint below is a human review, not a technical task.

## Acceptance Criteria

- [ ] No GitHub issues labelled `redirect-monitor` are open two weeks after
      deploy (by 2026-08-07).
- [ ] Google Search Console shows no spike in 404 coverage errors for the
      `/blog/`, `/news/`, `/events/`, `/reports/`, `/calls/`, `/policies/`,
      `/projects/`, or `/people/` URL prefixes.
- [ ] The `Redirect Health Monitor` workflow has run at least twice and passed.
- [ ] CIP-0001 status updated to `Implemented` once the above criteria are met.

## How to check Search Console

1. Go to [Google Search Console](https://search.google.com/search-console) and
   select the `ai.cam.ac.uk` property.
2. Open **Indexing → Pages** and filter by "Not found (404)".
3. Compare the 404 count to the baseline from before 2026-07-24. Any new 404s
   that match content URLs should be investigated.

## How to run the redirect test manually

```bash
python3 tests/test_redirects.py --base-url https://www.ai.cam.ac.uk
```

## Implementation Notes

Automated monitoring is handled by
`.github/workflows/redirect-monitor.yml`, which:
- Runs every Monday and Thursday at 07:00 UTC
- Opens a `redirect-monitor` labelled GitHub issue on failure (de-duplicated)
- Can be triggered manually from the Actions tab

## Related

- CIP: 0001
- Backlog: `2026-07-24_fix-data-swap-events-people` (editorial fixes still pending)
- Workflow: `.github/workflows/redirect-monitor.yml`

## Progress Updates

### 2026-07-24

CIP-0001 implementation complete. Monitoring window opens now.
Two-week deadline: 2026-08-07.
