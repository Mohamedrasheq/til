# Turning vision metrics into a structured, safety-checked LLM report

_Learned: 2025_

**The problem:** if you hand a model the raw video and ask for a write-up, it can invent measurements, or turn a number into advice you never asked it to give. I wanted a readable report that stayed inside what the vision pipeline actually computed.

**What worked:** the LLM never sees the video. It receives the structured metrics (events, angles, timestamps) and has to return a schema-checked report. After generation, code checks that every number in the report appears in the input metrics. If the report introduces a measurement, I drop or regenerate it. The prompt also forbids recommendations that aren't supported by those metrics.

```python
report = generate_report(metrics, schema=REPORT_SCHEMA)

def numbers_only(text: str) -> set[str]:
    return set(re.findall(r"\d+(?:\.\d+)?", text))

if not numbers_only(report) <= numbers_only(json.dumps(metrics)):
    raise ValueError("report introduced a measurement")
```

The model can still phrase things poorly, but it can't quietly add a figure the pipeline didn't measure.

**Why it matters:** language is for explaining the metrics. The metrics themselves should come from the vision code, not from the model.

Links: [OpenAI structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
