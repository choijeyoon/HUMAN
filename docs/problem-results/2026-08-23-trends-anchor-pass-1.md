# Google Trends anchor pass 1

## Scope

This pass screened all 40 short problem anchors in Japan, the United States, Spain, and Mexico.

## Settings

- Source: public Google Trends Explore
- Search type: Web Search
- Window: past five years
- Collection date: 2026-08-23
- Batch size: five anchors within one market
- Observations per anchor: 262 weekly values

## Direction rule

The recent-direction label compares the mean of the latest 26 weeks with the preceding 26 weeks.

- `rising`: increase of at least 20%
- `falling`: decrease of at least 20%
- `stable`: change between those thresholds
- `insufficient`: fewer than eight non-zero weeks, fewer than 52 total weeks, or a displayed batch mean below 0.5

These are descriptive screening rules, not hypothesis tests. No p-values were calculated, so no multiple-comparison correction was applied. Any later inferential comparisons of micro-answer outcomes will use the pre-registered primary outcome and Benjamini–Hochberg FDR correction for exploratory secondary contrasts within each market.

## Coverage result

| Market | Rising | Stable | Falling | Insufficient |
| --- | ---: | ---: | ---: | ---: |
| Japan | 2 | 5 | 0 | 3 |
| United States | 5 | 5 | 0 | 0 |
| Spain | 1 | 1 | 1 | 7 |
| Mexico | 0 | 1 | 1 | 8 |

## Interpretation

The US anchors produced usable weekly series across all ten problems. Seven Japanese anchors were usable in the first pass. Most Spanish and Mexican multi-word anchors were too sparse relative to the largest term in their five-query batch.

`insufficient` does not mean that the underlying problem has no demand. Google scales the five terms in each interface comparison jointly. A high-volume term such as `soledad` can compress smaller terms toward zero. Those anchors require one of three follow-ups:

1. check the phrase alone in Trends;
2. replace it with a shorter or more common local expression;
3. defer demand estimation to Keyword Planner, which provides approximate monthly volume.

The displayed batch averages must not be used to rank markets or to compare anchors from different batches.

## Directional candidates for follow-up

The first pass identified the following rising anchors:

- Japan: `AI 恋愛`, `感情がない`
- United States: `loneliness`, `social burnout`, `adult friendship`, `phone addiction`, `emotional numbness`
- Spain: `soledad`

These remain discovery leads rather than editorial winners. They must still pass monthly-demand, answer-gap, evidence-readiness, and micro-answer behavior gates.
