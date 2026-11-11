# When I'd use Ollama vs vLLM

_Learned: 2025_

**The problem:** both Ollama and vLLM run open-weight models behind an OpenAI-compatible API, so it's easy to treat them as interchangeable. They aren't. I kept picking the wrong one when I moved a prototype toward something that had to serve concurrent requests.

**What worked:** I now split them by job. Ollama is what I use on a laptop or a single-user box: one command to pull a model, a local server at `localhost:11434`, almost no serving config. vLLM is what I use when several requests should share a GPU: it serves an OpenAI-compatible API with continuous batching and paged attention, which is the point of it.

```bash
# Ollama: local dev, one user at a time is fine
ollama serve
ollama run qwen2.5

# vLLM: OpenAI-compatible server aimed at concurrent traffic
vllm serve Qwen/Qwen2.5-7B-Instruct
```

Clients can talk to either with the OpenAI SDK by changing `base_url` (`http://localhost:11434/v1` for Ollama, `http://localhost:8000/v1` for vLLM's default port). The prompt and schema stay the same; the serving characteristics don't.

**Why it matters:** use Ollama to get a model running quickly. Switch to vLLM when you care about throughput and a proper inference server, not because the API looks similar.

Links: [Ollama documentation](https://docs.ollama.com/), [vLLM documentation](https://docs.vllm.ai/en/stable/)
