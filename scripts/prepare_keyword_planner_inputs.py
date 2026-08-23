#!/usr/bin/env python3
"""Create private, market-specific Keyword Planner input files."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "data" / "problem-discovery" / "query-seeds.csv"
PRIVATE_ROOT = ROOT / "data" / "private" / "keyword-planner"
INPUT_DIR = PRIVATE_ROOT / "inputs"
EXPORT_DIR = PRIVATE_ROOT / "exports"


def load_seeds() -> list[dict[str, str]]:
    with SEEDS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_market_files(market_id: str, rows: list[dict[str, str]]) -> None:
    txt_path = INPUT_DIR / f"{market_id}.txt"
    map_path = INPUT_DIR / f"{market_id}-mapping.csv"

    txt_path.write_text("\n".join(row["query"] for row in rows) + "\n", encoding="utf-8")
    with map_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("query_id", "problem_id", "intent", "keyword"),
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "query_id": row["query_id"],
                    "problem_id": row["problem_id"],
                    "intent": row["intent"],
                    "keyword": row["query"],
                }
            )


def main() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    seeds = load_seeds()
    markets = sorted({row["market_id"] for row in seeds})
    for market_id in markets:
        rows = [row for row in seeds if row["market_id"] == market_id]
        if len(rows) != 30:
            raise ValueError(f"{market_id}: expected 30 seeds, found {len(rows)}")
        write_market_files(market_id, rows)

    readme = PRIVATE_ROOT / "README.txt"
    readme.write_text(
        "HUMAN Keyword Planner private workspace\n\n"
        "inputs/: generated keyword lists and query-ID mappings\n"
        "exports/: save original Google Ads CSV downloads here\n\n"
        "Suggested export filename: YYYY-MM-DD-<market-id>.csv\n"
        "Do not move this directory into a tracked repository path.\n",
        encoding="utf-8",
    )

    print(f"Keyword Planner files created in {PRIVATE_ROOT}")
    for market_id in markets:
        print(f"  {market_id}: 30 keywords")


if __name__ == "__main__":
    main()
