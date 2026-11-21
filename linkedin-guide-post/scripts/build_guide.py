#!/usr/bin/env python3
"""Builds the PDF guide (magenta and purple theme, author name from meta.json or config.json).

Usage: python3 build_guide.py <project_folder>

The project folder holds content/meta.json, content/extra.json and content/ch01.json … chNN.json
(schema: references/content-schema.md). The script writes <folder>/guide.html, then the PDF
<folder>/<meta.pdf_filename>, 1280 x 960 px per page, with headless Chrome.
The cover numbers (chapters, prompts, methods, workflows, checkpoints) are computed from the content,
so they are always true.
"""
import json, glob, html, re, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SKILL, find_chrome, uri, settings

if len(sys.argv) != 2:
    sys.exit("Usage: python3 build_guide.py <project_folder>")
HERE = os.path.abspath(sys.argv[1])
C = os.path.join(HERE, "content")

meta = json.load(open(os.path.join(C, "meta.json"), encoding="utf-8"))
extra = json.load(open(os.path.join(C, "extra.json"), encoding="utf-8"))
chapters = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(C, "ch*.json")))]
chapters.sort(key=lambda c: c["num"])
GUIDE_TITLE = meta["short_title"]
AUTHOR, MASCOT_ON, MASCOT = settings(meta)


def t(s):
    return html.escape(s, quote=False)


def accent(s):
    # *word* is shown in magenta
    return re.sub(r"\*([^*]+)\*", r'<span class="grad">\1</span>', t(s))


def prompt_html(p):
    s = re.sub(r"(\[[^\]]+\])", r'<span class="var">\1</span>', t(p))
    return s.replace("\n", "<br>")


def masc(name, cls=""):
    # without a mascot (mascot: false), the image is simply left out
    if not MASCOT_ON:
        return ""
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{uri(os.path.join(MASCOT, name + ".png"))}">'


def two_lines(lines):
    return f'{t(lines[0])}<br><span class="grad">{t(lines[1])}</span>'


pages, page_num = [], [0]


def footer(chap=None):
    page_num[0] += 1
    left = f"Chapter {chap:02d}" if chap else t(AUTHOR)
    return f"""<div class="foot"><span class="fl"><b>{left}</b> · {t(GUIDE_TITLE)}</span>
<span class="fr">{page_num[0]:02d}</span></div>"""


# ---------- Cover ----------
nb_prompts = sum(len(c["prompts"]) for c in chapters) + len(extra["setup_prompts"])
nb_check = sum(len(c["checklist"]) for c in chapters)
half = (len(chapters) + 1) // 2
li = lambda cs: "".join(f'<li><span class="n">{c["num"]:02d}</span><span class="tt">{t(c["title"])}</span></li>' for c in cs)
page_num[0] += 1
pages.append(f"""
<section class="page cover">
  <div class="blob"></div>
  {masc('cover', 'masc')}
  <div class="brand"><span class="dot"></span>{t(AUTHOR)}</div>
  <div class="side">{'<br>'.join(t(m) for m in meta['side_words'])}</div>
  <div class="pill">{t(meta['edition'])}</div>
  <h1>{'<br>'.join(accent(l) for l in meta['cover_title'])}</h1>
  <div class="rule"></div>
  <p class="lead">{t(meta['tagline'])}</p>
  <div class="stats">
    <div><b>{len(chapters)}</b><span>chapters</span></div>
    <div><b>{nb_prompts}</b><span>prompts</span></div>
    <div><b>{len(chapters)}</b><span>methods</span></div>
    <div><b>{len(chapters)}</b><span>workflows</span></div>
    <div><b>{nb_check}</b><span>checkpoints</span></div>
  </div>
  <div class="toc"><ol>{li(chapters[:half])}</ol><ol>{li(chapters[half:])}</ol></div>
  <div class="band"><span>{t(meta['banner'][0])}</span><span>{t(meta['banner'][1])}</span></div>
</section>""")

# ---------- Table of contents ----------
p = 3
rows = [("00", extra["toc_00"]["t"], extra["toc_00"]["st"], p)]
p += 1
for c in chapters:
    rows.append((f'{c["num"]:02d}', c["title"], c["subtitle"], p))
    p += 3
