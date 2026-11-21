# Comparing loss across models with different tokenizers

_Learned: 2026-11-20_

**The problem:** model 6 uses a 4,096-token tokenizer and model 7 an 8,192-token one. Their losses per token can't be compared: a token is a different amount of text in each.

**What worked:** sum the loss over all tokens and divide by the number of characters. That's the same unit for every tokenizer.

```python
total = sum(F.cross_entropy(logits, targets, reduction="sum") for each window)
loss_per_char = total / n_chars          # not / n_tokens
```

On the same 5,000 held-out web pages: model 6 (stories only) 2.030 per character, model 7 0.790. On TinyStories: model 6 0.342, model 7 0.397. Per token, those numbers would have been misleading: model 6's tokenizer cuts web text into 2.73 characters per token, model 7's into 3.86.

**Why it matters:** any time the tokenizer changes between runs, per-token loss stops being a fair yardstick. Per character (or per byte) still is.

Links: [mini-gpt/step09c_benchmarks.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/step09c_benchmarks.py)
