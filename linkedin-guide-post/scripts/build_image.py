#!/usr/bin/env python3
"""LinkedIn post image: the guide cover inside a PDF viewer.

Usage: python3 build_image.py <project_folder>

Run it after build_guide.py. Reads meta.json (keyword, PDF file name), guide.html and the PDF,
then writes <folder>/linkedin-post-image.png at 2560 x 1920 (4:3):
- PDF viewer bar: file name, page "1 / N", zoom "- 100% +", icons;
- left column with thumbnails of pages 1 to 7, the first one highlighted;
- the cover in the middle, the top of page 2 below it;
- at the very bottom, full width, the block COMMENT "KEYWORD" FOR FREE ACCESS ->.
"""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SKILL, find_chrome, uri

if len(sys.argv) != 2:
    sys.exit("Usage: python3 build_image.py <project_folder>")
HERE = os.path.abspath(sys.argv[1])
meta = json.load(open(os.path.join(HERE, "content", "meta.json"), encoding="utf-8"))
KEYWORD = meta["keyword"]
FILENAME = meta["pdf_filename"]
PDF = os.path.join(HERE, FILENAME)
MK = os.path.join(HERE, "mockup")
os.makedirs(MK, exist_ok=True)

info = subprocess.run(["pdfinfo", PDF], capture_output=True, text=True, check=True).stdout
NB_PAGES = int(re.search(r"Pages:\s+(\d+)", info).group(1))
subprocess.run(["pdftoppm", "-png", "-scale-to-x", "400", "-scale-to-y", "-1", "-f", "1", "-l", "7",
                PDF, os.path.join(MK, "thumb")], check=True)
subprocess.run(["pdftoppm", "-png", "-scale-to-x", "2100", "-scale-to-y", "-1", "-f", "2", "-l", "2",
                PDF, os.path.join(MK, "page")], check=True)
# pdftoppm uses 2 digits below 100 pages
thumb = lambda i: f"mockup/thumb-{i:02d}.png"

guide = open(os.path.join(HERE, "guide.html"), encoding="utf-8").read()
cover = re.search(r'<section class="page cover">.*?</section>', guide, re.S).group(0)
css = open(os.path.join(SKILL, "scripts", "style.css"), encoding="utf-8").read()

cta = f'''<div class="cta"><svg viewBox="0 0 24 24" width="54" height="54" fill="none" stroke="#fff" stroke-width="2"
stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.8 7L4 20.5l1.5-4.6A8 8 0 1 1 21 12z"/>
<path d="M8.5 12h.01M12 12h.01M15.5 12h.01" stroke-width="3"/></svg>
<span>COMMENT “{KEYWORD}” FOR FREE ACCESS</span><b>→</b></div>'''


def ico(path, w=24):
    return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="#E8EAED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'


thumbs = "".join(
    f'<div class="th{" on" if i == 1 else ""}"><img src="{thumb(i)}"><span>{i}</span></div>' for i in range(1, 8))

