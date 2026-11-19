# Reading perplexity as "how many choices the model is torn between"

_Learned: 2026-11-19_

**The problem:** a loss of 1.385 meant nothing to me. Is that good?

**What worked:** turn it into perplexity, `e^loss`. It reads as the number of equally likely options the model is choosing between, on average, for each next token.

```python
import math
math.exp(4.174)   # 65.0  random guess over 65 characters
math.exp(2.478)   # 11.9  bigram (sees one character)
math.exp(1.385)   #  4.0  my 10.8M GPT
```

It's an average: after `ROME` the next letter is almost certain (about 1 choice), while the first letter of a new word might be 10 or more. Lower is better, and 1 would be a perfect model.

**Why it matters:** perplexity is easy to picture and to compare against the baseline (random = vocabulary size). Only compare it between models that use the same tokenizer, because a token means something different in each.
