# Testing a language model's grammar with minimal pairs

_Learned: 2026-11-20_

**The problem:** my stories model had a good test loss, but loss doesn't say *what* the model knows about English. I wanted a grammar score I could track across models.

**What worked:** BLiMP: 67 files × 1,000 sentence pairs that differ in one small thing ("Paula references Robert." vs "Paula reference Robert."). The model writes nothing. It scores both sentences (total log-probability of every token, after a start token), and a pair passes when the correct one scores higher. Random guessing = 50%.

```python
seq = [start_id] + tok.encode(sentence)
logp = F.log_softmax(model(x[:, :-1]), dim=-1)
score = logp.gather(-1, x[:, 1:].unsqueeze(-1)).squeeze(-1).sum()   # good wins if score_good > score_bad
```

The per-area breakdown was the useful part. My 12M TinyStories model scored 60.4% overall: 86% on anaphor agreement, but only 55% on subject–verb agreement (BLiMP tests present tense; the stories are mostly past tense) and below 50% on NPI and island rules (it learned the wrong habit). The 30M FineWeb-Edu model reached 76.1%.

**Why it matters:** a minimal-pairs test isolates one skill at a time, so a low score points to what the training data is missing.

Links: [BLiMP](https://github.com/alexwarstadt/blimp), [mini-gpt/step09_blimp.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step09_blimp.py)
