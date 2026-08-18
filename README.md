# HUMAN

A zero-cost, multilingual human-science media MVP.

**Positioning:** broad human curiosity, explained through neuroscience, psychology, computation, and culture.

## Structure

- `/en/`, `/ko/`, `/ja/`, `/es/`, `/zh/` — language entrances
- `/en/love/`, `/en/ai/`, `/en/kpop/`, `/en/attention/`, `/en/society/`, `/en/consciousness/` — first category hubs
- `assets/` — shared design and interaction
- `.github/workflows/pages.yml` — static GitHub Pages deployment workflow

## Editorial rule

Every category must stand alone, and every category must open a door into another.

Reader journey: **Entry → Mechanism → Universal Human Question → Frontier**.

K-pop is a cross-category lens and audience-acquisition wedge, not a gossip/news silo.

## Local preview

Run any static web server from the repository root, for example:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.
