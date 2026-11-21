---
name: linkedin-guide-post
description: "LinkedIn Guide Post: builds a free PDF guide (lead magnet) of 8 to 10 chapters end to end, picks a keyword, makes the post image (cover inside a PDF viewer, page thumbnails, a COMMENT “KEYWORD” FOR FREE ACCESS → block), writes the LinkedIn post in English in the “FREE access 👇” format and publishes or schedules it on LinkedIn with Blotato. The PDF is saved in a local folder. Use this skill whenever the user wants a PDF guide to give away on LinkedIn, a lead magnet, to copy a post from a creator who offers a guide in the comments, or says “make me a guide + the LinkedIn post”, “same as the MARKETING guide on another topic”, “process the next topic in the Notion queue”, even without naming the skill."
---

# LinkedIn Guide Post

The idea: a creator posts “I put everything into one guide… FREE access 👇” with a preview of a PDF, then sends the
guide to everyone who comments the keyword. This skill does all the work, in this order:

1. the guide content (8 to 10 chapters);
2. the PDF, saved in the guide's local folder;
3. the post image;
4. the LinkedIn post text;
5. publishing (or scheduling) on LinkedIn with Blotato.

The reference guide is the **MARKETING** guide (“The complete guide to marketing with Claude 2026”, 35 pages,
10 chapters, 42 prompts), in `assets/example-marketing/`. It sets the bar for quality and tone.

## First: the configuration

Read `config.json` at the root of this skill. If it does not exist, this is the first run: follow
`references/first-setup.md` (4 questions, then create `config.json`). In auto mode, ask nothing: if `config.json` is
missing, stop and say so.

Values used everywhere:
- `author`: the name shown on the guide (cover, footer, “Tip from <author>”, signature);
- `signature`, `website`: the end page of the PDF (`website` can stay empty);
- `mascot`: `true` only if the user put their 3 images in `assets/mascot/` (see the setup);
- `guides_folder`: where each guide is stored;
- `blotato_linkedin_account_id`: the LinkedIn account to use in Blotato;
- `notion_data_source`, `publish_time`, `timezone`: auto mode.

## Writing rules

- Plain, direct American English. Never an em dash (—) or an en dash (–), no empty buzzwords.
- The PDF and the post talk to the reader as “you”.
- Nothing made up: no statistics, no client results, no “+230%”. The cover numbers are computed by the script, so they
  are always true. A tool feature is only mentioned if it exists; check anything that can change (plans, menus, prices).
- No third-party logo or brand (Anthropic, OpenAI…) on the cover: the guide is signed by the author. The last page says
  the guide is independent.
- Prefer parallel agents to write the chapters.
- Never write “[TO BE COMPLETED]” or “TODO”: for missing information in a prompt, write `[MISSING INFO]`.

## Steps

### 0. Frame the request (one question at most)

You need: the **topic** (e.g. “marketing with Claude”), the **audience** (default: curious beginners, entrepreneurs,
freelancers) and, if there is one, the **reference post** to imitate. If the topic is clear, ask nothing.

Create the project folder `<guides_folder>/<keyword in lowercase>/` (expand the `~`), with a `content/` subfolder.

### 1. Outline and keyword

Pick 8 to 10 chapters that cover the topic without overlapping, and the **keyword**: a short word, easy to say and type,
2 to 30 capital letters or digits, no accents (e.g. `MARKETING`). Check that no folder with that name already exists in
`guides_folder`.

Write `content/meta.json` yourself (with `author` and `mascot` taken from `config.json`) and `content/extra.json`
(chapter 00, 30-day plan, end page). Schemas and example: `references/content-schema.md`.

### 2. Write the chapters in parallel

Launch **two background agents** (chapters 1 to 5, then 6 to 10), each with the standard brief from
`references/content-schema.md`. Meanwhile, write `meta.json` and `extra.json`. Then:

```bash
python3 <skill>/scripts/check_content.py <project_folder>
```

Fix every reported problem (in the JSON files), then run it again until it says “Content valid”.

### 3. Build the PDF

```bash
python3 <skill>/scripts/build_guide.py <project_folder>
```

It writes `guide.html` and the PDF (name in `meta.pdf_filename`) in the project folder, landscape 1280 × 960: cover,
contents, chapter 00, 3 pages per chapter (method, 4 prompts, workflow + checklist), 30-day plan, end page. With
10 chapters: 35 pages.

**Look at the result** before going further. Render the pages as PNG (`pdftoppm -r 60 -png <pdf> <folder>/preview/p`)
and look at them. Check: the cover title does not touch the pink shape, no prompt card overflows, no lowercase text
after “Common mistake” or “Workflow”. Fix the content rather than the stylesheet when you can.

