# Keeping the best checkpoint, not the last one

_Learned: 2026-11-19_

**The problem:** my 10.8M-parameter GPT trained for 5,000 steps (70 minutes on a Mac). Val loss was best at step 1,750 (1.385). After that, train loss kept falling (1.09 → 0.59) while val loss rose (1.385 → 1.616). The model was memorising the training text. Saving only the final weights would have kept the worse model.

**What worked:** check val every 250 steps, save the weights only when val beats the best so far, and reload that file at the end. For the next run I added early stopping: stop once val hasn't improved for 4 checks.

```python
if val < best:
    best, since_best = val, 0
    torch.save(model.state_dict(), "best.pt")
else:
    since_best += 1
    if since_best >= patience:      # 4 checks = 1,000 steps without progress
        break
```

**Why it matters:** the last ~65% of that run added nothing. Watch the gap between train and val: when train keeps falling and val turns up, you're paying for memorisation.

Links: [mini-gpt/gpt.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/gpt.py)
