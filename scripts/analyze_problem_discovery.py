#!/usr/bin/env python3
"""Report collection coverage for aggregate Problem Discovery signals."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "problem-discovery"


def load(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    markets = load("markets.csv")
    anchors = load("trend-anchors.csv")
    seeds = load("query-seeds.csv")
    signals = load("google-signals.csv")
    collected: dict[tuple[str, str], set[str]] = defaultdict(set)

    for row in signals:
        collected[(row["market_id"], row["source"])].add(row["query_id"])

    print("HUMAN Problem Discovery v1 collection coverage")
    print("=" * 74)
    print(f"{'Market':<12} {'Anchors':>8} {'Seeds':>7} {'Trends':>10} {'Planner':>10}")
    print("-" * 74)
    for market in markets:
        market_id = market["market_id"]
        market_seeds = {row["query_id"] for row in seeds if row["market_id"] == market_id}
        market_anchors = {row["anchor_id"] for row in anchors if row["market_id"] == market_id}
        trends = collected[(market_id, "google_trends")]
        planner = collected[(market_id, "keyword_planner")]
        print(
            f"{market_id:<12} {len(market_anchors):>8} {len(market_seeds):>7} "
            f"{len(trends):>10} {len(planner):>10}"
        )

    print("\nCounts show collection coverage only. They do not rank markets or problems.")

    directions: dict[str, Counter[str]] = defaultdict(Counter)
    for row in signals:
        if row["source"] == "google_trends":
            directions[row["market_id"]][row["trends_recent_direction"] or "missing"] += 1

    if directions:
        print("\nFive-year Trends direction screen")
        print("=" * 74)
        print(f"{'Market':<12} {'Rising':>8} {'Stable':>8} {'Falling':>8} {'Sparse':>8}")
        print("-" * 74)
        for market in markets:
            counts = directions[market["market_id"]]
            print(
                f"{market['market_id']:<12} {counts['rising']:>8} {counts['stable']:>8} "
                f"{counts['falling']:>8} {counts['insufficient']:>8}"
            )
        print("\nDirection compares the latest 26 weeks with the preceding 26 weeks.")
        print("Sparse anchors need a separate wording check; they are not evidence of zero demand.")


if __name__ == "__main__":
    main()
