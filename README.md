# HN AI Tools

A static, searchable index of AI tools that Hacker News commenters keep recommending. Inspired by [Karpathy’s HackerTube](https://hackertube.org/). No frontend dependencies, build step, external fonts, paid APIs, or credentials.

Live: **https://hnaitools.dev**. Data comes from [open-index/hacker-news on Hugging Face](https://huggingface.co/datasets/open-index/hacker-news).

To rebuild after installing the dependencies below, run `bash scripts/download_hf.sh`, then `.venv/bin/python scripts/build.py`. The archive download is large; wait for it to finish for complete coverage. The committed `web/` directory is ready to deploy as static files without a build command.

## Setup

Run these commands from this folder. Dependencies are pinned official PyPI releases. Python 3.12 or later is supported; the local environment was built with Python 3.14.

```sh
UV_CACHE_DIR="$PWD/.uv-cache" uv venv .venv
UV_CACHE_DIR="$PWD/.uv-cache" uv pip install --python .venv/bin/python --only-binary :all: -r requirements.txt
.venv/bin/python scripts/build.py
```

The build reads existing `data/raw/YYYY-MM.parquet` files. It **never downloads the archive**. The separately supplied `scripts/download_hf.sh` and `logs/download.log` belong to the ongoing download. Files ending in `.parquet.part` are ignored. A corrupt complete file is reported and skipped; a later run retries it. A build with no readable months fails without replacing existing site data.

## Serve

```sh
cd web && python3 -m http.server 8788 --bind 0.0.0.0
```

Open `http://localhost:8788`. The JSON must be fetched over HTTP; opening `index.html` with `file://` will not work.

For a detached server, from the project root:

```sh
./scripts/serve.sh
```

The helper uses `nohup`, writes `logs/server.pid` and `logs/server.log`, and restarts only the matching server previously recorded by this project. It checks the process command before signaling a PID, leaving unrelated processes alone. It never operates on port 8787. If 8788 is occupied by another process, startup fails with an explanation in the log. Stop the managed server with `kill "$(cat logs/server.pid)"` after checking the pidfile still identifies that server.

## Rebuild and optional metadata

```sh
.venv/bin/python scripts/build.py
# Optional: enrich up to 50 uncurated GitHub repositories with public descriptions.
.venv/bin/python scripts/build.py --github-meta 50
# Optional: a bounded, recent sample; then rebuild to include it.
.venv/bin/python scripts/topup_algolia.py --limit 3000
.venv/bin/python scripts/build.py
```

No network requests are made by the default build. Cached GitHub descriptions and homepage URLs are used even without the flag. Older cache entries without a homepage still work; the curated homepage map fills known gaps without fetching anything. The optional GitHub REST enrichment makes at most 50 requests per invocation, waits at least a second between them, caches results in `data/cache/github_meta.json`, and stops on HTTP 403/429 or network failure. No token is needed.

The optional Algolia script samples comments containing `github.com` between September 1, 2026 and the current date. It splits overflowing result windows rather than relying on inaccessible result pages, waits at least 1.1 seconds between requests, caps requests at 60 and comments at 5,000, and skips gracefully if unavailable. Its newest-first, link-specific sample is **not** a complete census. Successful date-bounded caches are reused. Overlapping caches are deduplicated by comment ID in the build. No Algolia fetch is needed for the parquet archive.

## Data and extraction

Source: [open-index/hacker-news on Hugging Face](https://huggingface.co/datasets/open-index/hacker-news), under [Open Data Commons Attribution License 1.0](https://opendatacommons.org/licenses/by/1-0/), originally from [Hacker News](https://news.ycombinator.com/). The site attributes the dataset, source, license, inspiration, and individual comment excerpts. This is an independent project, not affiliated with Y Combinator.

The actual parquet schema uses numeric item types (`1` story, `2` comment). DuckDB counts **all comments**, then filters in SQL to live, non-deleted comments whose text contains `href` or `http`. It streams batches of 4,096 rows; no pandas or whole-file materialization. SQL uses UTC dates. HTML parsing handles entity-escaped `href` values, fully escaped anchor tags, plain text, and bare HTTP(S) URLs. Links and text are cached in gzip JSONL per month, independent of ranking rules.

Each cache is identified by source size, nanosecond modification time, and extraction version. Rebuilds only extract new or changed months, then reaggregate cached links so changes to policy or descriptions apply without rescanning parquet. A file completed during extraction is picked up in another discovery pass. Builds use a process lock and atomic file replacements. Months completed after discovery or during aggregation are included on the next run. The bundled Public Suffix List is used offline, so domain normalization performs no network requests.

**URL normalization:** GitHub URLs become lowercase `github.com/owner/repo`, stripping `.git` and trailing routes. GitLab similarly recognizes nested groups when a `/-/` route identifies the repository boundary; unmarked paths use the first two components. Hugging Face models keep `org/model`; Spaces keep `spaces/org/space`. PyPI retains `pypi.org/project/name` with PEP 503 name normalization, and npm retains `npmjs.com/package/name` (including scopes). Registry namespaces are retained to avoid collisions between unrelated packages. Other sites become their registrable domain, except explicitly preserved product hosts such as Gemini, NotebookLM, and Microsoft Copilot. The named GitHub Copilot product routes are preserved as a specific exception to the repository-only GitHub rule. Paths, query parameters, tracking, and fragments are discarded. Explicit rename aliases merge old domains or repository owners. Product websites and source repositories are merged before recommendation counts and ranking are calculated. `scripts/product_aliases.json` supplies reviewed aliases and repository homepages; a cached/fetched GitHub homepage also merges a repo when its normalized domain matches an observed domain tool. Curated homepages can establish the primary product site even when only the repo was linked. Company/shared hosting domains (including OpenAI, Anthropic, and Hugging Face) are excluded from automatic homepage merging. Claude and Anthropic, and ChatGPT and OpenAI, remain distinct. Repositories without a dedicated product site, such as llama.cpp and whisper.cpp, retain their canonical repository URL; old owner URLs merge through rename aliases, while bindings and forks remain independent.

`scripts/denylist.json` excludes news, papers, social networks, generic blogs, URL shorteners, generic root/profile pages, obvious resource lists, and other non-tools. `scripts/catalog.py` contains the human-written descriptions, known AI projects, category rules, generic-infrastructure exceptions, and URL rename aliases. `scripts/product_aliases.json` contains cross-key product merges and curated GitHub homepages. These files can be extended without invalidating extraction caches.

## Recommendations and ranking

- A product counts at most once per comment, even if links point to both its site and repository. Alias resolution groups all link positions before sentiment and relevance scoring. Comments, authors, and active months are unions, and year/month counters, strong recommendations, and raw mention counts are recomputed from distinct comment IDs; aggregate counters are never added together. Comment IDs are deduplicated across months and optional top-ups.
- A comment is a qualifying recommendation unless its link context is mostly negative or obviously self-promotional. Neutral, non-negative mentions count. Positive phrases such as “I use,” “highly recommend,” and “works great” increase strength. Negative phrases such as “avoid,” “terrible,” and “don’t use” subtract from it. Negative cues at least as numerous as positive cues exclude the mention.
- The heuristic uses a link neighborhood of up to 340 characters on each side, restricted to the paragraph when possible. Footnote-only link paragraphs look back into the preceding prose. Self-promotional phrases near a link, or in a short comment, exclude it from scoring. Obvious hiring ads are also treated as promotion. Self and negative counts remain available in JSON for transparency. No sentiment model or LLM is used.
- AI relevance uses explicit AI/ML terms in the comment or tool identity, **not unrelated story titles**. URLs are removed before matching comment terms so an `.ai` domain alone cannot qualify. At least 40% of all mentions must have AI context for unknown repositories/packages, 60% for unknown domains, and 85% for known generic infrastructure. Explicitly AI-related repository names count as AI context. A curated allowlist of known AI tools bypasses the fraction check, except generic-infrastructure entries. Non-allowlisted entries also need at least three independent recommending authors in AI context.
- Every listed entry needs **at least three distinct recommending authors**. Unknown/deleted authors cannot establish an independent recommendation.

The score is:

```text
active months + 0.5 × log2(1 + distinct recommending authors)
              + 2 × (strong recommendations / recommending comments)
```

A strong recommendation has more positive than negative cues. Months dominate: one author repeatedly posting cannot manufacture author diversity, and a one-month burst has less staying power than sustained discussion. The strong bonus is capped at two points. Ties use recommending comment count, then canonical key. Output is capped at 600 tools.

`comments`, `authors`, `months`, `first_seen`, `last_seen`, `by_year`, and `by_month` refer to qualifying recommendations, **not all raw mentions**. AI-context fractions use all observed mentions, including self/negative ones, to avoid cherry-picking a denominator. Representative excerpts are at most 280 characters, selected for positive language and recency, from up to three different authors. Each links to the original HN comment.

Descriptions use the curated catalog first, cached public GitHub descriptions second, and explicitly labeled HN excerpts as a fallback. Category rules use tool identity and descriptions, not unrelated wording elsewhere in a comment. This index observes links, so tools discussed without links are undercounted. Heuristics can misread sarcasm, comparisons, mixed opinions, and self-promotion; read the excerpts before interpreting a count as an endorsement. Historical recommendations do not guarantee a product is still available.

## Files and verification

```text
scripts/build.py          CLI, aggregation, scoring, optional GitHub metadata
scripts/extract.py        streaming extraction and per-month caches
scripts/policy.py         normalization, sentiment, relevance, snippets
scripts/catalog.py        curated descriptions, URL renames, categories
scripts/product_aliases.json reviewed product aliases and repository homepages
scripts/merge.py          offline product identity resolution
scripts/denylist.json     editable exclusions
scripts/topup_algolia.py  optional bounded recent sample
scripts/serve.sh          detached server helper
web/index.html            static page and method dialog
web/style.css             responsive light/dark styles
web/app.js                search, categories, sorting, activity, excerpts
web/data/tools.json       ranked tools (up to 600)
web/data/meta.json        exact coverage, counters, attribution, method
```

The browser uses DOM text nodes for dataset content and validates link protocols; comment text is never interpreted as HTML. Each tool has a primary `url` and a `links` array of secondary `{url, label}` objects (empty when there are none). Secondary links appear on its card. Search includes names, keys, secondary links, descriptions, and excerpts. Category counts follow search/activity filters. Ranks remain the global score ranks when filtering or sorting. The activity toggle is relative to the archive’s final date. Per-year bar sparklines show recommendations per calendar year (bar heights are relative within each tool).

```sh
.venv/bin/python -m unittest discover -s tests -v
bash -n scripts/serve.sh
```

Tests cover entity decoding, link positions, normalization, exclusions, recommendation/self-promotion rules, AI relevance, comment/author/month unions across product aliases, cached homepage matching, product/company separation, alias cycles, deduplication, and reuse of unchanged monthly extraction caches. Build logs and `data/cache/ranking_audit.json` help inspect included and excluded candidates. Generated `web/data/` is ready to serve; raw data, caches, the environment, logs, and research exports are ignored by git.

Project code is available under the [MIT License](LICENSE). Dataset content retains the source attribution and license described above.
