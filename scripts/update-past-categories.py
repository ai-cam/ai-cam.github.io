#!/usr/bin/env python3
"""
Scans _events/ and _calls/ markdown files, checks date fields against today,
and updates the category frontmatter to "Past" when the date has passed.

Uses only Python standard library — no external dependencies required.
"""

import os
import re
import sys
from datetime import date, datetime

EVENTS_DIR = "_events"
CALLS_DIR = "_calls"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_date(value):
    """Parse a YYYY-MM-DD date string (with optional time) into a date object."""
    if not value:
        return None
    value = value.strip().strip('"').strip("'")
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value[:19], fmt).date()
        except ValueError:
            continue
    return None


def extract_field(frontmatter_text, field_name):
    """Extract a single scalar field value from raw YAML frontmatter text."""
    pattern = re.compile(rf"^{re.escape(field_name)}\s*:\s*(.+)$", re.MULTILINE)
    match = pattern.search(frontmatter_text)
    if match:
        val = match.group(1).strip().strip('"').strip("'")
        return val if val else None
    return None


def replace_field(frontmatter_text, field_name, old_value, new_value):
    """Replace a field value in raw frontmatter text, preserving formatting."""
    pattern = re.compile(
        rf"^({re.escape(field_name)}\s*:\s*){re.escape(old_value)}(\s*)$",
        re.MULTILINE,
    )
    return pattern.sub(rf"\g<1>{new_value}\2", frontmatter_text)


def process_events(today):
    """Process all event files and return count of updated files."""
    if not os.path.isdir(EVENTS_DIR):
        print(f"  Directory not found: {EVENTS_DIR}")
        return 0

    updated = 0
    for filename in sorted(os.listdir(EVENTS_DIR)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(EVENTS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm_match = FRONTMATTER_RE.match(content)
        if not fm_match:
            continue

        fm_text = fm_match.group(1)
        category = extract_field(fm_text, "event_categories")

        if category != "Upcoming Events":
            continue

        end_date = parse_date(extract_field(fm_text, "event_end_date"))
        event_date = parse_date(extract_field(fm_text, "event_date"))
        check_date = end_date or event_date

        if check_date is None:
            continue

        if check_date < today:
            new_fm = replace_field(fm_text, "event_categories", "Upcoming Events", "Past Events")
            new_content = content[: fm_match.start(1)] + new_fm + content[fm_match.end(1) :]

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

            updated += 1
            print(f"  Updated: {filepath} (date: {check_date})")

    return updated


def process_calls(today):
    """Process all call files and return count of updated files."""
    if not os.path.isdir(CALLS_DIR):
        print(f"  Directory not found: {CALLS_DIR}")
        return 0

    updated = 0
    for filename in sorted(os.listdir(CALLS_DIR)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(CALLS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm_match = FRONTMATTER_RE.match(content)
        if not fm_match:
            continue

        fm_text = fm_match.group(1)
        category = extract_field(fm_text, "call_categories")

        if category != "Open Calls":
            continue

        deadline = parse_date(extract_field(fm_text, "application_deadline"))
        call_date = parse_date(extract_field(fm_text, "call_date"))
        check_date = deadline or call_date

        if check_date is None:
            continue

        if check_date < today:
            new_fm = replace_field(fm_text, "call_categories", "Open Calls", "Past Calls")
            new_content = content[: fm_match.start(1)] + new_fm + content[fm_match.end(1) :]

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

            updated += 1
            print(f"  Updated: {filepath} (date: {check_date})")

    return updated


def main():
    today = date.today()
    print(f"Auto-update past categories - {today}")
    print()

    print("Processing events...")
    events_updated = process_events(today)
    print(f"  Events updated: {events_updated}")
    print()

    print("Processing calls...")
    calls_updated = process_calls(today)
    print(f"  Calls updated: {calls_updated}")
    print()

    total = events_updated + calls_updated
    print(f"Total updated: {total}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
