"""Human-written tool descriptions and category rules; no generated marketing text."""
CATEGORIES = [
    'LLM apps & chat', 'Local inference & runtimes', 'Coding agents & assistants',
    'Frameworks & libraries (agents/RAG)', 'Model hubs & models',
    'Vector DBs & retrieval', 'Image/audio/video generation', 'Speech & transcription',
    'Training & fine-tuning', 'Evals & observability', 'MCP & tool integrations',
    'Dev tools/other AI',
]
# key | display name | category index | factual, intentionally short description
_ROWS = """
openai.com|OpenAI|0|Language, vision, and audio models available through an API.
chatgpt.com|ChatGPT|0|OpenAI's conversational assistant for writing, research, and coding.
anthropic.com|Anthropic|0|Claude language models and APIs for conversational and coding applications.
claude.ai|Claude|0|Anthropic's AI assistant for writing, analysis, and software development.
perplexity.ai|Perplexity|0|AI search and answers with links to supporting sources.
poe.com|Poe|0|Chat interface for accessing models and bots from multiple providers.
gemini.google.com|Gemini|0|Google's conversational AI assistant.
ai.google.dev|Google AI Studio|0|Developer tools and API access for Google's Gemini models.
notebooklm.google.com|NotebookLM|0|Research assistant that answers questions about supplied sources.
you.com|You.com|0|AI search and chat with tools for web research.
phind.com|Phind|2|AI search and question answering aimed at developers.
kagi.com|Kagi|0|Paid search with optional AI answering and summarization tools.
mistral.ai|Mistral AI|4|Open-weight language models, hosted APIs, and the Le Chat assistant.
deepseek.com|DeepSeek|4|Language and reasoning models with open weights and hosted access.
cohere.com|Cohere|0|Language, embedding, and reranking models for enterprise applications.
ai21.com|AI21|0|Language models and APIs for text generation and enterprise applications.
character.ai|Character.AI|0|Conversational AI characters and user-created chatbots.
pi.ai|Pi|0|A conversational AI assistant designed for everyday dialogue.
groq.com|Groq|1|Hosted model inference powered by Groq's specialized processors.
together.ai|Together AI|1|Hosted inference and fine-tuning for open-weight AI models.
fireworks.ai|Fireworks AI|1|Hosted inference and fine-tuning for generative models.
replicate.com|Replicate|6|Run hosted machine learning models through a web interface or API.
openrouter.ai|OpenRouter|0|A unified API for accessing models from multiple providers.
modal.com|Modal|11|Serverless Python compute with GPU support for AI workloads.
runpod.io|RunPod|11|GPU cloud compute and serverless inference infrastructure.
lambdalabs.com|Lambda|11|GPU cloud instances and hardware for machine learning workloads.
huggingface.co|Hugging Face|4|A hub for models, datasets, and interactive machine learning demos.
ollama.com|Ollama|1|Download and run language models locally through a CLI and API.
lmstudio.ai|LM Studio|1|Desktop application for downloading, chatting with, and serving local models.
gpt4all.io|GPT4All|1|Desktop software for running language models locally.
jan.ai|Jan|1|An open-source desktop assistant for running local language models.
nomic.ai|Nomic|5|Embedding models and tools for exploring large datasets.
llamafile.ai|llamafile|1|Package and run language models as portable executable files.
mlc.ai|MLC AI|1|Compile and deploy machine learning models across hardware platforms.
pytorch.org|PyTorch|8|Tensor computing and neural network training with Python.
tensorflow.org|TensorFlow|8|A framework for training and deploying machine learning models.
keras.io|Keras|8|A high-level API for building and training neural networks.
scikit-learn.org|scikit-learn|8|Classical machine learning algorithms and preprocessing tools for Python.
fast.ai|fast.ai|8|Deep learning courses and a PyTorch-based training library.
langchain.com|LangChain|3|Libraries and tools for building applications around language models.
llamaindex.ai|LlamaIndex|3|Connect language models to data for retrieval and agent applications.
haystack.deepset.ai|Haystack|3|Build search, retrieval, and language model application pipelines.
dspy.ai|DSPy|3|Program and optimize language model pipelines with structured modules.
pydantic.dev|Pydantic AI|3|A Python agent framework built around typed data and model outputs.
semantic-kernel.com|Semantic Kernel|3|An SDK for connecting AI models with application functions.
crewai.com|CrewAI|3|A framework for orchestrating teams of AI agents.
autogenhub.github.io|AutoGen|3|A framework for building applications with communicating AI agents.
langgraph.com|LangGraph|3|Build stateful agent workflows using graph-based control flow.
flowiseai.com|Flowise|3|A visual interface for building language model workflows.
dify.ai|Dify|3|An open-source platform for building AI applications and workflows.
n8n.io|n8n|10|A workflow automation platform with AI and tool integrations.
anythingllm.com|AnythingLLM|0|Chat with documents using local or hosted models.
openwebui.com|Open WebUI|0|A self-hosted interface for local and remote language models.
librechat.ai|LibreChat|0|A self-hosted chat interface supporting multiple model providers.
typingmind.com|TypingMind|0|A chat interface for using language models with your own API keys.
msty.app|Msty|0|A desktop interface for chatting with local and hosted AI models.
chatboxai.app|Chatbox|0|A desktop client for chatting with multiple language model providers.
aider.chat|Aider|2|A terminal coding assistant that edits files in your Git repository.
cursor.com|Cursor|2|A code editor with integrated AI chat, completion, and agent workflows.
cursor.sh|Cursor|2|A code editor with integrated AI chat, completion, and agent workflows.
codeium.com|Codeium|2|AI code completion and chat tools for software development.
windsurf.com|Windsurf|2|An AI-focused code editor with completion and agent-assisted editing.
continue.dev|Continue|2|Open-source AI coding assistance integrated with code editors.
tabnine.com|Tabnine|2|AI code completion and assistance for development environments.
sourcegraph.com|Sourcegraph Cody|2|Code search and AI assistance grounded in repository context.
replit.com|Replit|2|A browser-based development environment with AI coding assistance.
bolt.new|Bolt|2|Build and edit web applications using an AI assistant in the browser.
lovable.dev|Lovable|2|Generate and edit web applications through a conversational interface.
v0.dev|v0|2|Generate user interfaces and web applications from prompts.
zed.dev|Zed|2|A code editor with collaborative and AI-assisted development features.
pearai.com|PearAI|2|An open-source editor integrating AI coding assistance.
qdrant.tech|Qdrant|5|A vector database for similarity search and retrieval applications.
pinecone.io|Pinecone|5|A managed vector database for semantic retrieval.
weaviate.io|Weaviate|5|An open-source vector database with hybrid search support.
trychroma.com|Chroma|5|An open-source embedding database for AI applications.
lancedb.com|LanceDB|5|A database for storing and searching vector and multimodal data.
vespa.ai|Vespa|5|A search and serving engine supporting vectors and ranking models.
marqo.ai|Marqo|5|Embedding generation and vector search for text and images.
meilisearch.com|Meilisearch|5|A search engine with keyword, vector, and hybrid search features.
typesense.org|Typesense|5|An open-source search engine supporting keyword and vector retrieval.
midjourney.com|Midjourney|6|Generate and edit images from text and image prompts.
stability.ai|Stability AI|6|Generative image, audio, and video models, including Stable Diffusion.
blackforestlabs.ai|Black Forest Labs|6|The developers of FLUX image generation models.
runwayml.com|Runway|6|AI video generation and editing tools.
pika.art|Pika|6|Generate and modify short videos using AI.
ideogram.ai|Ideogram|6|Generate images from prompts, including designs with rendered text.
leonardo.ai|Leonardo|6|AI image creation and editing for visual assets.
civitai.com|Civitai|4|A community hub for image generation models and workflows.
suno.com|Suno|6|Generate songs and music from text prompts.
udio.com|Udio|6|Generate music and vocals from text prompts.
elevenlabs.io|ElevenLabs|7|Speech synthesis, voice cloning, and audio generation APIs.
deepgram.com|Deepgram|7|Speech recognition and voice APIs for audio applications.
assemblyai.com|AssemblyAI|7|Speech recognition and audio analysis APIs.
whisper.cpp|whisper.cpp|7|A portable C/C++ implementation of OpenAI's Whisper speech recognition.
macwhisper.com|MacWhisper|7|A macOS application for transcribing audio with Whisper models.
wisprflow.ai|Wispr Flow|7|Voice dictation software that turns speech into formatted text.
superwhisper.com|Superwhisper|7|Voice dictation for macOS using local and hosted speech models.
wandb.ai|Weights & Biases|9|Track experiments, evaluate models, and monitor AI applications.
comet.com|Comet|9|Experiment tracking and evaluation tools for machine learning.
langfuse.com|Langfuse|9|Open-source tracing, evaluations, and prompt management for LLM apps.
langsmith.com|LangSmith|9|Trace, test, and evaluate language model applications.
braintrust.dev|Braintrust|9|Tools for evaluating, monitoring, and iterating on AI applications.
helicone.ai|Helicone|9|Request logging, usage analytics, and observability for LLM APIs.
arize.com|Arize|9|Observability and evaluation tools for machine learning and LLM systems.
phoenix.arize.com|Arize Phoenix|9|Open-source tracing and evaluation for language model applications.
promptfoo.dev|Promptfoo|9|Test prompts and evaluate model outputs with repeatable comparisons.
humanloop.com|Humanloop|9|Tools for managing prompts and evaluating language model applications.
unsloth.ai|Unsloth|8|Tools for efficient fine-tuning and training of language models.
axolotl.ai|Axolotl|8|Configuration-driven fine-tuning of open language models.
lightning.ai|Lightning AI|8|PyTorch training tooling and cloud development environments.
mlflow.org|MLflow|9|Track experiments and manage machine learning and generative AI workflows.
bentoml.com|BentoML|1|Package and serve machine learning models as production services.
ray.io|Ray|8|Distributed Python execution for training, tuning, and model serving.
modelcontextprotocol.io|Model Context Protocol|10|A protocol connecting AI applications to external data and tools.
smithery.ai|Smithery|10|Discover and deploy integrations using Model Context Protocol.
github.com/ggml-org/llama.cpp|llama.cpp|1|Run language model inference in C/C++ on local CPUs and GPUs.
github.com/ggml-org/ggml|ggml|1|A tensor library for machine learning inference on commodity hardware.
github.com/ggml-org/whisper.cpp|whisper.cpp|7|Run Whisper speech recognition locally in C/C++.
github.com/ollama/ollama|Ollama|1|Download and run language models locally through a CLI and API.
github.com/nomic-ai/gpt4all|GPT4All|1|Run local language models with a desktop application and SDK.
github.com/mudler/localai|LocalAI|1|Self-host model inference behind an OpenAI-compatible API.
github.com/vllm-project/vllm|vLLM|1|High-throughput language model inference and serving with efficient batching.
github.com/sgl-project/sglang|SGLang|1|A runtime for serving language and multimodal models efficiently.
github.com/mlc-ai/mlc-llm|MLC LLM|1|Compile and run language models across desktop, mobile, and web hardware.
github.com/mozilla-ai/llamafile|llamafile|1|Distribute and run language models as portable executable files.
github.com/justineTunney/llamafile|llamafile|1|Distribute and run language models as portable executable files.
github.com/ml-explore/mlx|MLX|1|An array and machine learning framework for Apple silicon.
github.com/ml-explore/mlx-lm|MLX LM|1|Run and fine-tune language models on Apple silicon using MLX.
github.com/huggingface/transformers|Transformers|4|Load and use pretrained language, vision, audio, and multimodal models.
github.com/huggingface/diffusers|Diffusers|6|Python pipelines for diffusion-based image, audio, and video generation.
github.com/huggingface/accelerate|Accelerate|8|Simplify distributed and mixed-precision model training with PyTorch.
github.com/huggingface/peft|PEFT|8|Parameter-efficient fine-tuning methods for pretrained models.
github.com/huggingface/trl|TRL|8|Train language models with supervised and reinforcement learning methods.
github.com/huggingface/text-generation-inference|Text Generation Inference|1|Serve language models with batching and optimized inference kernels.
github.com/pytorch/pytorch|PyTorch|8|Tensor computing and automatic differentiation for deep learning.
github.com/jax-ml/jax|JAX|8|Accelerated array computation with automatic differentiation and compilation.
github.com/google/gemma.cpp|gemma.cpp|1|A lightweight C++ inference implementation for Gemma language models.
github.com/google-gemini/gemma-cookbook|Gemma Cookbook|4|Examples and recipes for using Google's Gemma models.
github.com/openai/whisper|Whisper|7|OpenAI's open-source multilingual speech recognition models.
github.com/systran/faster-whisper|faster-whisper|7|Run Whisper speech recognition with CTranslate2 for efficient inference.
github.com/vaibhavs10/insanely-fast-whisper|Insanely Fast Whisper|7|A tool for accelerated audio transcription using Whisper.
github.com/coqui-ai/tts|Coqui TTS|7|Tools and models for speech synthesis and voice generation.
github.com/rhasspy/piper|Piper|7|A lightweight neural text-to-speech system designed for local use.
github.com/openai/openai-python|OpenAI Python SDK|3|The official Python client for OpenAI's API.
github.com/openai/tiktoken|tiktoken|11|A fast byte-pair tokenizer for OpenAI models.
github.com/openai/clip|CLIP|4|A model for matching images and natural language in a shared embedding space.
github.com/openai/triton|Triton|8|A language and compiler for writing efficient GPU kernels.
github.com/karpathy/nanoGPT|nanoGPT|8|A compact implementation for training and fine-tuning GPT-style models.
github.com/karpathy/llm.c|llm.c|8|Train language models using minimal C and CUDA implementations.
github.com/karpathy/micrograd|micrograd|8|A small automatic differentiation engine for learning neural network basics.
github.com/karpathy/minGPT|minGPT|8|A compact PyTorch implementation of GPT for educational use.
github.com/karpathy/llm101n|LLM101n|8|Educational material about building and understanding language models.
github.com/karpathy/nanochat|nanochat|8|A compact end-to-end codebase for training and running a chat model.
github.com/langchain-ai/langchain|LangChain|3|Components for building language model applications with retrieval and tools.
github.com/langchain-ai/langgraph|LangGraph|3|Build stateful agent workflows with explicit graph-based control flow.
github.com/run-llama/llama_index|LlamaIndex|3|Connect language models to external data and retrieval pipelines.
github.com/deepset-ai/haystack|Haystack|3|Build retrieval, search, and language model application pipelines.
github.com/stanfordnlp/dspy|DSPy|3|Program and optimize language model pipelines with structured modules.
github.com/microsoft/autogen|AutoGen|3|Build applications composed of interacting AI agents.
github.com/microsoft/semantic-kernel|Semantic Kernel|3|Connect AI models to application functions and workflows.
github.com/crewAIInc/crewAI|CrewAI|3|Orchestrate role-based AI agents and their workflows.
github.com/pydantic/pydantic-ai|Pydantic AI|3|A typed Python framework for model-backed agents and tools.
github.com/guidance-ai/guidance|Guidance|3|Control language model generation with structured templates and constraints.
github.com/dottxt-ai/outlines|Outlines|3|Generate structured text from language models with schema constraints.
github.com/bitsandbytes-foundation/bitsandbytes|bitsandbytes|8|Quantized matrix operations and optimizers for efficient model training.
github.com/lm-sys/fastchat|FastChat|0|Train, serve, and evaluate chatbots based on large language models.
github.com/bigscience-workshop/petals|Petals|1|Run large language models collaboratively across distributed machines.
github.com/bellard/ts_server|TextSynth Server|1|A server for running language model inference through an API.
github.com/abetlen/llama-cpp-python|llama-cpp-python|1|Python bindings and an OpenAI-compatible server for llama.cpp.
github.com/oobabooga/text-generation-webui|Text generation web UI|0|A web interface for running and chatting with local language models.
github.com/open-webui/open-webui|Open WebUI|0|A self-hosted chat interface for local and remote language models.
github.com/lobehub/lobe-chat|LobeChat|0|A self-hostable chat interface with multiple model providers and tools.
github.com/danny-avila/librechat|LibreChat|0|A self-hosted chat application supporting multiple model providers.
github.com/mintplex-labs/anything-llm|AnythingLLM|0|Chat with documents using local or hosted models.
github.com/imartinez/privategpt|PrivateGPT|0|Ask questions about private documents using locally hosted models.
github.com/PromtEngineer/localGPT|LocalGPT|0|Chat with documents locally using retrieval and language models.
github.com/h2oai/h2ogpt|h2oGPT|0|A document chat and retrieval application for open language models.
github.com/Significant-Gravitas/AutoGPT|AutoGPT|3|Tools for building and running autonomous AI agent workflows.
github.com/yoheinakajima/babyagi|BabyAGI|3|An experimental framework exploring task-driven AI agents.
github.com/assafelovic/gpt-researcher|GPT Researcher|3|An agent that gathers sources and produces research reports.
github.com/All-Hands-AI/OpenHands|OpenHands|2|An open-source platform for software development agents.
github.com/Aider-AI/aider|Aider|2|A terminal coding assistant that edits files in your Git repository.
github.com/continuedev/continue|Continue|2|Open-source AI coding assistance integrated with code editors.
github.com/cline/cline|Cline|2|An editor-based coding agent that can edit files and run development tools.
github.com/RooCodeInc/Roo-Code|Roo Code|2|An editor-based AI coding agent with configurable modes and tools.
github.com/TabbyML/tabby|Tabby|2|A self-hosted AI coding assistant and completion server.
github.com/paul-gauthier/aider|Aider|2|A terminal coding assistant that edits files in your Git repository.
github.com/sweepai/sweep|Sweep|2|An AI coding assistant for repository changes and code maintenance.
github.com/princeton-nlp/swe-agent|SWE-agent|2|A software engineering agent that works on repository issues.
github.com/geekan/MetaGPT|MetaGPT|3|A multi-agent framework for coordinating software development tasks.
github.com/chroma-core/chroma|Chroma|5|An embedding database for retrieval and AI applications.
github.com/qdrant/qdrant|Qdrant|5|A vector search engine with filtering and hybrid retrieval support.
github.com/facebookresearch/faiss|FAISS|5|A library for efficient similarity search over dense vectors.
github.com/pgvector/pgvector|pgvector|5|Vector storage and similarity search inside PostgreSQL.
github.com/milvus-io/milvus|Milvus|5|A distributed vector database for similarity search.
github.com/lancedb/lancedb|LanceDB|5|A database for vector and multimodal search.
github.com/UKPLab/sentence-transformers|Sentence Transformers|5|Create text and multimodal embeddings for semantic search and similarity.
github.com/spotify/annoy|Annoy|5|A library for approximate nearest-neighbor search over vectors.
github.com/nmslib/hnswlib|hnswlib|5|A lightweight approximate nearest-neighbor search library.
github.com/ AUTOMATIC1111/stable-diffusion-webui|Stable Diffusion web UI|6|A browser interface for running and customizing Stable Diffusion.
github.com/comfyanonymous/ComfyUI|ComfyUI|6|A node-based interface for image and video generation workflows.
github.com/invoke-ai/InvokeAI|InvokeAI|6|A local image generation and editing environment based on diffusion models.
github.com/lllyasviel/Fooocus|Fooocus|6|An image generation interface that simplifies Stable Diffusion workflows.
github.com/lllyasviel/ControlNet|ControlNet|6|Control diffusion image generation using structures such as edges and poses.
github.com/Stability-AI/stablediffusion|Stable Diffusion|6|Code for latent diffusion text-to-image models.
github.com/CompVis/stable-diffusion|Stable Diffusion|6|The original open-source Stable Diffusion text-to-image implementation.
github.com/black-forest-labs/flux|FLUX|6|Inference code for Black Forest Labs' FLUX image generation models.
github.com/Sanster/IOPaint|IOPaint|6|An image inpainting and editing tool using machine learning models.
github.com/facebookresearch/segment-anything|Segment Anything|6|A promptable model for identifying and segmenting objects in images.
github.com/facebookresearch/sam2|SAM 2|6|Promptable object segmentation for images and video.
github.com/suno-ai/bark|Bark|7|A generative text-to-audio model supporting speech and other sounds.
github.com/facebookresearch/audiocraft|AudioCraft|6|Research code for generative music and audio models.
github.com/unslothai/unsloth|Unsloth|8|Efficient fine-tuning and training tools for language models.
github.com/axolotl-ai-cloud/axolotl|Axolotl|8|Configuration-driven training and fine-tuning of language models.
github.com/hiyouga/LLaMA-Factory|LLaMA-Factory|8|A unified interface for fine-tuning and evaluating language models.
github.com/artidoro/qlora|QLoRA|8|Code for parameter-efficient fine-tuning of quantized language models.
github.com/microsoft/DeepSpeed|DeepSpeed|8|Optimize large-model training and inference across GPUs.
github.com/Lightning-AI/pytorch-lightning|PyTorch Lightning|8|Organize PyTorch training code and scale it across accelerators.
github.com/EleutherAI/lm-evaluation-harness|LM Evaluation Harness|9|Evaluate language models on a collection of reproducible benchmark tasks.
github.com/promptfoo/promptfoo|Promptfoo|9|Test prompts and compare model outputs with repeatable evaluations.
github.com/langfuse/langfuse|Langfuse|9|Tracing, evaluation, and prompt management for language model applications.
github.com/Arize-ai/phoenix|Arize Phoenix|9|Open-source tracing and evaluation for language model applications.
github.com/BerriAI/litellm|LiteLLM|3|Call multiple model providers through a unified API and proxy.
github.com/jmorganca/ollama|Ollama|1|Download and run language models locally through a CLI and API.
github.com/simonw/llm|LLM|11|A command-line tool and Python library for working with language models.
github.com/simonw/datasette|Datasette|11|Explore and publish structured data, with plugins for AI-assisted queries.
github.com/modelcontextprotocol/servers|MCP servers|10|Reference implementations connecting AI applications to tools and data.
github.com/modelcontextprotocol/python-sdk|MCP Python SDK|10|Python tooling for building Model Context Protocol clients and servers.
github.com/jlowin/fastmcp|FastMCP|10|Build Model Context Protocol servers and clients in Python.
github.com/browser-use/browser-use|Browser Use|10|Let AI agents interact with websites through browser automation.
github.com/mendableai/firecrawl|Firecrawl|10|Extract website content into formats suited to AI applications.
github.com/jina-ai/reader|Jina Reader|10|Convert web pages into readable text for search and AI applications.
github.com/gradio-app/gradio|Gradio|11|Build web interfaces and share demos for machine learning models.
github.com/streamlit/streamlit|Streamlit|11|Build interactive data and machine learning applications in Python.
github.com/rasbt/LLMs-from-scratch|LLMs from Scratch|8|Educational code for implementing and training language models.
github.com/rasbt/lit-llama|Lit-LLaMA|8|A compact implementation of LLaMA training and fine-tuning.
github.com/BlinkDL/RWKV-LM|RWKV|4|A recurrent language model architecture and its training code.
github.com/nomic-ai/atlas|Nomic Atlas|5|Tools for exploring and organizing large embedding datasets.
github.com/ggerganov/llama.cpp|llama.cpp|1|Run language model inference in C/C++ on local CPUs and GPUs.
"""
CURATED = {}
for row in _ROWS.strip().splitlines():
    key, name, category, description = row.split('|')
    CURATED[key.lower().replace(' ', '')] = dict(name=name, categories=[CATEGORIES[int(category)]], description=description)