rows.append(("+", extra["toc_plan"]["t"], extra["toc_plan"]["st"], p))
toc = "".join(
    f'<div class="sl"><span class="sn">{n}</span><div><b>{t(ti)}</b><small>{t(st)}</small></div><span class="dots"></span><span class="sp">{pg:02d}</span></div>'
    for n, ti, st, pg in rows)
pages.append(f"""
<section class="page sommaire">
  <div class="kick">CONTENTS</div>
  <h2>What you will<br><span class="grad">put in place</span></h2>
  <div class="slist">{toc}</div>
  <div class="howto">
    <div class="ht"><b>How to read this guide</b>Each chapter fits on 3 pages: a method, 4 ready-to-copy prompts, a workflow and its checklist.</div>
    <div class="ht"><b>The [BRACKETS]</b>In each prompt, replace the text in brackets with your own information before you send it.</div>
    <div class="ht"><b>In order or not</b>Start with page 03, then go straight to the chapter that solves your problem of the moment.</div>
  </div>
  {footer()}
</section>""")

# ---------- Chapter 00: setup ----------
setup_steps = "".join(
    f'<div class="ss"><span class="num">{i+1}</span><div><b>{t(s["t"])}</b><p>{t(s["d"])}</p></div></div>'
    for i, s in enumerate(extra["setup_steps"]))
setup_prompts = "".join(
    f'<div class="pcard"><div class="ph"><b>{t(sp["title"])}</b><small>{t(sp["use"])}</small></div><div class="pbody">{prompt_html(sp["prompt"])}</div></div>'
    for sp in extra["setup_prompts"])
feats = "".join(f'<div class="feat"><b>{t(f["t"])}</b><span>{t(f["d"])}</span></div>' for f in extra["features"])
pages.append(f"""
<section class="page setup">
  <div class="kick">{t(extra['setup_kicker'])}</div>
  <h2>{two_lines(extra['setup_title'])}</h2>
  <p class="intro">{t(extra["setup_intro"])}</p>
  <div class="setgrid">
    <div class="steps3">{setup_steps}<div class="feats"><div class="fk">{t(extra['features_title'])}</div>{feats}</div></div>
    <div class="sprompts">{setup_prompts}</div>
  </div>
  {footer()}
</section>""")

