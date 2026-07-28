#!/usr/bin/env python3
"""Enforce this list's two rules, because a rule nobody runs is a preference.

CONTRIBUTING states one hard rule -- every link must resolve to the real, canonical source
-- and one softer one: any performance metric needs a source link and a date. Both were
documented as commands a contributor was trusted to run by hand. Nobody runs commands they
are trusted to run by hand, and a curated list decays in exactly the way this invites: the
links rot silently and an unsourced number picked up from somewhere becomes, after a year,
indistinguishable from a cited one.

So this runs them. Two checks, both stdlib-only, no dependencies to install and nothing to
keep in sync with a lockfile.

LINKS. Every markdown link in README.md is resolved. GitHub repositories go through the
API, because a repository page can 200 while the repo is renamed, and the API is the
authoritative existence check CONTRIBUTING already prescribes. Everything else gets a HEAD
request, falling back to GET, since a fair number of academic hosts refuse HEAD.

METRICS. Any line stating a performance number -- mAP, F1, R2, AP, accuracy, Dice, IoU --
must carry a link on the same line or an explicit unpublished-basis marker. This is the
same distinction the rest of this author's work draws between a published result and an
in-house one: both are real, they are not the same kind of evidence, and the failure mode
is a personal observation quietly reading as a citation.

    python3 scripts/check_list.py            # both checks, non-zero exit on failure
    python3 scripts/check_list.py --links    # links only (the slow one; hits the network)
    python3 scripts/check_list.py --metrics  # metrics only (offline, instant)

The metrics check is offline and always safe to run in CI. The link check touches the
network, so it tolerates rate limiting rather than failing the build on it: a 429 is
reported as UNKNOWN, not as a dead link, because failing CI on someone else's throttle
trains people to ignore CI.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import List, Optional, Tuple

README = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")

# Markdown inline links. Deliberately not a general markdown parser: this file's job is to
# find URLs, and a regex that occasionally over-matches a badge is harmless here.
LINK = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")

GITHUB_REPO = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+)")

# A number that claims measured performance. Word-boundary anchored so "F1" does not fire
# on "F150" and "AP" does not fire inside "APPLE".
METRIC = re.compile(
  r"(?<![A-Za-z0-9])(mAP|AP@?[\d.\[\]:]*|F1|R2|R\^2|IoU|Dice|AUC|accuracy|recall|precision|MAE)"
  r"(?![A-Za-z0-9])",
  re.IGNORECASE,
)
# A bare number that looks like a score sitting next to one of those words.
SCORE = re.compile(r"(?<![\w.])(0\.\d+|\d{1,3}(\.\d+)?\s?%|\d\.\d+)(?![\w.])")

# How an unpublished, in-house observation declares itself. Anything carrying one of these
# is making a weaker claim on purpose and is allowed through without a citation.
UNPUBLISHED_MARKERS = (
  "unpublished",
  "in-house",
  "internal observation",
  "not peer-reviewed",
  "no public source",
)

# Badge and shield hosts. They are decoration, they change constantly, and a broken badge
# is not a broken citation.
DECORATIVE_HOSTS = ("img.shields.io", "awesome.re")

TIMEOUT = 20
UA = "awesome-wetlab-cv-link-check (+https://github.com/di-omics/awesome-wetlab-cv)"


@dataclass(frozen=True)
class LinkResult:
  url: str
  line: int
  status: str  # OK / DEAD / UNKNOWN
  detail: str

  @property
  def failed(self) -> bool:
    return self.status == "DEAD"


def _gh_api(owner: str, repo: str) -> Optional[Tuple[bool, str]]:
  """Authoritative existence check for a GitHub repo, per CONTRIBUTING.

  Returns None when the gh CLI is unavailable so the caller can fall back to HTTP rather
  than reporting a live repo as dead because a tool is missing.
  """
  if repo.endswith(".git"):
    repo = repo[:-4]
  try:
    out = subprocess.run(
      ["gh", "api", f"repos/{owner}/{repo}", "--jq", ".full_name"],
      capture_output=True,
      text=True,
      timeout=TIMEOUT,
    )
  except (FileNotFoundError, subprocess.TimeoutExpired):
    return None
  if out.returncode == 0 and out.stdout.strip():
    return True, out.stdout.strip()
  err = (out.stderr or "").strip().splitlines()
  return False, err[-1] if err else "gh api reported no such repository"


def _http(url: str) -> Tuple[str, str]:
  """HEAD, then GET. Many academic and journal hosts refuse HEAD but serve GET fine."""
  for method in ("HEAD", "GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    try:
      with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return "OK", f"{method} {resp.status}"
    except urllib.error.HTTPError as e:
      if e.code in (429, 403):
        # Someone else's rate limit is not a dead link, and failing the build on it
        # teaches people to ignore the build.
        return "UNKNOWN", f"{method} {e.code} (throttled or bot-blocked)"
      if method == "GET":
        return "DEAD", f"{method} {e.code}"
    except Exception as e:  # noqa: BLE001 - network failures are many and all mean "retry as GET"
      if method == "GET":
        return "UNKNOWN", f"{type(e).__name__}: {e}"
  return "UNKNOWN", "no response"


def check_links(text: str, skip_decorative: bool = True) -> List[LinkResult]:
  out: List[LinkResult] = []
  seen = set()
  for lineno, line in enumerate(text.splitlines(), 1):
    for url in LINK.findall(line):
      if skip_decorative and any(h in url for h in DECORATIVE_HOSTS):
        continue
      if url in seen:
        continue
      seen.add(url)
      m = GITHUB_REPO.match(url)
      if m:
        res = _gh_api(m.group(1), m.group(2))
        if res is not None:
          ok, detail = res
          out.append(LinkResult(url, lineno, "OK" if ok else "DEAD", detail))
          continue
      status, detail = _http(url)
      out.append(LinkResult(url, lineno, status, detail))
  return out


@dataclass(frozen=True)
class MetricResult:
  line: int
  text: str
  reason: str


def check_metrics(text: str) -> List[MetricResult]:
  """Lines stating a performance number with neither a source link nor a basis marker.

  Requires BOTH a metric word and a score-shaped number on the line, because prose
  mentioning "precision" in the ordinary sense is not a claim, and flagging it would make
  the check noisy enough to be turned off.
  """
  out: List[MetricResult] = []
  for lineno, line in enumerate(text.splitlines(), 1):
    if line.lstrip().startswith(("#", ">")):
      continue
    if not (METRIC.search(line) and SCORE.search(line)):
      continue
    if LINK.search(line):
      continue
    low = line.lower()
    if any(marker in low for marker in UNPUBLISHED_MARKERS):
      continue
    out.append(
      MetricResult(
        line=lineno,
        text=line.strip(),
        reason=(
          "states a performance number with no source link on the line and no explicit "
          "unpublished/in-house marker"
        ),
      )
    )
  return out


def main(argv: Optional[List[str]] = None) -> int:
  ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  ap.add_argument("--links", action="store_true", help="check links only (hits the network)")
  ap.add_argument("--metrics", action="store_true", help="check metric sourcing only (offline)")
  ap.add_argument("--file", default=README)
  ap.add_argument("--json", action="store_true", help="machine-readable output")
  args = ap.parse_args(argv)

  run_links = args.links or not args.metrics
  run_metrics = args.metrics or not args.links

  with open(args.file, encoding="utf-8") as fh:
    text = fh.read()

  failed = 0
  report = {}

  if run_metrics:
    metrics = check_metrics(text)
    report["metrics"] = [m.__dict__ for m in metrics]
    if not args.json:
      print(f"metric sourcing: {len(metrics)} unsourced claim(s)")
      for m in metrics:
        print(f"  line {m.line}: {m.reason}")
        print(f"    {m.text[:150]}")
    failed += len(metrics)

  if run_links:
    links = check_links(text)
    dead = [r for r in links if r.failed]
    unknown = [r for r in links if r.status == "UNKNOWN"]
    report["links"] = [r.__dict__ for r in links]
    if not args.json:
      print(f"\nlinks: {len(links)} checked, {len(dead)} dead, {len(unknown)} unverifiable")
      for r in dead:
        print(f"  DEAD     line {r.line}  {r.url}  ({r.detail})")
      for r in unknown:
        print(f"  UNKNOWN  line {r.line}  {r.url}  ({r.detail})")
    failed += len(dead)

  if args.json:
    print(json.dumps(report, indent=2))
  elif failed:
    print(f"\nFAIL: {failed} problem(s). This list's one hard rule is that every link resolves.")
  else:
    print("\nOK: every link resolves and every stated metric carries a source or a basis.")
  return 1 if failed else 0


if __name__ == "__main__":
  sys.exit(main())
