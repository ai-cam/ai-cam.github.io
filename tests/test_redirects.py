#!/usr/bin/env python3
"""
Redirect smoke test for CIP-0001.

Reads every redirect_from entry from content files and verifies that the URL
is reachable on the live site.  jekyll-redirect-from generates HTML pages with
a <meta http-equiv="refresh"> tag (HTTP 200, not 301), so the test accepts 200
and optionally checks that the refresh destination points at the expected page.

Usage:
  python tests/test_redirects.py
  python tests/test_redirects.py --base-url https://www.ai.cam.ac.uk
  python tests/test_redirects.py --check-destination   # also parse meta-refresh
  python tests/test_redirects.py --timeout 10
"""

import argparse
import html.parser
import os
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlsplit, urlunsplit, quote

DEFAULT_BASE_URL = "https://www.ai.cam.ac.uk"

COLLECTION_PREFIX = {
    "_blog_posts":   "/blog",
    "_calls":        "/calls",
    "_events":       "/events",
    "_news":         "/news",
    "_people":       "/people",
    "_policies":     "/policies",
    "_projects":     "/projects",
    "_reports":      "/reports",
    "_team_members": "/team",
}


# ---------------------------------------------------------------------------
# Frontmatter helpers (no dependency on python-frontmatter)
# ---------------------------------------------------------------------------

def extract_frontmatter_block(content: str) -> str:
    """Return the raw YAML between the first two --- delimiters, or ''."""
    m = re.match(r'^---\n(.*?)^---\n', content, re.DOTALL | re.MULTILINE)
    return m.group(1) if m else ""


def extract_redirect_from(fm: str) -> list[str]:
    """Return all URLs listed under redirect_from: in the frontmatter block."""
    # Match the redirect_from block (key on its own line, items on next lines)
    block_m = re.search(r'^redirect_from:\s*\n((?:[ \t]+-[ \t]*.+\n?)+)', fm, re.MULTILINE)
    if not block_m:
        return []
    items = re.findall(r'[ \t]+-[ \t]*(.+)', block_m.group(1))
    return [item.strip().strip('"\'') for item in items]


def extract_slug(fm: str) -> str | None:
    m = re.search(r'^slug:\s*(.+)', fm, re.MULTILINE)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# Collect all redirect entries from the repo
# ---------------------------------------------------------------------------

def collect_redirects(repo_root: str) -> list[dict]:
    """Return list of {file, redirect_url, page_slug, collection_prefix}."""
    entries = []
    for coll, prefix in COLLECTION_PREFIX.items():
        coll_dir = os.path.join(repo_root, coll)
        if not os.path.isdir(coll_dir):
            continue
        for fname in sorted(os.listdir(coll_dir)):
            if not fname.endswith(".md") or fname.startswith(".") or fname.startswith("#"):
                continue
            fpath = os.path.join(coll_dir, fname)
            try:
                with open(fpath, encoding="utf-8") as f:
                    content = f.read()
            except OSError:
                continue
            fm = extract_frontmatter_block(content)
            redirects = extract_redirect_from(fm)
            if not redirects:
                continue
            slug = extract_slug(fm)
            for redir_url in redirects:
                entries.append({
                    "file": os.path.relpath(fpath, repo_root),
                    "redirect_url": redir_url,        # what redirect_from lists
                    "slug": slug,
                    "prefix": prefix,
                })
    return entries


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def encode_url(url: str) -> str:
    parts = urlsplit(url)
    encoded_path = quote(parts.path, safe="/-_.")
    return urlunsplit((parts.scheme, parts.netloc, encoded_path, parts.query, parts.fragment))


def fetch(url: str, timeout: int) -> tuple[int, str, bytes]:
    """Return (status, final_url, body_bytes).  Does not raise on 4xx/5xx."""
    safe_url = encode_url(url)
    try:
        resp = urllib.request.urlopen(safe_url, timeout=timeout)
        return resp.status, resp.url, resp.read(4096)
    except urllib.error.HTTPError as exc:
        return exc.code, safe_url, b""
    except Exception as exc:
        return 0, str(exc), b""


