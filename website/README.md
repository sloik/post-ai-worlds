# Public introduction source

This is the canonical source for the existing [Omnicorp website](https://stocki-apps.pages.dev/omnicorp/). The maintained arguments live in [omnicorp/](../omnicorp/README.md) and [post-ai/](../post-ai/README.md). The website is the shorter introduction, with visible links to both tracks and contributions.

Build with `python3 website/build.py` from the repository root. This uses only Python's standard library. The tracked `dist/` includes the hand-authored homepage and CSS/JavaScript seed assets; it is intentionally retained and must not be deleted as disposable output. The builders regenerate the publication, artwork, curve and Observatory surfaces, then add canonical documentation links consistently to every page.

`content/` contains only the already-public curated article and Observatory inputs, not raw transcripts, private calculation audits or internal source notes. The frozen [forecast export](../evidence/forecasts/2026-11-05-records.json) retains its originally published bytes, dates, probabilities and criteria. Source relocation is not preregistration or a forecast update.

The existing host keeps a deployment snapshot, not a second authoring copy. From this checkout run `python3 website/prepare_publication.py /path/to/apps-site`, then in that host run its base `python3 build.py`, existing tests and `python3 build_omnicorp.py` before deploying its complete `dist/` through its existing Cloudflare Pages project. Preserve other app routes and host security headers. No hosting credentials or account configuration belong in this repository.

Original content and illustrations are CC BY 4.0; Python/JavaScript/CSS are MIT. See [LICENSING.md](../LICENSING.md).
