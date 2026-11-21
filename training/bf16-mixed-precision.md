# bf16 mixed precision is not quantization

_Learned: 2026-11-20_

**The problem:** I mixed up three things: training in 32-bit, training in 16-bit, and quantizing a model to 8 or 4 bits.

**What worked:** a clear split.

- **Mixed precision (training):** the master weights stay 32-bit; the heavy matrix maths runs in bf16 under autocast. Modern GPUs have tensor cores for 16-bit maths, so training is faster and uses less memory, with about the same final loss. The weights stay 32-bit because tiny updates (like 0.0001) would round away in 16-bit.
- **Quantization (after training):** rounding a finished model's weights to 8 or 4 bits so it's smaller to run. It costs some accuracy, and small models lose more. A 30M model doesn't need it.

```python
use_bf16 = device == "cuda" and torch.cuda.is_bf16_supported()   # older GPUs (e.g. T4): fall back to 32-bit
with torch.autocast("cuda", dtype=torch.bfloat16, enabled=use_bf16):
    _, loss = model(x, y)
loss.backward()                                                  # gradients land on the 32-bit weights
```

bf16 has the same range as fp32, so unlike fp16 it needs no gradient scaler.

**Why it matters:** "16-bit training" is a speed setting; the saved model is still full precision.

Links: [PyTorch autocast](https://pytorch.org/docs/stable/amp.html), [mini-gpt/step10_train.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/step10_train.py)