class MetaRefreshParser(html.parser.HTMLParser):
    """Extract the URL from <meta http-equiv="refresh" content="0; url=...">."""

    def __init__(self):
        super().__init__()
        self.destination: str | None = None

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        attrs_d = dict(attrs)
        if attrs_d.get("http-equiv", "").lower() != "refresh":
            return
        content = attrs_d.get("content", "")
        m = re.search(r'url=(.+)', content, re.IGNORECASE)
        if m:
            self.destination = m.group(1).strip().strip("'\"")


def parse_meta_refresh(body: bytes, base_url: str) -> str | None:
    parser = MetaRefreshParser()
    try:
        parser.feed(body.decode("utf-8", errors="replace"))
    except Exception:
        return None
    if parser.destination:
        return urljoin(base_url, parser.destination)
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help=f"Live site base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--check-destination", action="store_true",
                        help="Parse meta-refresh and verify it points to the right page")
    parser.add_argument("--timeout", type=int, default=15,
                        help="HTTP timeout in seconds (default: 15)")
    parser.add_argument("--repo", default=None,
                        help="Path to repo root (default: two levels up from this script)")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    repo_root = args.repo or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    entries = collect_redirects(repo_root)
    if not entries:
        print("No redirect_from entries found.")
        return 0

    print(f"Checking {len(entries)} redirect_from entries against {base}")
    if args.check_destination:
        print("Mode: check that meta-refresh destination matches expected page URL")
    print("=" * 70)

    failures = []
    skipped = 0

    for entry in entries:
        redir_path = entry["redirect_url"]
        full_url = base + redir_path

        status, final_url, body = fetch(full_url, args.timeout)

        # A redirect_from entry that equals the page's current slug URL is a
        # no-op right now (the plugin ignores it to avoid self-loops).  It will
        # only become active after the slug field is removed in a later
        # migration step.  Skip it to avoid noise.
        if entry["slug"]:
            slug_clean = re.sub(r"[^\w\s-]", "", str(entry["slug"]).lower().strip())
            slug_clean = re.sub(r"\s+", "-", slug_clean).strip("-")
            current_path = f"{entry['prefix']}/{slug_clean}/"
            if redir_path.rstrip("/") == current_path.rstrip("/"):
                print(f"  ⏭  (future) {redir_path}  — active after slug removal")
                skipped += 1
                continue

        ok = status == 200
        icon = "✅" if ok else "❌"
        print(f"{icon} [{status}] {redir_path}  ({entry['file']})")

        if not ok:
            failures.append({
                "check": "redirect page reachable",
                "url": full_url,
                "status": status,
                "file": entry["file"],
            })
            continue

        if args.check_destination and body:
            destination = parse_meta_refresh(body, final_url)
            if destination:
                # Expected: page's slug URL
                slug = entry["slug"]
                if slug:
                    slug_clean = re.sub(r"[^\w\s-]", "", str(slug).lower().strip())
                    slug_clean = re.sub(r"\s+", "-", slug_clean).strip("-")
                    expected_path = f"{entry['prefix']}/{slug_clean}/"
                    dest_ok = destination.rstrip("/").endswith(expected_path.rstrip("/"))
                    d_icon = "  ✅" if dest_ok else "  ❌"
                    print(f"{d_icon}  → {destination}")
                    if not dest_ok:
                        failures.append({
                            "check": "meta-refresh destination",
                            "url": full_url,
                            "destination": destination,
                            "expected": base + expected_path,
                            "file": entry["file"],
                        })
            else:
                print(f"  ⚠️  no meta-refresh found — may be the live page itself")

    print("=" * 70)
    if skipped:
        print(f"\n⏭  {skipped} future redirect(s) skipped (active only after slug field is removed)")

    if failures:
        print(f"\n❌  {len(failures)} check(s) failed:\n")
        for f in failures:
            print(f"  {f['check']:30s} {f['url']}")
            if "destination" in f:
                print(f"    → got {f['destination']}")
                print(f"    → expected {f['expected']}")
            else:
                print(f"    → HTTP {f['status']}")
        return 1

    active = len(entries) - skipped
    print(f"\n✅  All {active} active redirect(s) reachable." +
          (f"  ({skipped} future redirect(s) pending slug removal.)" if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
