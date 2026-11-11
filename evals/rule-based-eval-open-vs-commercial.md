# Comparing a commercial model to an open-weight one with rule-based checks

_Learned: 2025_

**The problem:** I wanted to move a workload to a self-hosted open-weight model, but "it looks about the same" is not an eval. I needed a way to compare the two models on the same cases without relying on a judge model.

**What worked:** I wrote a small rule-based eval and ran the same fixtures through both models. Each case has a source text and a list of things the output must satisfy: it parses against the schema, required fields are present, and every extracted value appears in the source. The score is the set of checks, not a vibe.

```python
def rule_checks(output, source, required) -> dict[str, bool]:
    data = parse_json(output)
    return {
        "parses": data is not None,
        "required": bool(data) and all(data.get(k) not in (None, "") for k in required),
        "grounded": bool(data) and not invented_values(data, source),
    }

# Compare the check vectors from both models on the same cases.
commercial = [rule_checks(run(commercial_model, c), c.source, c.required) for c in cases]
open_weight = [rule_checks(run(open_model, c), c.source, c.required) for c in cases]
```

I used this to iterate on the open model's prompt. The eval tells me which checks still fail; it does not, by itself, prove the models are equivalent.

**Why it matters:** when the question is "did this output break a hard rule?", deterministic checks are cheaper and more stable than an LLM judge.
