# Asking a clarifying question instead of guessing a date or target

_Learned: 2025_

**The problem:** users often say things like "move it to Friday" or "update the draft" when more than one record or date could fit. If the agent guesses, it silently changes the wrong thing.

**What worked:** I treated ambiguity as a first-class outcome. After the model extracts an action, code checks whether the target and any date resolve to exactly one value. If they don't, the agent asks a short clarifying question and waits, instead of calling a write tool.

```python
def plan_action(action, records, today):
    matches = resolve_all(action["target"], records)
    date = parse_date(action.get("when"), today=today)

    if len(matches) != 1 or date == "ambiguous":
        return {
            "type": "clarify",
            "question": clarify_question(action, matches, date),
        }

    return {"type": "action", "record_id": matches[0].id, "date": date}
```

I keep the question specific: list the matching records, or the possible dates, rather than a generic "can you clarify?"

**Why it matters:** a clarifying question is cheaper than an undo, and it stops the model inventing a date or a target that was never stated.

Links: [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling)
