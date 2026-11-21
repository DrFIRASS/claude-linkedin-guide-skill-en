# Scheduled task: “LinkedIn post links”

Optional. It fills the “Post link” column in Notion once the post is published.

- **Name**: LinkedIn post links
- **Frequency**: every day, 30 minutes after your publish time (e.g. 8:30 am)
- **Task text**:

```text
Short task, no questions.

1. Read the config.json of the linkedin-guide-post skill (in ~/.claude/skills/linkedin-guide-post/). Load with ToolSearch the Notion tools (notion-query-data-sources, notion-update-page) and the Blotato tool (blotato_get_post_status).
2. In the Notion data source notion_data_source from config.json, find the rows where “Status” = “Done”, “Blotato ID” is not empty and “Post link” is empty.
3. For each one, call blotato_get_post_status with postSubmissionId = “Blotato ID” (at least 10 seconds between calls):
   - status “published”: set “Post link” = the returned publicUrl;
   - status “scheduled” or “in-progress”: change nothing;
   - status “failed”: set “Status” = “Error” and “Error message” = “LinkedIn publishing failed: ” followed by Blotato's message.
4. Do not publish, schedule or delete any post. Do not touch any other column.

End with a one to three line report: links added, posts still scheduled, failures.
```
