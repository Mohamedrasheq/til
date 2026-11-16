# Synthetic data teaches, real data judges

_Learned: 2026-11-16_

**The problem:** my classifier made the same kinds of mistakes again and again (real bank alerts flagged as scams, romance scams missed), and the public datasets didn't have enough of those cases. I generated 4,000 extra messages with an AI, but if they also ended up in the test set, the score would only show how well the model reads AI-written text.

**What worked:** synthetic messages go **only into training**. Validation and test stay real messages. Before merging the new data I checked it for:

- duplicates and near-duplicates (TF-IDF on character n-grams, cosine ≥ 0.9)
- reused templates (the same opening with the brand or number swapped)
- shortcuts: links, phone numbers, length and "Brand:" prefixes should appear on both labels at similar rates
- overlap with any test set (should be zero)

I also wrote the generation prompt in general terms. It never mentioned the exact test messages the model got wrong, so the model learns the pattern and not my test cases.

```python
is_synthetic = df["source"].str.startswith("synthetic")
real, synthetic = df[~is_synthetic], df[is_synthetic]
# split only the real rows into train / val / test, then:
train = pd.concat([real_train, synthetic]).sample(frac=1, random_state=42)
```

**Why it matters:** with that rule, false alarms fell from 17% to 8% on an unseen test set, and the gain was real rather than the model recognising its own writer's style.
