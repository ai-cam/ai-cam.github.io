#!/usr/bin/env python3
"""
GitHub Branch Ruleset Validation Script

Validates that the expected ruleset rules are active on a branch using the
GitHub REST API. Read-only: this script never modifies repository settings.

Usage:
    python scripts/configure-branch-protection.py [--repo REPO] [--branch BRANCH]

Requirements:
    - GitHub token with repo read access (set via GITHUB_TOKEN env var)
    - requests library
"""

import argparse
import logging
import os
import sys
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Rules we require to be active on main. Add entries here if you later
# enable additional ruleset rules in GitHub Settings → Rules.
REQUIRED_RULES = {
    "deletion": "Restrict deletions",
    "non_fast_forward": "Block force pushes",
}


def get_branch_rules(token: str, repo: str, branch: str) -> list:
    """Return all rules currently active on a branch via the rulesets API."""
    url = f"https://api.github.com/repos/{repo}/rules/branches/{branch}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        logger.error(f"Branch '{branch}' not found in '{repo}'")
        sys.exit(1)
    response.raise_for_status()
    return response.json()


def validate(rules: list) -> bool:
    """Check all required rules are present. Returns True if compliant."""
    active_types = {rule["type"] for rule in rules}
    compliant = True
    for rule_type, description in REQUIRED_RULES.items():
        if rule_type in active_types:
            logger.info(f"  PASS: {description} ({rule_type})")
        else:
            logger.warning(f"  NOT compliant: {description} ({rule_type}) is not configured")
            compliant = False
    return compliant


def main():
    parser = argparse.ArgumentParser(description="Validate GitHub branch ruleset rules")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", "ai-cam/ai-cam.github.io"),
    )
    parser.add_argument("--branch", default="main")
    args = parser.parse_args()

    if not args.token:
        logger.error("GitHub token required. Set GITHUB_TOKEN env var or use --token")
        sys.exit(1)

    logger.info(f"Checking ruleset rules for '{args.branch}' in '{args.repo}'")
    rules = get_branch_rules(args.token, args.repo, args.branch)
    logger.info(f"Found {len(rules)} active rule(s) on '{args.branch}'")

    compliant = validate(rules)
    if compliant:
        logger.info("Branch rules are compliant")
    else:
        logger.warning(
            "Branch rules are NOT compliant — update manually in GitHub Settings → Rules"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