# ---------- Chapters: opening, prompts, workflow ----------
cap = lambda s: s[:1].upper() + s[1:]
for c in chapters:
    n = c["num"]
    steps = "".join(
        f'<div class="fs"><span class="num">{i+1}</span><b>{t(s["t"])}</b><p>{t(s["d"])}</p></div>'
        for i, s in enumerate(c["framework"]["steps"]))
    mistake = cap(re.sub(r"^Common mistake\s*:\s*", "", c["mistake"], flags=re.I))
    tip = cap(re.sub(r"^[^:]{0,40}\btip\s*:\s*", "", c["tip"], flags=re.I))
    pages.append(f"""
<section class="page chap">
  <div class="hero">
    <div class="bignum">{n:02d}</div>
    <div class="htxt"><div class="kick w">CHAPTER {n:02d}</div>
    <h2>{t(c["title"])}</h2><p class="sub">{t(c["subtitle"])}</p></div>
  </div>
  <p class="intro">{t(c["intro"])}</p>
  <div class="fwname"><span class="kick">THE METHOD</span><h3>{t(c["framework"]["name"])}</h3></div>
  <div class="fsteps">{steps}</div>
  <div class="duo">
    <div class="warn"><div class="tag r">COMMON MISTAKE</div><p>{t(mistake)}</p></div>
    <div class="tip{'' if MASCOT_ON else ' nomasc'}">{masc('tip')}<div><div class="tag v">TIP FROM {t(AUTHOR).upper()}</div><p>{t(tip)}</p></div></div>
  </div>
  {footer(n)}
</section>""")

    cards = "".join(
        f'<div class="pcard"><div class="ph"><span class="pn">P{n}.{i+1}</span><div><b>{t(pr["title"])}</b><small>{t(pr["use"])}</small></div></div><div class="pbody">{prompt_html(pr["prompt"])}</div></div>'
        for i, pr in enumerate(c["prompts"]))
    pages.append(f"""
<section class="page prompts">
  <div class="phead"><div class="kick">CHAPTER {n:02d} · {t(c["title"]).upper()}</div>
  <h2>{len(c["prompts"])} prompts <span class="grad">ready to copy</span></h2></div>
  <div class="pgrid">{cards}</div>
  {footer(n)}
</section>""")

    wsteps = "".join(f'<li><span class="num">{i+1}</span><p>{t(s)}</p></li>' for i, s in enumerate(c["workflow"]["steps"]))
    checks = "".join(f'<li><span class="box"></span><p>{t(s)}</p></li>' for s in c["checklist"])
    wtitle = cap(re.sub(r"^Workflow\s*:\s*", "", c["workflow"]["title"], flags=re.I))
    following = next((x for x in chapters if x["num"] == n + 1), None)
    nxt = (f'Next chapter: <b>{t(following["title"])}</b> →' if following
           else f"Last step: <b>{t(extra['toc_plan']['t'][:1].lower() + extra['toc_plan']['t'][1:])}</b> →")
    pages.append(f"""
<section class="page wf">
  <div class="phead"><div class="kick">CHAPTER {n:02d} · WORKFLOW AND CHECKLIST</div>
  <h2>Put it <span class="grad">into action</span></h2></div>
  <div class="wgrid">
    <div class="wcard"><div class="tag v">WORKFLOW</div><h3>{t(wtitle)}</h3>
      <div class="where"><span>WHERE</span>{t(c["workflow"]["where"])}</div>
      <ol class="wsteps">{wsteps}</ol></div>
    <div class="ccard"><div class="tag g">CHECKLIST</div><h3>Before you sign off</h3><ul class="checks">{checks}</ul>
      <div class="next">{nxt}</div></div>
  </div>
  {footer(n)}
</section>""")

# ---------- Action plan ----------
weeks = "".join(
    f'<div class="week"><div class="wk">WEEK {i+1}</div><h3>{t(w["t"])}</h3><p class="wch">{t(w["chapters"])}</p><ul>' +
    "".join(f"<li>{t(x)}</li>" for x in w["actions"]) + "</ul></div>"
    for i, w in enumerate(extra["plan30"]))
pages.append(f"""
<section class="page plan">
  <div class="kick">YOUR ACTION PLAN</div>
  <h2>{two_lines(extra['plan_title'])}</h2>
  <p class="intro">{t(extra["plan_intro"])}</p>
  <div class="weeks">{weeks}</div>
  {footer()}
</section>""")

# ---------- End page ----------
page_num[0] += 1
pages.append(f"""
<section class="page fin">
  <div class="blob"></div>
  {masc('end', 'masc')}
  <div class="brand w"><span class="dot"></span>{t(AUTHOR)}</div>
  <div class="fintxt">
    <div class="kick w">WHAT NOW?</div>
    <h2>{t(extra["end_title"])}</h2>
    {"".join(f"<p>{t(x)}</p>" for x in extra["end_paras"])}
    <div class="sig"><b>{t(AUTHOR)}</b><span>{t(extra['end_signature'])}</span><span class="url">{t(extra['end_url'])}</span></div>
  </div>
  <p class="legal">{t(extra["legal"])}</p>
</section>""")

css = open(os.path.join(SKILL, "scripts", "style.css"), encoding="utf-8").read()
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{t(GUIDE_TITLE)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=block" rel="stylesheet">
<style>{css}</style></head><body>{''.join(pages)}</body></html>"""
out = os.path.join(HERE, "guide.html")
open(out, "w", encoding="utf-8").write(doc)

pdf = os.path.join(HERE, meta["pdf_filename"])
subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                "--no-pdf-header-footer", "--virtual-time-budget=15000", f"--print-to-pdf={pdf}", uri(out)],
               check=True, capture_output=True)
print(json.dumps({"pdf": pdf, "pages": len(pages), "chapters": len(chapters), "prompts": nb_prompts,
                  "checkpoints": nb_check}, ensure_ascii=False))
