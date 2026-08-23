# HUMAN

A zero-cost, multilingual human-science media MVP.

**Positioning:** broad human curiosity, explained through neuroscience, psychology, computation, and culture.

## Structure

- `/en/`, `/ko/`, `/ja/`, `/es/`, `/zh/` — language entrances
- `/en/love/`, `/en/ai/`, `/en/kpop/`, `/en/attention/`, `/en/society/`, `/en/consciousness/` — first category hubs
- `assets/` — shared design and interaction
- `docs/topic-experiment-v1.md` — Topic Demand v1 measurement and decision rules
- `docs/problem-discovery-v1.md` — Google-first problem discovery protocol for Japan, the United States, Spain, and Mexico
- `docs/topic-results/` — human-readable aggregate experiment results and decisions
- `data/topic-demand-summary.csv` — canonical public aggregate metrics table
- `data/problem-discovery/` — market definitions, localized query seeds, and aggregate Google observations
- `scripts/analyze_topic_demand.py` — dependency-free aggregate metric summary
- `scripts/validate_problem_discovery.py` — safety and schema checks for discovery inputs
- `scripts/analyze_problem_discovery.py` — collection coverage report without a combined market score
- `scripts/prepare_keyword_planner_inputs.py` — private market-specific Keyword Planner input generator
- `docs/keyword-planner-collection.md` — fixed collection and data-safety procedure
- `.github/workflows/pages.yml` — static GitHub Pages deployment workflow

## Experiment data policy

GitHub is the source of truth for HUMAN's public experiment design, aggregate results, and reproducible analysis code. Raw visitor/session analytics and credentials belong in the analytics provider or another private store, not in this public repository.

The repository `.gitignore` blocks common raw-export, credential, and visitor-level file patterns. Only non-identifying aggregate counts/rates should be committed under `data/` or `docs/topic-results/`.

## Editorial rule

Every category must stand alone, and every category must open a door into another.

Reader journey: **Entry → Mechanism → Universal Human Question → Frontier**.

K-pop is a cross-category lens and audience-acquisition wedge, not a gossip/news silo.

## Topic Demand analysis

After updating aggregate counts in `data/topic-demand-summary.csv`, run:

```bash
python3 scripts/analyze_topic_demand.py
```

The report keeps attraction (feature CTR) separate from reading quality (30-second engagement, 50% read, completion, and next-article rate) so editorial choices are not made from pageviews alone.

## Problem Discovery analysis

The first discovery pass uses 10 short Trends anchors and 30 natural-language seed queries in each of four markets: Japan/Japanese, United States/English, Spain/Spanish, and Mexico/Spanish. Validate the fixed protocol and inspect collection coverage with:

```bash
python3 scripts/validate_problem_discovery.py
python3 scripts/analyze_problem_discovery.py
```

Seed queries are hypotheses until checked against Google data in their exact market. Google Trends indices, Keyword Planner volume, and qualitative context remain separate evidence types.

## Local preview

Run any static web server from the repository root, for example:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.
