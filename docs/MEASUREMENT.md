# HUMAN launch measurement

## Current state

The site emits a vendor-neutral `human:track` CustomEvent for every measurement event. `assets/analytics.js` also forwards the same payload to each destination enabled in `assets/analytics-config.js`.

No destination is enabled by default. With an empty configuration, no analytics payload leaves the page.

Topic Demand v1 events:

- `feature_impression`: at least 50% of a homepage feature card entered the viewport
- `select_feature`: a visitor selected a homepage feature
- `view_article`: a flagship article page loaded
- `engaged_read`: the article stayed visible for 30 or 60 seconds
- `scroll_depth`: the reader crossed 25%, 50%, 75%, or 90%
- `article_complete`: the reader crossed 90%

The layer also emits `view_page`, `select_related_article`, and `article_exit` for supporting analysis.

## Connect GA4

Open `assets/analytics-config.js` and replace the empty value:

```js
measurementId: '',
```

with the Measurement ID from the HUMAN GA4 Web data stream:

```js
measurementId: 'G-ABC123XYZ9',
```

Use the exact `G-...` value. Do not add a Google API key, service-account file, account password, raw event export, or visitor-level data. A GA4 Measurement ID is included in public page source by design and is not a secret.

The build check accepts an empty value or an uppercase ID matching `G-[A-Z0-9]+`. It fails before deployment when a configured value has the wrong format.

## Local validation

Run:

```bash
python3 scripts/build_site.py
python3 scripts/measurement_hooks.py
node --check assets/analytics-config.js
node --check assets/analytics.js
```

Then serve the repository root and open:

```text
http://localhost:8000/?debug_analytics=1
```

The query flag prints emitted payloads in the browser console. It does not enable a destination by itself. When GA4 is configured, it also adds `debug_mode=true` so the events appear in DebugView. Verify `view_page`, `feature_impression`, and `select_feature` on the homepage, then verify `view_article`, `engaged_read`, `scroll_depth`, and `article_complete` on each article. Use GA4 Realtime or DebugView for the final production-stream check.

## Data policy

Keep public experiment design, aggregate results, and reproducible analysis code in GitHub. Keep raw visitor or session data in GA4 or another private store. Commit only non-identifying aggregate counts and rates under `data/` or `docs/topic-results/`.
