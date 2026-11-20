# Scoring the test set in one fixed pass, then explaining the gap

_Learned: 2026-11-19_

**The problem:** during training I estimated loss from 100 random batches, so the number moves a little every run. For the final test score I wanted one stable number. Then test came out worse than val (1.536 vs 1.380), and I needed to know whether something was broken.

**What worked:** walk through the whole split in side-by-side windows so every character is scored exactly once, and score val the same way.

```python
starts = torch.arange((len(d) - 1) // block) * block
for s in starts.split(32):
    x = torch.stack([d[j:j + block] for j in s])
    y = torch.stack([d[j + 1:j + block + 1] for j in s])
    total += F.cross_entropy(model(x)[0].flatten(0, 1), y.flatten(), reduction="sum").item()
    count += y.numel()
loss = total / count
```

For the gap, I counted speaker names. 62% of test speeches belonged to characters never seen in training (*The Tempest*), against 7% for val. The smaller model showed the same gap, so it's the data, not a bug.

**Why it matters:** a fixed full pass gives a number you can quote. When test and val disagree, look at what's in each split before blaming the model.

Links: [mini-gpt/step06_evaluate.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/step06_evaluate.py)
