# HUMAN Problem Discovery v1

## Goal

Find recurring human problems with measurable search demand before HUMAN commissions full articles. The first round compares four markets without treating language as a proxy for a single global audience:

| Market ID | Country | Language | Google geo |
| --- | --- | --- | --- |
| ja-jp | Japan | Japanese | JP |
| en-us | United States | English | US |
| es-es | Spain | Spanish | ES |
| es-mx | Mexico | Spanish | MX |

This round discovers candidates. It does not rank countries by one combined score or claim that search interest measures population prevalence.

## Source roles

### Google Trends

Use Trends for direction, persistence, seasonality, related searches, and regional variation. Its 0–100 index is normalized within the selected geography and time window. Do not interpret it as absolute search volume or compare raw index values from separately normalized downloads.

### Google Keyword Planner

Use Keyword Planner for approximate monthly demand and keyword expansion with a fixed language, country, and date range. Record the collection date because historical metrics are updated over time.

### Public communities

Review a small purposive sample only after a problem cluster passes the Google demand screen. Communities help interpret context, vocabulary, answer gaps, and recurring misconceptions. They do not provide population prevalence.

Do not commit usernames, copied posts, private URLs, or raw platform exports. Store only non-identifying notes and aggregate counts in the public repository.

## Query construction

Use two query layers because Google Trends often cannot resolve long, natural-language questions.

`data/problem-discovery/trend-anchors.csv` contains one short, relatively common expression per problem and market. Use it to assess persistence, recent direction, seasonality, and related searches. An anchor is a measurement aid, not the final article title.

`data/problem-discovery/query-seeds.csv` contains three natural problem expressions per cluster and market:

- `experience`: how people describe the state
- `explanation`: why it happens
- `solution`: what they want to do about it

Anchors and seeds are hypotheses, not observed demand. Keep their status `unvalidated` until the wording has been checked against Google suggestions, related searches, or Keyword Planner ideas for that exact market. Do not translate a winning query literally into another language.

## Collection protocol

Use the same procedure for all four markets.

1. Set the country and language shown in `markets.csv`.
2. Check the short anchor in Trends. If it is too sparse or ambiguous, replace it and document the reason before collecting the full market.
3. Collect the natural-language seeds and their close Google-suggested variants in Keyword Planner.
4. Use the latest complete 12 months for approximate monthly search demand.
5. Use a five-year Trends window for persistence and a 12-month window for recent direction.
6. Export related `top` and `rising` searches when available.
7. Record whether the query is seasonal, event-driven, ambiguous, or too sparse for Trends.
8. Audit the first search-results page only for candidates that pass the demand screen.
9. Keep collection dates and source settings with every aggregate observation.

Never fill missing values with zero. A blank means not collected or unavailable; zero means the source reported zero.

## Stage gates

Avoid a single weighted score. Apply these gates in order within each market.

### Gate 1: demand

A cluster passes when at least one validated query has non-trivial monthly demand or a sustained/rising Trends signal. Record the decision and the evidence used. Do not impose one universal volume threshold across countries.

### Gate 2: persistence

Exclude short-lived news spikes unless the underlying problem remains present after the event. Prefer recurring or stable demand over one-week peaks.

### Gate 3: answer gap

Review the leading results for the cluster. Record whether existing answers are shallow, unsupported, overly clinical, commercial, or fail to address the user's actual question.

### Gate 4: HUMAN fit

The problem must support a careful explanation grounded in psychology, neuroscience, computation, or culture. Exclude queries requiring individual diagnosis, crisis intervention, legal advice, or medical treatment recommendations.

### Gate 5: testability

The problem must be expressible as a short, language-matched answer page with one consistent request for a deeper article.

Select up to five clusters per market after all gates. The same cluster may pass in one market and fail in another.

## Context audit

For each shortlisted cluster, review 10–20 recent, public examples across suitable communities or search results. Record only aggregate fields:

- number reviewed
- recurring situations
- common wording
- common misconceptions
- deficiencies in existing answers
- sensitivity or safety concerns

This is a purposive qualitative audit. Do not report percentages as prevalence estimates.

## Micro-answer validation

Create a 300–600 word page in the user's language for each final candidate. Match page structure, visual weight, and call to action within a market.

Recommended events:

1. `problem_impression`
2. `select_problem`
3. `micro_answer_view`
4. `micro_answer_complete`
5. `request_deep_dive`
6. `related_problem_select`

The primary outcome is the deep-dive request rate:

```text
request_deep_dive / micro_answer_view
```

Pre-register one primary comparison within each market. Treat cross-market differences as descriptive unless recruitment and exposure are comparable. For exploratory secondary outcomes and multiple candidate contrasts, control the false discovery rate with the Benjamini–Hochberg procedure within each market and outcome family. FDR is preferable to Bonferroni here because the discovery round tests several correlated candidates and should retain enough power to identify signals for replication.

Do not make a winner decision from small denominators. Record confidence intervals and raw counts beside rates. A candidate advances only when demand, answer gap, reading behavior, and evidence readiness point in the same direction.

## Repository outputs

Public, versioned files:

- `markets.csv`: fixed market definitions
- `problem-clusters.csv`: editorial problem hypotheses
- `trend-anchors.csv`: short expressions used for within-query trend assessment
- `query-seeds.csv`: language- and market-specific natural problem expressions
- `google-signals.csv`: aggregate Google observations once collected
- `docs/problem-results/`: aggregate summaries and decisions
- analysis and validation scripts

Private or external only:

- account credentials and OAuth tokens
- raw analytics and visitor/session exports
- usernames or copied community posts
- private or access-controlled URLs
- unredacted qualitative notes

## Version-one stopping rule

End the discovery pass when every market has:

- at least 30 localized seeds checked
- at least 5 clusters with usable Google evidence, or a documented reason why fewer passed
- an answer-gap audit for the finalists
- no more than 5 candidates selected for micro-answer testing

Revision of the seed universe begins only after this first pass is documented, so early observations do not silently change the protocol.
