# Masking links made my scam detector blind to fake domains

_Learned: 2026-11-16_

**The problem:** I replaced every link, phone number and long number with tags like `<URL>` before training. It stopped the model memorising specific links and made data from different sources look alike. But on a new test set many missed scams had one clue only, a lookalike domain such as `bank-card-unlock.top`, and the model never sees it.

**What worked (so far):** naming the trade-off and measuring it. I split test results by "has a link" and read the misses. About 10 of 21 missed scams depended only on the domain. The planned fix is to keep a cleaned domain token instead of a bare `<URL>`.

```python
URL = re.compile(r"(https?://\S+|www\.\S+|\b[\w-]+(\.[\w-]+)*\.(com|net|org|top|xyz|...)\b(/\S*)?)", re.I)

def mask(s):
    return URL.sub(" <URL> ", s)   # "verify at bank-unlock.top/x" -> "verify at <URL>"
```

A small trap on the way: the test set used made-up `.example` domains that my pattern didn't recognise, so links slipped through unmasked. Any input your training data never had needs the same cleaning as the training data.

**Why it matters:** preprocessing decides what the model can see. Before masking a field, ask whether it's noise or the very signal you're trying to learn.
