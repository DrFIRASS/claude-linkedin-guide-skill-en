"""Shared helpers for build_guide.py and build_image.py.

- read_config(): reads config.json at the root of the skill (created on first run from config.example.json).
- find_chrome(): finds Chrome, Chromium or Edge on macOS, Windows or Linux (or the CHROME_PATH variable).
- uri(): turns a local path into a file:// address that works on every system.
"""
import json, os, shutil
from pathlib import Path

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
CHROME_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]


def read_config():
    for name in ("config.json", "config.example.json"):
        f = os.path.join(SKILL, name)
        if os.path.exists(f):
            return json.load(open(f, encoding="utf-8"))
    return {}


def find_chrome():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    for name in CHROME_NAMES:
        p = shutil.which(name)
        if p:
            return p
    raise SystemExit("Chrome not found. Install Google Chrome, or set its path in the CHROME_PATH variable.")


def uri(path):
    return Path(path).resolve().as_uri()


def settings(meta):
    """Author and mascot: meta.json first, then config.json."""
    config = read_config()
    author = meta.get("author") or config.get("author") or "Your name"
    mascot = meta.get("mascot", config.get("mascot", False))
    folder = os.path.join(SKILL, "assets", "mascot")
    if mascot and not all(os.path.exists(os.path.join(folder, f"{n}.png"))
                          for n in ("cover", "tip", "end")):
        mascot = False
    return author, bool(mascot), folder
