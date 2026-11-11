# Staying inside retrieved passages and keeping figures as written

_Learned: 2025_

**The problem:** even with good retrieval, a model will sometimes add a fact that isn't in the passages, or it will tidy a figure into a rounder number. That's unusable anywhere the exact figure matters.

**What worked:** two layers. The prompt tells the model to answer only from the provided passages, to copy figures exactly, and to say when the passages don't contain the answer. Then code checks the draft: every number in the answer must appear in the retrieved text. If a figure fails that check, I strip or regenerate that sentence instead of sending it.

```python
import re

def figures_are_grounded(answer: str, passages: str) -> bool:
    figures = re.findall(r"\d+(?:\.\d+)?%?", answer)
    return all(fig in passages for fig in figures)
```

This is a conservative check, not a complete one. A model can rephrase a fact without using a number, and a formatted number ("1,000" vs "1000") can look ungrounded. I normalize separators before comparing, and I still require the prompt rule for everything that isn't a figure.

**Why it matters:** "don't make things up" is a wish in a prompt. "Every figure must appear in the source" is a test you can run on the way out.
