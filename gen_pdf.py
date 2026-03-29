#!/usr/bin/env python3
"""Generate a PDF of @langkilde's X following, organized by list. Excludes personal list."""

import re
from pathlib import Path

EXCLUDE_LISTS = {"personal"}

# --- Parse lists.md ---
lists: list[tuple[str, str, list[str]]] = []
current_name = ""
current_desc = ""
current_handles: list[str] = []

for line in Path("lists.md").read_text().splitlines():
    if line.startswith("## "):
        if current_name:
            lists.append((current_name, current_desc, current_handles))
        current_name = line[3:].strip()
        current_desc = ""
        current_handles = []
    elif current_name and not current_desc and line.strip() and not line.startswith("#") and not line.startswith("---"):
        current_desc = line.strip()
    elif current_name and line.strip().startswith("@"):
        handles = [h.strip() for h in line.split(",") if h.strip()]
        current_handles.extend(handles)

if current_name:
    lists.append((current_name, current_desc, current_handles))

# Filter out excluded lists
lists = [(n, d, h) for n, d, h in lists if n not in EXCLUDE_LISTS]

# --- Build text ---
total_unique: set[str] = set()
lines: list[str] = []
lines.append("@langkilde X (Twitter) Following — Organized by List")
lines.append("Generated: 2026-03-29")
lines.append("")

for name, desc, handles in lists:
    total_unique.update(h.lower() for h in handles)
    lines.append("=" * 60)
    lines.append(f"  {name} ({len(handles)})")
    lines.append(f"  {desc}")
    lines.append("=" * 60)
    for h in sorted(handles, key=str.lower):
        lines.append(f"  {h}")
    lines.append("")

lines.insert(2, f"Total: {len(total_unique)} unique accounts (excl. personal)")
lines.append("")

text = "\n".join(lines)

# --- Write PDF ---
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

pdf_path = "following-by-list.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4
margin = 20 * mm
y = height - margin
line_height = 12
font_size = 9

c.setFont("Courier", font_size)

for line in text.split("\n"):
    while len(line) > 90:
        c.drawString(margin, y, line[:90])
        y -= line_height
        line = "  " + line[90:]
        if y < margin:
            c.showPage()
            c.setFont("Courier", font_size)
            y = height - margin

    c.drawString(margin, y, line)
    y -= line_height

    if y < margin:
        c.showPage()
        c.setFont("Courier", font_size)
        y = height - margin

c.save()
print(f"PDF written to {pdf_path} ({len(total_unique)} unique accounts)")
