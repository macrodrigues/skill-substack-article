# 📰 Substack Publish Article

> Publish markdown articles to Substack automatically using browser automation — no APIs, no tokens, powered by [cloakbrowser](https://cloakbrowser.dev/) ✨

![Substack article](https://i.ibb.co/VcVDgXyk/Screenshot-From-2026-05-11-12-11-05.png)

---

## 🚀 What It Does

This skill lets you publish a markdown article directly to your Substack newsletter. It:

1. 🌐 Opens Substack in a browser launched via **cloakbrowser**
2. 🔐 Logs in with your credentials
3. 📝 Creates a new **Article** draft from your `.md` file
4. 🎯 Fills in the title, subtitle, and body
5. 📤 Publishes with **"Send to everyone now"**

Perfect for newsletter writers who want to stay in markdown but ship to Substack 🚀

---

## 📦 Prerequisites

- Python 3.x
- Dependencies installed from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```
  > Installs: `cloakbrowser`, `markdown`
- A working **cloakbrowser** setup on the machine (see the package docs for browser/runtime requirements — `publish.py` uses `launch` from `cloakbrowser`)

---

## 🔑 Credentials Setup

Before running, set these **environment variables** in your `.env` or shell:

| Variable | Description | Example |
|----------|-------------|---------|
| `SUBSTACK_EMAIL` | Your Substack login email | `you@example.com` |
| `SUBSTACK_PASSWORD` | Your Substack password | `supersecret123` |
| `SUBSTACK_URL` | Your publication entry URL | `https://substack.com/@yourhandle` |

⚠️ **Never commit these values or paste them into chat!** Keep them in your `.env` file only.

---

## 📝 Article Markdown Format

Your markdown file must follow this structure:

```markdown
# Post Title Here

## Subtitle shown under the title on Substack

Body starts here. You can use **bold**, *italic*, lists, and any other markdown.

### More headings are fine in the body

Everything after the first `##` subtitle line becomes the article body.
```

### Rules

- ✅ **Title**: exactly one `# ` heading at the top
- ✅ **Subtitle**: the first `## ` line after the title
- ✅ **Body**: everything after the subtitle → converted to HTML
- ✅ Optional UTF-8 BOM at start is fine
- ✅ Encoding: UTF-8

---

## 🖥️ Usage

### Default article (`article.md` next to `publish.py`)

```bash
cd substack-publish-article
python publish.py
```

### Custom article path

```bash
python publish.py /path/to/your-article.md
```

### From repo root

```bash
python substack-publish-article/publish.py substack-publish-article/article.md
python substack-publish-article/publish.py /path/to/any-article.md
```

---

## ✅ Pre-Flight Checklist

- [ ] Markdown has a `# ` title
- [ ] Markdown has a `## ` subtitle
- [ ] `SUBSTACK_EMAIL`, `SUBSTACK_PASSWORD`, and `SUBSTACK_URL` are set in the environment
- [ ] You understand this will **live publish** to all subscribers (not save as draft)
- [ ] Article path is correct (or using default `article.md`)

---

## ⚠️ Fragility Notice

Substack's UI strings and selectors can change without warning. If the script fails:

1. Open `publish.py`
2. Inspect `fill_article_from_markdown` and the `get_by_role` / locator calls
3. Update them to match the current Substack editor

---

## 🗂️ File Layout

```
substack-publish-article/
├── publish.py           # Main automation script
├── requirements.txt     # Python dependencies
├── SKILL.md             # Hermes agent skill definition
└── README.md            # This file ✨
```

---

## 🙋 FAQ

**Q: Does this create drafts or publish immediately?**
A: It publishes immediately with "Send to everyone now" and "Publish without buttons". This is a **live publish** — be careful!

**Q: Can I schedule posts?**
A: Not yet — the skill currently publishes instantly. Scheduling would require extending `publish.py`.

**Q: What if I have 2FA enabled?**
A: The script may not handle 2FA prompts. You might need to disable 2FA or extend the script to wait for the 2FA code.

---

Happy publishing! 🎉✍️
