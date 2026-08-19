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

print("HUMAN measurement hooks: OK")
