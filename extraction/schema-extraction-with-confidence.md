# Schema-driven extraction with a confidence score per field

_Learned: 2025_

**The problem:** extracting a whole record as one JSON object hides the fact that some fields are clear in the source and some are guessed. A single "looks good" pass then either accepts the invented ones or rejects the whole record.

**What worked:** the schema asks for each field as a value, a confidence, and the source span the value came from. After the model returns, code checks the span against the source text. If the span isn't there, I treat the field as untrusted, regardless of the model's confidence.

```python
field = {
    "type": "object",
    "properties": {
        "value": {"type": ["string", "null"]},
        "confidence": {"type": "number"},
        "span": {"type": ["string", "null"]},
    },
    "required": ["value", "confidence"],
    "additionalProperties": False,
}

def trust(field, source: str) -> bool:
    if not field["value"]:
        return False
    if not field.get("span") or field["span"] not in source:
        return False
    return True
```

I don't take the model's confidence at face value. It's a useful sort key, but the span check is the actual evidence.

**Why it matters:** per-field structure lets you accept the easy values and hold back the shaky ones, instead of all-or-nothing on the whole object.

Links: [OpenAI structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
