"""Deterministic, inspectable URL, recommendation, and relevance rules."""
import ipaddress
from functools import lru_cache
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import tldextract
from catalog import ALIASES, CURATED, GENERIC

DENY = json.loads((Path(__file__).parent / 'denylist.json').read_text())
DENIED_DOMAINS = set(DENY['domains'])
DENIED_KEYS = set(DENY['keys'])
REPO_DENY = re.compile('|'.join(DENY['repo_patterns']), re.I)
# Use the packaged Public Suffix List, with no network or external cache writes.
SUFFIX = tldextract.TLDExtract(suffix_list_urls=(), cache_dir=None, include_psl_private_domains=True)
PRODUCT_HOSTS = {'gemini.google.com', 'notebooklm.google.com', 'ai.google.dev',
                 'chat.openai.com', 'bard.google.com', 'chat.deepseek.com', 'ai.meta.com', 'copilot.microsoft.com', 'copilot.github.com'}
AI = re.compile(r'\b(?:ai|ml|llms?|gpt[\w.-]*|chatgpt|claude|llama[\w.-]*|ollama|vllm|'
                r'langchain|langgraph|hugging\s?face|copilot|chatbots?|tokenizers?|'
                r'embeddings?|rag|transformers?|diffusion|fine[ -]?tun\w*|'
                r'inference|neural|deep learning|machine learning|artificial intelligence|'
                r'generative|mcp|model context protocol|whisper|stable diffusion|'
                r'prompt(?:ing|s|ed)?|agentic|openai|anthropic|mistral|deepseek|qwen|'
                r'vector (?:database|db|search)|language models?|coding agents?)\b', re.I)
AI_ID = re.compile(r'(?:^|[./_-])(?:llama(?:\.cpp)?|llm|gpt\w*|whisper|ollama|vllm|'
                   r'langchain|langgraph|chatgpt|diffusers|diffusion|tiktoken|'
                   r'transformers|deepseek|qwen|ggml|mcp)(?:$|[./_-])', re.I)
POSITIVE = re.compile(r"\b(?:i (?:use|recommend|love|like|prefer)|i['’]ve been using|"
                      r"i have been using|we (?:use|recommend)|highly recommend|recommend(?:ed|ing)?|"
                      r"check (?:it |this |them )?out|works? (?:great|well|really well)|"
                      r"my favou?rite|you might (?:like|try)|give .{0,35} a try|"
                      r"worth (?:trying|checking)|great (?:tool|library|project)|"
                      r"(?:can|could|should) try|try (?:using|out)|been (?:using|happy)|"
                      r"(?:useful|excellent|fantastic|amazing|love it))\b", re.I)
NEGATIVE = re.compile(r"\b(?:avoid|terrible|awful|garbage|useless|unusable|"
                      r"(?:do not|don['’]t|wouldn['’]t|shouldn['’]t) (?:use|recommend)|"
                      r"(?:doesn['’]t|does not|didn['’]t|did not) work|"
                      r"(?:stopped|stop) using|not recommend|waste of (?:time|money)|"
                      r"(?:is|was) (?:broken|a scam)|overhyped)\b", re.I)
SELF = re.compile(r"\b(?:i (?:have )?(?:personally )?(?:built|made|created|developed|wrote|maintain)|"
                  r"we (?:built|made|created|developed)|my (?:project|tool|app|library|startup)|"
                  r"our (?:project|tool|app|startup)|shameless plug|(?:author|creator|maintainer) here)\b", re.I)
HIRING = re.compile(r"\b(?:we(?:['’]re| are) hiring|(?:seeking|looking for) (?:work|freelancers?)|join our team|apply (?:now|here)|open positions|careers@|hiring (?:for|a|an)|\|\s*(?:full[ -]?time|remote|on[ -]?site|hybrid|contract)|(?:remote|on[ -]?site)\s*\|.{0,80}(?:full[ -]?time|part[ -]?time)|(?:full[ -]?time|part[ -]?time)\s*\|.{0,80}(?:remote|on[ -]?site))\b", re.I)
REPO_RESERVED = {'features','topics','collections','settings','marketplace','sponsors','login',
                 'search','explore','orgs','organizations','users','about','pricing','apps',
                 'enterprise','security','site','contact','readme','notifications','new'}
HF_RESERVED = {'blog','docs','papers','datasets','learn','posts','collections','organizations',
               'settings','join','login','models','tasks','pricing','api','spaces'}


