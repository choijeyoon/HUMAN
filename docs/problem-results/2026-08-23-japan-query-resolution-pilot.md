# Japan query-resolution pilot

## Purpose

Check whether natural-language problem statements are sufficiently frequent for direct use in Google Trends before collecting all four markets.

## Settings

- Geography: Japan
- Search type: Web Search
- Window: past five years
- Collection date: 2026-08-23
- Interface: public Google Trends Explore

## Batch 1: natural-language problem expressions

| Query | Jointly normalized average |
| --- | ---: |
| 人といても孤独 | 0 |
| 人と会うと疲れる | 1 |
| 大人になって友達が減った | 0 |
| やる気が出ない | 67 |
| スマホを見るのをやめられない | 0 |

Four of the five phrases were too sparse relative to `やる気が出ない` to support useful five-year comparisons in this batch.

## Batch 2: shorter problem anchors

| Query | Jointly normalized average |
| --- | ---: |
| 孤独 | 26 |
| 人間関係 疲れた | 0 |
| 大人 友達 | 1 |
| やる気が出ない | 3 |
| スマホ依存 | 2 |

The shorter anchors produced usable time-series data for more concepts, although `人間関係 疲れた` remained sparse in the joint comparison.

## Decision

Keep two query layers:

1. Short anchors for within-query persistence, direction, seasonality, and related searches in Google Trends.
2. Natural-language expressions for Keyword Planner expansion, search-results audits, and eventual reader-facing copy.

Do not rank the problems from the displayed averages. Google normalizes each comparison batch jointly, which is why the value for `やる気が出ない` changed when the other terms changed. Cross-problem demand will rely primarily on Keyword Planner estimates and stage-gate evidence, not a Trends average score.
