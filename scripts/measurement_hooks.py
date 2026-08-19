from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(
    path: str,
    body_attr: str | None = None,
    config_src: str = "assets/analytics-config.js?v=1",
    script_src: str = "assets/analytics.js?v=2",
) -> None:
    p = ROOT / path
    s = p.read_text(encoding="utf-8")

    if body_attr and body_attr not in s:
        s = s.replace("<body>", f'<body data-article="{body_attr}">', 1)

    marker = "HUMAN_ANALYTICS_HOOK"
    if marker not in s:
        tag = (
            f'  <!-- {marker} -->\n'
            f'  <script src="{config_src}"></script>\n'
            f'  <script src="{script_src}"></script>\n'
        )
        s = s.replace("</body>", tag + "</body>", 1)

    p.write_text(s, encoding="utf-8")


patch("index.html")
patch(
    "articles/index.html",
    config_src="../assets/analytics-config.js?v=1",
    script_src="../assets/analytics.js?v=2",
)
patch(
    "en/articles/idol-dating-betrayal/index.html",
    "feature-001",
    "../../../assets/analytics-config.js?v=1",
    "../../../assets/analytics.js?v=2",
)
patch(
    "en/articles/ai-love/index.html",
    "feature-002",
    "../../../assets/analytics-config.js?v=1",
    "../../../assets/analytics.js?v=2",
)
patch(
    "en/articles/scrolling/index.html",
    "feature-003",
    "../../../assets/analytics-config.js?v=1",
    "../../../assets/analytics.js?v=2",
)

# CI-facing validation: the existing Pages workflow executes this script after every build.
analytics = (ROOT / "assets/analytics.js").read_text(encoding="utf-8")
for event_name in (
    "feature_impression",
    "select_feature",
    "view_article",
    "scroll_depth",
    "engaged_read",
    "article_complete",
    "select_related_article",
    "article_exit",
):
    assert event_name in analytics, event_name

config = (ROOT / "assets/analytics-config.js").read_text(encoding="utf-8")
assert "window.HUMAN_ANALYTICS" in config
assert "measurementId" in config
assert "plausibleDomain" in config
assert "endpoint" in config

for path in (
    "index.html",
    "articles/index.html",
    "en/articles/idol-dating-betrayal/index.html",
    "en/articles/ai-love/index.html",
    "en/articles/scrolling/index.html",
):
    built = (ROOT / path).read_text(encoding="utf-8")
    assert "HUMAN_ANALYTICS_HOOK" in built, path
    assert "analytics-config.js?v=1" in built, path
    assert "analytics.js?v=2" in built, path

print("HUMAN measurement hooks + Topic Demand v1 instrumentation: OK")
