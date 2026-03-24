#!/usr/bin/env python3
"""Generate resume.pdf from resume.html using headless Chromium via Playwright.

Usage:
    pip install playwright
    playwright install --with-deps chromium
    python scripts/build_pdf.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
HTML = ROOT / "resume.html"
PDF = ROOT / "resume.pdf"


def main():
    if not HTML.exists():
        raise FileNotFoundError(f"{HTML} not found — run build_resume.py first")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # networkidle waits for web fonts (Google Fonts) to finish loading
        page.goto(HTML.resolve().as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(PDF),
            format="Letter",
            print_background=False,
            margin={
                "top": "0.5in",
                "bottom": "0.5in",
                "left": "0.75in",
                "right": "0.75in",
            },
        )
        browser.close()

    print(f"Built {PDF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
