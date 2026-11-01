"""Policy and incremental-extraction regressions using small synthetic fixtures."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import duckdb
from build import aggregate, consume, fresh_stats
from collections import defaultdict
from extract import extract_month, parse_comment
from policy import canonical, is_relevant, signal, snippet
from merge import product_map, product_url

ROOT=Path(__file__).resolve().parents[1]


class URLPolicyTests(unittest.TestCase):
    def test_repository_roots_and_renames(self):
        self.assertEqual(canonical('https://github.com/GGERGANOV/llama.cpp.git/tree/master?utm_source=x#readme'),'github.com/ggml-org/llama.cpp')
        self.assertEqual(canonical('https://gitlab.com/org/repo/-/blob/main/model.py'),'gitlab.com/org/repo')
        self.assertEqual(canonical('https://gitlab.com/group/subgroup/repo/-/issues/1'),'gitlab.com/group/subgroup/repo')
        for url in ['https://github.com','https://github.com/openai','https://github.com/topics/llm','https://gitlab.com/-/search']:
            self.assertIsNone(canonical(url))

    def test_domains_and_packages(self):
        self.assertEqual(canonical('https://docs.anthropic.com/en/docs?ref=a'),'anthropic.com')
        self.assertEqual(canonical('https://ollama.ai/download'),'ollama.com')
        self.assertEqual(canonical('https://chat.openai.com/'),'chatgpt.com')
        self.assertEqual(canonical('https://gemini.google.com/app'),'gemini.google.com')
        self.assertEqual(canonical('https://github.com/features/copilot'),'github.com/features/copilot')
        self.assertEqual(canonical('https://copilot.github.com/'),'github.com/features/copilot')
        self.assertEqual(canonical('https://copilot.microsoft.com/'),'copilot.microsoft.com')
        self.assertEqual(canonical('https://pypi.org/project/Sentence_Transformers/1.2/'),'pypi.org/project/sentence-transformers')
        self.assertEqual(canonical('https://npmjs.com/package/@scope/llm/v/1.0'),'npmjs.com/package/@scope/llm')
        self.assertEqual(canonical('https://huggingface.co/spaces/org/demo/tree/main'),'huggingface.co/spaces/org/demo')
        self.assertEqual(canonical('https://huggingface.co/mistralai/Mistral-7B-Instruct/resolve/main/config.json'),'huggingface.co/mistralai/Mistral-7B-Instruct')
        self.assertIsNone(canonical('https://huggingface.co/blog/foo'))

    def test_exclusions_and_untrusted_links(self):
        for url in ['javascript:alert(1)','https://user:password@example.com','http://127.0.0.1/a','https://arxiv.org/abs/123','https://subdomain.medium.com/post','https://www.nytimes.com/','https://gist.github.com/user/123','https://google.com/search?q=ai','https://github.com/a/awesome-llms','https://github.com/org%2Fother/repo']:
            self.assertIsNone(canonical(url),url)


class ProductMergeTests(unittest.TestCase):
    def test_curated_products_and_renames(self):
        keys = {'ollama.com', 'github.com/ollama/ollama', 'aider.chat',
                'github.com/aider-ai/aider', 'github.com/ggml-org/llama.cpp',
                'github.com/ggml-org/whisper.cpp', 'github.com/comfyanonymous/comfyui',
                'github.com/vllm-project/vllm', 'github.com/langchain-ai/langchain',
                'github.com/open-webui/open-webui', 'claude.ai', 'anthropic.com',
                'chatgpt.com', 'openai.com'}
        identities = product_map(keys)
        for repo, site in [('ollama/ollama', 'ollama.com'), ('aider-ai/aider', 'aider.chat'),
                           ('vllm-project/vllm', 'vllm.ai'), ('langchain-ai/langchain', 'langchain.com'),
                           ('comfyanonymous/comfyui', 'comfy.org'), ('open-webui/open-webui', 'openwebui.com')]:
            self.assertEqual(identities['github.com/' + repo], site)
        for key in ['claude.ai', 'anthropic.com', 'chatgpt.com', 'openai.com',
                    'github.com/ggml-org/llama.cpp', 'github.com/ggml-org/whisper.cpp']:
            self.assertEqual(identities[key], key)
        self.assertEqual(product_map({'github.com/ggerganov/llama.cpp'})['github.com/ggerganov/llama.cpp'], 'github.com/ggml-org/llama.cpp')

    def test_model_mirrors_and_distinct_products(self):
        keys = {'llama.com', 'github.com/facebookresearch/llama',
                'huggingface.co/deepseek-ai/DeepSeek-R1', 'github.com/deepseek-ai/deepseek-r1',
                'deepseek.com', 'github.com/abetlen/llama-cpp-python',
                'github.com/ggml-org/llama.cpp', 'github.com/openai/whisper',
                'github.com/ggml-org/whisper.cpp'}
        identities = product_map(keys)
        self.assertEqual(identities['github.com/facebookresearch/llama'], 'llama.com')
        self.assertEqual(identities['huggingface.co/deepseek-ai/DeepSeek-R1'], 'github.com/deepseek-ai/deepseek-r1')
        for key in keys - {'github.com/facebookresearch/llama', 'huggingface.co/deepseek-ai/DeepSeek-R1'}:
            self.assertEqual(identities[key], key)

    def test_cached_homepage_matching(self):
        keys = {'fresh-tool.ai', 'github.com/acme/runtime', 'github.com/acme/other',
                'openai.com', 'github.com/openai/sdk', 'anthropic.com', 'github.com/anthropics/sdk',
                'ai-sdk.dev', 'github.com/acme/sdk'}
        metadata = {'github.com/acme/runtime': {'homepage': 'https://docs.fresh-tool.ai/guide'},
                    'github.com/acme/other': {'homepage': 'https://absent.ai'},
                    'github.com/openai/sdk': {'homepage': 'https://openai.com'},
                    'github.com/anthropics/sdk': {'homepage': 'https://anthropic.com'},
                    'github.com/acme/sdk': {'homepage': 'https://vercel.ai'}}
        identities = product_map(keys, metadata)
        self.assertEqual(identities['github.com/acme/runtime'], 'fresh-tool.ai')
        self.assertEqual(identities['github.com/acme/sdk'], 'ai-sdk.dev')
        for key in ['github.com/acme/other', 'github.com/openai/sdk', 'github.com/anthropics/sdk']:
            self.assertEqual(identities[key], key)

    def test_union_comments_authors_months_and_signal(self):
        identities = product_map({'ollama.com', 'github.com/ollama/ollama'})
        stats = defaultdict(fresh_stats); seen = set()
        rows = [dict(id=1, author='alice', date='2026-01-01', text='I use this LLM tool.',
                     links=[['https://ollama.com', 6], ['https://github.com/ollama/ollama', 6]]),
                dict(id=2, author='alice', date='2026-02-01', text='An LLM tool.',
                     links=[['https://github.com/ollama/ollama', 3]]),
                dict(id=3, author='bob', date='2026-02-02', text='An LLM tool.',
                     links=[['https://ollama.com', 3]])]
        consume(rows, stats, seen, identities)
        consume(rows, stats, seen, identities)  # Same IDs in overlapping months/top-ups.
        self.assertEqual(set(stats), {'ollama.com'})
        stat = stats['ollama.com']
        self.assertEqual((stat['mentions'], stat['comments'], stat['strong']), (3, 3, 1))
        self.assertEqual(stat['authors'], {'alice', 'bob'})
        self.assertEqual(stat['months'], {'2026-01', '2026-02'})
        self.assertEqual(dict(stat['by_month']), {'2026-01': 1, '2026-02': 2})
        self.assertEqual(stat['keys'], {'ollama.com', 'github.com/ollama/ollama'})

    def test_aggregate_secondary_links_offline(self):
        rows = [dict(id=i, author=f'author{i}', date='2026-01-01',
                     text='I use this LLM tool.', links=[['https://ollama.com', 6],
                     ['https://github.com/ollama/ollama', 6]]) for i in range(3)]
        with tempfile.TemporaryDirectory(dir=ROOT/'data/cache') as directory:
            with patch('build.CACHE', Path(directory)), patch('build.read_month', return_value=rows), \
                 patch('build.urllib.request.urlopen', side_effect=AssertionError('Unexpected network')):
                tools, topups = aggregate({'2026-01': {}}, 0)
        self.assertEqual(len(tools), 1)
        tool = tools[0]
        self.assertEqual((tool['comments'], tool['authors'], tool['months']), (3, 3, 1))
        self.assertEqual(tool['url'], 'https://ollama.com')
        self.assertEqual(tool['links'], [{'url': 'https://github.com/ollama/ollama', 'label': 'github.com/ollama/ollama'}])
        self.assertEqual(topups, [])
        self.assertEqual(product_url('block.github.io'), 'https://block.github.io/goose')

    def test_alias_cycles_fail(self):
        with self.assertRaises(ValueError):
            product_map({'a.ai', 'b.ai'}, rules=dict(aliases={'a.ai': 'b.ai', 'b.ai': 'a.ai'}, github_homepages={}))


class SignalTests(unittest.TestCase):
    def test_html_and_bare_links(self):
        raw='I use <a href="https:&#x2F;&#x2F;github.com&#x2F;O&#x2F;R?x=1&amp;y=2">this tool</a>.<p>Try https://ollama.com/docs.'
        text,links=parse_comment(raw)
        self.assertIn('this tool',text)
        self.assertEqual(links[0][0],'https://github.com/O/R?x=1&y=2')
        self.assertEqual(links[1][0],'https://ollama.com/docs')
        self.assertEqual(text[links[0][1]:][:9],'this tool')
        text,links=parse_comment('&lt;a href="https://ollama.com/"&gt;Ollama&lt;/a&gt;')
        self.assertEqual(links[0][0],'https://ollama.com/')

    def test_anchor_display_is_not_a_second_url(self):
        text,links=parse_comment('<a href="https://huggingface.co/org/full-model-name">https://huggingface.co/org/full-model...</a>')
        self.assertEqual(len(links),1)
        self.assertEqual(links[0][0],'https://huggingface.co/org/full-model-name')

    def test_hiring_is_promotion(self):
        self.assertEqual(signal('We are hiring engineers. Try https://example.ai', [30])[0],'self')

    def test_sentiment_and_self_promotion(self):
        for text,kind in [('I use this and highly recommend it','recommendation'),('Avoid this, it is terrible','negative'),("I built this tool, check it out",'self'),('This is a link','recommendation')]:
            self.assertEqual(signal(text,[text.find('this')])[0],kind)
        self.assertGreaterEqual(signal('I use this, works great',[6])[1],2)
        self.assertEqual(signal('Avoid this tool.\n'+'Other things. '*40+'\nI recommend this other tool',[5])[0],'negative')

    def test_bounded_excerpt(self):
        text='prefix '*100+'I use this tool '+'suffix '*100
        self.assertLessEqual(len(snippet(text,710)),280)

    def test_author_threshold_and_relevance(self):
        stat=fresh_stats(); stat['mentions']=10; stat['ai_mentions']=3; stat['ai_authors']={'a','b','c'}
        self.assertFalse(is_relevant('github.com/acme/general',stat))
        stat['ai_mentions']=4
        self.assertTrue(is_relevant('github.com/acme/general',stat))
        self.assertFalse(is_relevant('unknown-tool.com',stat))
        self.assertTrue(is_relevant('github.com/acme/llm-runtime',stat))
        self.assertTrue(is_relevant('anthropic.com',stat))

    def test_one_recommendation_per_comment_per_tool(self):
        stats=defaultdict(fresh_stats); seen=set()
        row={'id':1,'author':'alice','date':'2026-01-01','text':'I use this LLM tool.','links':[['https://github.com/acme/llm-tool',6],['https://github.com/acme/llm-tool/issues/1',6]]}
        consume([row,row],stats,seen)
        stat=stats['github.com/acme/llm-tool']
        self.assertEqual(stat['comments'],1)
        self.assertEqual(stat['authors'],{'alice'})
        self.assertEqual(stat['by_year']['2026'],1)
        row=dict(row,id=2,text='I built this LLM tool.')
        consume([row],stats,seen)
        self.assertEqual(stat['comments'],1)
        self.assertEqual(stat['self'],1)

    def test_ai_tld_does_not_establish_relevance(self):
        stats=defaultdict(fresh_stats)
        row={'id':123,'author':'alice','date':'2026-01-01','text':'See https://fresh-example.ai for this.', 'links':[['https://fresh-example.ai',4]]}
        consume([row],stats,set())
        self.assertEqual(stats['fresh-example.ai']['ai_mentions'],0)

    def test_incremental_cache(self):
        # Everything, including test scratch data, stays inside the project.
        with tempfile.TemporaryDirectory(dir=ROOT/'data/cache') as directory:
            folder=Path(directory); source=folder/'2026-01.parquet'
            conn=duckdb.connect(); conn.execute("SET TimeZone='UTC'")
            conn.execute('CREATE TABLE items (id INTEGER, "by" VARCHAR, time TIMESTAMP, text VARCHAR, type TINYINT, deleted INTEGER, dead INTEGER)')
            conn.execute("INSERT INTO items VALUES (1,'alice','2026-01-01','I use https://ollama.com',2,0,0),(2,'bob','2026-01-02','No links',2,0,0),(3,'alice','2026-01-03','A story',1,0,0)")
            conn.execute('COPY items TO ? (FORMAT PARQUET)',[str(source)])
            first=extract_month(conn,source,folder); target=folder/'2026-01.links.jsonl.gz'; stamp=target.stat().st_mtime_ns
            second=extract_month(conn,source,folder)
            self.assertEqual(first,second); self.assertEqual(first['comments_scanned'],2); self.assertEqual(first['comments_with_links'],1)
            self.assertEqual(target.stat().st_mtime_ns,stamp)
            conn.close()


if __name__=='__main__':
    unittest.main()
