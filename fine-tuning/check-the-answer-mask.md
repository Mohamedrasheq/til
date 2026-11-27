# Checking that the model only learns the answer

_Learned: 2026-11-24_

**The problem:** when fine-tuning a vision model, each example is image tokens + prompt + answer. The loss should only count the answer. If the mask is off by a few tokens, the model also learns to "predict" the prompt, or misses the start of the answer. Nothing crashes, so you don't notice.

**What worked:** set every label to -100 (ignored), then copy back only the last `n_ans` tokens. Before training, decode what is left and assert it equals the answer text exactly.

```python
lab = enc["input_ids"].clone()
lab[:] = -100                                     # -100 = not learned
for row, (a, n) in enumerate(zip(answers, enc["attention_mask"].sum(1).tolist())):
    n_ans = len(tok(a, add_special_tokens=False)["input_ids"])
    lab[row, n - n_ans:n] = enc["input_ids"][row, n - n_ans:n]   # learn the answer only

# check once, before training
learned = tok.decode(lab[0][lab[0] != -100])
assert learned == answers[0], f"mask wrong: {learned[:120]}"
```

**Why it matters:** a two-line check turns a silent training bug into a loud one, before you pay for the run.
