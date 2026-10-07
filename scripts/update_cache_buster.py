#!/usr/bin/env python3
"""
Automated Cache Buster for Rusdi's GitHub Profile README.
Updates all `./dist/*.svg` image references in README.md and README.id.md
with a fresh timestamp query string (?v=<unix_epoch>).

Why this is needed:
GitHub uses aggressive CDN edge caching (Fastly & Camo) with a default
time-to-live. By appending a unique timestamp whenever profile art is generated,
all CDN edge nodes and visitor browsers are guaranteed to fetch the latest
real-time SVGs immediately on every commit.
"""
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(HERE, "..")

FILES_TO_UPDATE = [
    os.path.join(ROOT_DIR, "README.md"),
    os.path.join(ROOT_DIR, "README.id.md"),
]

# Pattern matching any ./dist/filename.svg with or without existing query params
PATTERN = re.compile(r'(\./dist/[a-zA-Z0-9_\-]+\.svg)(?:\?[^"\'\s>]*)?')


def update_file(filepath, timestamp):
    if not os.path.exists(filepath):
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, count = PATTERN.subn(rf"\1?v={timestamp}", content)

    if count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {count} image URLs in {os.path.basename(filepath)} with ?v={timestamp}")
    else:
        print(f"No matching image URLs found in {os.path.basename(filepath)}")

    return count


def main():
    # Use specified timestamp or current unix epoch seconds
    ts = sys.argv[1] if len(sys.argv) > 1 else str(int(time.time()))
    total = sum(update_file(f, ts) for f in FILES_TO_UPDATE)
    print(f"Cache buster finished: {total} total image tags updated.")


if __name__ == "__main__":
    main()
