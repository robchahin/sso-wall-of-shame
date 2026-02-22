"""
Check that all pricing_source URLs in vendor YAML files return a successful
HTTP response. Exits 0 if all links are OK, 1 if any are dead or unreachable.

Usage:
    python scripts/check_links.py [_vendors/]
"""

import glob
import os
import sys
import time
import yaml
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


USER_AGENT = "sso.tax/linkchecker (+https://github.com/robchahin/sso-wall-of-shame)"
TIMEOUT = 15


def check_url(url):
    """
    Returns (http_status_or_None, error_string_or_None).
    Tries HEAD first; falls back to GET if the server returns 405.
    Follows redirects automatically.
    """
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, method=method, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=TIMEOUT) as resp:
                return resp.status, None
        except HTTPError as e:
            if method == "HEAD" and e.code == 405:
                continue  # server doesn't allow HEAD, retry with GET
            return e.code, None
        except URLError as e:
            return None, str(e.reason)
        except Exception as e:
            return None, str(e)
    return None, "All methods failed"


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
    search_paths = sys.argv[1:] if len(sys.argv) > 1 else ["_vendors"]
    vendor_files = collect_vendor_files(search_paths)

    if not vendor_files:
        print("No vendor files found.")
        sys.exit(0)

    dead = []
    total_urls = 0

    for path in vendor_files:
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
        except Exception:
            continue

        if not data:
            continue

        name = data.get("name", os.path.basename(path))
        sources = data.get("pricing_source", [])
        if isinstance(sources, str):
            sources = [sources]

        for url in sources:
            if not isinstance(url, str) or not url.startswith("http"):
                continue

            total_urls += 1
            status, error = check_url(url)

            is_dead = (status is not None and status >= 400) or status is None
            if is_dead:
                reason = str(status) if status else f"connection error: {error}"
                dead.append((name, url, reason))
                print(f"  DEAD  {name}: {url} ({reason})")
            else:
                print(f"  OK    {name}: {url} ({status})")

            time.sleep(0.3)  # gentle rate limiting

    print(f"\nChecked {total_urls} URL(s) across {len(vendor_files)} vendor file(s).")
    if dead:
        print(f"{len(dead)} dead link(s) found.")
        sys.exit(1)
    else:
        print("All links OK.")
        sys.exit(0)


if __name__ == "__main__":
    main()
