#!/usr/bin/env python3
"""
CIP-0001 URL smoke test.

Two modes:

  baseline  (default)
    For every real slug/title mismatch, verify the *current live URL* (derived
    from the slug field) returns HTTP 200. Run this now to capture the pre-
    migration baseline.

  post-redirect
    After redirect_from entries have been added and the site rebuilt, run with
    --post-redirect to additionally verify that the *title-derived URL* returns
    200 or redirects (301/302) to the slug URL.

Usage:
  python tests/test_slug_urls.py
  python tests/test_slug_urls.py --base-url https://www.ai.cam.ac.uk
  python tests/test_slug_urls.py --base-url https://www.ai.cam.ac.uk --post-redirect
  python tests/test_slug_urls.py --base-url https://www.ai.cam.ac.uk --timeout 10
"""

import argparse
import os
import re
import sys
import urllib.request
import urllib.error

try:
    import frontmatter
except ImportError:
    print("Install python-frontmatter: pip install python-frontmatter")
    sys.exit(1)

DEFAULT_BASE_URL = "https://www.ai.cam.ac.uk"

# Collection directory → URL prefix (mirrors _config.yml permalink settings)
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

COLLECTIONS = list(COLLECTION_PREFIX.keys())

# ---------------------------------------------------------------------------
# Slug helpers (mirrors Jekyll's default slugify filter)
# ---------------------------------------------------------------------------

def jekyll_slugify(s: str) -> str:
    s = str(s).lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def live_url_path(prefix: str, slug: str) -> str:
    """Return the full URL path: collection prefix + slug."""
    return prefix + "/" + str(slug).strip("/") + "/"


# ---------------------------------------------------------------------------
# Collect mismatches from the repo
# ---------------------------------------------------------------------------

def collect_mismatches(repo_root: str) -> list[dict]:
    mismatches = []
    for collection in COLLECTIONS:
        prefix = COLLECTION_PREFIX[collection]
        coll_dir = os.path.join(repo_root, collection)
        if not os.path.isdir(coll_dir):
            continue
        for fname in sorted(os.listdir(coll_dir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(coll_dir, fname)
            try:
                post = frontmatter.load(fpath)
            except Exception:
                continue
            actual = post.get("slug")
            title = post.get("title")
            if not actual or not title:
                continue
            actual_slug = jekyll_slugify(actual)
            expected_slug = jekyll_slugify(title)
            if actual_slug != expected_slug:
                mismatches.append(
                    {
                        "file": os.path.relpath(fpath, repo_root),
                        "slug": str(actual).strip(),
                        "slug_url": live_url_path(prefix, actual),
                        "title": title,
                        "title_url": prefix + "/" + expected_slug + "/",
                    }
                )
    return mismatches


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def encode_url(url: str) -> str:
    """Percent-encode non-ASCII and space characters in the URL path."""
    from urllib.parse import urlsplit, urlunsplit, quote
    parts = urlsplit(url)
    encoded_path = quote(parts.path, safe="/-_.")
    return urlunsplit((parts.scheme, parts.netloc, encoded_path, parts.query, parts.fragment))


def fetch_status(url: str, timeout: int, follow_redirects: bool = True) -> tuple[int, str]:
    """Return (final_status_code, final_url).  Does NOT raise on 4xx/5xx."""
    safe_url = encode_url(url)
    try:
        if follow_redirects:
            req = urllib.request.urlopen(safe_url, timeout=timeout)
            return req.status, req.url
        else:
            import http.client
            from urllib.parse import urlparse
            parsed = urlparse(safe_url)
            conn = http.client.HTTPSConnection(parsed.netloc, timeout=timeout)
            conn.request("HEAD", parsed.path or "/")
            resp = conn.getresponse()
            location = resp.getheader("Location", "")
            conn.close()
            return resp.status, location
    except urllib.error.HTTPError as exc:
        return exc.code, safe_url
    except Exception as exc:
        return 0, str(exc)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help=f"Live site base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--post-redirect", action="store_true",
                        help="Also verify title-derived URLs redirect correctly")
    parser.add_argument("--timeout", type=int, default=15,
                        help="HTTP timeout in seconds (default: 15)")
    parser.add_argument("--repo", default=None,
                        help="Path to repo root (default: parent of this script's directory)")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    repo_root = args.repo or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    mismatches = collect_mismatches(repo_root)
    if not mismatches:
        print("No slug/title mismatches found — nothing to test.")
        return 0

    print(f"Testing {len(mismatches)} real mismatch URLs against {base}")
    print(f"Mode: {'post-redirect' if args.post_redirect else 'baseline'}")
    print("=" * 70)

    failures = []

    for item in mismatches:
        slug_url = base + item["slug_url"]
        status, final_url = fetch_status(slug_url, args.timeout)
        ok = status == 200
        icon = "✅" if ok else "❌"
        print(f"{icon} [{status}] {item['slug_url']}  ({item['file']})")
        if not ok:
            failures.append(
                {"check": "slug URL (baseline)", "url": slug_url, "status": status,
                 "file": item["file"]}
            )

        if args.post_redirect:
            title_url = base + item["title_url"]
            # Don't follow redirects — we want to see the 301/302
            redir_status, location = fetch_status(title_url, args.timeout, follow_redirects=False)
            # Accept 200 (already at slug URL) or 3xx to the slug URL
            redir_ok = redir_status == 200 or (
                300 <= redir_status < 400
                and item["slug_url"].rstrip("/") in location.rstrip("/")
            )
            r_icon = "✅" if redir_ok else "❌"
            print(f"  {r_icon} [{redir_status}] redirect {item['title_url']} → {location or '(none)'}")
            if not redir_ok:
                failures.append(
                    {"check": "title redirect", "url": title_url, "status": redir_status,
                     "location": location, "expected": item["slug_url"], "file": item["file"]}
                )

    print("=" * 70)
    if failures:
        print(f"\n❌  {len(failures)} check(s) failed:\n")
        for f in failures:
            print(f"  {f['check']:25s} {f['url']}")
            if "location" in f:
                print(f"    → got {f['status']} to {f['location'] or '(none)'}, "
                      f"expected 3xx to {f['expected']}")
            else:
                print(f"    → HTTP {f['status']}")
        return 1
    else:
        total = len(mismatches) * (2 if args.post_redirect else 1)
        print(f"\n✅  All {total} check(s) passed.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
