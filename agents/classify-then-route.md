# Classifying the message before picking a model

_Learned: 2025_

**The problem:** not every user turn needs the same pipeline. A short chat reply, a write action, and a heavier request (for example, a visual) cost different amounts and need different tools. Sending every message straight into the large agent made simple turns slower and easier to misroute.

**What worked:** a first, cheap classifier labels the message (`chat`, `action`, or `request`) with a constrained schema. That label then picks the model, tools, and prompts for the turn. The classifier only routes; it doesn't perform the action.

```python
route_schema = {
    "type": "object",
    "properties": {
        "kind": {"type": "string", "enum": ["chat", "action", "request"]},
    },
    "required": ["kind"],
    "additionalProperties": False,
}

route = client.chat.completions.create(
    model=SMALL_MODEL,
    messages=[
        {"role": "system", "content": "Classify the user message. Do not answer it."},
        {"role": "user", "content": message},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {"name": "route", "schema": route_schema, "strict": True},
    },
)
kind = json.loads(route.choices[0].message.content)["kind"]
reply = handle[kind](message)
```

If the classifier is unsure, I fall through to the full agent rather than inventing a label I'm not willing to trust.

**Why it matters:** routing is a cheap, testable decision, and it keeps the expensive path for the turns that actually need it.

Links: [OpenAI structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
