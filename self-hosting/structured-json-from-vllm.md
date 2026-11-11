# Getting reliable JSON out of a self-hosted model on vLLM

_Learned: 2025_

**The problem:** asking an open-weight model for JSON in the prompt works most of the time, but every so often it adds prose or breaks the shape, and the parser fails.

**What worked:** vLLM's OpenAI-compatible server can constrain decoding to a JSON schema, so the model can only produce tokens that fit it. You keep using the normal OpenAI client and pass `response_format`.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "tags"],
}

resp = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[{"role": "user", "content": "Summarise this page as a title and 3 tags: ..."}],
    response_format={"type": "json_schema", "json_schema": {"name": "summary", "schema": schema}},
)
print(resp.choices[0].message.content)
```

**Why it matters:** the shape is guaranteed, but the content isn't. Still validate the values in code (and drop anything the source doesn't support) before using them.

Links: [vLLM structured outputs](https://docs.vllm.ai/en/latest/features/structured_outputs.html)
