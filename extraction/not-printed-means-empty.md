# Not printed on the receipt means empty, never a guess

_Learned: 2026-11-26_

**The problem:** a public receipt dataset had labels that "helped": a total worked out from the line items, a year added to "29 DEC", a store name taken from a faint logo, the legal company name from the footer. A model trained on that learns to invent values, which is the worst thing an expense app can do.

**What worked:** one rule for every label: **a field holds only what is printed. If it's not there, it stays empty.** I checked every test receipt by eye against it and wrote down each decision:

- **Store name:** the brand at the top, not the legal company name in the small print. A table maps the known legal names to their brand.
- **Booking site vs operator:** whoever issued the receipt.
- **Only a "Subtotal" line:** keep it if the receipt is complete; empty if the photo is cut off.
- **Paid in advance, no total line:** empty.
- **Fake or template receipts, statements, refunded tickets:** removed, not labelled.

```python
BRAND_OF_LEGAL_NAME = [
    (re.compile(r"ANI Technologies", re.I), "Ola"),
    (re.compile(r"Agoda Company", re.I), "agoda"),
    # ...
]
```

**Why it matters:** the model copies the labelling habits, not just the values. If the labels never guess, the model learns that empty is an allowed answer.
