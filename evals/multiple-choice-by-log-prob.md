# Scoring a base model on multiple-choice tests without generating text

_Learned: 2026-11-20_

**The problem:** HellaSwag, PIQA and ARC are multiple-choice, but a small base model can't follow "answer A, B, C or D".

**What worked:** score each answer instead of asking for one. Build `context + answer`, sum the log-probabilities of the answer's tokens only (mask the context), and pick the highest. One function covers every test; only the prompt changes.

```python
pairs = [(f"Question: {q}\nAnswer:", " " + choice) for choice in choices]
first = len(ctx_ids)                           # only the answer's tokens count
mask[j, first - 1:len(seq) - 1] = True
pick = max(range(len(choices)), key=lambda k: logp[k] / len(choices[k]))   # acc_norm
```

Two scores are standard. `acc` uses the total log-probability, which favours short answers. `acc_norm` divides by the answer's length. Neither is always higher: my 30M model got 44.1% acc but 39.9% acc_norm on ARC-Easy, so report which one you use. WinoGrande needs a twist: put each option in the blank, then score only the words *after* the blank, which are the same for both options.

**Why it matters:** a base model can be compared on the same tests as released models from day one, before any instruction tuning.

Links: [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness), [mini-gpt/step09c_benchmarks.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/step09c_benchmarks.py)
