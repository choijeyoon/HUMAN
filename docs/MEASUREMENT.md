# HUMAN launch measurement

## Current state

The site now exposes a stable, vendor-neutral event layer without sending any visitor data to a third party.

Events:

- `select_feature` with `id=feature-001|feature-002|feature-003`
- `view_article` with the same stable feature IDs

The browser emits these as `human:track` CustomEvents. No network request is made by `assets/analytics.js`.

## Why this structure

HUMAN can launch without adding a cookie banner or choosing an analytics vendor prematurely. Later, a small adapter can subscribe to `human:track` and forward only the fields we decide to collect.

## Zero-cost next connections

1. Google Search Console — add the verification token when available and submit `/sitemap.xml`.
2. Optional site analytics — connect a free/privacy-conscious provider or GA4 through one adapter file.
3. Keep the launch event schema minimal: page path, feature ID, and event name. Avoid collecting article text selections, form contents, or sensitive user attributes.

## Launch KPIs

- Homepage → flagship feature click-through
- Relative clicks for Feature 001 / 002 / 003
- Search impressions and queries by article
- Indexed-page coverage
- Referral traffic to individual flagship articles

Do not optimize for raw pageviews alone; the editorial objective is qualified entry into long-form features.
