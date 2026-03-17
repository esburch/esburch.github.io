#!/usr/bin/env python3
"""
Build resume.html from resume-content/current/EmilyBurch.md + resume.template.html

Usage:
    python scripts/build_resume.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEMPLATE = ROOT / "resume.template.html"
MARKDOWN = ROOT / "resume-content" / "current" / "EmilyBurch.md"
OUTPUT = ROOT / "resume.html"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc(text):
    """HTML-escape plain text."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def linkify(text):
    """Auto-link phone numbers, emails, and bare domain URLs in plain text."""
    # Phone: (xxx) xxx-xxxx
    def phone_sub(m):
        digits = re.sub(r"\D", "", m.group(0))
        return f'<a href="tel:+1{digits}">{m.group(0)}</a>'
    text = re.sub(r"\(\d{3}\) \d{3}-\d{4}", phone_sub, text)

    # Email
    text = re.sub(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        lambda m: f'<a href="mailto:{m.group(0)}">{m.group(0)}</a>',
        text,
    )

    # Bare URLs: linkedin.com/... github.com/... (no https:// prefix in source)
    text = re.sub(
        r"(?<![\"'=@])\b((?:linkedin|github)\.com/[^\s|,<>]*)",
        lambda m: f'<a href="https://{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>',
        text,
    )

    return text


def normalize_date(d):
    """Replace plain hyphens used as date range dashes with en-dashes."""
    return re.sub(r"\s*-\s*", "\u2013", d.strip())


# ---------------------------------------------------------------------------
# Parser — handles the markdown format used in EmilyBurch.md
# ---------------------------------------------------------------------------

def parse(md):
    lines = md.splitlines()
    i = 0

    # --- Name ---
    assert lines[i].startswith("# "), "First line must be '# Name'"
    name = lines[i][2:].strip()
    i += 1

    # --- Contact lines (before first --- or ## ) ---
    contact = []
    while i < len(lines) and not lines[i].startswith("---") and not lines[i].startswith("## "):
        l = lines[i].strip()
        if l:
            contact.append(l)
        i += 1

    # --- Sections ---
    sections = []
    current = None

    while i < len(lines):
        line = lines[i]

        if line.startswith("---"):
            i += 1
            continue

        if line.startswith("## "):
            if current:
                sections.append(current)
            current = {"title": line[3:].strip(), "entries": [], "body": []}
            i += 1
            continue

        if current is None:
            i += 1
            continue

        title = current["title"]

        if title == "Summary":
            l = line.strip()
            if l:
                current["body"].append(l)
            i += 1

        elif title == "Work Experience":
            # Entry header: **Company** - Job Title
            m = re.match(r"^\*\*([^*]+)\*\*\s*[-\u2013]\s*(.+)$", line)
            if m:
                entry = {
                    "company": m.group(1).strip(),
                    "title": m.group(2).strip(),
                    "date": "",
                    "location": "",
                    "team": "",
                    "bullets": [],
                }
                i += 1
                # Date line: "03/2015 - 11/2017" or "11/2017 - 03/2026 (remote)"
                if i < len(lines):
                    dm = re.match(r"^([\d/]+\s*[-\u2013]\s*[\d/]+)\s*(?:\(([^)]*)\))?$", lines[i].strip())
                    if dm:
                        entry["date"] = normalize_date(dm.group(1))
                        entry["location"] = dm.group(2) or ""
                        i += 1
                # Team line: *Team Name*
                if i < len(lines):
                    tm = re.match(r"^\*([^*]+)\*$", lines[i].strip())
                    if tm:
                        entry["team"] = tm.group(1).strip()
                        i += 1
                current["entries"].append(entry)
            elif line.startswith("- ") and current["entries"]:
                current["entries"][-1]["bullets"].append(line[2:].strip())
                i += 1
            else:
                i += 1

        elif title == "Skills":
            l = line.strip()
            if l:
                m = re.match(r"^\*\*([^*]+?):\*\*\s*(.*)", l)
                if m:
                    current["entries"].append({"label": m.group(1).strip(), "value": m.group(2).strip()})
            i += 1

        elif title == "Education":
            m = re.match(r"^\*\*([^*]+)\*\*\s*[-\u2013]\s*(.+)$", line)
            if m:
                entry = {"school": m.group(1).strip(), "location": m.group(2).strip(), "degree": "", "date": ""}
                i += 1
                if i < len(lines):
                    dl = lines[i].strip()
                    if "|" in dl:
                        parts = dl.rsplit("|", 1)
                        entry["degree"] = parts[0].strip()
                        entry["date"] = parts[1].strip()
                    else:
                        entry["degree"] = dl
                    i += 1
                current["entries"].append(entry)
            else:
                i += 1

        else:
            i += 1

    if current:
        sections.append(current)

    return name, contact, sections


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------

