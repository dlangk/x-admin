#!/usr/bin/env python3
"""Generate a PDF of @langkilde's X following, organized by list."""

import re
from pathlib import Path

# --- Parse following.txt ---
following: dict[str, str] = {}  # handle_lower -> "@handle — Display Name"
for line in Path("following.txt").read_text().splitlines():
    line = line.strip()
    if not line:
        continue
    # format: @handle — Display Name
    m = re.match(r"(@\S+)\s+—\s+(.*)", line)
    if m:
        following[m.group(1).lower()] = f"{m.group(1)} — {m.group(2)}"

# --- Parse lists.md ---
lists: list[tuple[str, str, list[str]]] = []  # (name, description, [handles])
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

# --- Find uncategorized accounts ---
all_listed: set[str] = set()
for _, _, handles in lists:
    for h in handles:
        all_listed.add(h.lower())

uncategorized = []
for handle_lower, entry in sorted(following.items(), key=lambda x: x[1].lower()):
    if handle_lower not in all_listed:
        uncategorized.append(entry)

# --- Build text content ---
lines: list[str] = []
lines.append("@langkilde X (Twitter) Following — Organized by List")
lines.append(f"Generated: 2026-03-29")
lines.append(f"Total following: {len(following)}")
lines.append("")
lines.append("=" * 60)

for name, desc, handles in lists:
    lines.append("")
    lines.append(f"LIST: {name}")
    lines.append(f"Description: {desc}")
    lines.append(f"Members: {len(handles)}")
    lines.append("-" * 40)
    for h in sorted(handles, key=str.lower):
        entry = following.get(h.lower())
        if entry:
            lines.append(f"  {entry}")
        else:
            lines.append(f"  {h} (not currently followed)")
    lines.append("")

lines.append("=" * 60)
lines.append("")
lines.append(f"UNCATEGORIZED ({len(uncategorized)} accounts)")
lines.append("Accounts followed but not assigned to any list.")
lines.append("-" * 40)
for entry in uncategorized:
    lines.append(f"  {entry}")

text = "\n".join(lines)

# --- Write PDF using reportlab ---
try:
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
        # Handle lines that might be too long
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
    print(f"PDF written to {pdf_path}")

except ImportError:
    # Fallback: write text file and convert with another method
    Path("following-by-list.txt").write_text(text)
    print("reportlab not available, wrote following-by-list.txt instead")
