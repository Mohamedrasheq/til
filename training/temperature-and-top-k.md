# Temperature and top-k when sampling from a small model

_Learned: 2026-11-19_

**The problem:** my GPT's raw output (temperature 1.0) was full of made-up words. I wanted to know whether the model was bad or the sampling was.

**What worked:** keep the seed and prompt fixed and change only the sampling settings. Temperature divides the scores before softmax: below 1 sharpens toward the likely tokens, above 1 flattens. Top-k drops everything except the k most likely tokens.

```python
logits = logits[:, -1, :] / temperature
if top_k:
    v, _ = torch.topk(logits, top_k)
    logits[logits < v[:, [-1]]] = -float("inf")
next_id = torch.multinomial(F.softmax(logits, dim=-1), 1)
```

Prompt `ROMEO:`, same seed:
- **0.5:** `JULIET: What! what, wilt thou love?` Clean and readable.
- **1.0:** `Must his scave bedward! it is no best thy` Some invented words.
- **1.5:** `WorthniYman in a canest way` Broken spelling.
- **0.8 with top-k 10:** a good balance for this model.

**Why it matters:** sampling settings change output quality a lot without touching the model. Judge a model by its loss, and pick sampling settings for the output you want.

Links: [mini-gpt/step06_chat.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/step06_chat.py)
