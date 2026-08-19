from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://choijeyoon.github.io/HUMAN"
COVER_WEBP = "assets/images/issue-001-cover-4k-v2.webp?v=20260819-launch2"
COVER_JPG = "assets/images/issue-001-cover-4k-v2.jpg?v=20260819-launch2"
COVER_JPG_ABS = f"{BASE}/assets/images/issue-001-cover-4k-v2.jpg?v=20260819-launch2"
OPENING_VERSION = "v=20260819-opening1"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Expected markup not found for {label}")
    return text.replace(old, new, 1)


ARTICLES = [
    {
        "path": "en/articles/idol-dating-betrayal/index.html",
        "href": "en/articles/idol-dating-betrayal/",
        "slug": "idol-dating-betrayal",
        "feature_id": "feature-001",
        "title": "Why Does Idol Dating Feel Like Betrayal?",
        "description": "A rigorous guide to parasocial relationships, fandom identity and why idol dating news can feel unexpectedly personal.",
        "section": "Culture × Attachment",
        "keywords": ["parasocial relationships", "K-pop", "fandom", "social cognition", "attachment"],
        "opening_class": "opening--kpop",
        "opening_asset": "assets/openings-v4/idol-dating-opening-v4.svg",
        "opening_alt": "Editorial illustration of a performer under stage light above a dense audience, representing mediated intimacy.",
        "opening_title": "Mediated intimacy becomes psychologically real before it becomes reciprocal.",
    },
    {
        "path": "en/articles/ai-love/index.html",
        "href": "en/articles/ai-love/",
        "slug": "ai-love",
        "feature_id": "feature-002",
        "title": "Could You Really Fall in Love With an AI?",
        "description": "What experiments, longitudinal studies and real AI-companion users tell us about attachment, closeness, anthropomorphism and the limits of human-AI relationships.",
        "section": "AI × Human Connection",
        "keywords": ["AI companions", "attachment", "anthropomorphism", "human-AI interaction", "consciousness"],
        "opening_class": "opening--ai",
        "opening_asset": "assets/openings-v4/ai-love-opening-v4.svg",
        "opening_alt": "Editorial illustration of a human profile facing a translucent artificial presence across a narrow boundary.",
        "opening_title": "A human bond can be measurable without settling what the machine is.",
    },
    {
        "path": "en/articles/scrolling/index.html",
        "href": "en/articles/scrolling/",
        "slug": "scrolling",
        "feature_id": "feature-003",
        "title": "Why Can’t We Stop Scrolling?",
        "description": "A rigorous guide to reward learning, habit, anticipation, personalization, boredom and interface friction behind repetitive social-media scrolling.",
        "section": "Attention × Digital Behavior",
        "keywords": ["scrolling", "reinforcement learning", "habit", "attention", "social media"],
        "opening_class": "opening--scrolling",
        "opening_asset": "assets/openings-v4/scrolling-opening-v4.svg",
        "opening_alt": "Editorial illustration of a person in a dark room facing a glowing phone beneath repeated feed layers.",
        "opening_title": "The next swipe is easy; stopping requires a decision point.",
    },
]


def build_homepage() -> None:
    path = "index.html"
    s = read(path)

    old_img = '<img src="assets/images/issue-001-cover-ultra.jpg?v=20260818-7" width="1536" height="1024" loading="eager" fetchpriority="high" alt="Editorial composite of a serene human portrait between a luminous concert crowd and an abstract artificial profile dissolving into structured fragments.">'
    new_img = (
        '<picture class="issue-cover-picture">'
        f'<source srcset="{COVER_WEBP}" type="image/webp">'
        f'<img src="{COVER_JPG}" width="4096" height="2730" loading="eager" fetchpriority="high" '
        'alt="HUMAN Issue 001 editorial cover: a crowd, a human portrait and a dissolving digital profile.">'
        '</picture>'
    )
    if old_img in s:
        s = s.replace(old_img, new_img, 1)
    elif "issue-001-cover-4k-v2" not in s:
        raise RuntimeError("Homepage cover markup is not recognized")

    for old_url in (
        f"{BASE}/assets/images/issue-001-cover-ultra.jpg",
        f"{BASE}/assets/images/issue-001-cover-4k.jpg?v=20260819-4k1",
    ):
        s = s.replace(old_url, COVER_JPG_ABS)

    card_updates = {
        '<span class="feature-foot">Evidence: established core / direct dating evidence limited →</span>': '<span class="feature-foot"><span class="feature-evidence">Evidence: established core / direct dating evidence limited</span><strong class="feature-cta">Read Feature 001 ↗</strong></span>',
        '<span class="feature-foot">Evidence: emerging direct human–AI studies →</span>': '<span class="feature-foot"><span class="feature-evidence">Evidence: emerging direct human–AI studies</span><strong class="feature-cta">Read Feature 002 ↗</strong></span>',
        '<span class="feature-foot">Evidence: multi-process / mixed directness →</span>': '<span class="feature-foot"><span class="feature-evidence">Evidence: multi-process / mixed directness</span><strong class="feature-cta">Read Feature 003 ↗</strong></span>',
    }
    for old, new in card_updates.items():
        if old in s:
            s = s.replace(old, new, 1)

    track_updates = {
        '<a class="issue-feature" href="en/articles/idol-dating-betrayal/">': '<a class="issue-feature" data-track="feature-001" href="en/articles/idol-dating-betrayal/">',
        '<a class="issue-feature" href="en/articles/ai-love/">': '<a class="issue-feature" data-track="feature-002" href="en/articles/ai-love/">',
        '<a class="issue-feature" href="en/articles/scrolling/">': '<a class="issue-feature" data-track="feature-003" href="en/articles/scrolling/">',
    }
    for old, new in track_updates.items():
        if old in s:
            s = s.replace(old, new, 1)

    for article in ARTICLES:
        anchor = f'<a class="issue-feature" data-track="{article["feature_id"]}" href="{article["href"]}">'
        if anchor not in s:
            raise RuntimeError(f"Homepage card anchor not found for {article['slug']}")
        if article["opening_asset"] not in s:
            art = (
                '<span class="feature-art-shell" aria-hidden="true">'
                f'<img class="feature-art" src="{article["opening_asset"]}?{OPENING_VERSION}" width="1000" height="1800" loading="lazy" decoding="async" alt="">'
                '</span>'
            )
            s = s.replace(anchor, anchor + art, 1)

    write(path, s)


