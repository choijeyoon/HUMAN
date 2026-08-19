from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def insert_before(text: str, marker: str, block: str, sentinel: str) -> str:
    if sentinel in text:
        return text
    if marker not in text:
        raise RuntimeError(f"Figure insertion marker missing: {marker[:60]}")
    return text.replace(marker, block + "\n\n        " + marker, 1)


# Validate every launch figure as XML before touching article markup.
figure_paths = [
    "assets/figures/parasocial-attachment.svg",
    "assets/figures/kpop-evidence-map.svg",
    "assets/figures/ai-relationship-v2.svg",
    "assets/figures/ai-evidence-map.svg",
    "assets/figures/scrolling-control-loop.svg",
    "assets/figures/scrolling-evidence-map.svg",
]
for figure_path in figure_paths:
    ET.parse(ROOT / figure_path)


# K-pop: add a separate evidence figure before the individual-differences section.
kpop_path = "en/articles/idol-dating-betrayal/index.html"
kpop = read(kpop_path)
kpop_block = '''        <!-- HUMAN_FIGURE_KPOP_EVIDENCE -->
        <figure class="editorial-figure editorial-figure--article">
          <img src="../../../assets/figures/kpop-evidence-map.svg" alt="Evidence matrix separating general parasocial evidence, parasocial disruption, K-pop fandom identity, and the open gap in controlled idol-dating experiments.">
          <figcaption class="figure-caption">
            <span class="figure-no">FIG. 02</span>
            <span class="figure-title">Where the evidence is strong—and where it stops.</span>
            <span class="figure-note"><strong>Evidence map.</strong> General parasocial and fandom findings are distinguished from the still-missing controlled test of idol dating announcements.</span>
          </figcaption>
        </figure>'''
kpop = insert_before(
    kpop,
    '<h2><span class="sec-no">05</span>Why do some fans feel almost nothing?</h2>',
    kpop_block,
    "HUMAN_FIGURE_KPOP_EVIDENCE",
)
write(kpop_path, kpop)


# AI: renumber figures within the article and align the evidence caption with the new ladder.
ai_path = "en/articles/ai-love/index.html"
ai = read(ai_path)
ai = ai.replace('<span class="figure-no">FIG. 02</span>', '<span class="figure-no">FIG. 01</span>', 1)
ai = ai.replace('<span class="figure-no">FIG. 03</span>', '<span class="figure-no">FIG. 02</span>', 1)
ai = ai.replace(
    'alt="Evidence map comparing an AI social-connection experiment, a randomized relationship-building study and an observational study of Character.AI users."',
    'alt="Evidence ladder separating immediate experimental connection, randomized relationship building, longitudinal chatbot use, real-world wellbeing, and the separate question of machine consciousness."',
    1,
)
ai = ai.replace(
    '<span class="figure-title">Three studies answer three different questions.</span>',
    '<span class="figure-title">Evidence is strongest for immediate human response.</span>',
    1,
)
ai = ai.replace(
    '<span class="figure-note"><strong>Empirical evidence map.</strong> Sample sizes and study designs are reported directly; the layout intentionally avoids turning observational associations into causal effects.</span>',
    '<span class="figure-note"><strong>Evidence ladder.</strong> Short experimental effects, longitudinal durability and real-world wellbeing are different questions. Step height represents question scope, not effect size.</span>',
    1,
)
write(ai_path, ai)


# Scrolling: renumber the mechanism figure and add a separate evidence ledger before boredom/switching.
scroll_path = "en/articles/scrolling/index.html"
scroll = read(scroll_path)
scroll = scroll.replace('<span class="figure-no">FIG. 04</span>', '<span class="figure-no">FIG. 01</span>', 1)
scroll = scroll.replace(
    '<span class="figure-note"><strong>Conceptual synthesis.</strong> Reward-sensitive sampling and habit are shown as parallel contributors. The stop gate represents interface friction and deliberate reconsideration; this is not an empirically fitted single model.</span>',
    '<span class="figure-note"><strong>Conceptual synthesis.</strong> The loop separates sampling, habit, personalization and an explicit stop gate. Geometry does not represent effect size or a single fitted model.</span>',
    1,
)
scroll_block = '''        <!-- HUMAN_FIGURE_SCROLL_EVIDENCE -->
        <figure class="editorial-figure editorial-figure--article">
          <img src="../../../assets/figures/scrolling-evidence-map.svg" alt="Evidence ledger distinguishing causal reward-learning evidence, computational habit evidence, direct but correlational scrolling evidence, and personalized neural-response evidence.">
          <figcaption class="figure-caption">
            <span class="figure-no">FIG. 02</span>
            <span class="figure-title">Not all scrolling evidence answers the same question.</span>
            <span class="figure-note"><strong>Evidence ledger.</strong> Some of the strongest causal evidence concerns adjacent posting behavior, while more direct scrolling evidence is less causal or less mechanism-specific.</span>
          </figcaption>
        </figure>'''
scroll = insert_before(
    scroll,
    '<h2><span class="sec-no">05</span>We scroll to escape boredom—and switching can make boredom worse.</h2>',
    scroll_block,
    "HUMAN_FIGURE_SCROLL_EVIDENCE",
)
write(scroll_path, scroll)


# Lightweight build assertions.
assert "HUMAN_FIGURE_KPOP_EVIDENCE" in read(kpop_path)
assert read(ai_path).count('<span class="figure-no">FIG. 01</span>') >= 1
assert read(ai_path).count('<span class="figure-no">FIG. 02</span>') >= 1
assert "HUMAN_FIGURE_SCROLL_EVIDENCE" in read(scroll_path)
assert "scrolling-evidence-map.svg" in read(scroll_path)
print("HUMAN flagship figure integration: OK")
