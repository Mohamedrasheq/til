# A 10% share of the old data keeps the old skill

_Learned: 2026-11-21_

**The problem:** moving from children's stories to educational web text, I didn't want the new model to forget how to write a clean, simple story.

**What worked:** mix the old data in at a small share. Each training sequence comes from TinyStories with probability 0.1, otherwise from FineWeb-Edu (1.8B + 0.2B tokens). The tokenizer is learned from the same 90/10 mix, so it knows both kinds of words.

```python
from_stories = rng.random(micro_batch) < 0.10        # per sequence, every batch
```

TinyStories test loss per character: 0.342 for the stories-only model, 0.397 for the mixed model, which still writes clear stories ("Once upon a time, there was a little dog named Spot…"). In exchange, grammar (BLiMP) went from 60.4% to 76.1% and web-text loss from 2.03 to 0.79 per character.

**Why it matters:** a small slice of the old data is a cheap insurance policy when you change the main training set.

Links: [mini-gpt/step10_train.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step10_train.py)
