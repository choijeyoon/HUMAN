# HUMAN Topic Demand Experiment v1

## Goal

Identify which HUMAN topic creates the strongest combination of curiosity and genuine reading interest before scaling editorial production.

This first pilot compares the three finished flagship features under matched distribution conditions:

| ID | Topic | Article |
| --- | --- | --- |
| feature-001 | K-pop / parasocial attachment | Why Does Idol Dating Feel Like Betrayal? |
| feature-002 | AI / intimacy | Could You Really Fall in Love With an AI? |
| feature-003 | Attention / scrolling | Why Can't We Stop Scrolling? |

The pilot is not intended to prove that one of these three is the globally optimal HUMAN topic. It is a calibration round for the measurement system and a first signal about topic demand.

## Primary funnel

1. `feature_impression` — at least 50% of a feature card entered the viewport.
2. `select_feature` — the visitor clicked that feature.
3. `view_article` — the article page loaded with its stable feature ID.
4. `engaged_read` — the article remained actively visible for 30 or 60 seconds.
5. `scroll_depth` — the reader crossed 25%, 50%, 75%, or 90%.
6. `article_complete` — the reader crossed 90%.
7. `select_related_article` — the reader chose another flagship article.

`article_exit` records active seconds and maximum scroll depth as an additional diagnostic signal.

## Decision metrics

Do not select a winner from raw pageviews alone.

### Attraction

**Feature CTR** = `select_feature / feature_impression`

This estimates whether the topic/title/visual package creates enough curiosity to earn a click once it was actually seen.

### Consumption

**30-second engaged rate** = unique sessions with `engaged_read(seconds=30) / view_article`

**50% read rate** = unique sessions reaching `scroll_depth(percent=50) / view_article`

**Completion rate** = unique sessions with `article_complete / view_article`

These distinguish genuine reading interest from a high-click, low-consumption headline.

### Depth / network effect

**Next-article rate** = `select_related_article / view_article`

This is a useful signal that the topic brought the reader into HUMAN rather than only satisfying one isolated curiosity.

## Winner rule

For the first pilot, avoid a single magic score until sample sizes are meaningful. Rank each topic on:

- Feature CTR
- 30-second engaged rate
- 50% read rate
- Completion rate
- Next-article rate

A strong candidate should be above the other topics on attraction and at least competitive on reading quality. A topic with the best CTR but clearly worse engagement should be treated as a headline/thumbnail winner, not yet an editorial-topic winner.

Do not make a strong editorial decision from tiny samples. As a practical pilot threshold, aim for at least 300 genuine feature-card impressions per topic before treating CTR differences as more than directional, and continue longer when results are close.

## Distribution rules

Keep the comparison as symmetric as possible:

- same platform and account quality
- similar posting time/day
- similar post length and visual quality
- similar paid budget if paid distribution is used
- do not selectively boost the early winner during the comparison window
- do not change article titles or opening visuals mid-cell without starting a new variant label

Use UTM parameters on every distributed link.

Recommended campaign structure:

```text
utm_campaign=topic-demand-v1
utm_source=<platform>
utm_medium=<organic|paid|social|community>
utm_content=<feature-id>-<creative-variant>
```

Examples:

```text
?utm_source=x&utm_medium=organic&utm_campaign=topic-demand-v1&utm_content=feature-001-a
?utm_source=reddit&utm_medium=community&utm_campaign=topic-demand-v1&utm_content=feature-002-a
?utm_source=instagram&utm_medium=organic&utm_campaign=topic-demand-v1&utm_content=feature-003-a
```

The analytics layer also records `referrer_host` so unattributed traffic can be diagnosed separately.

## Analytics activation

The site loads `assets/analytics-config.js` before `assets/analytics.js`.

Configure at least one destination before sending real experiment traffic:

- GA4: set `measurementId`
- Plausible: set `plausibleDomain`
- custom collector: set `endpoint`

Until one of these is configured, HUMAN still emits the browser-level `human:track` events but no data leaves the page.

For manual QA, append `?debug_analytics=1`. Events will be printed in the browser console without changing production configuration.

## Phase 2: broader topic search

After the three-topic calibration works, expand beyond the finished Issue 001 articles. Test lightweight topic packages before commissioning full articles: title + deck + thumbnail/visual + a consistent landing or waitlist action.

Candidate families can include AI/consciousness, love/relationships, music, fear, status/social behavior, attention, memory, identity, and culture. The purpose of Phase 2 is to discover demand outside the three topics that happened to be available at launch.

Do not build large newsletter, membership, payment, or localization systems before this broader demand round produces repeatable winners.
