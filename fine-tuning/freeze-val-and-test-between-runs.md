# Freezing the validation and test sets between training runs

_Learned: 2026-11-16_

**The problem:** each time I added data and re-ran my split script, the random split changed. Messages the old model had trained on could land in the new test set, and the scores of two runs were measured on different messages, so I couldn't tell whether a change helped.

**What worked:** once val and test exist, the split script keeps them and only adds new rows to train. A `--fresh` flag forces a brand-new split when I really want one.

```python
def norm(texts):
    return texts.str.lower().str.replace(r"\s+", " ", regex=True).str.strip()

frozen = (OUT / "val.csv").exists() and (OUT / "test.csv").exists() and "--fresh" not in sys.argv
if frozen:
    old_val = set(norm(pd.read_csv(OUT / "val.csv")["text"]))
    old_test = set(norm(pd.read_csv(OUT / "test.csv")["text"]))
    key = norm(real["text"])
    val, test = real[key.isin(old_val)], real[key.isin(old_test)]
    real_train = real[~key.isin(old_val | old_test)]
```

I also train every run from the same base model with the same settings, so the only thing that changes is the data.

**Why it matters:** a fixed yardstick is what makes "run 4 beat run 3" mean something. Without it you're comparing numbers from different exams.
