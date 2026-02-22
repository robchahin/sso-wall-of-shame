"""
List vendor files whose updated_at date is older than a given threshold.
Exits 0 always. Prints stale vendors to stdout.

Usage:
    python scripts/find_stale_vendors.py [--days N] [_vendors/]

Default threshold: 730 days (2 years).
"""

import argparse
import glob
import os
import sys
from datetime import date, timedelta

import yaml


def collect_vendor_files(paths):
    files = []
    for path in paths:
        if os.path.isfile(path) and path.endswith((".yaml", ".yml")):
            files.append(path)
        elif os.path.isdir(path):
            files.extend(sorted(glob.glob(os.path.join(path, "*.yaml"))))
            files.extend(sorted(glob.glob(os.path.join(path, "*.yml"))))
    return files


def main():
    parser = argparse.ArgumentParser(description="Find stale vendor entries.")
    parser.add_argument("paths", nargs="*", default=["_vendors"], help="Vendor files or directories.")
    parser.add_argument("--days", type=int, default=730, help="Staleness threshold in days (default: 730).")
    args = parser.parse_args()

    cutoff = date.today() - timedelta(days=args.days)
    vendor_files = collect_vendor_files(args.paths)

    stale = []

    for path in vendor_files:
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
        except Exception:
            continue

        if not data:
            continue

        updated_at = data.get("updated_at")
        if not updated_at:
            continue

        try:
            updated_date = date.fromisoformat(str(updated_at))
        except ValueError:
            continue

        if updated_date < cutoff:
            name = data.get("name", os.path.basename(path))
            stale.append((updated_date, name, path))

    stale.sort()  # oldest first

    if stale:
        print(f"Found {len(stale)} vendor(s) not updated since {cutoff} ({args.days} days ago):\n")
        for updated_date, name, path in stale:
            print(f"  {updated_date}  {name}  ({os.path.basename(path)})")
    else:
        print(f"No vendors older than {args.days} days. All up to date.")

    sys.exit(0)


if __name__ == "__main__":
    main()
