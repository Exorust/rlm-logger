"""Render docs/hero/hero.html to docs/img/hero.png at 1600x840 @ 2x."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "docs" / "hero" / "hero.html"
OUT = ROOT / "docs" / "img" / "hero.png"


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1600, "height": 840},
            device_scale_factor=2,
        )
        page = context.new_page()
        page.goto(HTML.as_uri())
        page.wait_for_load_state("networkidle")
        page.screenshot(path=str(OUT), omit_background=False, full_page=False)
        browser.close()

    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