@lru_cache(maxsize=131072)
def canonical(url):
    try:
        if '…' in url or '...' in url:
            return None
        parsed = urlsplit(url)
        if parsed.scheme.lower() not in ('https', 'http') or not parsed.hostname or parsed.username:
            return None
        host = parsed.hostname.lower().rstrip('.')
        if len(host) > 253 or '.' not in host:
            return None
        try:
            ipaddress.ip_address(host)
            return None
        except ValueError:
            pass
        host = host.removeprefix('www.')
        host = {'www.github.com':'github.com', 'www.gitlab.com':'gitlab.com'}.get(host, host)
        parts = [unquote(p) for p in parsed.path.split('/') if p]
        # Never turn arbitrary encoded path separators into another resource identity.
        if any('/' in p or '\\' in p or any(ord(c) < 32 for c in p) for p in parts):
            return None
        # These are named AI products, rather than GitHub profile/root pages.
        if host == 'github.com' and (parts[:2] == ['features','copilot'] or parts[:1] == ['copilot']):
            return 'github.com/features/copilot'
        if host in ('github.com','gitlab.com'):
            if len(parts) < 2 or parts[0].lower() in REPO_RESERVED:
                return None
            # GitLab nested groups are preserved until the explicit /-/ route marker.
            if host == 'gitlab.com' and '-' in parts:
                parts = parts[:parts.index('-')]
            else:
                parts = parts[:2]
            if not all(re.fullmatch(r'[\w.-]+', p, re.ASCII) for p in parts):
                return None
            if len(parts) < 2:
                return None
            parts[-1] = re.sub(r'\.git$', '', parts[-1], flags=re.I)
            if not parts[-1] or REPO_DENY.search(parts[-1]):
                return None
            key = host + '/' + '/'.join(parts).lower()
        elif host == 'huggingface.co':
            if parts and parts[0] == 'spaces':
                if len(parts) < 3:
                    return None
                key = host + '/spaces/' + '/'.join(parts[1:3])
            elif len(parts) >= 2 and parts[0] not in HF_RESERVED:
                key = host + '/' + '/'.join(parts[:2])
            elif not parts or (len(parts) == 1 and parts[0] in ('models','spaces')):
                key = host
            else:
                return None
        elif host == 'pypi.org':
            if len(parts) < 2 or parts[0] != 'project':
                return None
            name = re.sub(r'[-_.]+', '-', parts[1].lower())
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
                return None
            key = 'pypi.org/project/' + name
        elif host in ('npmjs.com','npmjs.org'):
            if len(parts) < 2 or parts[0] != 'package':
                return None
            name = '/'.join(parts[1:3]) if parts[1].startswith('@') else parts[1]
            if not re.fullmatch(r'@?[a-z0-9._-]+(?:/[a-z0-9._-]+)?', name.lower()):
                return None
            key = 'npmjs.com/package/' + name.lower()
        elif host in PRODUCT_HOSTS:
            key = host
        else:
            if host in DENIED_DOMAINS or any(host.endswith('.' + d) for d in DENIED_DOMAINS):
                return None
            domain = SUFFIX(host)
            key = domain.top_domain_under_public_suffix
            if not key or domain.suffix in ('edu','gov','mil'):
                return None
        key = ALIASES.get(key, key)
        if key in DENIED_KEYS or key in DENIED_DOMAINS:
            return None
        return key
    except (ValueError, UnicodeError):
        return None


def local_context(text, pos, radius=340):
    """Use the link neighborhood; avoid scoring an unrelated paragraph's opinion."""
    left, right = max(0,pos-radius), min(len(text),pos+radius)
    paragraph_left = text.rfind('\n', left, pos)
    paragraph_right = text.find('\n', pos, right)
    if paragraph_left >= 0:
        left = paragraph_left + 1
    if paragraph_right >= 0:
        right = paragraph_right
    context = text[left:right]
    # Footnote-only link paragraphs carry their recommendation in the preceding prose.
    if len(URL_CLEAN.sub('', context).strip(' []0123456789.:')) < 25:
        context = text[max(0,pos-radius):min(len(text),pos+180)]
    return context


URL_CLEAN = re.compile(r'https?://\S+')


def signal(text, positions):
    if HIRING.search(text):
        return 'self', 0
    contexts = [local_context(text, p) for p in positions]
    if any(SELF.search(c) for c in contexts) or (len(text)<900 and SELF.search(text)):
        return 'self', 0
    positive = max((len(POSITIVE.findall(c)) for c in contexts), default=0)
    negative = max((len(NEGATIVE.findall(c)) for c in contexts), default=0)
    if negative and negative >= positive:
        return 'negative', 0
    return 'recommendation', min(3, 1 + max(0, positive-negative))


def is_relevant(key, stat):
    if (key in CURATED or key.startswith('huggingface.co/')) and key not in GENERIC:
        return True
    ratio = stat['ai_mentions'] / max(1, stat['mentions'])
    threshold = .85 if key in GENERIC else (.4 if key.startswith(('github.com/','gitlab.com/','pypi.org/','npmjs.com/')) else .6)
    return (bool(AI_ID.search(key)) or ratio >= threshold) and len(stat['ai_authors']) >= 3


def snippet(text, pos, limit=280):
    left = max(0,pos-110)
    right = min(len(text),left+limit-2)
    if left:
        next_space = text.find(' ',left,min(left+35,right))
        if next_space >= 0:
            left = next_space+1
    if right < len(text):
        prev_space=text.rfind(' ',left,right)
        if prev_space > left:
            right=prev_space
    result = re.sub(r'\s+', ' ', text[left:right]).strip()
    return (('…' if left else '') + result + ('…' if right<len(text) else ''))[:limit]
