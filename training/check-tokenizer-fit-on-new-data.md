# Checking whether a tokenizer fits new data before training on it

_Learned: 2026-11-20_

**The problem:** I wanted to train on FineWeb-Edu (adult, educational web text) and wasn't sure if my 4,096-token tokenizer, learned on children's stories, was good enough to reuse.

**What worked:** measure it on a 50 MB sample, next to fresh tokenizers learned on the new data. Two numbers: characters per token (higher = fewer cuts) and the share of words that stay one token.

| Tokenizer | Chars per token | Whole words |
|---|---:|---:|
| Stories, 4,096 | 2.72 | 58% |
| Fresh on FineWeb, 4,096 | 3.40 | 67% |
| Fresh on FineWeb, 8,192 | 3.82 | 77% |
| Fresh on FineWeb, 16,384 | 4.20 | 85% |

The stories tokenizer was 20% worse than a fresh one of the same size ("government" became `go | ver | n | ment`), so I learned a new one. I picked 8,192: 4K → 8K gained 40%, 8K → 16K only 10%, and in a 512-wide 30M model the word table grows from 14% to 25% of all parameters.

```python
counts = Counter(m for m in SPLIT.findall(text))      # BPE works chunk by chunk: encode each once
chars_per_token = sum(n * len(c) for c, n in counts.items()) / sum(n * len(tok.encode(c)) for c, n in counts.items())
```

**Why it matters:** vocabulary size follows the variety of words in the data, not the amount of data. Ten times more stories would still fit in 4K tokens; adult text needs more.

Links: [mini-gpt/step10_fineweb_check.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/step10_fineweb_check.py)
