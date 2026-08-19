from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
articles = {
    'en/articles/idol-dating-betrayal/index.html': {
        'figure-atlas--kpop-01': ('idol-dating-fig01.svg', 'Visual explainer showing repeated media exposure, an internal social model, dating news, and emotional updating.'),
        'figure-atlas--kpop-02': ('idol-dating-fig02.svg', 'Visual evidence landscape showing strong general parasocial evidence and an open question for idol-dating-specific tests.'),
    },
    'en/articles/ai-love/index.html': {
        'figure-atlas--ai-01': ('ai-love-fig01.svg', 'Visual explainer separating human attachment to AI from the independent question of machine consciousness.'),
        'figure-atlas--ai-02': ('ai-love-fig02.svg', 'Visual evidence staircase from short-term AI connection to long-term wellbeing questions.'),
    },
    'en/articles/scrolling/index.html': {
        'figure-atlas--scroll-01': ('scrolling-fig01.svg', 'Visual explainer of the scrolling loop: cue, open, sample and continue, with reward, habit and personalization.'),
        'figure-atlas--scroll-02': ('scrolling-fig02.svg', 'Visual evidence summary comparing reward learning, habit, compulsive scrolling and brain evidence.'),
    },
}

for rel, reps in articles.items():
    p = ROOT / rel
    s = p.read_text(encoding='utf-8')
    s = s.replace('  <link rel="stylesheet" href="../../../assets/figure-atlas-v3.css">\n', '')
    for cls, (asset, alt) in reps.items():
        old_prefix = f'<div class="figure-atlas-panel {cls}" role="img" aria-label="'
        start = s.find(old_prefix)
        if start < 0:
            if f'assets/figures-v4/{asset}' in s:
                continue
            raise RuntimeError(f'{cls} not found in {rel}')
        end = s.find('</div>', start)
        if end < 0:
            raise RuntimeError(f'closing div not found for {cls}')
        end += len('</div>')
        img = (f'<img class="figure-vector-v4" '
               f'src="../../../assets/figures-v4/{asset}?v=20260819-vector1" '
               f'width="1200" height="800" loading="lazy" decoding="async" alt="{alt}">')
        s = s[:start] + img + s[end:]
    p.write_text(s, encoding='utf-8')

for rel, reps in articles.items():
    s=(ROOT/rel).read_text(encoding='utf-8')
    assert 'figure-atlas--' not in s
    assert 'figure-atlas-v3.css' not in s
    for _,(asset,_) in reps.items():
        assert f'assets/figures-v4/{asset}' in s
print('Vector figures materialized into article source HTML: OK')
