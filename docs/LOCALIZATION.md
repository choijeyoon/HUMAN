# HUMAN localization policy — launch phase

## Launch status

English is the only fully indexable Issue 001 edition at launch.

Korean, Japanese, Chinese and Spanish entry pages remain visible as edition previews, but incomplete pages are marked `noindex,follow` during the build. They stay navigable for users without competing with the finished English articles in search.

## Expansion order

1. Korean — first full localization of the three flagship features.
2. Japanese — second full localization.
3. Chinese and Spanish — expand after the English/KO/JA article template is stable.

## One evidence base, multiple editions

Localization should preserve:

- evidence strength labels;
- the distinction between direct findings and mechanistic synthesis;
- figure status (`conceptual`, `empirical`, `open question`);
- DOI/reference targets;
- uncertainty language;
- article IDs and concept-hub links.

Do not translate claims into stronger certainty than the English evidence review supports.

## Indexing rule

A localized flagship becomes indexable only when it includes the full evidence review, references, figure captions and editorial-standard language. At that point, remove `noindex` and add reciprocal `hreflang` links across complete editions.
