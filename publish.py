import argparse
import asyncio
import os
from pathlib import Path

from camoufox import AsyncCamoufox

import markdown

_SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ARTICLE_PATH = _SCRIPT_DIR / "article.md"


def parse_article_md(text: str) -> tuple[str, str, str]:
    """Split markdown into title (#), first subtitle (##), and remaining body."""
    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    title = ""
    title_idx: int | None = None
    for i, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            title_idx = i
            break
    if title_idx is None:
        raise ValueError("article.md: missing top-level # title")
    for j in range(title_idx + 1, len(lines)):
        line = lines[j]
        if line.startswith("## "):
            subtitle = line[3:].strip()
            body_lines = lines[j + 1 :]
            while body_lines and not body_lines[0].strip():
                body_lines.pop(0)
            return title, subtitle, "\n".join(body_lines)
    raise ValueError("article.md: missing ## subtitle")


def article_body_to_html(body_md: str) -> str:
    return markdown.markdown(
        body_md,
        extensions=["extra", "sane_lists", "nl2br"],
    )


async def paste_html_into_editor(page, html: str) -> None:
    """Insert HTML into TipTap/ProseMirror (no Clipboard API — Firefox/Camoufox
    does not support Playwright's clipboard-* grant_permissions)."""
    editor = page.locator('[data-testid="editor"]')
    await editor.wait_for(state="visible")
    await editor.click()
    await page.keyboard.press("Control+a")
    await page.keyboard.press("Backspace")

    await editor.evaluate(
        """(el, html) => {
            el.focus();
            const range = document.createRange();
            range.selectNodeContents(el);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            document.execCommand('insertHTML', false, html);
        }""",
        html,
    )


async def fill_article_from_markdown(page, article_path: Path) -> None:
    raw = article_path.read_text(encoding="utf-8-sig")
    title, subtitle, body_md = parse_article_md(raw)
    body_html = article_body_to_html(body_md)

    await page.locator("#post-title").wait_for(state="visible")
    await page.locator("#post-title").fill(title)

    subtitle_box = page.get_by_placeholder("Add a subtitle…")
    await subtitle_box.fill(subtitle)

    await paste_html_into_editor(page, body_html)


async def main(username: str, password: str, url: str, article_path: Path | None = None):
    """Automate posts on Substack"""
    path = article_path or DEFAULT_ARTICLE_PATH

    async with AsyncCamoufox(
        os="windows",
        humanize=True,  # Enable humanized cursor movement
        headless=True,  # Keep visible for debugging
        window=(1280, 720),  # Set window size
    ) as browser:

        # create a page
        page = await browser.new_page()

        # go to the page
        await page.goto(url, wait_until="domcontentloaded")

        # click create post button (accessible name from aria-label + text)
        await page.get_by_role("button", name="Create").first.click()

        # sign in with password
        await page.get_by_role("button", name="Sign in with password").first.click()

        # input username
        await page.get_by_role("textbox", name="Email").first.fill(username)

        # input password
        await page.get_by_role("textbox", name="Password").first.fill(password)

        # click continue button
        await page.get_by_role("button", name="Continue").first.click()

        await page.wait_for_timeout(3000)

        # click create post button
        await page.locator("button[aria-label='Create']").first.click()

        # select article (Radix menu item)
        await page.get_by_role("menuitem", name="Article").click()

        await page.wait_for_timeout(3000)        

        await fill_article_from_markdown(page, path)

        # click continue button
        await page.get_by_role("button", name="Continue").first.click()

        # click sent to everyone
        await page.get_by_role(
            "button", name="Send to everyone now").first.click()

        await page.wait_for_timeout(5000)

        # publish withhout buttons
        await page.get_by_role(
            "button", name="Publish without buttons").first.click()

        await page.wait_for_timeout(5000)            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Publish a Substack article from a markdown file (browser automation).",
    )
    parser.add_argument(
        "article",
        nargs="?",
        type=Path,
        default=None,
        help=f"path to article markdown (default: {DEFAULT_ARTICLE_PATH})",
    )
    args = parser.parse_args()
    article_path = args.article.resolve() if args.article is not None else None
    if article_path is not None and not article_path.is_file():
        raise SystemExit(f"Article file not found: {article_path}")

    username = os.environ.get("SUBSTACK_EMAIL", "").strip()
    password = os.environ.get("SUBSTACK_PASSWORD", "")
    url = os.environ.get("SUBSTACK_URL", "").strip()
    if not username or not password or not url:
        raise SystemExit(
            "Set SUBSTACK_EMAIL, SUBSTACK_PASSWORD, and SUBSTACK_URL "
            "(Substack sign-in email, password, and publication URL, e.g. https://substack.com/@yourhandle)."
        )

    asyncio.run(
        main(username=username, password=password, url=url, article_path=article_path)
    )