def seo_block(article: dict) -> str:
    url = f"{BASE}/en/articles/{article['slug']}/"
    opening_abs = f"{BASE}/{article['opening_asset']}?{OPENING_VERSION}"
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["description"],
        "image": [opening_abs, COVER_JPG_ABS],
        "datePublished": "2026-08-18",
        "dateModified": "2026-08-19",
        "inLanguage": "en",
        "articleSection": article["section"],
        "keywords": article["keywords"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@type": "Organization", "name": "HUMAN Editorial"},
        "publisher": {"@type": "Organization", "name": "HUMAN", "url": BASE + "/"},
    }
    schema_json = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    return (
        '\n  <!-- HUMAN_ARTICLE_SEO -->\n'
        f'  <link rel="canonical" href="{url}">\n'
        f'  <link rel="alternate" type="application/rss+xml" title="HUMAN" href="{BASE}/feed.xml">\n'
        '  <meta name="author" content="HUMAN Editorial">\n'
        '  <meta property="og:type" content="article">\n'
        '  <meta property="og:site_name" content="HUMAN">\n'
        f'  <meta property="og:title" content="{article["title"]} — HUMAN">\n'
        f'  <meta property="og:description" content="{article["description"]}">\n'
        f'  <meta property="og:url" content="{url}">\n'
        f'  <meta property="og:image" content="{opening_abs}">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{article["title"]} — HUMAN">\n'
        f'  <meta name="twitter:description" content="{article["description"]}">\n'
        f'  <meta name="twitter:image" content="{opening_abs}">\n'
        f'  <script type="application/ld+json">{schema_json}</script>'
    )


def opening_block(article: dict) -> str:
    src = f"../../../{article['opening_asset']}?{OPENING_VERSION}"
    return f'''\n\n    <!-- HUMAN_ARTICLE_OPENING -->
    <figure class="article-opening-visual {article['opening_class']}">
      <div class="article-opening-art">
        <img src="{src}" width="1000" height="1800" loading="eager" fetchpriority="high" alt="{article['opening_alt']}">
      </div>
      <figcaption class="article-opening-copy">
        <span class="opening-label">Editorial illustration / Feature opening</span>
        <strong>{article['opening_title']}</strong>
        <span class="opening-note">Not empirical data</span>
      </figcaption>
    </figure>
    <div class="article-reading-map" aria-label="How this feature is structured">
      <span><small>01</small><strong>Question</strong></span>
      <span><small>02</small><strong>Evidence</strong></span>
      <span><small>03</small><strong>Mechanism</strong></span>
      <span><small>04</small><strong>Unknowns</strong></span>
    </div>'''


def build_articles() -> None:
    for article in ARTICLES:
        s = read(article["path"])
        if "HUMAN_ARTICLE_SEO" not in s:
            desc = f'<meta name="description" content="{article["description"]}">'
            s = replace_once(s, desc, desc + seo_block(article), f"SEO {article['slug']}")

        if "HUMAN_ARTICLE_OPENING" not in s:
            target = '    </header>\n\n    <div class="article-layout">'
            replacement = '    </header>' + opening_block(article) + '\n\n    <div class="article-layout">'
            s = replace_once(s, target, replacement, f"opening {article['slug']}")

        write(article["path"], s)


def noindex_previews() -> None:
    paths = [
        "ko/index.html",
        "ja/index.html",
        "zh/index.html",
        "es/index.html",
        "ko/articles/idol-dating-betrayal/index.html",
        "ja/articles/idol-dating-betrayal/index.html",
    ]
    for path in paths:
        p = ROOT / path
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        if 'name="robots"' in s:
            continue
        needle = '<meta name="viewport" content="width=device-width,initial-scale=1">'
        if needle in s:
            s = s.replace(needle, needle + '<meta name="robots" content="noindex,follow">', 1)
        else:
            s = s.replace('<head>', '<head><meta name="robots" content="noindex,follow">', 1)
        p.write_text(s, encoding="utf-8")


def validate() -> None:
    home = read("index.html")
    assert "issue-001-cover-4k-v2.webp?v=20260819-launch2" in home
    assert home.count("feature-cta") == 3
    assert home.count("feature-art-shell") == 3
    for article in ARTICLES:
        assert article["opening_asset"] in home
        s = read(article["path"])
        assert "HUMAN_ARTICLE_SEO" in s
        assert "HUMAN_ARTICLE_OPENING" in s
        assert f'{BASE}/en/articles/{article["slug"]}/' in s
        assert '"@type":"Article"' in s
        opening_abs = f"{BASE}/{article['opening_asset']}?{OPENING_VERSION}"
        assert article["opening_asset"] in s
        assert f'<meta property="og:image" content="{opening_abs}">' in s
        assert f'<meta name="twitter:image" content="{opening_abs}">' in s


if __name__ == "__main__":
    build_homepage()
    build_articles()
    noindex_previews()
    validate()
    print("HUMAN launch build transforms: OK")
