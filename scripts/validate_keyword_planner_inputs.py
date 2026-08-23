#!/usr/bin/env python3
"""Verify generated private Keyword Planner inputs against public seed IDs."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "data" / "problem-discovery" / "query-seeds.csv"
INPUT_DIR = ROOT / "data" / "private" / "keyword-planner" / "inputs"


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    seeds = csv_rows(SEEDS)
    markets = sorted({row["market_id"] for row in seeds})

    for market_id in markets:
        expected = [row for row in seeds if row["market_id"] == market_id]
        text_keywords = (INPUT_DIR / f"{market_id}.txt").read_text(encoding="utf-8").splitlines()
        mapping = csv_rows(INPUT_DIR / f"{market_id}-mapping.csv")

        if text_keywords != [row["query"] for row in expected]:
            raise ValueError(f"{market_id}: text input does not match canonical seeds")
        if [row["query_id"] for row in mapping] != [row["query_id"] for row in expected]:
            raise ValueError(f"{market_id}: mapping IDs do not match canonical seeds")
        if [row["keyword"] for row in mapping] != text_keywords:
            raise ValueError(f"{market_id}: mapping keywords do not match text input")
        if len(set(text_keywords)) != 30:
            raise ValueError(f"{market_id}: expected 30 unique keywords")

    print("HUMAN Keyword Planner private inputs: OK")
    print(f"Markets: {len(markets)} | Keywords: {len(seeds)}")


if __name__ == "__main__":
    main()
