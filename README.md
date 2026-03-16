# Emily S. Burch — Portfolio Site

Personal portfolio and resume site, deployed via GitHub Pages.

**Live site:** https://esburch.github.io/

## Pages

| File | URL | Description |
|------|-----|-------------|
| `index.html` | `/` | Landing page with nav cards |
| `resume.html` | `/resume.html` | Full resume (also print-friendly) |
| `projects.html` | `/projects.html` | Code examples and project samples |

## Local Development

No build step. Open `index.html` directly in a browser, or use the VS Code Live Preview extension:

1. Open the workspace: `landing-zone.code-workspace`
2. Install the recommended extensions when prompted (`ms-vscode.live-server`)
3. Click **Go Live** in the status bar

## Deployment

Pushes to `master` automatically deploy via GitHub Actions (`.github/workflows/deploy.yml`).

To enable on a new repo: **Settings → Pages → Source → GitHub Actions**

## Structure

```
index.html          Landing page
resume.html         Resume
projects.html       Projects / code examples
style.css           Single shared stylesheet (all pages)
landing-zone.code-workspace   VS Code workspace config
```

All pages are self-contained HTML with no JavaScript or external dependencies beyond Google Fonts.
