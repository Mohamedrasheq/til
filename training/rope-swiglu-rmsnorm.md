# RoPE, SwiGLU and RMSNorm: the three upgrades to a GPT-2 style block

_Learned: 2026-11-20_

**The problem:** my GPT followed the 2019 GPT-2 design. Most recent small models swap three parts, and I wanted to know what each one does before using them.

**What worked:**

- **RoPE (Rotary Position Embedding):** no position table. Each head's query and key vectors are rotated by an angle that grows with position, so attention sees *how far apart* two tokens are. Zero parameters.
- **SwiGLU (Swish-Gated Linear Unit):** the feed-forward layer gets two paths: a gate (through Swish/SiLU) and a value, multiplied together. The gate decides how much of each value passes. A hidden size of about 8/3 × width keeps the parameter count equal to GELU's 4 × width.
- **RMSNorm (Root Mean Square Normalisation):** only rescales the vector to a steady size; no mean subtraction, no bias.

```python
def rotate(x, cos, sin):                       # RoPE on pairs of dimensions
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), -1).flatten(-2)

ff = w2(F.silu(w1(x)) * w3(x))                 # SwiGLU: gate * value, back to model width
norm = nn.RMSNorm(n_embd)
```

**Why it matters:** each is a small gain on its own, and together they're the default block in recent small models. The biggest jump in my run still came from better data, not from these.

Links: [RoFormer (RoPE)](https://arxiv.org/abs/2104.09864), [GLU variants (SwiGLU)](https://arxiv.org/abs/2002.05202), [RMSNorm](https://arxiv.org/abs/1910.07467), [mini-gpt/step10_model.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step10_model.py)
