# app/cli.py

import argparse
import asyncio
import json
from pathlib import Path
from typing import List, Dict

from rich.console import Console
from rich.table import Table
from app.providers.remoteok import fetch_remoteok_jobs
from app.core.scoring import score_gig, DEFAULT_PREFERENCES
from app.core.summaries import summarize_gig
from app.sources.remoteok import score_remote
from app.user_config import load_user_config, UserConfig

console = Console()

# -----------------------------
# Argument parsing
# -----------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="gig-agent CLI")

    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Number of gigs to fetch from each source",
    )
    parser.add_argument(
        "--out",
        type=str,
        help="Optional path to write raw gigs JSON (e.g., gigs.json)",
    )
    parser.add_argument(
        "--recommend",
        action="store_true",
        help="Score gigs and print top recommendations to stdout",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="How many top gigs to show when using --recommend",
    )
    parser.add_argument(
        "--table",
        action="store_true",
        help="Render recommendations as a Rich table UI",
    )
    parser.add_argument(
        "--remote-only",
        action="store_true",
        help="Filter results to remote/hybrid-friendly gigs only.",
    )
    parser.add_argument(
        "--profile",
        "-p",
        type=str,
        help="User profile name (e.g. 'cindy') to load preferences from configs/<profile>.json",
    )
    return parser.parse_args()


# -----------------------------
# Core fetch logic
# -----------------------------
async def fetch_gigs(limit: int, remote_only: bool = False) -> List[Dict]:
    """
    Fetch gigs from all sources (for now just RemoteOK, later we add others).

    If remote_only=True, filter to gigs that look remote/hybrid friendly
    using app.sources.remoteok.score_remote.
    """
    remoteok_gigs = await fetch_remoteok_jobs(limit=limit)

    if not remote_only:
        # later: add other sources and concatenate
        return remoteok_gigs

    filtered: List[Dict] = []

    for gig in remoteok_gigs:
        text_parts = [
            gig.get("title", ""),
            gig.get("company", ""),
            gig.get("description", ""),
            gig.get("location", ""),
        ]
        text = " ".join(p for p in text_parts if p)

        remote = score_remote(text)
        if not remote.is_remote_ok:
            # Skip non-remote / onsite-only gigs
            continue

        # Optional: attach metadata for debugging / later display
        gig["remote_meta"] = remote.to_dict()
        filtered.append(gig)

    return filtered


# -----------------------------
# Output helpers
# -----------------------------
def write_out(path_str: str, gigs: List[Dict]) -> None:
    path = Path(path_str)
    path.write_text(json.dumps(gigs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ OK  ] Wrote {len(gigs)} gigs to {path}")


def print_recommendations(gigs: List[Dict], top_n: int = 10) -> None:
    """
    Score gigs, sort, and print pretty summaries.
    """
    scored: List[Dict] = []
    for gig in gigs:
        s = score_gig(gig, DEFAULT_PREFERENCES)
        gig_with_score = {**gig, "score": s}
        scored.append(gig_with_score)

    scored.sort(key=lambda g: g["score"], reverse=True)
    top = scored[:top_n]

    print(f"\nTop {len(top)} gig recommendations:\n" + "-" * 60)
    for i, gig in enumerate(top, start=1):
        print(format_gig_summary(i, gig))
        print("-" * 60)


def print_recommendations_table(gigs: List[Dict], top_n: int = 10) -> None:
    """
    Pretty terminal UI using Rich to display top gigs in a table.
    """
    scored: List[Dict] = []
    for gig in gigs:
        s = score_gig(gig, DEFAULT_PREFERENCES)
        gig_with_score = {**gig, "score": s}
        scored.append(gig_with_score)

    scored.sort(key=lambda g: g["score"], reverse=True)
    top = scored[:top_n]

    if not top:
        console.print("[bold yellow]No gigs to display.[/bold yellow]")
        return

    table = Table(title=f"Top {len(top)} gig recommendations")

    table.add_column("#", style="bold cyan", justify="right")
    table.add_column("Title", style="bold")
    table.add_column("Company")
    table.add_column("Score", justify="right")
    table.add_column("Location")
    table.add_column("Salary")
    table.add_column("Summary", overflow="fold")
    table.add_column("Link", overflow="fold")

    for idx, gig in enumerate(top, start=1):
        title = gig.get("position") or gig.get("title") or "Untitled role"
        company = gig.get("company") or "Unknown"
        score = f"{gig.get('score', 0):.1f}"
        location = gig.get("location") or "Remote / Unspecified"
        salary = gig.get("salary") or "Not listed"
        link = gig.get("url") or "N/A"

        summary = summarize_gig(gig, max_length=140)

        table.add_row(
            str(idx),
            title,
            company,
            score,
            location,
            str(salary),
            summary,
            link,
        )

    console.print(table)


def format_gig_summary(idx: int, gig: Dict) -> str:
    title = gig.get("position") or gig.get("title") or "Untitled role"
    company = gig.get("company") or "Unknown company"
    score = gig.get("score", 0)
    url = gig.get("url") or "No URL"
    location = gig.get("location") or "Remote / Unspecified"
    salary = gig.get("salary") or "Not listed"

    tags = gig.get("tags") or []
    tags_str = ", ".join(tags) if tags else "No tags"

    summary = summarize_gig(gig)

    lines = [
        f"{idx}. {title} @ {company}",
        f"   Score: {score:.1f}",
        f"   Location: {location}",
        f"   Salary: {salary}",
        f"   Tags: {tags_str}",
        f"   Summary: {summary}",
        f"   Link: {url}",
    ]
    return "\n".join(lines)


# -----------------------------
# Main entrypoint
# -----------------------------
def main() -> None:
    args = parse_args()

    # 🔹 Try to load a user profile (e.g. configs/cindy.json)
    try:
        user_config = load_user_config(getattr(args, "profile", None))
    except FileNotFoundError as e:
        print(f"[warning] {e}")
        user_config = None

    async def _go():
        gigs = await fetch_gigs(limit=args.limit, remote_only=args.remote_only)

        # 🔹 Apply profile-based scoring if we have a config
        if user_config is not None:
            for gig in gigs:
                gig["score"] = score_gig(gig, user_config=user_config)
            gigs.sort(key=lambda g: g.get("score", 0), reverse=True)

        if args.out:
            write_out(args.out, gigs)

        if args.recommend:
            if args.table:
                print_recommendations_table(gigs, top_n=args.top)
            else:
                print_recommendations(gigs, top_n=args.top)
        elif not args.out:
            print(
                f"[INFO] Fetched {len(gigs)} gigs. "
                f"Use --out or --recommend to see details."
            )

    asyncio.run(_go())

if __name__ == "__main__":
    main()
