# One pass over a big dataset: train and val stay together

_Learned: 2026-11-20_

**The problem:** on Tiny Shakespeare every GPT I trained overfit: val loss turned up while train kept falling, and I needed early stopping to rescue the best checkpoint. I wanted a run where the model keeps learning to the end.

**What worked:** give a small model more text than it can read in one run. A 12.3M-parameter GPT on TinyStories (2.7M stories, 558M tokens) read 246M tokens in 15,000 steps, about 20 tokens per parameter and less than half the training set. No story was seen twice, so I set dropout to 0, like real pre-training.

```python
"stories": Config(n_layer=6, n_head=6, n_embd=384, block_size=256, dropout=0.0, batch_size=64,
                  steps=15000, lr=1e-3, min_lr=1e-4, warmup=500, beta2=0.95, vocab_size=4096)
# 15,000 x 64 x 256 = 246M tokens
```

Train and val moved together for the whole run (1.355 vs 1.368 at the end), and the held-out test score matched val: 1.364 vs 1.366. The model writes short stories with correct grammar and a clear ending.

**Why it matters:** overfitting is a data problem more than a model problem. When the model sees each example once, the val curve is an honest view of how it will do on new text.

Links: [mini-gpt/step05_gpt.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step05_gpt.py)
