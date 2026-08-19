# HUMAN

A zero-cost, multilingual human-science media MVP.

**Positioning:** broad human curiosity, explained through neuroscience, psychology, computation, and culture.

## Structure

- `/en/`, `/ko/`, `/ja/`, `/es/`, `/zh/` — language entrances
- `/en/love/`, `/en/ai/`, `/en/kpop/`, `/en/attention/`, `/en/society/`, `/en/consciousness/` — first category hubs
- `assets/` — shared design and interaction
- `docs/topic-experiment-v1.md` — Topic Demand v1 measurement and decision rules
- `docs/topic-results/` — human-readable aggregate experiment results and decisions
- `data/topic-demand-summary.csv` — canonical public aggregate metrics table
- `scripts/analyze_topic_demand.py` — dependency-free aggregate metric summary
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

## Local preview

Run any static web server from the repository root, for example:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.
