"""Versioned, lossless-enough link extraction cache, independent of ranking policy."""
import gzip
import html
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path

VERSION = 3
URL_RE = re.compile(r'https?://[^\s<>"\x00-\x20]+', re.I)


def decode(text):
    for _ in range(2):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    return text


class CommentHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.links = []
        self.length = 0
        self.skip = 0
        self.anchor_starts = []
        self.anchor_spans = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if tag in ('p', 'br', 'li', 'div', 'blockquote'):
            self.handle_data('\n')
        if tag == 'a':
            self.anchor_starts.append(self.length)
            href = dict(attrs).get('href', '')
            if href:
                self.links.append([decode(href), self.length])

    def handle_endtag(self, tag):
        if tag == 'a' and self.anchor_starts:
            self.anchor_spans.append((self.anchor_starts.pop(), self.length))
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip:
            data = decode(data)
            self.parts.append(data)
            self.length += len(data)


def parse_comment(raw):
    parser = CommentHTML()
    # Normal HN HTML contains entity-escaped attribute values, not escaped tags.
    if '<a' not in raw.lower() and '&lt;a' in raw.lower():
        raw = html.unescape(raw)
    parser.feed(raw)
    plain = ''.join(parser.parts)
    links = parser.links + [[m.group(), m.start()] for m in URL_RE.finditer(plain)
                            if not any(start <= m.start() < end for start, end in parser.anchor_spans)]
    unique = {}
    for url, pos in links:
        url = url.rstrip('.,;:!?\'”’')
        while url.endswith(')') and url.count(')') > url.count('('):
            url = url[:-1]
        if url.lower().startswith(('https://', 'http://')) and url not in unique:
            unique[url] = pos
    return plain, [[url, pos] for url, pos in unique.items()]


def write_json(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    os.replace(temp, path)


def extract_month(conn, source, cache):
    source = Path(source)
    stat = source.stat()
    fingerprint = {'size': stat.st_size, 'mtime_ns': stat.st_mtime_ns, 'version': VERSION}
    target = cache / f'{source.stem}.links.jsonl.gz'
    meta_path = cache / f'{source.stem}.meta.json'
    if target.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        if meta.get('fingerprint') == fingerprint:
            print(f'  cached {source.stem}: {meta["comments_scanned"]:,} comments', flush=True)
            return meta
    print(f'  extracting {source.stem}', flush=True)
    schema = dict((r[0], r[1]) for r in conn.execute('DESCRIBE SELECT * FROM read_parquet(?)', [str(source)]).fetchall())
    # open-index encodes story=1, comment=2; also accept string schemas for portability.
    comment_type = "type = 'comment'" if 'VARCHAR' in schema['type'] else 'type = 2'
    scanned, first, last = conn.execute(f'''
        SELECT count(*), min(time)::DATE::VARCHAR, max(time)::DATE::VARCHAR
        FROM read_parquet(?) WHERE {comment_type}
    ''', [str(source)]).fetchone()
    cursor = conn.execute(f'''
        SELECT id, "by", time::DATE::VARCHAR, text
        FROM read_parquet(?) WHERE {comment_type}
          AND coalesce(deleted,0)=0 AND coalesce(dead,0)=0
          AND (contains(lower(text), 'href') OR contains(lower(text), 'http'))
        ORDER BY id
    ''', [str(source)])
    linked = 0
    temp = target.with_suffix('.gz.tmp')
    with gzip.open(temp, 'wt', encoding='utf-8', compresslevel=3) as out:
        while batch := cursor.fetchmany(4096):
            for ident, author, date, raw in batch:
                plain, links = parse_comment(raw or '')
                if not links:
                    continue
                linked += 1
                out.write(json.dumps({'id': ident, 'author': author or '', 'date': date,
                                      'text': plain, 'links': links}, ensure_ascii=False) + '\n')
    os.replace(temp, target)
    meta = {'month': source.stem, 'comments_scanned': scanned,
            'comments_with_links': linked, 'first': first, 'last': last,
            'fingerprint': fingerprint}
    write_json(meta_path, meta)
    return meta


def read_month(cache, month):
    with gzip.open(cache / f'{month}.links.jsonl.gz', 'rt', encoding='utf-8') as handle:
        for line in handle:
            yield json.loads(line)