# Explicit aliases only: domains and source repositories otherwise remain separate entries.
ALIASES = {
    'ollama.ai': 'ollama.com', 'cursor.sh': 'cursor.com', 'bard.google.com': 'gemini.google.com',
    'chat.openai.com': 'chatgpt.com', 'chat.deepseek.com': 'deepseek.com',
    'github.com/ggerganov/llama.cpp': 'github.com/ggml-org/llama.cpp',
    'github.com/ggerganov/ggml': 'github.com/ggml-org/ggml',
    'github.com/ggerganov/whisper.cpp': 'github.com/ggml-org/whisper.cpp',
    'github.com/jmorganca/ollama': 'github.com/ollama/ollama',
    'github.com/paul-gauthier/aider': 'github.com/aider-ai/aider',
    'github.com/jerryjliu/llama_index': 'github.com/run-llama/llama_index',
    'github.com/hwchase17/langchain': 'github.com/langchain-ai/langchain',
    'github.com/stanfordnlp/dspy': 'github.com/stanfordnlp/dspy',
    'github.com/stanfordnlp/dsp': 'github.com/stanfordnlp/dspy',
    'github.com/justinetunney/llamafile': 'github.com/mozilla-ai/llamafile',
    'github.com/cthewhale/llama.cpp': 'github.com/ggml-org/llama.cpp',
    'github.com/lm-sys/fastchat': 'github.com/lm-sys/fastchat',
    'github.com/openinterpreter/open-interpreter': 'github.com/openinterpreter/open-interpreter',
    'github.com/langgenius/dify': 'github.com/langgenius/dify',
    'github.com/tmatis/llama.cpp': 'github.com/tmatis/llama.cpp',
}
# Generic infrastructure must earn a much higher AI-context fraction, not an allowlist pass.
GENERIC = {'kagi.com','modal.com','runpod.io','lambdalabs.com','n8n.io','replit.com','zed.dev',
           'github.com/simonw/datasette','github.com/streamlit/streamlit','pydantic.dev',
           'sourcegraph.com','meilisearch.com','typesense.org','ray.io'}

