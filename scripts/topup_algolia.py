#!/usr/bin/env python3
"""Optional, bounded sample of recent GitHub-link comments. No credentials required."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from extract import parse_comment, write_json

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'data/cache'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=3000,help='Maximum unique comments, hard cap 5000')
    args = parser.parse_args()
    limit = max(0,min(5000,args.limit))
    start = datetime(2026,9,1,tzinfo=timezone.utc)
    end = datetime.now(timezone.utc)
    if end <= start or not limit:
        print('No top-up interval requested.')
        return
    CACHE.mkdir(parents=True,exist_ok=True)
    path = CACHE / f'algolia_{start.date()}_{end.date()}.json'
    if path.exists():
        print(f'Already cached: {path.relative_to(ROOT)}; no network requests.')
        return
    comments = {}
    windows = [(int(start.timestamp()),int(end.timestamp())+1)]
    last_request = 0
    requests = 0
    warnings = []
    while windows and len(comments)<limit and requests<60:
        low,high=windows.pop()
        # Always leave at least 1.1 seconds between request start times.
        time.sleep(max(0,1.1-(time.monotonic()-last_request)))
        query=urlencode({'tags':'comment','query':'github.com','numericFilters':f'created_at_i>{low-1},created_at_i<{high}',
                         'hitsPerPage':1000,'page':0})
        last_request=time.monotonic()
        requests+=1
        try:
            request=Request('https://hn.algolia.com/api/v1/search_by_date?'+query,headers={'User-Agent':'HN-AI-Tools/1.0'})
            with urlopen(request,timeout=20) as response:
                payload=json.load(response)
        except (OSError,ValueError) as error:
            warnings.append(str(error))
            print(f'Algolia unavailable; stopping gracefully: {error}')
            break
        hits=payload.get('hits',[])
        # Algolia caps accessible search results; split time rather than losing pages.
        if payload.get('nbHits',0)>len(hits) and high-low>1:
            mid=(low+high)//2
            windows.extend([(low,mid),(mid,high)])
            continue
        for hit in hits:
            raw=hit.get('comment_text') or ''
            plain,links=parse_comment(raw)
            ident=str(hit.get('objectID',''))
            if ident.isdigit() and links and ident not in comments:
                date=datetime.fromtimestamp(hit['created_at_i'],timezone.utc).date().isoformat()
                comments[ident]={'id':int(ident),'author':hit.get('author') or '', 'date':date,'text':plain,'links':links}
            if len(comments)>=limit:
                break
        print(f'{requests} requests; {len(comments)} unique comments',flush=True)
    if comments:
        write_json(path,{'source':'HN Algolia API','start':start.isoformat(),'end':end.isoformat(),
                         'query':'github.com','sampled':True,'requests':requests,'warnings':warnings,
                         'comments':list(comments.values())})
        print(f'Cached {len(comments)} comments. Run scripts/build.py to include them.')
    else:
        print('No comments cached; the parquet build is unaffected.')


if __name__=='__main__':
    main()
