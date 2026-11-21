# First run: create config.json

This file is only read when `config.json` does not exist at the root of the skill. Ask the questions all at once
(AskUserQuestion if the tool exists, otherwise a single message), then write `config.json` from `config.example.json`.

## The questions

1. **Your name**, as it should appear on the guide (e.g. “Jane Smith”) → `author`.
2. **What you do, in one line** (e.g. “Marketing and AI for solopreneurs”) → `signature`.
   Optional: your website or page (e.g. `janesmith.com`) → `website`, otherwise an empty string.
3. **Where to store the guides** on the computer. Default `~/Documents/linkedin-guides` → `guides_folder`.
4. **The mascot**: the skill ships with Dr. Firas's mascot, used only for the example. Two choices:
   - no mascot (default) → `mascot: false`. The guide stays complete, just without a character;
   - your own mascot → the user replaces the 3 images in `assets/mascot/` with their own, transparent PNGs, with the
     **same names**: `cover.png` (cover, character presenting), `tip.png` (“Tip” box, character pointing),
     `end.png` (end page) → `mascot: true`. Check that all 3 files were replaced before setting `true`.

Also ask the **time zone** (default `America/New_York`; for example `Europe/London`, `Europe/Paris`,
`America/Los_Angeles`) → `timezone`.

## The Blotato account

No question to ask: load the Blotato tools with ToolSearch, then `blotato_list_accounts(platform: "linkedin")`.

- No Blotato tools: the connector is not installed. Give the install link from the README
  (`https://mcp.blotato.com/mcp`) and carry on without publishing: the skill still produces the PDF, the image and
  the text.
- A single LinkedIn account: take its `id`.
- Several accounts: ask which one (display name and id). If the account has company pages, also ask whether the post
  goes on the profile or on a page (`pageId`), and store it in `config.json` as `blotato_linkedin_page_id`.

→ `blotato_linkedin_account_id`.

## Auto mode (optional)

If the user wants one post a day without doing anything, they duplicate the Notion template “LinkedIn guide queue”
(link in the repository README). Ask for the link to **their copy**, run `notion-fetch` on it and store the
`collection://…` URL of the data source → `notion_data_source`. Ask for the publishing time (default `08:00`).

Then offer to create the scheduled task with the text of `scheduled-tasks/nightly-linkedin-guide.md` from the repository
(`create_scheduled_task` tool in the Claude app, or the `/schedule` command).

## Example of a filled config.json

```json
{
  "author": "Jane Smith",
  "signature": "Marketing and AI for solopreneurs",
  "website": "janesmith.com",
  "mascot": false,
  "guides_folder": "~/Documents/linkedin-guides",
  "blotato_linkedin_account_id": "12345",
  "notion_data_source": "collection://xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "publish_time": "08:00",
  "timezone": "America/New_York"
}
```

Show the final file to the user, one line per value, then go back to the original request.