# The viewer classes start with v-: style.css already uses .side and .next in the guide.
doc = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=block" rel="stylesheet">
<style>{css}
html, body {{ margin: 0; width: 1280px; height: 960px; overflow: hidden; background: #525659; }}
.viewer {{ position: relative; width: 1280px; height: 960px; background: #525659; font-family: 'IBM Plex Sans', sans-serif; }}
.vbar {{ position: absolute; inset: 0 0 auto 0; height: 46px; background: #323639; display: flex; align-items: center; padding: 0 20px;
  color: #E8EAED; font-size: 16px; box-shadow: 0 2px 6px rgba(0,0,0,.35); z-index: 10; }}
.vbar .fn {{ margin-left: 22px; width: 400px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.vbar .mid {{ display: flex; align-items: center; gap: 14px; margin-left: 40px; }}
.vbar .pg {{ background: #202124; border-radius: 3px; padding: 3px 12px; font-size: 15px; }}
.vbar .sep {{ width: 1px; height: 22px; background: #5F6368; }}
.vbar .zoom {{ display: flex; align-items: center; gap: 12px; background: #202124; border-radius: 3px; padding: 3px 12px; font-size: 15px; }}
.vbar .right {{ margin-left: auto; display: flex; gap: 22px; }}
.vside {{ position: absolute; left: 0; top: 46px; bottom: 0; width: 236px; background: #323639; padding: 16px 0 0 36px; overflow: hidden; }}
.vside::after {{ content: ''; position: absolute; right: 6px; top: 12px; width: 6px; height: 260px; border-radius: 3px; background: #6B6F73; }}
.th {{ width: 156px; margin-bottom: 14px; text-align: center; color: #E8EAED; font-size: 13px; }}
.th img {{ width: 156px; display: block; border: 4px solid transparent; outline: 1px solid #1E1E1E; }}
.th.on img {{ border-color: var(--mag); outline: 0; }}
.th span {{ display: block; margin-top: 4px; }}
.vmain {{ position: absolute; left: 236px; top: 46px; right: 0; bottom: 0; overflow: hidden; padding: 12px 0 0 15px; }}
.sheet {{ width: 1014px; height: 760.5px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,.45); position: relative; }}
.sheet .page {{ transform: scale(0.7922); transform-origin: 0 0; }}
.vnext {{ width: 1014px; margin-top: 12px; box-shadow: 0 2px 10px rgba(0,0,0,.45); display: block; }}
.cta {{ position: absolute; left: 20px; right: 20px; bottom: 14px; height: 120px; border-radius: 28px; z-index: 20;
  background: linear-gradient(100deg, #C7346D, #8747A1); display: flex; align-items: center; padding: 0 34px; gap: 18px;
  color: #fff; box-shadow: 0 -6px 34px rgba(0,0,0,.45); border: 3px solid rgba(255,255,255,.9); }}
.cta svg {{ flex: none; }}
.cta span {{ font-family: 'Archivo'; font-weight: 900; font-size: {38 if len(KEYWORD) <= 10 else 33}px; flex: 1; text-align: center; white-space: nowrap; }}
.cta b {{ font-size: 54px; font-weight: 400; line-height: 1; }}
</style></head><body><div class="viewer">
<div class="vbar">
  {ico('<path d="M4 6h16M4 12h16M4 18h16"/>')}
  <span class="fn">{FILENAME}</span>
  <div class="mid"><span class="pg">1</span><span>/&nbsp;{NB_PAGES}</span>{ico('<path d="M9 6l6 6-6 6"/>', 22)}
  <span class="sep"></span><span class="zoom">{ico('<path d="M5 12h14"/>', 18)}<span>100%</span>{ico('<path d="M12 5v14M5 12h14"/>', 18)}</span>
  <span class="sep"></span>{ico('<rect x="5" y="4" width="14" height="16" rx="1"/><path d="M9 4v16"/>', 22)}</div>
  <div class="right">{ico('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>')}
  {ico('<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>')}
  {ico('<path d="M7 9V4h10v5M6 18H4v-8h16v8h-2M8 14h8v6H8z"/>')}
  {ico('<circle cx="12" cy="5" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="12" cy="19" r="1.2"/>')}</div>
</div>
<div class="vside">{thumbs}</div>
<div class="vmain"><div class="sheet">{cover}</div><img class="vnext" src="mockup/page-02.png"></div>
{cta}
</div></body></html>"""

html_path = os.path.join(HERE, "mockup-post.html")
open(html_path, "w", encoding="utf-8").write(doc)
png = os.path.join(HERE, "linkedin-post-image.png")
subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--hide-scrollbars",
                "--force-device-scale-factor=2", "--window-size=1280,960", "--virtual-time-budget=15000",
                f"--screenshot={png}", uri(html_path)], check=True, capture_output=True)
print(png)