RULES = [
    (1, r'ollama|llama[.-]cpp|llamafile|vllm|sglang|gpt4all|localai|mlx|inference|runtime|exllama|ctranslate|tensorrt'),
    (2, r'copilot|aider|cursor|codeium|windsurf|continue|tabby|swe-agent|openhands|cline|roo-code|coding assistant'),
    (3, r'langchain|llama.?index|haystack|dspy|autogen|crewai|metagpt|litellm|langgraph|semantic.kernel|agent|rag\b'),
    (4, r'huggingface|transformers|mistral|deepseek|llama|gemma|qwen|rwkv|model hub'),
    (5, r'vector|embedding|faiss|chroma|qdrant|milvus|pgvector|lancedb|weaviate|pinecone|retriev|sentence-transformers'),
    (6, r'diffusion|comfyui|controlnet|midjourney|image generation|text-to-image|flux|musicgen|audiocraft|bark'),
    (7, r'whisper|speech|transcri|text-to-speech|\btts\b|piper|voice clon'),
    (8, r'train|fine.?tun|qlora|unsloth|axolotl|pytorch|tensorflow|keras|deepspeed|jax|nanogpt|micrograd'),
    (9, r'eval|observab|langfuse|langsmith|promptfoo|helicone|benchmark|wandb|mlflow'),
    (10, r'\bmcp\b|modelcontextprotocol|fastmcp|browser-use|firecrawl|tool integration'),
    (0, r'chat|gpt|claude|perplexity|openai|anthropic|poe\b'),
]

