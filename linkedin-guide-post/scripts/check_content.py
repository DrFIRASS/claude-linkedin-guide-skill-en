#!/usr/bin/env python3
"""Checks the guide content before building the PDF.

Usage: python3 check_content.py <project_folder>

Checks the schema (references/content-schema.md), the lengths that keep the layout intact,
and the writing rules of the skill. Exits with code 1 and the list of problems if there are any.
"""
import json, glob, os, re, sys

if len(sys.argv) != 2:
    sys.exit("Usage: python3 check_content.py <project_folder>")
C = os.path.join(os.path.abspath(sys.argv[1]), "content")
pb = []

# Banned characters and words. A leftover "[TO BE COMPLETED]" or "TODO" in a prompt looks like a draft:
# for missing information in a prompt, write [MISSING INFO].
BANNED = [("—", "em dash"), ("–", "en dash"), ("TO BE COMPLETED", "[TO BE COMPLETED] marker"), ("TODO", "TODO marker")]
WORDS = r"\b(incredible|revolutionary|ultimate|game[ -]changer|game[ -]changing|supercharge\w*|unleash\w*|skyrocket\w*|delve\w*|synergy)\b"


def text(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from text(y)
    elif isinstance(x, dict):
        for y in x.values():
            yield from text(y)


def rules(name, obj):
    for s in text(obj):
        for char, label in BANNED:
            if char in s:
                pb.append(f"{name}: {label} in \"{s[:60]}...\"")
        m = re.search(WORDS, s, re.I)
        if m:
            pb.append(f"{name}: banned word \"{m.group(0)}\" in \"{s[:60]}...\"")


def bounds(name, s, lo, hi):
    if not (lo <= len(s) <= hi):
        pb.append(f"{name}: {len(s)} characters (expected {lo} to {hi})")


for f in ("meta.json", "extra.json"):
    if not os.path.exists(os.path.join(C, f)):
        pb.append(f"{f} missing")
if pb:
    sys.exit("\n".join(pb))

meta = json.load(open(os.path.join(C, "meta.json"), encoding="utf-8"))
extra = json.load(open(os.path.join(C, "extra.json"), encoding="utf-8"))
rules("meta.json", meta)
rules("extra.json", extra)
for l in meta["cover_title"]:
    # beyond this, the line runs over the pink shape of the cover
    if len(l.replace("*", "")) > 17:
        pb.append(f"meta.cover_title: \"{l}\" is longer than 17 characters")
if len(meta["cover_title"]) != 4:
    pb.append("meta.cover_title: 4 lines expected")
if not re.fullmatch(r"[A-Z0-9]{2,30}", meta["keyword"]):
    pb.append("meta.keyword: 2 to 30 capital letters or digits, no accents or spaces")
if len(extra["setup_steps"]) != 3 or len(extra["setup_prompts"]) != 2:
    pb.append("extra: 3 setup_steps and 2 setup_prompts expected")
if len(extra["plan30"]) != 4 or any(len(w["actions"]) != 4 for w in extra["plan30"]):
    pb.append("extra.plan30: 4 weeks of 4 actions expected")
for sp in extra["setup_prompts"]:
    bounds("extra.setup_prompts.prompt", sp["prompt"], 250, 560)

chs = sorted(glob.glob(os.path.join(C, "ch*.json")))
if not 6 <= len(chs) <= 10:
    pb.append(f"{len(chs)} chapters: the layout is built for 6 to 10")
nums = []
for f in chs:
    name = os.path.basename(f)
    try:
        c = json.load(open(f, encoding="utf-8"))
    except json.JSONDecodeError as err:
        pb.append(f"{name}: invalid JSON ({err})")
        continue
    rules(name, c)
    nums.append(c["num"])
    bounds(f"{name}.title", c["title"], 5, 42)
    bounds(f"{name}.intro", c["intro"], 220, 400)
    if len(c["framework"]["steps"]) != 4:
        pb.append(f"{name}: 4 method steps expected")
    for s in c["framework"]["steps"]:
        bounds(f"{name}.framework.d", s["d"], 60, 145)
    if len(c["prompts"]) != 4:
        pb.append(f"{name}: 4 prompts expected")
    for p in c["prompts"]:
        bounds(f"{name}.prompt \"{p['title']}\"", p["prompt"], 300, 620)
    if len(c["workflow"]["steps"]) != 5:
        pb.append(f"{name}: 5 workflow steps expected")
    if len(c["checklist"]) != 6:
        pb.append(f"{name}: 6 checklist items expected")
    for s in c["checklist"]:
        bounds(f"{name}.checklist", s, 15, 95)
    bounds(f"{name}.mistake", c["mistake"], 60, 240)
    bounds(f"{name}.tip", c["tip"], 60, 240)
if nums != list(range(1, len(nums) + 1)):
    pb.append(f"chapter numbers are not consecutive: {nums}")

if pb:
    print("Content to fix:")
    print("\n".join(f"- {x}" for x in pb))
    sys.exit(1)
print(f"Content valid: {len(chs)} chapters.")
