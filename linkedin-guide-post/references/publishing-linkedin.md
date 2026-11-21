# Publishing the post on LinkedIn with Blotato

Blotato connector tools (load them with ToolSearch if they are deferred): `blotato_list_accounts`,
`blotato_create_presigned_upload_url`, `blotato_create_post`, `blotato_get_post_status`.

No Blotato account? Create one here: https://blotato.com/?ref=firas. The connector is added to Claude with the URL
`https://mcp.blotato.com/mcp` (details in the README).

## 1. The right account

```
blotato_list_accounts(platform: "linkedin")
```

Use `blotato_linkedin_account_id` from `config.json`, and `blotato_linkedin_page_id` if it exists (post published on a
company page). If that id is no longer in the list, do not guess: in normal mode, ask which one to use; in auto mode,
stop with an error.

## 2. Upload the image

```
blotato_create_presigned_upload_url(filename: "<keyword>.png")
```

Then send the raw PNG bytes (no JSON, no multipart):

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: image/png" \
  --data-binary "@<project_folder>/linkedin-post-image.png" "<presignedUrl>"
curl -sI "<publicUrl>" | grep -iE "^(HTTP|content-type)"
```

Expected: `200`, then `200` and `image/png` on the public URL.

## 3. Publish or schedule

```
blotato_create_post(
  accountId: "<blotato_linkedin_account_id>",
  platform: "linkedin",
  text: "<exact text of linkedin-post.md, without the title line>",
  mediaUrls: ["<publicUrl>"]
)
```

Add `pageId` only if `config.json` has one. Without `scheduledTime`, the post goes out right away. To schedule, pass
`scheduledTime` (ISO 8601 with the time offset, e.g. `2026-11-22T08:00:00-05:00`).

The response gives `status` and `publicUrl`. If the status is `in-progress`, call `blotato_get_post_status` (at least
10 seconds between calls) until `published` or `failed`. Do not retry a failed post without understanding the error: a
second attempt risks a duplicate.

## 4. Report

| Network | Account | Status | ID |
|---|---|---|---|
| LinkedIn | <account name> (<id>) | Published / Scheduled for <time> | `<postSubmissionId>` |

Give the `publicUrl`. The browser often shows the LinkedIn login page on that link: say that the status comes from
Blotato and invite the user to check how the image looks in their feed.
