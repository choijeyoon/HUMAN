# Keyword Planner collection protocol

## Purpose

Collect approximate monthly search demand and keyword ideas for the 120 natural-language Problem Discovery seeds. Google Trends remains the source for persistence and direction; Keyword Planner supplies the demand scale that the normalized Trends interface cannot provide.

## Private working files

Run:

```bash
python3 scripts/prepare_keyword_planner_inputs.py
python3 scripts/validate_keyword_planner_inputs.py
```

This creates a private workspace under:

```text
data/private/keyword-planner/
```

The repository already ignores `data/private/`. Do not force-add this directory.

For each market, the generator creates:

- `<market-id>.txt`: 30 keywords for pasting into Keyword Planner
- `<market-id>-mapping.csv`: stable HUMAN query IDs for later matching

Save original Google Ads CSV downloads under `data/private/keyword-planner/exports/` using:

```text
YYYY-MM-DD-<market-id>.csv
```

## Fixed market settings

| Market ID | Location | Language |
| --- | --- | --- |
| ja-jp | Japan | Japanese |
| en-us | United States | English |
| es-es | Spain | Spanish |
| es-mx | Mexico | Spanish |

Collect one market at a time. Do not combine Spain and Mexico in one plan or export.

## Interface procedure

1. Open Keyword Planner and choose the historical search-volume workflow.
2. Paste the 30 lines from the market's text file.
3. Set exactly one location and the language listed above.
4. Use the latest complete 12 months.
5. Export the keyword table as CSV without editing it.
6. Save it in the private export directory with the required filename.
7. Record unexpected filters, unavailable metrics, or search-volume ranges before changing the next market.

Do not start a campaign, set a budget, or publish ads for this collection.

## Public output

After checking the actual Google export headers and whether volume is exact or reported as a range, normalize only these fields into `data/problem-discovery/google-signals.csv`:

- stable HUMAN query ID
- market ID
- collection date
- source and 12-month window
- exact average monthly searches, or explicit lower and upper bounds
- a short non-identifying data-quality note

Do not commit the original export, Google account identifiers, bids, campaign information, credentials, cookies, or OAuth tokens.
