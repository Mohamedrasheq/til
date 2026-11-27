# A pixel budget instead of a fixed size for receipt images

_Learned: 2026-11-23_

**The problem:** a vision model turns every image into tokens, and the token count follows the pixel count. Resizing every receipt to one fixed size squashes long, thin receipts until the text can't be read. Leaving them at full size blows past the sequence limit.

**What worked:** shrink each image until its area fits a budget (1280 × 1280 pixels), keep the shape, and never enlarge. A typical receipt becomes about 1,100–1,600 image tokens. A tall receipt stays about 500 px wide, so its text is still sharp.

Then I counted tokens (image + prompt + answer) for every receipt before training. With a 3,072-token limit, 98.8% fit. The rest were left out of **training only**. They stay in the test set and are scored as their own group.

```python
def resize(im, budget=1280):
    """Shrink so that width x height <= budget**2, keeping the shape. Never enlarges."""
    im = im.convert("RGB")
    w, h = im.size
    s = (budget * budget / (w * h)) ** 0.5
    return im.resize((round(w * s), round(h * s)), Image.BICUBIC) if s < 1 else im
```

**Why it matters:** one number controls both memory use and readability, and counting tokens up front tells you exactly what gets cut before training starts.
