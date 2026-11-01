#!/usr/bin/env python3
"""Build HN AI Tools from complete local monthly parquet files. No network by default."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request

import duckdb
from catalog import CATEGORIES, CURATED, categories_for
from extract import extract_month, read_month, write_json
from merge import product_map, product_url
from policy import AI, AI_ID, canonical, is_relevant, signal, snippet, URL_CLEAN

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'data/cache'
OUT = ROOT / 'web/data'


def fresh_stats():
    return {'mentions':0, 'ai_mentions':0, 'ai_authors':set(), 'authors':set(),
            'comments':0, 'strong':0, 'months':set(), 'by_year':Counter(), 'by_month':Counter(),
            'first':None, 'last':None, 'self':0, 'negative':0, 'snippets':[], 'keys':set()}


def consume(records, stats, seen, identities=None):
    identities = identities or {}
    for row in records:
        ident = str(row['id'])
        if ident in seen:
            continue
        seen.add(ident)
        text, author, date = row['text'], row['author'], row['date']
        if not date:
            continue
        grouped = defaultdict(list)
        members = defaultdict(set)
        ai_keys = defaultdict(bool)
        for url, position in row['links']:
            key = canonical(url)
            if key:
                primary = identities.get(key, key)
                grouped[primary].append(position)
                members[primary].add(key)
                ai_keys[primary] |= bool(AI_ID.search(key))
        if not grouped:
            continue
        ai_context = bool(AI.search(URL_CLEAN.sub('',text)))
        for key, positions in grouped.items():
            stat = stats[key]
            stat['keys'].update(members[key])
            stat['mentions'] += 1
            ai = ai_context or ai_keys[key] or bool(AI_ID.search(key))
            stat['ai_mentions'] += ai
            kind, strength = signal(text,positions)
            if kind != 'recommendation':
                stat[kind] += 1
                continue
            # Unknown/deleted authors cannot establish independent endorsements.
            if not author or author in ('[deleted]','deleted'):
                continue
            stat['comments'] += 1
            stat['authors'].add(author)
            if ai:
                stat['ai_authors'].add(author)
            stat['strong'] += strength >= 2
            stat['months'].add(date[:7])
            stat['by_year'][date[:4]] += 1
            stat['by_month'][date[:7]] += 1
            stat['first'] = min(stat['first'] or date, date)
            stat['last'] = max(stat['last'] or date, date)
            quote = {'text':snippet(text,positions[0]), 'author':author, 'date':date,
                     'url':f'https://news.ycombinator.com/item?id={ident}', 'strength':strength}
            # Retain a bounded, author-diverse shortlist, favoring explicit endorsements.
            old = next((x for x in stat['snippets'] if x['author']==author),None)
            priority = lambda x:(x['strength'],x['date'],x['url'])
            if old and priority(old) >= priority(quote):
                continue
            if old:
                stat['snippets'].remove(old)
            stat['snippets'].append(quote)
            stat['snippets'].sort(key=priority, reverse=True)
            del stat['snippets'][6:]


def github_descriptions(keys, limit):
    """Optional bounded public REST metadata; never requires a token."""
    path = CACHE / 'github_meta.json'
    metadata = json.loads(path.read_text()) if path.exists() else {}
    requests = 0
    for key in keys:
        if key in CURATED or not key.startswith('github.com/') or key in metadata:
            continue
        if requests >= min(limit,50):
            break
        if requests:
            time.sleep(1.1)
        requests += 1
        print(f'  GitHub metadata {requests}: {key}',flush=True)
        req = urllib.request.Request('https://api.github.com/repos/'+key.removeprefix('github.com/'),
                                     headers={'User-Agent':'HN-AI-Tools/1.0','Accept':'application/vnd.github+json'})
        try:
            with urllib.request.urlopen(req,timeout=15) as response:
                data=json.load(response)
                metadata[key]={'description':data.get('description') or '', 'homepage':data.get('homepage') or '', 'fetched_at':datetime.now(timezone.utc).isoformat()}
        except urllib.error.HTTPError as error:
            print(f'  GitHub HTTP {error.code}; metadata is optional',flush=True)
            if error.code in (403,429):
                break
            if error.code==404:
                metadata[key]={'description':'','status':404}
        except (OSError,ValueError) as error:
            print(f'  Metadata unavailable: {error}',flush=True)
            break
        write_json(path,metadata)
    return metadata


def fallback_description(stat):
    # Label source-derived text explicitly: do not invent product capabilities.
    for quote in stat['snippets']:
        phrase = ' '.join(URL_CLEAN.sub('', quote['text']).split()).strip(' .…[]0123456789:')
        if len(phrase)>30:
            return 'HN commenter: “' + phrase[:145].rsplit(' ',1)[0] + '…”'
    return 'A project linked in Hacker News AI and machine learning discussions.'


def aggregate(months, github_limit):
    # Discover identities first, then replay caches with aliases applied before signal/counting.
    # This avoids summing aggregates that may share the same comment IDs.
    topup_rows = []
    for path in sorted(CACHE.glob('algolia_*.json')):
        payload = json.loads(path.read_text())
        if isinstance(payload, dict):
            topup_rows.extend(payload.get('comments', []))
    keys = set()
    for month in sorted(months):
        print(f'  discovering products {month}', flush=True)
        for row in read_month(CACHE, month):
            keys.update(k for url, _ in row['links'] if (k := canonical(url)))
    for row in topup_rows:
        keys.update(k for url, _ in row['links'] if (k := canonical(url)))
    metadata = github_descriptions(sorted(keys), github_limit)
    identities = product_map(keys, metadata)
    stats = defaultdict(fresh_stats)
    seen = set()
    for month in sorted(months):
        print(f'  aggregating {month}', flush=True)
        consume(read_month(CACHE, month), stats, seen, identities)
    topups = []
    for row in topup_rows:
        if str(row['id']) not in seen:
            consume([row], stats, seen, identities)
            topups.append(row)
    tools = []
    for key, stat in stats.items():
        if len(stat['authors'])<3 or not any(is_relevant(k,stat) for k in {key} | stat['keys']):
            continue
        strong_bonus = 2 * stat['strong'] / stat['comments']
        score = len(stat['months']) + .5*math.log2(1+len(stat['authors'])) + strong_bonus
        member_keys = [key] + sorted(stat['keys'] - {key})
        curated = next((CURATED[k] for k in member_keys if k in CURATED), {})
        tools.append({'key':key, 'name':curated.get('name',key.split('/')[-1] if '/' in key else key),
                      'url':product_url(key), 'description':curated.get('description',''),
                      'links':[{'url':'https://'+k, 'label':k} for k in sorted(stat['keys'] - {key})],
                      'categories':[], 'score':round(score,3), 'comments':stat['comments'],
                      'authors':len(stat['authors']), 'months':len(stat['months']),
                      'first_seen':stat['first'], 'last_seen':stat['last'],
                      'by_year':dict(sorted(stat['by_year'].items())),
                      'by_month':dict(sorted(stat['by_month'].items())),
                      'snippets':[{k:v for k,v in q.items() if k!='strength'} for q in stat['snippets'][:3]],
                      'mentions':stat['mentions'], 'ai_context_fraction':round(stat['ai_mentions']/stat['mentions'],3),
                      'strong_recommendations':stat['strong'], 'self_mentions':stat['self'],
                      'negative_mentions':stat['negative']})
    tools.sort(key=lambda t:(-t['score'],-t['comments'],t['key']))
    tools=tools[:600]
    for tool in tools:
        key=tool['key']
        desc = next((metadata[k]['description'] for k in [key] + sorted(stats[key]['keys'] - {key})
                     if metadata.get(k, {}).get('description')), '')
        tool['description_source'] = 'curated' if tool['description'] else ('github' if desc else 'hn_excerpt')
        if not tool['description']:
            tool['description'] = ' '.join(desc.split())[:240] if desc else fallback_description(stats[key])
        tool['categories'] = categories_for(key,tool['description'] if tool['description_source']!='hn_excerpt' else '')
    audit = [{'key':key, 'mentions':s['mentions'], 'recommendations':s['comments'],
              'authors':len(s['authors']), 'ai_fraction':round(s['ai_mentions']/max(1,s['mentions']),3),
              'included':any(t['key']==key for t in tools)} for key,s in stats.items() if len(s['authors'])>=3]
    audit.sort(key=lambda x:-x['recommendations'])
    write_json(CACHE/'ranking_audit.json',audit)
    return tools, topups


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--github-meta',type=int,default=0,metavar='N',help='Fetch up to N uncached GitHub descriptions (hard cap 50); default offline')
    args=parser.parse_args()
    CACHE.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    lock = (CACHE/'build.lock').open('w')
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        parser.exit(1,'Another build is running.\n')
    conn=duckdb.connect(config={'memory_limit':'512MB','threads':'4','temp_directory':str(CACHE/'duckdb_tmp')})
    conn.execute("SET TimeZone='UTC'")
    months={}
    skipped=[]
    # Recheck after each batch to include months completed during extraction.
    while True:
        sources=[p for p in sorted((ROOT/'data/raw').glob('????-??.parquet')) if p.stem not in months and p.stem not in skipped]
        if not sources:
            break
        for source in sources:
            try:
                months[source.stem]=extract_month(conn,source,CACHE)
            except (duckdb.Error,OSError,ValueError) as error:
                print(f'WARNING: skipping {source.name}: {error}',file=sys.stderr,flush=True)
                skipped.append(source.stem)
    conn.close()
    if not months:
        parser.exit(1,'No readable complete monthly parquet files; existing web data preserved.\n')
    print('Aggregating recommendations',flush=True)
    tools,topups=aggregate(months,args.github_meta)
    dates=[m[k] for m in months.values() for k in ('first','last') if m.get(k)] + [r['date'] for r in topups]
    now=datetime.now(timezone.utc).isoformat()
    # Identify this build in metadata for reproducibility.
    build_id=hashlib.sha256((now+json.dumps(tools,sort_keys=True)).encode()).hexdigest()[:16]
    meta={'build_id':build_id,'generated_at':now,'tools_listed':len(tools),
          'comments_scanned':sum(m['comments_scanned'] for m in months.values())+len(topups),
          'comments_with_links':sum(m['comments_with_links'] for m in months.values())+len(topups),
          'date_range':{'start':min(dates),'end':max(dates)}, 'months_processed':sorted(months),
          'month_stats':[months[m] for m in sorted(months)],'skipped_months':skipped,
          'topup_comments':len(topups),'categories':CATEGORIES,
          'score_formula':'months + 0.5 × log2(1 + authors) + 2 × (strong recommendations / recommending comments)',
          'source':{'name':'open-index/hacker-news','url':'https://huggingface.co/datasets/open-index/hacker-news',
                    'license':'ODC-By 1.0','license_url':'https://opendatacommons.org/licenses/by/1-0/',
                    'origin':'https://news.ycombinator.com/','inspiration':'https://hackertube.org/'},
          'method_version':'1.1','minimum_authors':3,
          'notes':['Counts are heuristic recommendations, including neutral non-negative mentions.',
                   'Self-promotion and mostly negative link contexts do not contribute to score.',
                   'First/last seen and activity counts refer to qualifying recommendations.',
                   'Product aliases and matching repository homepages are merged before counting; secondary links are retained.',
                   'The date range reflects loaded data, not a guarantee that every comment was captured.']}
    # Keep a compact list payload; a separate ID file is unnecessary for a static build.
    write_json(OUT/'tools.json',tools)
    write_json(OUT/'meta.json',meta)
    print(f'Built {len(tools)} tools from {meta["comments_scanned"]:,} comments across {len(months)} months',flush=True)
    for i,tool in enumerate(tools[:50],1):
        print(f'{i:2}  {tool["key"]:52} {tool["comments"]:5} comments  {tool["authors"]:4} authors  {tool["months"]:2} months  AI {tool["ai_context_fraction"]:.0%}',flush=True)


if __name__=='__main__':
    main()
