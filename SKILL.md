---
name: substack-publish-article
description: >-
  Publishes a Substack post from a local markdown file using Camoufox browser
  automation and substack-publish-article/publish.py. Use when the user wants
  to publish or schedule automation for Substack, run publish.py, or push an
  article .md file live to their newsletter.
disable-model-invocation: true
---

# Publish articles on Substack

## What runs

From the repository root (or any working directory), execute `publish.py` in `substack-publish-article/`. The script opens Substack in a browser, signs in, creates an **Article** draft from the markdown, then publishes with **Send to everyone now** and **Publish without buttons** (see script for exact flow).

## Prerequisites

- Python environment with dependencies from `substack-publish-article/requirements.txt` (`camoufox`, `markdown`).
- Camoufox/browser setup that `AsyncCamoufox` expects on the machine (same as a normal run of this script).

## Credentials (required)

Set before running (never commit values or echo them in chat):

| Variable | Meaning |
|----------|---------|
| `SUBSTACK_EMAIL` | Substack sign-in email |
| `SUBSTACK_PASSWORD` | Account password |
| `SUBSTACK_URL` | Publication entry URL, e.g. `https://substack.com/@yourhandle` |

## Article markdown format

The file must match what `parse_article_md` in `publish.py` expects:

1. **Title**: exactly one top-level heading as the first `# ` line (not `##`).
2. **Subtitle**: the first `## ` line after the title; its text becomes the Substack subtitle field.
3. **Body**: everything after that subtitle line is converted to HTML (Markdown extensions: `extra`, `sane_lists`, `nl2br`). Additional `##` / `###` sections in the body are normal body content.

Optional UTF-8 BOM at the start is fine. Encoding: UTF-8.

Example layout (repo sample: `substack-publish-article/article.md`):

```markdown
# Post title here

## Subtitle shown under the title on Substack

Body starts here. More **markdown** and headings below as needed.
```

If the user supplies a path to any other `.md` file, use that path as the single positional argument.

## Command

Default article path inside the package is `substack-publish-article/article.md` when no file is passed.

```bash
cd /path/to/substack-automate-post/substack-publish-article
python publish.py /absolute/or/relative/path/to/article.md
```

Or from repo root:

```bash
python substack-publish-article/publish.py substack-publish-article/article.md
python substack-publish-article/publish.py /path/to/any-article.md
```

Omit the positional argument to use `substack-publish-article/article.md` next to `publish.py`.

## Agent checklist

- [ ] Confirm the markdown has `# ` title and first `## ` subtitle before running.
- [ ] Use the user-provided article path when they give one; otherwise default `article.md` or ask which file to publish.
- [ ] Ensure `SUBSTACK_EMAIL`, `SUBSTACK_PASSWORD`, and `SUBSTACK_URL` are set in the shell for the run (do not paste secrets into rules or commits).
- [ ] Treat a successful run as **live publish** to subscribers (per script: send to everyone, publish). Warn the user if that is not what they want.

## Fragility

Substack’s UI strings and selectors can change; if steps fail, inspect `fill_article_from_markdown` and the `get_by_role` / locator calls in `publish.py` against the current editor.
