# Splitting a text corpus by position, not by random lines

_Learned: 2026-11-19_

**The problem:** to train a small GPT on Tiny Shakespeare I needed train, validation and test text. Shuffling lines into three piles looks fair, but plays repeat short lines ("All: Speak, speak.", "Exeunt."), so the same line lands in train and test. The model then gets graded on text it has already memorised.

**What worked:** split by position. The first 90% is train, the next 5% val, the last 5% test, and each cut moves to the nearest blank line so no speech is broken in half.

```python
def cut_at_blank_line(pos):
    nxt = text.find("\n\n", pos)          # move the cut to the next blank line
    return len(text) if nxt == -1 else nxt + 2

cut1 = cut_at_blank_line(int(len(text) * 0.90))
cut2 = cut_at_blank_line(int(len(text) * 0.95))
parts = {"train": text[:cut1], "val": text[cut1:cut2], "test": text[cut2:]}
```

The character list (vocabulary) is also built from train only, so nothing about val or test leaks into the model.

**Why it matters:** with text data, "random" isn't the same as "unseen". Contiguous blocks give an honest score, and test even ends up as mostly a different play.

Links: [mini-gpt/step01_prepare_data.py](https://github.com/Mohamedrasheq/mini-gpt/blob/main/step01_prepare_data.py)
