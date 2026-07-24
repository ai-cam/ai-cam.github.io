#!/usr/bin/env python3
"""
CIP-0001 audit script: compare frontmatter slug against title | slugify
across all content collections.

Reports:
  - MATCH         : slug == slugify(title) — safe to migrate
  - MALFORMED     : slug contains title text (spaces/caps) but slugify(slug) ==
                    slugify(title) — URL is the same, just needs field cleanup
  - REAL MISMATCH : slugify(slug) != slugify(title) — URL genuinely differs,
                    needs a redirect_from entry before migration
  - NO SLUG       : no slug field — already title-derived or missing
  - NO TITLE      : no title field — cannot compute expected slug
"""
import os
import re
import sys

try:
    import frontmatter
except ImportError:
    print("Install python-frontmatter: pip install python-frontmatter")
    sys.exit(1)

# Collection directory → URL prefix (from _config.yml permalink settings)
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

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jekyll_slugify(s):
    """Replicate Jekyll's default slugify filter."""
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)   # remove non-word/non-space/non-hyphen
    s = re.sub(r"\s+", "-", s)        # spaces → hyphens
    s = re.sub(r"-{2,}", "-", s)      # collapse multiple hyphens
    s = s.strip("-")
    return s


def audit():
    results = {"match": [], "malformed": [], "mismatch": [], "no_slug": [], "no_title": []}

    for collection in COLLECTIONS:
        prefix = COLLECTION_PREFIX[collection]
        coll_dir = os.path.join(REPO_ROOT, collection)
        if not os.path.isdir(coll_dir):
            continue

        for fname in sorted(os.listdir(coll_dir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(coll_dir, fname)
            try:
                post = frontmatter.load(fpath)
            except Exception as e:
                print(f"  PARSE ERROR: {fpath}: {e}")
                continue

            slug = post.get("slug")
            title = post.get("title")
            rel = os.path.relpath(fpath, REPO_ROOT)

            if not title:
                results["no_title"].append(rel)
                continue
            if not slug:
                results["no_slug"].append((rel, title))
                continue

            expected = jekyll_slugify(str(title))
            actual = str(slug).strip()

            if actual == expected:
                results["match"].append(rel)
            elif jekyll_slugify(actual) == expected:
                # slug contains title text (spaces/caps) but resolves to same URL
                results["malformed"].append((rel, actual, expected, prefix))
            else:
                results["mismatch"].append((rel, actual, expected, prefix))

    return results


def main():
    results = audit()

    print(f"\n{'='*70}")
    print(f"  CIP-0001 Slug Audit")
    print(f"{'='*70}\n")

    print(f"✅  MATCH ({len(results['match'])}) — slug equals title | slugify, safe to migrate")
    print(f"🔧  MALFORMED ({len(results['malformed'])}) — slug has wrong format but URL is unchanged, just needs cleanup")
    print(f"🚨  REAL MISMATCH ({len(results['mismatch'])}) — URL differs, needs redirect_from before migration")
    print(f"❓  NO SLUG ({len(results['no_slug'])}) — no slug field present")
    print(f"❌  NO TITLE ({len(results['no_title'])}) — cannot compute expected slug\n")

    safe_to_migrate = len(results["match"]) + len(results["malformed"])
    print(f"  → {safe_to_migrate} files need no redirect (safe to migrate)")
    print(f"  → {len(results['mismatch'])} files need a redirect_from entry first\n")

    if results["mismatch"]:
        print(f"{'─'*70}")
        print("REAL MISMATCHES (each needs redirect_from before migration):\n")
        for path, actual, expected, prefix in sorted(results["mismatch"]):
            print(f"  {path}")
            print(f"    live URL     : {prefix}/{actual}/")
            print(f"    title-derived: {prefix}/{expected}/")
            print()

    if results["malformed"]:
        print(f"{'─'*70}")
        print("MALFORMED slugs (URL unchanged — just clean up the field value):\n")
        for path, actual, expected, prefix in sorted(results["malformed"]):
            print(f"  {path}")
            print(f"    slug field   : '{actual}'")
            print(f"    should be    : '{expected}'")

    if results["no_slug"]:
        print(f"{'─'*70}")
        print("NO SLUG FIELD (review manually):\n")
        for path, title in results["no_slug"]:
            print(f"  {path}  (title: {title})")

    if results["no_title"]:
        print(f"{'─'*70}")
        print("NO TITLE FIELD (review manually):\n")
        for path in results["no_title"]:
            print(f"  {path}")

    print(f"\n{'─'*70}")
    total = sum(len(v) for v in results.values())
    print(f"Total files audited: {total}")
    print(f"Migration effort:")
    print(f"  {len(results['mismatch'])} redirect_from entries to add (real URL changes)")
    print(f"  {len(results['malformed'])} slug field values to clean up (no URL change)")
    print(f"  1 template to update (_layouts/events-category.html)\n")

    # Also scan templates for page.slug references
    print(f"{'─'*70}")
    print("Templates referencing page.slug (will need updating):\n")
    template_dirs = ["_layouts", "_includes"]
    slug_refs = []
    for d in template_dirs:
        dpath = os.path.join(REPO_ROOT, d)
        if not os.path.isdir(dpath):
            continue
        for root, _, files in os.walk(dpath):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    content = open(fp).read()
                except Exception:
                    continue
                if "page.slug" in content or "post.slug" in content:
                    lines = [i+1 for i, l in enumerate(content.splitlines())
                             if "page.slug" in l or "post.slug" in l]
                    slug_refs.append((os.path.relpath(fp, REPO_ROOT), lines))

    if slug_refs:
        for path, lines in slug_refs:
            print(f"  {path}  (lines: {lines})")
    else:
        print("  None found — templates don't reference page.slug directly")

    print()


if __name__ == "__main__":
    main()
