# Word pieces need more data than characters

_Learned: 2026-11-19_

**The problem:** I swapped my Shakespeare GPT's 65-character tokenizer for a 1,024-piece BPE, expecting better text. The same 11M-parameter model got worse, and the per-token losses couldn't be compared with the character model at all.

**What worked:** compare on loss per character, not per token. Total loss over a text is the same whichever way you cut it, so divide the per-token loss by the characters each token covers.

```python
chars_per_token = len(val_text) / len(val_tokens)   # 2.28 for this BPE
loss_per_char = loss_per_token / chars_per_token
```

On that scale, BPE lost: test 1.628 per character vs 1.536 for characters. The reason was data. In word pieces, 1 MB of Shakespeare is only 411K training tokens (vs 1M characters), so the model memorised it and overfit by step 750 (train 0.81, val 4.19). The same tokenizer idea on TinyStories (558M tokens) worked well.

**Why it matters:** a bigger vocabulary shortens the text, which also shrinks the number of training examples. On a small dataset, characters can win; word pieces pay off once there's plenty of text.

Links: [mini-gpt/step07_bpe_tokenizer.py](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step07_bpe_tokenizer.py)