def render_contact(contact):
    """
    Render contact lines. Items within a line are | -separated and joined
    with ·. Lines are joined with <br>.
    """
    rendered = []
    for line in contact:
        parts = [linkify(esc(p.strip())) for p in line.split("|")]
        rendered.append(" \u00b7 ".join(parts))
    return ' <br>\n    '.join(rendered)


def render(name, contact, sections):
    out = []

    out.append(f"    <h1>{esc(name)}</h1>")
    out.append(f'    <p class="subtitle">{render_contact(contact)}</p>')

    for sec in sections:
        out.append("")
        out.append('    <div class="section">')
        out.append(f"      <h2>{esc(sec['title'])}</h2>")

        if sec["title"] == "Summary":
            text = " ".join(sec["body"])
            out.append(f'      <p class="section-body">{esc(text)}</p>')

        elif sec["title"] == "Skills":
            out.append('      <div class="skill-list">')
            for e in sec["entries"]:
                out.append('        <div class="skill-row">')
                out.append(f'          <span class="skill-label">{esc(e["label"])}</span>')
                out.append(f'          <span>{esc(e["value"])}</span>')
                out.append("        </div>")
            out.append("      </div>")

        elif sec["title"] == "Work Experience":
            for e in sec["entries"]:
                org_parts = [e["company"]]
                if e["team"]:
                    org_parts.append(e["team"])
                if e["location"]:
                    org_parts.append(e["location"].capitalize())
                org = " \u00b7 ".join(org_parts)

                out.append('      <div class="entry">')
                out.append('        <div class="entry-header">')
                out.append(f'          <h3>{esc(e["title"])}</h3>')
                if e["date"]:
                    out.append(f'          <span class="date">{esc(e["date"])}</span>')
                out.append("        </div>")
                out.append(f'        <div class="org">{esc(org)}</div>')
                if e["bullets"]:
                    out.append("        <ul>")
                    for b in e["bullets"]:
                        out.append(f"          <li>{esc(b)}</li>")
                    out.append("        </ul>")
                out.append("      </div>")

        elif sec["title"] == "Education":
            for e in sec["entries"]:
                org = f'{e["school"]} \u00b7 {e["location"]}' if e["location"] else e["school"]
                out.append('      <div class="entry">')
                out.append('        <div class="entry-header">')
                out.append(f'          <h3>{esc(e["degree"])}</h3>')
                if e["date"]:
                    out.append(f'          <span class="date">{esc(e["date"])}</span>')
                out.append("        </div>")
                out.append(f'        <div class="org">{esc(org)}</div>')
                out.append("      </div>")

        out.append("    </div>")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MARKDOWN.exists():
        print(
            f"ERROR: {MARKDOWN} not found.\n"
            "Did you run: git submodule update --init --recursive?",
            file=sys.stderr,
        )
        sys.exit(1)

    md = MARKDOWN.read_text(encoding="utf-8")
    name, contact, sections = parse(md)
    content = render(name, contact, sections)

    template = TEMPLATE.read_text(encoding="utf-8")
    output = template.replace("<!-- RESUME_CONTENT -->", content)
    OUTPUT.write_text(output, encoding="utf-8")
    print(f"Built {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
