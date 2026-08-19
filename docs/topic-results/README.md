# Topic Demand Results

This directory is the human-readable decision log for HUMAN's topic experiments.

## What belongs here

- experiment summaries
- aggregate counts and rates
- interpretation of attraction vs reading quality
- creative/UTM notes needed to reproduce a comparison
- editorial decisions and the evidence behind them

## What does not belong here

Do not commit visitor-level analytics, IP addresses, email addresses, raw session histories, API secrets, service-account credentials, or unredacted analytics exports. The public repository should contain only aggregate, non-identifying results.

## Current experiment

`topic-demand-v1` compares the three Issue 001 flagship topics:

1. `feature-001` — K-pop / parasocial attachment
2. `feature-002` — AI / intimacy
3. `feature-003` — Attention / scrolling

The canonical aggregate table is `data/topic-demand-summary.csv`. It intentionally contains blank metrics until real traffic has been collected; blank means **not measured**, not zero.

Run:

```bash
python3 scripts/analyze_topic_demand.py
```

to print CTR, 30-second engaged rate, 50% read rate, completion rate, and next-article rate from the aggregate table.

## Decision discipline

Use the experiment specification in `docs/topic-experiment-v1.md`. In particular, do not treat the highest CTR as an automatic editorial winner if reading-quality metrics are materially worse. Preserve the same feature IDs and record any creative/title variant in UTM content so comparisons remain interpretable.
