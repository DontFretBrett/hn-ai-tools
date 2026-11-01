"""Resolve product identities before counting comments; entirely offline by default."""
import json
from pathlib import Path

from policy import canonical

RULES = json.loads(Path(__file__).with_name('product_aliases.json').read_text())


def product_map(keys, metadata=None, rules=None):
    rules = RULES if rules is None else rules
    aliases = {canonical('https://' + k): canonical('https://' + v)
               for k, v in rules['aliases'].items()}
    aliases = {k: v for k, v in aliases.items() if k and v and k != v}

    def resolve(key):
        visited = set()
        while key in aliases:
            if key in visited:
                raise ValueError(f'Product alias cycle at {key}')
            visited.add(key)
            key = aliases[key]
        return key

    domains = {resolve(k) for k in keys if '/' not in k}
    # Curated homepages also establish a product site when only the repo was linked.
    for repo, homepage in rules['github_homepages'].items():
        key, site = canonical('https://' + repo), canonical(homepage)
        if key and site and '/' not in site:
            aliases[resolve(key)] = resolve(site)
    excluded = set(rules.get('excluded_homepage_domains', []))
    for repo, entry in (metadata or {}).items():
        key = canonical('https://' + repo)
        site = canonical(entry.get('homepage') or '')
        site = resolve(site) if site else None
        if (key and key.startswith('github.com/') and key == resolve(key)
                and site in domains and site not in excluded):
            aliases[key] = resolve(site)
    return {key: resolve(canonical('https://' + key) or key) for key in set(keys) | set(aliases)}


def product_url(key):
    """Keep a curated product site's landing path (for example Goose on GitHub Pages)."""
    return next((url.rstrip('/') for url in RULES['github_homepages'].values()
                 if canonical(url) == key), 'https://' + key)
