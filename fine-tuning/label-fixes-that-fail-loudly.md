# Hand-made label fixes that fail loudly when they go stale

_Learned: 2026-11-26_

**The problem:** I fixed a few hundred labels by hand after looking at the images. Editing the dataset file directly loses the history. Keeping a fix list is better, but if the source data or an earlier rule changes, a fix can quietly apply to a value it was never meant for.

**What worked:** each fix records the value it expects to replace (`from`), the new value (`to`) and a reason. The build stops if the current label doesn't match `from`. Removed receipts go in a separate list with a comment saying why.

```json
{"id": "3_DiningPurchaseTicket_479", "field": "total", "from": "64.85", "to": "65.00", "why": "Total, not Total Due"}
```

```python
for fix in manual.get(receipt_id, []):
    assert label.get(fix["field"]) == fix["from"], \
        f"{receipt_id}.{fix['field']}: label is {label.get(fix['field'])!r}, fix expects {fix['from']!r}"
    label[fix["field"]] = fix["to"]
```

```text
# exclude.txt: one id per line, '#' starts a comment
3_FlightItinerary_683   # fake boarding pass
```

**Why it matters:** the clean dataset can be rebuilt from the raw one at any time, every change has a reason, and a stale fix is an error instead of a silent wrong label.
