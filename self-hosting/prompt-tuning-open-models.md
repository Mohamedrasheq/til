# Prompt-tuning a smaller open model against a commercial baseline

_Learned: 2025_

**The problem:** a commercial model was doing a generation job well, but I wanted the same job on a smaller self-hosted open-weight model. A straight prompt port usually wasn't enough: the open model drifted on format, tone, or groundedness.

**What worked:** I didn't fine-tune. I used the commercial model's outputs on a fixed fixture set as a reference, then iterated on the open model's system prompt and decoding settings. After each change I scored both models with the same rule-based eval (schema, required fields, no values that aren't in the source). The prompt absorbed the differences I could actually see in the failures.

```python
def iterate(prompt, cases, open_model, baseline_model):
    base = [rule_checks(run(baseline_model, c, prompt=BASELINE_PROMPT), c) for c in cases]
    candidate = [rule_checks(run(open_model, c, prompt=prompt), c) for c in cases]
    return compare(base, candidate)
    # inspect the failing cases, adjust the prompt, run again
```

This is prompt work, not a claim that the two models are equal. The eval only tells me which hard rules still fail.

**Why it matters:** before you reach for fine-tuning, a measured prompt loop on a real fixture set is cheaper, and you can see exactly what still breaks.
