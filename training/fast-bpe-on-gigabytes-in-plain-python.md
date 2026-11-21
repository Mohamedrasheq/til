# Learning and applying BPE on 2 GB of text in plain Python

_Learned: 2026-11-19_

**The problem:** my from-scratch BPE recounted every pair after each join. Fine for 1 MB of Shakespeare, but TinyStories is 2.2 GB, which would take hours to learn and encode.

**What worked:** three changes.
1. Learn the joins from a 40 MB sample spread across the file. Common pieces look the same in 40 MB as in 2 GB.
2. After each join, only update the words that contain that pair, using an index from pair to words.
3. Encode in 8 MB blocks that end on a story boundary, on all CPU cores, with a cache per unique word.

```python
for w in list(where[best]):              # only words that contain the chosen pair
    old = words[w]
    for p in zip(old, old[1:]):
        pairs[p] -= freq[w]
    words[w] = new = merge(old, best, new_id)
    for p in zip(new, new[1:]):
        pairs[p] += freq[w]
        where[p].add(w)
```

Learning 4,096 tokens took 4 seconds, and encoding all 2.2 GB into 558M tokens took about 20 seconds using every CPU core. I checked the result: one end-of-story token per story (2,717,495) and an exact decode back to the original text.

**Why it matters:** simple text has few unique words, so caching per word makes encoding almost free. You don't need a Rust tokenizer to work with a few gigabytes.

Links: [mini-gpt/step08_tinystories_tokenizer.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step08_tinystories_tokenizer.py)
