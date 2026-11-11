# Letting code resolve targets after the model extracts actions

_Learned: 2025_

**The problem:** one user message can hold several requests at once. If I let the model pick database ids or decide which records to change, it sometimes points at the wrong row, or changes more records than the user asked for.

**What worked:** the model only extracts a list of structured actions, in the user's own words. Code then resolves each target against the database. If a target matches one record, I use that id. If it matches none or several, I stop and ask, instead of letting the model guess an id.

```python
schema = {
    "type": "object",
    "properties": {
        "actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "verb": {"type": "string", "enum": ["create", "update", "complete", "delete"]},
                    "target": {"type": "string"},  # as the user said it, not an id
                    "fields": {"type": "object"},
                },
                "required": ["verb", "target"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["actions"],
}

def resolve(target, records):
    matches = [row for row in records if fuzzy_match(row.label, target)]
    if len(matches) == 1:
        return matches[0].id
    return None  # ask; don't pick an id here
```

**Why it matters:** the model is good at reading intent, but identity and "which row?" belong in code, where you can test them.

Links: [OpenAI structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
