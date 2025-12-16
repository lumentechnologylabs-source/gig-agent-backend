from __future__ import annotations
from pathlib import Path
import json
import csv
from typing import Sequence, Mapping, Any, Iterable


def _to_path(path: str | Path) -> Path:
    return Path(path)


def save_json(listings: Sequence[Mapping[str, Any]], path: str | Path) -> None:
    """
    Save listings as pretty-printed JSON.
    """
    p = _to_path(path)
    p.write_text(
        json.dumps(listings, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[export] JSON      → {p}")


def save_csv(listings: Sequence[Mapping[str, Any]], path: str | Path) -> None:
    """
    Save listings as a flat CSV. We collect all keys that appear in any listing
    and use them as columns.
    """
    p = _to_path(path)

    if not listings:
        p.write_text("", encoding="utf-8")
        print(f"[export] CSV       → {p} (no rows)")
        return

    # union of keys across all listings
    fieldnames = sorted({key for item in listings for key in item.keys()})

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in listings:
            row = {k: item.get(k, "") for k in fieldnames}
            writer.writerow(row)

    print(f"[export] CSV       → {p}")


def save_md(listings: Sequence[Mapping[str, Any]], path: str | Path) -> None:
    """
    Save listings as a Markdown report, roughly human-readable.
    """
    p = _to_path(path)

    lines: list[str] = ["# Gig Agent Results", ""]

    for i, item in enumerate(listings, start=1):
        title = item.get("title", "(no title)")
        company = item.get("company", "")
        location = item.get("location", "")
        url = item.get("url", "")
        source = item.get("source", "")
        score = item.get("score")

        lines.append(f"## {i}. {title}")

        meta_bits = []
        if company:
            meta_bits.append(company)
        if location:
            meta_bits.append(location)
        if source:
            meta_bits.append(f"[{source}]")

        if meta_bits:
            lines.append("**" + " • ".join(meta_bits) + "**")

        if score is not None:
            lines.append(f"_Score: {score}_")

        if url:
            lines.append(f"[View listing]({url})")

        lines.append("")  # blank line between entries

    p.write_text("\n".join(lines), encoding="utf-8")
    print(f"[export] Markdown  → {p}")
