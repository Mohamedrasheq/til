# Pool.imap reads ahead the whole input: feed it in small groups

_Learned: 2026-11-20_

**The problem:** encoding 7 GB of text on all CPU cores with `multiprocessing.Pool.imap`. It looks lazy, but its feeder thread pulls items from the input as fast as it can, so it can end up holding most of the input in memory.

**What worked:** hand the pool a few jobs at a time with `islice`, and stop early once the token target is reached.

```python
todo = jobs(docs)                                      # a generator of 1,000-document lists
while n < limit:
    group = list(islice(todo, 4 * pool._processes))   # a few jobs per worker, then wait
    if not group:
        break
    for arr in pool.map(encode_docs, group):
        arr.tofile(out)
        n += len(arr)
```

Memory stays flat, every core stays busy, and the output order is kept.

**Why it matters:** with a big generator as input, "lazy" `imap` isn't lazy on the input side. Bounding the batch is a two-line fix.

Links: [mini-gpt/step10b_data.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step10b_data.py)
