# Scoring free-text answers with a rubric and an LLM grader

_Learned: 2025_

**The problem:** some answers aren't schema-shaped. Short explanations and spoken replies need a judgement against a rubric, and a person can't score every one by hand.

**What worked:** I wrote a fixed rubric with integer score bands and a required rationale, then asked a grader model to return only that JSON. The grader sees the question, the rubric, the learner's answer, and any source material it is allowed to use. It does not see a sample "good essay" that it can copy a score from without reading.

```python
RUBRIC = """
Score 0-3:
3 covers every required point with no contradiction
2 covers most points, with only minor gaps
1 has major gaps or a contradiction
0 is off-topic or incorrect
Return JSON: {"score": 0, "rationale": ""}
"""

grade = client.chat.completions.create(
    model=GRADER_MODEL,
    messages=[
        {"role": "system", "content": RUBRIC},
        {"role": "user", "content": f"Question: {q}\nAnswer: {answer}"},
    ],
    response_format={"type": "json_schema", "json_schema": {"name": "grade", "schema": GRADE_SCHEMA, "strict": True}},
)
```

LLM judges are noisy, so I treat a one-point gap as a possible disagreement and only automate decisions I'm willing to have a second grader (or a person) spot-check.

**Why it matters:** a published rubric plus a constrained grade is something you can audit. A free-form "looks good" from a model is not.

Links: [OpenAI structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
