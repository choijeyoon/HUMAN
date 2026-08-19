from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: str, body_attr: str | None = None, script_src: str = "assets/analytics.js?v=1") -> None:
    p = ROOT / path
    s = p.read_text(encoding="utf-8")

    if body_attr and body_attr not in s:
        s = s.replace("<body>", f'<body data-article="{body_attr}">', 1)

    marker = "HUMAN_ANALYTICS_HOOK"
    if marker not in s:
        tag = f'  <!-- {marker} -->\n  <script src="{script_src}"></script>\n'
        s = s.replace("</body>", tag + "</body>", 1)

    p.write_text(s, encoding="utf-8")


patch("index.html")
patch("articles/index.html", script_src="../assets/analytics.js?v=1")
patch("en/articles/idol-dating-betrayal/index.html", "feature-001", "../../../assets/analytics.js?v=1")
patch("en/articles/ai-love/index.html", "feature-002", "../../../assets/analytics.js?v=1")
patch("en/articles/scrolling/index.html", "feature-003", "../../../assets/analytics.js?v=1")

print("HUMAN measurement hooks: OK")
