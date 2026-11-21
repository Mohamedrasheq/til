# Choosing a BPE vocabulary size for a tiny dataset

_Learned: 2026-11-19_

**The problem:** GPT-2 uses 50,257 BPE pieces. My training text was 1 MB of Shakespeare. With that many pieces, most would be seen only a handful of times, too rarely to learn.

**What worked:** learn the joins once up to the largest size, then compare smaller sizes by taking the first N joins (BPE learns them in order of frequency). I measured characters per piece on val and how many pieces appear fewer than 50 times in train.

| Pieces | Chars per piece | Rare pieces |
|---:|---:|---:|
| 512 | 1.89 | 38% |
| 1,024 | 2.28 | 24% |
| 2,048 | 2.58 | 45% |

```python
big = BPETokenizer.train(train_text, 2048)
for size in (512, 1024, 2048):
    tk = BPETokenizer(big.merges[:size - 256])   # 256 byte pieces + the first joins
```

1,024 was the sweet spot. Going to 2,048 shortened the text only a little but made almost half the pieces rare. (Some "rare" pieces are byte values that never appear in plain English text.)

**Why it matters:** vocabulary size should fit the data, not copy a big model. Pre-splitting text into words before learning joins also stops a piece from spanning two words.

Links: [mini-gpt/step07_bpe_tokenizer.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step07_bpe_tokenizer.py)
