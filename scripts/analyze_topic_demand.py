#!/usr/bin/env python3
"""Summarize HUMAN Topic Demand experiment aggregate metrics.

Reads only the public aggregate table in data/topic-demand-summary.csv.
Raw visitor/session exports should never be committed to this repository.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "topic-demand-summary.csv"

COUNT_FIELDS = (
    "impressions",
    "clicks",
    "article_views",
    "engaged_30s",
    "read_50pct",
    "completions",
    "next_article_clicks",
)


def parse_count(value: str):
    value = (value or "").strip()
    return None if value == "" else int(value)


def rate(num, den):
    if num is None or den in (None, 0):
        return None
    return 100.0 * num / den


def fmt(value):
    return "—" if value is None else f"{value:.1f}%"


with DATA.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

print("HUMAN Topic Demand summary")
print("=" * 108)
print(f"{'Feature':<12} {'Topic':<30} {'Impr.':>7} {'CTR':>8} {'30s':>8} {'50% read':>10} {'Complete':>10} {'Next':>8}")
print("-" * 108)

for row in rows:
    counts = {field: parse_count(row.get(field, "")) for field in COUNT_FIELDS}
    ctr = rate(counts["clicks"], counts["impressions"])
    engaged = rate(counts["engaged_30s"], counts["article_views"])
    read_50 = rate(counts["read_50pct"], counts["article_views"])
    complete = rate(counts["completions"], counts["article_views"])
    next_rate = rate(counts["next_article_clicks"], counts["article_views"])
    impressions = "—" if counts["impressions"] is None else str(counts["impressions"])
    print(
        f"{row['feature_id']:<12} {row['topic'][:30]:<30} {impressions:>7} "
        f"{fmt(ctr):>8} {fmt(engaged):>8} {fmt(read_50):>10} {fmt(complete):>10} {fmt(next_rate):>8}"
    )

print("\nInterpretation: rank attraction and reading quality separately; do not choose a winner from pageviews alone.")
