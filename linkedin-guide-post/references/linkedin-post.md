# The “FREE access 👇” LinkedIn post

## Why this format

LinkedIn reduces the reach of posts that ask for comments (“comment below”, “drop the keyword”, “type X”). So the text
never asks for a comment: it shows the value, lists what the reader gets, then ends with “FREE access! 👇”. The
COMMENT “KEYWORD” call appears **only in the image**, which LinkedIn does not read as text.

## Structure, in this order

1. **Hook** (2 lines): a concrete action in the first person, then the result in numbers, using the real numbers of the
   PDF. “I put everything I have Claude do for my marketing into one guide. / 10 chapters, 42 ready-to-copy prompts,
   35 pages.”
2. **The reader's problem** in 2 or 3 very short lines, then the reframe “The problem isn't X. / It's Y.” and a
   contrasting sentence.
3. **“What changes in practice:”** then 4 or 5 “→” lines, each with the real name of a feature or a step.
4. **“What you get:”** then 3 or 4 “→” lines. The last one is the honesty note (a limit, what the guide does not promise).
5. **Before / After**, one line each. No made-up numbers: if there is no real measurement, stay qualitative.
6. **Closing** of one or two lines that sums up the idea.
7. **Ending, always:**
   ```
   FREE access! 👇
   Reposts get top priority. ♻️
   ```

## Rules

- Never the words “comment”, “comments”, “type”, “drop”, “like”, “share” in the text, and no keyword to post.
- No link in the post, no first comment: access goes out by direct message.
- “→” lists of 5 lines at most. No closing question. No hashtags, or 2 at most right before “FREE access”.
- Talk to the reader as “you”, short sentences, one idea per line, no em dash, no empty marketing words.
- The numbers (chapters, prompts, pages, checkpoints) are the ones returned by `build_guide.py`.
- Length: 900 to 1,500 characters. Count them: `sed -n '3,$p' linkedin-post.md | wc -m`.

## Approved example (MARKETING guide)

The full text is in `assets/example-marketing/linkedin-post.md`. The French version of this post was published with the
PDF viewer image, created and published entirely by Claude: more than 10,000 impressions.

## Direct message to send to each person who comments

The PDF is in the guide's local folder. The user chooses how to share it: attachment in the LinkedIn message, or a
link (Google Drive, Notion, Dropbox, their website). Offer both versions:

```text
Here's your access to [short guide title]: [PDF link]
Start with chapter 00, it takes 10 minutes.
```

```text
Here's [short guide title], attached 👆
Start with chapter 00, it takes 10 minutes.
```