def categories_for(key, description=''):
    import re
    if key in CURATED:
        return CURATED[key]['categories']
    # Link identity and description, not unrelated terms elsewhere in the comment.
    text = key + ' ' + description
    found = [CATEGORIES[i] for i, pattern in RULES if re.search(pattern, text, re.I)]
    return found[:2] or [CATEGORIES[11]]

# Additional frequent projects discovered while reviewing the archive's first ranking.
_MORE = """
ai.meta.com|Meta AI models|4|Meta's open-weight models and tools, including the Llama model family.
meta.ai|Meta AI|0|Meta's conversational assistant with image generation features.
llama.com|Llama|4|Meta's family of open-weight language and multimodal models.
artificialanalysis.ai|Artificial Analysis|9|Compare model quality, speed, and pricing through independent evaluations.
lmsys.org|LMSYS|9|Open research tools for serving and comparing language models.
lmarena.ai|LMArena|9|Compare model responses through human preference voting and leaderboards.
arena.ai|Arena|9|Compare AI model outputs through human preference evaluations.
claude.com|Claude|0|Anthropic's Claude products, including chat and coding assistance.
x.ai|xAI|0|The developer of Grok models and associated chat and API services.
qwen.ai|Qwen|4|Alibaba's Qwen language and multimodal models and chat interface.
z.ai|Z.ai|0|Hosted chat and APIs for the GLM family of language models.
githubnext.com|GitHub Next|2|Experimental developer tools from GitHub, including AI-assisted coding projects.
allenai.org|Allen Institute for AI|4|Open models and AI tools, including OLMo language models and Semantic Scholar.
comma.ai|comma|11|Hardware and open-source software for driver assistance using machine learning.
roboflow.com|Roboflow|8|Prepare image datasets and train and deploy computer vision models.
sbert.net|Sentence Transformers|5|Create embeddings and reranking models for semantic search.
cerebras.ai|Cerebras|1|AI training hardware and hosted language model inference.
vllm.ai|vLLM|1|High-throughput language model inference and serving with efficient batching.
lakera.ai|Lakera|9|Security tools for detecting prompt injection and protecting AI applications.
scale.com|Scale AI|8|Data annotation and evaluation services for machine learning systems.
rewind.ai|Rewind|0|Searchable recordings of personal computer activity with AI-assisted recall.
limitless.ai|Limitless|7|AI-assisted recording, transcription, and recall of conversations.
coral.ai|Coral|1|Edge TPU hardware and software for running machine learning on devices.
imbue.com|Imbue|2|AI systems and tools aimed at collaborative software development.
fal.ai|fal|6|Hosted inference APIs for image, video, and audio generation models.
unstract.com|Unstract|3|Extract structured information from documents using language models.
metr.org|METR|9|Evaluations and research measuring AI systems' ability to complete tasks.
epoch.ai|Epoch AI|9|Research datasets and benchmarks tracking AI capabilities and compute.
livebench.ai|LiveBench|9|A language model benchmark with regularly updated evaluation questions.
oxen.ai|Oxen|8|Version and manage machine learning datasets and model artifacts.
vast.ai|Vast.ai|11|A marketplace for renting GPU compute for AI workloads.
exa.ai|Exa|10|Web search and content retrieval APIs designed for AI applications.
krea.ai|Krea|6|AI tools for generating, editing, and enhancing images and video.
e2b.dev|E2B|10|Sandboxed cloud environments for running code produced by AI agents.
vlm.run|VLM Run|3|Extract structured information from images and documents using vision models.
folivora.ai|BetterTouchTool AI integration|11|Mac automation software with integrations for AI-assisted workflows.
inotherwords.app|In Other Words|0|An AI-assisted writing and rewriting application.
opencode.ai|OpenCode|2|An open-source coding agent for use from the terminal and other clients.
vercel.ai|Vercel AI SDK|3|A TypeScript toolkit for building model-powered applications and chat interfaces.
ai-sdk.dev|AI SDK|3|A TypeScript toolkit for language models, streaming outputs, and tool calls.
jina.ai|Jina AI|5|Embedding, reranking, and web content extraction tools for retrieval applications.
litellm.ai|LiteLLM|3|Access multiple model providers through a unified API and proxy.
onnxruntime.ai|ONNX Runtime|1|Run and optimize machine learning models across hardware platforms.
zilliz.com|Zilliz|5|Managed vector search infrastructure built around Milvus.
eleuther.ai|EleutherAI|4|Open language models, datasets, and tools for language model research.
gptzero.me|GPTZero|9|A service that estimates whether text was generated by AI.
mythic.ai|Mythic|1|Analog compute hardware designed for edge AI inference.
nooks.ai|Nooks|11|AI-assisted dialing and workflow software for sales teams.
elicit.com|Elicit|0|Find research papers and extract information for literature reviews.
tbench.ai|Terminal-Bench|9|Benchmark coding agents on tasks carried out in terminal environments.
baseten.co|Baseten|1|Deploy and serve machine learning models with managed infrastructure.
ggerganov.com|ggml model demos|1|Browser-based machine learning demos from the creator of ggml.
continua.ai|Continua|0|An AI assistant designed for coordinating and participating in group conversations.
pangram.com|Pangram|9|A service for estimating whether text was generated by AI.
deepset.ai|deepset|3|Tools for building search and retrieval applications, including Haystack.
stablehorde.net|AI Horde|6|Distributed, community-powered image and text generation.
aihorde.net|AI Horde|6|Distributed, community-powered image and text generation.
recall.ai|Recall.ai|7|An API for recording, transcribing, and integrating with meeting platforms.
getomni.ai|OmniAI|3|Extract structured data from documents for AI and business workflows.
figure.ai|Figure|11|AI-powered humanoid robots for physical tasks.
timefold.ai|Timefold|11|A constraint solver and planning platform for scheduling and optimization.
cline.bot|Cline|2|An editor-based coding agent that edits files and runs development tools.
augmentcode.com|Augment Code|2|AI coding assistance grounded in large codebase context.
v7labs.com|V7|8|Tools for labeling visual datasets and automating document processing.
eqbench.com|EQ-Bench|9|Benchmarks evaluating language models' emotional understanding and writing.
boundaryml.com|BAML|3|A language and toolkit for typed, structured language model functions.
rapids.ai|RAPIDS|8|GPU-accelerated Python libraries for data science and machine learning.
getzep.com|Zep|3|Memory and knowledge graph infrastructure for AI agents.
topazlabs.com|Topaz Labs|6|AI-powered image and video enhancement tools.
lumalabs.ai|Luma AI|6|Generative video tools and APIs, including Dream Machine.
coderabbit.ai|CodeRabbit|2|AI-assisted code reviews for pull requests.
spacy.io|spaCy|3|A Python library for production natural language processing.
recurse.chat|RecurseChat|0|A desktop application for chatting with local models and documents.
mastra.ai|Mastra|3|A TypeScript framework for agents, workflows, and retrieval applications.
drawthings.ai|Draw Things|6|Run image generation models locally on Apple devices.
otter.ai|Otter|7|Meeting transcription, summaries, and conversational search.
openpipe.ai|OpenPipe|8|Tools for training and deploying specialized language models.
shortwave.com|Shortwave|0|An email application with AI search, writing, and organization features.
anyscale.com|Anyscale|8|Managed distributed AI compute built around Ray.
devin.ai|Devin|2|A hosted software engineering agent from Cognition.
marqo.ai|Marqo|5|Embedding generation and vector search for text and images.
github.com/anthropics/claude-code|Claude Code|2|Anthropic's agentic coding tool for working with repositories from the terminal.
github.com/openai/codex|Codex CLI|2|OpenAI's coding agent for working with repositories from the terminal.
github.com/neuml/txtai|txtai|5|An embeddings database and workflows for semantic search and language models.
github.com/karthink/gptel|gptel|0|A language model chat client integrated into Emacs.
github.com/sigoden/aichat|AIChat|0|A command-line client for models, document retrieval, and tool use.
github.com/m-bain/whisperx|WhisperX|7|Speech transcription with word-level alignment and speaker diarization.
github.com/huggingface/candle|Candle|1|A minimalist Rust framework for machine learning inference.
github.com/lostruins/koboldcpp|KoboldCpp|1|Run local language models through a portable llama.cpp-based application.
github.com/charmbracelet/crush|Crush|2|A terminal coding agent with support for multiple model providers.
github.com/boundaryml/baml|BAML|3|Typed functions and tooling for structured language model outputs.
github.com/vectara/hallucination-leaderboard|Hallucination Leaderboard|9|Evaluate factual consistency in language model summarization outputs.
github.com/acly/krita-ai-diffusion|Krita AI Diffusion|6|Use diffusion image generation and editing inside Krita.
github.com/ther1d/shell_gpt|ShellGPT|11|A terminal assistant for generating commands, code, and text with language models.
github.com/outlines-dev/outlines|Outlines|3|Generate structured language model outputs constrained by types and schemas.
github.com/openai/evals|OpenAI Evals|9|A framework and examples for evaluating language model behavior.
github.com/openai/openai-cookbook|OpenAI Cookbook|3|Practical code examples for building applications with OpenAI's API.
github.com/block/goose|Goose|2|An open-source coding agent that connects to development tools.
github.com/imartinez/privategpt|PrivateGPT|0|Ask questions about private documents using locally hosted models.
github.com/const-me/whisper|Whisper for Windows|7|A Windows implementation of Whisper speech recognition with GPU support.
github.com/mlc-ai/web-llm|WebLLM|1|Run language models in web browsers using WebGPU.
github.com/github/copilot.vim|Copilot for Vim|2|GitHub Copilot code completion integrated with Vim and Neovim.
github.com/skyvern-ai/skyvern|Skyvern|10|Automate browser workflows using language and vision models.
github.com/yetone/avante.nvim|avante.nvim|2|AI-assisted code editing and chat inside Neovim.
github.com/jxnl/instructor|Instructor|3|Extract structured, validated data from language model outputs.
github.com/obra/superpowers|Superpowers|2|Reusable skills and workflows for coding agents.
github.com/simonw/files-to-prompt|files-to-prompt|11|Combine source files into a prompt-friendly format for language models.
github.com/vikparuchuri/marker|Marker|3|Convert PDF and other documents into Markdown and structured content.
github.com/microsoft/bitnet|BitNet|1|Inference tooling for Microsoft's low-bit language models.
github.com/janhq/jan|Jan|1|An open-source desktop assistant for local language models.
huggingface.co/spaces/mteb/leaderboard|MTEB Leaderboard|9|Compare embedding models on the Massive Text Embedding Benchmark.
huggingface.co/spaces/lmsys/chatbot-arena-leaderboard|Chatbot Arena Leaderboard|9|Human preference rankings comparing conversational language models.
huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard|Open LLM Leaderboard|9|Compare open language models on standardized evaluation tasks.
"""
for row in _MORE.strip().splitlines():
    key, name, category, description = row.split('|')
    CURATED[key] = dict(name=name, categories=[CATEGORIES[int(category)]], description=description)
