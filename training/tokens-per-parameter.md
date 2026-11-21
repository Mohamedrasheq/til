# Sizing a training run with tokens per parameter

_Learned: 2026-11-20_

**The problem:** for a 30M-parameter model I needed to decide how much data to train on, and the numbers (millions of parameters, billions of tokens) were hard to reason about.

**What worked:** one ratio: training tokens ÷ parameters.

- **~20 tokens per parameter** is the compute-optimal point (Chinchilla, 2022): the best model for a fixed training budget.
- **More than 20** still helps, with smaller gains each time. Small released models go far beyond it on purpose: they pay more once at training time so the model stays cheap to run.
- My stories model: 246M tokens / 12.3M = 20. My FineWeb model: 2.0B / 29.9M ≈ 67.

```python
tokens_per_step = micro_batch * context * grad_accum      # 64 * 512 * 8 = 262,144
steps = math.ceil(train_tokens / tokens_per_step)         # 2.0B -> 7,630 steps
```

Training compute is about `6 × parameters × tokens` FLOPs, so the same ratio also gives a rough cost before any run (then a short speed test gives the real one).

**Why it matters:** it turns "how much data?" into one number to pick, and it explains why a bigger model on the same data isn't always better.

Links: [Chinchilla paper](https://arxiv.org/abs/2203.15556), [mini-gpt/step10_train.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step10_train.py)
