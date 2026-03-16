# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development

No build step — this is a static HTML/CSS site. Open `index.html` directly in a browser, or use the VS Code Live Preview extension (`ms-vscode.live-server`) configured in `landing-zone.code-workspace`.

To deploy, push to a GitHub repo and enable GitHub Pages (Settings → Pages → source: `master` branch, root `/`).

## Architecture

Single shared stylesheet (`style.css`) used by all three pages. It defines two layout modes via CSS classes:

- **`body` centered layout** — used by `index.html` for the card grid landing page
- **`.page` container** — used by `resume.html` and `projects.html` for content pages with a back link

All pages are self-contained HTML files with no JavaScript or build tooling.

## Content to Personalize

- `index.html` — name, tagline, GitHub URL (already updated to `github.com/esburch`)
- `resume.html` — contact info, work history, education, skills
- `projects.html` — project names, descriptions, tech stack tags, GitHub/demo links
