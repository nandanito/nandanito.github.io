#!/usr/bin/env python3
"""Em-dash budget for posts on nandan.me.

Heavy em-dash use reads as machine-generated prose. The rule (see CLAUDE.md,
"Voice and visual principles") is:

  - at most 2 em dashes per 1,000 words of prose, with a floor of 2 per post;
  - none in the title, excerpt, headings or figure captions.

Code (fenced blocks and inline code) and HTML tag attributes (e.g. img alt
text) are not counted. En dashes in ranges ("2–4") are fine.

Usage:
  _tools/check_em_dashes.py FILE...    check files; exit 1 on any violation
  _tools/check_em_dashes.py --all      report every post under _posts/writing
  _tools/check_em_dashes.py --hook     Claude Code PostToolUse hook: read the
                                       hook JSON on stdin, check the edited
                                       file if it is a post or draft, exit 2
                                       with the violations on stderr

The budget applies to posts dated on or after ENFORCE_FROM and to every
draft. Older posts predate the rule and are only reported by --all.
"""
import glob
import json
import os
import re
import sys

EM = "\u2014"
PER_1000 = 2
FLOOR = 2
ENFORCE_FROM = "2026-09-25"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def split_front_matter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5:]
    return "", text


def prose(body):
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"`[^`\n]*`", "", body)
    body = re.sub(r"<[^>]+>", "", body)  # tags and their attributes
    return body


def check(path):
    """Return (violations, count, words) for one file."""
    text = open(path, encoding="utf-8").read()
    fm, body = split_front_matter(text)
    problems = []

    for field in ("title", "excerpt"):
        m = re.search(r"^%s:\s*(.*)$" % field, fm, re.M)
        if m and EM in m.group(1):
            problems.append("front matter %s contains an em dash" % field)

    for n, line in enumerate(body.split("\n"), 1):
        if re.match(r"#{1,6} ", line) and EM in line:
            problems.append("heading has an em dash: %s" % line.strip())
    for cap in re.findall(r"<figcaption>(.*?)</figcaption>", body, re.S):
        if EM in cap:
            problems.append("figure caption has an em dash: %s" % cap.strip()[:80])

    p = prose(body)
    count = p.count(EM)
    words = len(p.split())
    budget = max(FLOOR, int(words * PER_1000 / 1000))
    if count > budget:
        problems.append(
            "%d em dashes in %d words of prose; budget is %d "
            "(%d per 1,000 words, minimum %d)" % (count, words, budget, PER_1000, FLOOR))
    return problems, count, words


def enforced(path):
    rel = os.path.relpath(os.path.abspath(path), ROOT)
    if rel.startswith("_drafts" + os.sep):
        return rel.endswith((".md", ".markdown"))
    if rel.startswith("_posts" + os.sep) and rel.endswith((".md", ".markdown")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-", os.path.basename(rel))
        return bool(m) and m.group(1) >= ENFORCE_FROM
    return False


def lines_with_dashes(path):
    out = []
    in_code = False
    for n, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not in_code and EM in re.sub(r"<[^>]+>", "", line):
            out.append("  line %d: %s" % (n, line.strip()[:110]))
    return out


def main(argv):
    if argv[:1] == ["--hook"]:
        try:
            payload = json.load(sys.stdin)
        except ValueError:
            return 0
        path = (payload.get("tool_input") or {}).get("file_path") or ""
        if not path or not enforced(path) or not os.path.exists(path):
            return 0
        problems, _, _ = check(path)
        if not problems:
            return 0
        sys.stderr.write(
            "Em-dash budget exceeded in %s (see CLAUDE.md voice rules):\n- %s\n"
            "Rewrite with commas, colons, parentheses or full stops. Keep an em dash "
            "only where it carries a deliberate beat. Don't touch code blocks.\n"
            "Lines with em dashes:\n%s\n"
            % (os.path.relpath(path, ROOT), "\n- ".join(problems),
               "\n".join(lines_with_dashes(path))))
        return 2

    if argv[:1] == ["--all"]:
        files = sorted(glob.glob(os.path.join(ROOT, "_posts", "writing", "*.md")))
        for f in files:
            problems, count, words = check(f)
            flag = "FAIL" if problems else "ok  "
            scope = "" if enforced(f) else " (pre-rule, not enforced)"
            print("%s %3d em / %5d words  %s%s" % (
                flag, count, words, os.path.basename(f), scope))
        return 0

    failed = False
    for f in argv:
        problems, count, words = check(f)
        if problems:
            failed = True
            print("%s:\n- %s" % (f, "\n- ".join(problems)))
        else:
            print("%s: ok (%d em dashes, %d words)" % (f, count, words))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
