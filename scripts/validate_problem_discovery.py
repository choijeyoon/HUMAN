#!/usr/bin/env python3
"""Validate public inputs for HUMAN Problem Discovery v1."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "problem-discovery"

EXPECTED_MARKETS = {"ja-jp", "en-us", "es-es", "es-mx"}
EXPECTED_INTENTS = {"experience", "explanation", "solution"}
VALID_SEED_STATUS = {"unvalidated", "validated", "rejected"}
VALID_SOURCES = {"google_trends", "keyword_planner"}
VALID_WINDOWS = {"latest_12_months", "latest_5_years"}
VALID_DIRECTIONS = {"rising", "stable", "falling", "event_spike", "insufficient"}
URL_OR_EMAIL = re.compile(r"https?://|www\.|\b[^\s@]+@[^\s@]+\.[^\s@]+\b", re.IGNORECASE)


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows and name != "google-signals.csv":
        raise ValueError(f"{name}: expected at least one row")
    return rows


def require_unique(rows: list[dict[str, str]], field: str, label: str) -> None:
    counts = Counter(row[field] for row in rows)
    duplicates = sorted(value for value, count in counts.items() if count > 1)
    if duplicates:
        raise ValueError(f"{label}: duplicate {field}: {', '.join(duplicates[:5])}")


def parse_optional_number(value: str, field: str, minimum: float = 0) -> float | None:
    if value.strip() == "":
        return None
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{field}: expected a number, found {value!r}") from exc
    if number < minimum:
        raise ValueError(f"{field}: must be at least {minimum}")
    return number


def validate_markets(rows: list[dict[str, str]]) -> set[str]:
    require_unique(rows, "market_id", "markets.csv")
    markets = {row["market_id"] for row in rows}
    if markets != EXPECTED_MARKETS:
        raise ValueError(f"markets.csv: expected {sorted(EXPECTED_MARKETS)}, found {sorted(markets)}")
    for row in rows:
        if row["status"] != "active":
            raise ValueError(f"markets.csv: {row['market_id']} must remain active during v1")
        if len(row["google_geo"]) != 2 or row["google_geo"] != row["google_geo"].upper():
            raise ValueError(f"markets.csv: invalid Google geo for {row['market_id']}")
    return markets


def validate_clusters(rows: list[dict[str, str]]) -> set[str]:
    require_unique(rows, "problem_id", "problem-clusters.csv")
    if len(rows) != 10:
        raise ValueError(f"problem-clusters.csv: v1 is frozen at 10 clusters, found {len(rows)}")
    clusters = {row["problem_id"] for row in rows}
    if any(row["status"] != "seed" for row in rows):
        raise ValueError("problem-clusters.csv: initial clusters must have status=seed")
    return clusters


def validate_seeds(
    rows: list[dict[str, str]], markets: set[str], clusters: set[str]
) -> set[str]:
    require_unique(rows, "query_id", "query-seeds.csv")
    query_ids = {row["query_id"] for row in rows}
    expected_total = len(markets) * len(clusters) * len(EXPECTED_INTENTS)
    if len(rows) != expected_total:
        raise ValueError(f"query-seeds.csv: expected {expected_total} rows, found {len(rows)}")

    cells: dict[tuple[str, str], set[str]] = defaultdict(set)
    queries_by_market: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        market = row["market_id"]
        problem = row["problem_id"]
        intent = row["intent"]
        query = row["query"].strip()
        if market not in markets:
            raise ValueError(f"query-seeds.csv: unknown market {market}")
        if problem not in clusters:
            raise ValueError(f"query-seeds.csv: unknown problem {problem}")
        if intent not in EXPECTED_INTENTS:
            raise ValueError(f"query-seeds.csv: invalid intent {intent}")
        if row["seed_status"] not in VALID_SEED_STATUS:
            raise ValueError(f"query-seeds.csv: invalid seed status {row['seed_status']}")
        if not query or URL_OR_EMAIL.search(query):
            raise ValueError(f"query-seeds.csv: unsafe or empty query in {row['query_id']}")
        folded = query.casefold()
        if folded in queries_by_market[market]:
            raise ValueError(f"query-seeds.csv: duplicate query within {market}: {query}")
        queries_by_market[market].add(folded)
        cells[(market, problem)].add(intent)

    for market in sorted(markets):
        for problem in sorted(clusters):
            if cells[(market, problem)] != EXPECTED_INTENTS:
                raise ValueError(f"query-seeds.csv: incomplete intent set for {market}/{problem}")
    return query_ids


def validate_anchors(
    rows: list[dict[str, str]], markets: set[str], clusters: set[str]
) -> set[str]:
    require_unique(rows, "anchor_id", "trend-anchors.csv")
    expected_total = len(markets) * len(clusters)
    if len(rows) != expected_total:
        raise ValueError(f"trend-anchors.csv: expected {expected_total} rows, found {len(rows)}")

    anchor_ids = {row["anchor_id"] for row in rows}
    cells: set[tuple[str, str]] = set()
    for row in rows:
        market = row["market_id"]
        problem = row["problem_id"]
        query = row["query"].strip()
        if market not in markets or problem not in clusters:
            raise ValueError(f"trend-anchors.csv: unknown market/problem in {row['anchor_id']}")
        if row["anchor_status"] not in VALID_SEED_STATUS:
            raise ValueError(f"trend-anchors.csv: invalid status in {row['anchor_id']}")
        if not query or URL_OR_EMAIL.search(query):
            raise ValueError(f"trend-anchors.csv: unsafe or empty query in {row['anchor_id']}")
        cell = (market, problem)
        if cell in cells:
            raise ValueError(f"trend-anchors.csv: duplicate market/problem cell {cell}")
        cells.add(cell)
    return anchor_ids


def validate_signals(
    rows: list[dict[str, str]], query_ids: set[str], anchor_ids: set[str], markets: set[str]
) -> None:
    seen: set[tuple[str, str, str]] = set()
    for line, row in enumerate(rows, start=2):
        query_id = row["query_id"]
        market = row["market_id"]
        source = row["source"]
        window = row["window"]
        if query_id not in query_ids | anchor_ids:
            raise ValueError(f"google-signals.csv:{line}: unknown query_id {query_id}")
        if market not in markets or not query_id.startswith(f"{market}-"):
            raise ValueError(f"google-signals.csv:{line}: query and market do not match")
        if source not in VALID_SOURCES:
            raise ValueError(f"google-signals.csv:{line}: invalid source {source}")
        if window not in VALID_WINDOWS:
            raise ValueError(f"google-signals.csv:{line}: invalid window {window}")
        try:
            date.fromisoformat(row["collected_on"])
        except ValueError as exc:
            raise ValueError(f"google-signals.csv:{line}: use YYYY-MM-DD for collected_on") from exc

        key = (query_id, source, window)
        if key in seen:
            raise ValueError(f"google-signals.csv:{line}: duplicate observation {key}")
        seen.add(key)

        volume = parse_optional_number(row["avg_monthly_searches"], "avg_monthly_searches")
        trends_mean = parse_optional_number(row["trends_mean"], "trends_mean")
        if trends_mean is not None and trends_mean > 100:
            raise ValueError(f"google-signals.csv:{line}: trends_mean must be within 0–100")
        for field in ("related_top_count", "related_rising_count"):
            value = parse_optional_number(row[field], field)
            if value is not None and not value.is_integer():
                raise ValueError(f"google-signals.csv:{line}: {field} must be an integer")
        for field in ("weeks_observed", "nonzero_weeks"):
            value = parse_optional_number(row[field], field)
            if value is not None and not value.is_integer():
                raise ValueError(f"google-signals.csv:{line}: {field} must be an integer")
        weeks = parse_optional_number(row["weeks_observed"], "weeks_observed")
        nonzero_weeks = parse_optional_number(row["nonzero_weeks"], "nonzero_weeks")
        if weeks is not None and nonzero_weeks is not None and nonzero_weeks > weeks:
            raise ValueError(f"google-signals.csv:{line}: nonzero_weeks exceeds weeks_observed")
        parse_optional_number(row["recent_26w_mean"], "recent_26w_mean")
        parse_optional_number(row["previous_26w_mean"], "previous_26w_mean")
        direction = row["trends_recent_direction"].strip()
        if direction and direction not in VALID_DIRECTIONS:
            raise ValueError(f"google-signals.csv:{line}: invalid direction {direction}")
        breakout = row["trends_breakout"].strip().lower()
        if breakout not in {"", "true", "false"}:
            raise ValueError(f"google-signals.csv:{line}: trends_breakout must be true, false, or blank")
        if volume is not None and source != "keyword_planner":
            raise ValueError(f"google-signals.csv:{line}: monthly searches belong to Keyword Planner")
        if trends_mean is not None and source != "google_trends":
            raise ValueError(f"google-signals.csv:{line}: trends_mean belongs to Google Trends")
        if source == "google_trends" and query_id not in anchor_ids:
            raise ValueError(f"google-signals.csv:{line}: Trends observations must use a trend anchor")
        if source == "google_trends" and not row["batch_id"].strip():
            raise ValueError(f"google-signals.csv:{line}: Trends observations require batch_id")
        if URL_OR_EMAIL.search(row["notes"]):
            raise ValueError(f"google-signals.csv:{line}: notes must not contain URLs or email addresses")


def main() -> None:
    markets = validate_markets(read_csv("markets.csv"))
    clusters = validate_clusters(read_csv("problem-clusters.csv"))
    query_ids = validate_seeds(read_csv("query-seeds.csv"), markets, clusters)
    anchor_ids = validate_anchors(read_csv("trend-anchors.csv"), markets, clusters)
    signals = read_csv("google-signals.csv")
    validate_signals(signals, query_ids, anchor_ids, markets)

    print("HUMAN Problem Discovery v1 inputs: OK")
    print(
        f"Markets: {len(markets)} | Clusters: {len(clusters)} | "
        f"Trend anchors: {len(anchor_ids)} | Natural-language seeds: {len(query_ids)}"
    )
    print(f"Google observations collected: {len(signals)}")


if __name__ == "__main__":
    main()
