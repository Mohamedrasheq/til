# Using the model's own doubts to find wrong labels

_Learned: 2026-11-16_

**The problem:** my scam data came from public reports, and people report anything they're unsure about. Many "scams" were really OTP codes, receipts, "I'll call you later" or even warnings about scams. The model was learning from wrong answers.

**What worked:** I scored every row labelled "scam" with the trained model and pulled out the ones it rated under 50% scam: 224 rows. Then I read each one by hand with one rule: **the label must be clear from the text alone.** I dropped 163 (real service messages, comments about scams, chats too vague to judge) and kept 61 that were real scams the model was simply missing. The drop list lives in a CSV so the cleaning can be repeated.

```python
probs = predict_scam_prob(model, imc["text"])        # one score per row
candidates = imc[probs < 0.5].sort_values("scam_prob")
# read every candidate by hand -> label_fixes.csv (text, reason)
fixes = set(pd.read_csv("label_fixes.csv")["text"].map(norm))
df = df[~((df["source"] == "imc2025") & df["text"].map(norm).isin(fixes))]
```

One catch: rows the model doubts are the rows it gets wrong. Cleaning them out of the **test** set as well makes the test score look better than it really is. Run 3's recall jumped from 97.3% to 99.1% partly for that reason, so I treated the new number as optimistic and judged the next model on a separate test set.

**Why it matters:** a model's confident disagreements are the cheapest way to find label errors, but a human still makes the call.
