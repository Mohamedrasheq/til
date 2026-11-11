# Dropping invented facts with a post-generation code check

_Learned: 2025_

**The problem:** schema-checked JSON can still contain a value the source never supported. The shape is valid; the content isn't. I didn't want those values to reach the user just because the model sounded sure.

**What worked:** after generation, code walks each extracted field and keeps it only if the normalized value appears in the source text (or in a small allowlist, for things like enums I defined). Values that don't appear are dropped, not "fixed" by asking the model to try again in the same breath.

```python
def drop_invented(fields: dict, source: str) -> dict:
    text = normalize(source)
    kept = {}
    for key, value in fields.items():
        if value in (None, ""):
            continue
        if normalize(str(value)) in text:
            kept[key] = value
        # else: dropped
    return kept
```

This catches invented strings and copied-wrong identifiers. It will not catch a fluent paraphrase of a fact that isn't in the source, so I still keep the prompt tight and, where it matters, send uncertain fields to review.

**Why it matters:** structured output constrains the shape. A code check is what constrains the values to the evidence you actually have.
