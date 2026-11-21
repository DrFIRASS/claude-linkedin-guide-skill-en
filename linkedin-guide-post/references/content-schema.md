# Guide content: schemas and writers' brief

The project's `content/` folder holds three kinds of files. The full examples are in
`assets/example-marketing/content/`. Copy them as a starting point.

## Writing rules (for every file)

- Talk to the reader as “you”. Plain American English.
- No em dash (—) or en dash (–): use a comma, a colon or a new sentence.
- Curly quotes “ ” for quotations.
- No empty words: incredible, revolutionary, ultimate, game changer, supercharge, unleash, skyrocket, delve, synergy.
- Short, concrete sentences. Every item can be applied today, no theory.
- No made-up statistics, client results or study numbers.
- Only mention tool features that really exist. For Claude (November 2026): Projects (instructions and files shared by
  the Project's conversations), Artifacts, web search and Research, file analysis (PDF, CSV, Excel), Skills, connectors
  (Google Drive, Gmail, Google Calendar, Notion, HubSpot, Slack…), Claude Code, scheduled tasks. No made-up menu names.
- Never “[TO BE COMPLETED]” or “TODO”: write `[MISSING INFO]`.

## meta.json

```json
{
  "author": "Dr. Firas",
  "mascot": true,
  "short_title": "The guide to marketing with Claude 2026",
  "pdf_filename": "The guide to marketing with Claude 2026 - Dr Firas.pdf",
  "keyword": "MARKETING",
  "edition": "2026 EDITION",
  "cover_title": ["The complete", "guide to", "marketing with", "*Claude* 2026"],
  "tagline": "Methods, ready-to-copy prompts and workflows to run your marketing with Claude.",
  "side_words": ["STRATEGY", "PROMPTS", "WORKFLOWS", "CHECKLISTS"],
  "banner": ["Free guide · by Dr. Firas", "AI, automation and content, made simple"]
}
```

- `author`, `mascot`: taken from `config.json` (the name shown on the guide, and `true` only if `assets/mascot/`
  holds the user's 3 images).
- `short_title`: footer and PDF title.
- `pdf_filename`: the name shown at the top of the post image. No special characters except hyphens and spaces.
- `cover_title`: 4 lines of 17 characters at most. `*word*` turns the word magenta (only one per title).
- `tagline`: one sentence of 80 to 110 characters.
- `side_words`: 4 short words in capitals, top right of the cover.

## extra.json

Keys, in order: `toc_00`, `toc_plan`, `setup_kicker`, `setup_title`, `setup_intro`, `setup_steps`, `setup_prompts`,
`features_title`, `features`, `plan_title`, `plan_intro`, `plan30`, `end_title`, `end_paras`, `end_signature`,
`end_url`, `legal`.

- **Chapter 00 “Before you start”**: the most useful page of the guide. It sets up the tool once and for all (for
  Claude: a Project, a brand sheet, instructions). `setup_title` on 2 lines (the 2nd in magenta), `setup_intro` in 2 or
  3 sentences, exactly 3 `setup_steps` `{t, d}`, exactly 2 `setup_prompts` `{title, use, prompt}` (250 to 560
  characters), 4 or 5 `features` `{t, d}` that explain the features mentioned in the guide.
  `toc_00` = `{t, st}` for the contents line.
- **30-day plan**: `plan_title` on 2 lines, `plan_intro`, and `plan30` = 4 weeks
  `{t, chapters: "Chapters 00, 01, 02", actions: [4 short actions]}`. `toc_plan` = `{t, st}` for the contents line.
- **End page**: short `end_title` (“Your turn”), 3 `end_paras`, `end_signature` (the `signature` from `config.json`),
  `end_url` (the `website` from `config.json`, or an empty string), `legal`: independent free guide, not endorsed by the
  tool's publisher, trademark, features dated to the current month.

## ch01.json … chNN.json

```json
{
  "num": 1,
  "title": "Marketing strategy",
  "subtitle": "A clear 90-day plan before you write a single line",
  "intro": "2 or 3 sentences, 280 to 380 characters.",
  "framework": {
    "name": "The CAP 90 method",
    "steps": [ { "t": "Take stock", "d": "1 sentence, 90 to 140 characters." } ]
  },
  "prompts": [
    { "title": "The quick diagnosis", "use": "When to use it, under 90 characters.", "prompt": "350 to 600 characters, with [VARIABLES], a role, the context, the output format." }
  ],
  "workflow": {
    "title": "Workflow: your 90-day plan in a Claude Project",
    "where": "A Claude Project + an Artifact",
    "steps": ["5 steps, one sentence each, under 130 characters"]
  },
  "checklist": ["6 checkpoints, under 90 characters, phrased as checks"],
  "mistake": "Common mistake: 1 or 2 sentences, under 220 characters.",
  "tip": "<Author>'s tip: 1 or 2 concrete sentences, under 220 characters."
}
```

Exact counts: 4 method steps, 4 prompts, 5 workflow steps, 6 checklist items.
`title`: 2 to 5 words (it is displayed very large, on 2 lines at most). Lengths matter: beyond them, a card overflows.

## Standard brief for a writing agent

Launch two `general-purpose` agents in the background, in the same message. Adapt the brackets:

```text
You write the content of 5 chapters of a PDF guide in English: “[GUIDE TITLE]”, signed by [AUTHOR]
([WHAT THE AUTHOR DOES], audience of curious beginners, entrepreneurs, freelancers). The guide is free and shared on LinkedIn.

Your chapters:
[N]. [Title] ([what it covers, in a few words])
… (5 chapters)

Write ONE JSON file per chapter: [FOLDER]/content/chNN.json, with EXACTLY this schema:
[paste the “ch01.json” schema above, with the counts and lengths]

Style rules (mandatory):
[paste the “Writing rules” section above]
- Vary the prompts: some ask the tool to ask questions first, others to critique, others to produce a table.
- Valid JSON, checked with python3 -c "import json;json.load(open(...))". No comments in the JSON.

Another writer handles chapters [list of the other chapters and their topics]: do not overlap with those topics.

When you are done, reply only with the list of files written and the name of each chapter's method.
```

For an 8-chapter guide, use 2 agents of 4 chapters. When they are back, run `check_content.py`.
