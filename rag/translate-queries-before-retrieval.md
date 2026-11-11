# Translating a regional-language question into search terms first

_Learned: 2025_

**The problem:** people asked questions in a regional language, but most of the corpus I was searching was written in another language (and with a different wording style). Embedding the raw question often missed the right passages, and keyword search had almost nothing to match.

**What worked:** I added a cheap first step that rewrites the question into search terms in the language of the index, then I run hybrid search on that rewrite. The rewrite is a structured object (a short query string, plus optional keywords), not the final answer. The answer is still generated from the retrieved passages, in the user's original language.

```python
rewrite_schema = {
    "type": "object",
    "properties": {
        "search_query": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["search_query"],
}

rewrite = extract_search_terms(user_question, schema=rewrite_schema)
hits = hybrid_search(query_text=rewrite["search_query"], embedding=embed(rewrite["search_query"]))
answer = generate(user_question, passages=hits)
```

I don't retrieve with the raw question alone when the language doesn't match the corpus. If the rewrite is empty, I fall back to a multilingual embedding of the original text rather than searching for nothing.

**Why it matters:** retrieval wants the query in the same language and vocabulary as the documents. Generation can still reply in the language the user used.

Links: [OpenAI structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
