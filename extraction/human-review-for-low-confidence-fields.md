# Sending low-confidence fields to human review instead of guessing

_Learned: 2025_

**The problem:** once extraction has a confidence score, it's tempting to still fill the field when the score is low, or to ask the model to "try harder." That just produces a more fluent guess.

**What worked:** I split fields into auto-accept and review. A field is auto-accepted only if it passes the source-span check and its confidence is above a threshold I set and later tuned. Everything else goes to a review queue with the original snippet attached. The record can be saved with the trusted fields filled and the rest left blank until a person decides.

```python
def route_fields(extracted, source, threshold: float):
    auto, review = {}, {}
    for name, field in extracted.items():
        if trust(field, source) and field["confidence"] >= threshold:
            auto[name] = field["value"]
        else:
            review[name] = field
    return auto, review
```

The reviewer sees the value, the span, and the surrounding source, and can accept, edit, or clear it. I don't send the field back through the model as a second guess in that path.

**Why it matters:** a blank field that waits for review is safer than a confident-looking value you couldn't support.

Links: [OpenAI structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