The PDF stays in the project folder: it is the file the user will send (or upload to Google Drive, Notion, their
website…) to the people who comment.

### 4. Make the post image

```bash
python3 <skill>/scripts/build_image.py <project_folder>
```

It writes `linkedin-post-image.png` (2560 × 1920): a PDF viewer (bar with the file name, “1 / N”, zoom, icons), the
column of thumbnails for pages 1 to 7, the cover in the middle, and at the bottom the gradient block
COMMENT “KEYWORD” FOR FREE ACCESS → on a single line.

Open the image and check that the block text fits on one line. For a long keyword the script lowers the font size; if
that is not enough, shorten the keyword rather than breaking the sentence.

The word “comment” must appear **only in the image**, never in the post text: LinkedIn reduces the reach of posts that
ask for comments.

### 5. Write the LinkedIn post

“FREE access 👇” format, full rules and approved example in `references/linkedin-post.md`. Aim for 900 to 1,500
characters (count them). Save it in `<project_folder>/linkedin-post.md`.

### 6. Publish on LinkedIn with Blotato

Exact procedure in `references/publishing-linkedin.md`: account `blotato_linkedin_account_id`, image sent through a
presigned URL, `blotato_create_post`, then the post link.

Publishing on LinkedIn is public and hard to undo. If the user's request already says to publish (“post it now”,
“publish it”, “schedule it tomorrow at 8 am”), do it. Otherwise, show the final text and image, and ask for a single
“go”.

### Auto mode (scheduled task and Notion queue)

When the skill is started by a scheduled task, or when the user asks to “process the queue” or “the next topic on the
list”, read `references/auto-mode.md`: the topic comes from the Notion database (`notion_data_source`), nothing is
asked, the post is **scheduled** at `publish_time` (not published right away), and the Notion row moves to “Done” with
the keyword, the PDF path and the date, or to “Error” with the reason.

### 7. Wrap up

Give the user:
- the path of the PDF and the image (send them with SendUserFile if the tool exists);
- the keyword;
- the post text and the LinkedIn link if it is published;
- the **direct message** to send to each person who comments (template in `references/linkedin-post.md`);
- anything that could not be checked (a tool feature, a number).

## Skill files

| File | Role |
|---|---|
| `config.example.json` | Configuration template, copied to `config.json` on first run |
| `scripts/check_content.py` | Validates the JSON: schema, lengths that fit the layout, banned words and characters |
| `scripts/build_guide.py` | Builds `guide.html` then the PDF with headless Chrome |
| `scripts/build_image.py` | Builds the post image (PDF viewer + COMMENT block) |
| `scripts/common.py` | Configuration, Chrome lookup (macOS, Windows, Linux) |
| `scripts/style.css` | The theme: magenta `#CB3672`, purple `#8747A1`, coral `#EEA39C`, ink `#131325`, Archivo + IBM Plex |
| `assets/mascot/` | 3 mascot images (Dr. Firas's, for the example only; replace them with yours) |
| `assets/example-marketing/` | The full MARKETING guide: `content/*.json` and `linkedin-post.md` |
| `references/first-setup.md` | First run: questions and creation of `config.json` |
| `references/content-schema.md` | JSON schemas, writing rules, brief for the writing agents |
| `references/linkedin-post.md` | Post format, approved example, direct message |
| `references/publishing-linkedin.md` | Step-by-step Blotato publishing |
| `references/auto-mode.md` | Notion queue, scheduled task, scheduling, error handling |

Tools needed: Google Chrome (or Chromium, Edge), `pdftoppm` and `pdfinfo` (poppler package), Python 3.

## Known pitfalls

- **Gradient text** (`background-clip: text`): Chrome draws a stray frame around it in the PDF. The theme uses solid
  magenta for highlighted words.
- **Cover title** too long: it runs over the pink shape. 17 characters per line at most, 4 lines (the check enforces it).
- **CSS classes**: the image reuses `style.css`, which already defines `.side` and `.next`. The viewer classes therefore
  start with `v` (`.vside`, `.vnext`…). Keep this if you edit the script.
- **Fonts**: they come from Google Fonts. Without an internet connection, Chrome uses a fallback font and the layout
  shifts.
- **`rm` with a variable**: write `"${VAR:?}"/*.png`, never `$VAR/*.png`.
- **LinkedIn**: the post page asks for a login in the browser. The “published” status and the `publicUrl` returned by
  Blotato are the proof; tell the user so.
