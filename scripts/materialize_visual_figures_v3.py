from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSS_LINE = '  <link rel="stylesheet" href="../../../assets/figure-atlas-v3.css">\n'

ARTICLES = {
    "en/articles/idol-dating-betrayal/index.html": [
        ("parasocial-attachment.svg", "figure-atlas--kpop-01", "Visual explainer showing repeated media exposure building a social model, followed by dating news triggering an emotional update."),
        ("kpop-evidence-map.svg", "figure-atlas--kpop-02", "Visual evidence landscape showing strong general parasocial evidence, moderate disruption and fandom evidence, and an open question for controlled idol-dating tests."),
    ],
    "en/articles/ai-love/index.html": [
        ("ai-relationship-v2.svg", "figure-atlas--ai-01", "Visual explainer showing AI behavior, perceived responsiveness and human attachment, separated from the independent question of machine consciousness."),
        ("ai-evidence-map.svg", "figure-atlas--ai-02", "Visual evidence staircase moving from short-term AI connection experiments toward longer-term relationship and wellbeing questions."),
    ],
    "en/articles/scrolling/index.html": [
        ("scrolling-control-loop.svg", "figure-atlas--scroll-01", "Visual explainer of the scrolling loop: cue, open, sample and continue, with reward, habit, personalization and a stop gate."),
        ("scrolling-evidence-map.svg", "figure-atlas--scroll-02", "Visual evidence summary comparing reward learning, habit formation, compulsive scrolling and brain evidence by strength and meaning."),
    ],
}

for rel, replacements in ARTICLES.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if "figure-atlas-v3.css" not in text:
        anchor = '  <link rel="stylesheet" href="../../../assets/flagship.css">\n'
        if anchor not in text:
            raise RuntimeError(f"stylesheet anchor missing: {rel}")
        text = text.replace(anchor, anchor + CSS_LINE, 1)

    for asset, cls, aria in replacements:
        if cls in text:
            continue
        pattern = rf'\s*<img\s+src="\.\./\.\./\.\./assets/figures/{re.escape(asset)}"\s+alt="[^"]*">'
        replacement = f'\n          <div class="figure-atlas-panel {cls}" role="img" aria-label="{aria}"></div>'
        text, count = re.subn(pattern, replacement, text, count=1)
        if count != 1:
            raise RuntimeError(f"figure asset not found exactly once: {asset} in {rel}")

    path.write_text(text, encoding="utf-8")

# Assertions ensure all six visual panels are now source HTML, not deployment-time substitutions.
for rel, replacements in ARTICLES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    assert "figure-atlas-v3.css" in text
    for _, cls, _ in replacements:
        assert cls in text

print("Visual explainer figures materialized into article HTML: OK")