ALIASES.update({
    'github.com/mozilla-ocho/llamafile':'github.com/mozilla-ai/llamafile',
    'github.com/guillaumekln/faster-whisper':'github.com/systran/faster-whisper',
    'github.com/openaccess-ai-collective/axolotl':'github.com/axolotl-ai-cloud/axolotl',
    'github.com/go-skynet/localai':'github.com/mudler/localai',
    'github.com/sst/opencode':'github.com/anomalyco/opencode',
    'github.com/opencode-ai/opencode':'github.com/anomalyco/opencode',
    'github.com/outlines-dev/outlines':'github.com/dottxt-ai/outlines',
    'suno.ai':'suno.com','together.xyz':'together.ai','hf.co':'huggingface.co',
    'langchain.dev':'langchain.com','metaphor.systems':'exa.ai',
})

GENERIC.update({'folivora.ai','timefold.ai','stately.ai'})
ALIASES.pop('github.com/cthewhale/llama.cpp', None)

GENERIC.update({'github.com/gnachman/iterm2','gitlab.com/gnachman/iterm2',
                'github.com/cloudflare/workers-oauth-provider','github.com/wasmedge/wasmedge'})
ALIASES.update({'cursor.so':'cursor.com', 'wandb.io':'wandb.ai',
                'gpt-index.readthedocs.io':'llamaindex.ai', 'langchain.readthedocs.io':'langchain.com'})
CURATED['inotherwords.app'] = dict(name='In Other Words', categories=[CATEGORIES[11]],
    description='Word and semantic association games built around text embeddings.')
CURATED['specr.net'] = dict(name='GenAI Showdown', categories=[CATEGORIES[9]],
    description='Compare image generation models on a collection of visual prompts.')
CURATED['block.github.io'] = dict(name='Goose', categories=[CATEGORIES[2]],
    description='An open-source coding agent that connects to development tools.')
CURATED['happyscribe.com'] = dict(name='Happy Scribe', categories=[CATEGORIES[7]],
    description='Audio transcription and subtitle creation with AI and human services.')

CURATED['github.com/features/copilot'] = dict(name='GitHub Copilot', categories=[CATEGORIES[2]],
    description='AI code completion, chat, and coding agents integrated with development tools.')
CURATED['copilot.microsoft.com'] = dict(name='Microsoft Copilot', categories=[CATEGORIES[0]],
    description="Microsoft's conversational assistant for web search, writing, and productivity.")
ALIASES['copilot.github.com'] = 'github.com/features/copilot'
