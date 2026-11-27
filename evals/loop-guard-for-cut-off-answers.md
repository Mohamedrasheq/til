# Long answers loop, and a bigger answer limit doesn't fix it

_Learned: 2026-11-25_

**The problem:** about 1.5% of test receipts were long hotel bills with 80–200 line items. The model had never seen answers that long in training. It started repeating rows until it hit the answer limit, so the JSON was cut off and the whole receipt scored zero, even the store, date and total it had got right.

**What worked:**

- **I tested the obvious fix first.** Raising the answer limit from 2,048 to 8,192 tokens: 20 of 31 long receipts still looped (invented rows, dates like "38/03/2019") and 7 stopped early. So the limit went back down.
- **A loop guard in the scorer.** If the JSON is broken, keep the fields written before the item list, and mark the receipt as "cut off". The key-field score on long receipts went from 13% to 32%.
- **Report long receipts as their own group** so they don't hide inside the average.

```python
def extract_answer(text):
    obj = extract_json(text)
    if obj is not None:
        return obj, False
    start, cut = text.find("{"), text.find('"detail"')   # items come last
    if start == -1 or cut < start:
        return None, False
    obj = json.loads(text[start:cut].rstrip().rstrip(",") + "}")
    obj["detail"] = []
    return obj, True                                      # cut_off = True
```

In the end I dropped line items: the next model answers only 4 fields (about 26 tokens), so there's nothing long left to loop on.

**Why it matters:** put the fields you care about first in the answer, so a runaway answer still keeps them.
