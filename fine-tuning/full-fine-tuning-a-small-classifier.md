# Full fine-tuning a small BERT model into a text classifier

_Learned: 2026-11-12_

**The problem:** I wanted a scam vs safe message classifier that runs on a laptop. Training a network from scratch would mean teaching it English first, which needs far more data than I had.

**What worked:** I started from DistilBERT (67M parameters), which already understands English, and put a small classification head on top: a 768 → 768 layer with ReLU, then 768 → 2 for the two labels. The head starts random. I trained **all** the weights, not just the head, with a tiny learning rate (2e-5), 10% warm-up, AdamW and early stopping on validation loss. The small learning rate nudges the pretrained layers instead of overwriting them, so the model keeps its English and learns the new task.

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")
tok.add_tokens(["<URL>", "<PHONE_NUMBER>", "<EMAIL_ADDRESS>", "<NUMBER>"])
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert/distilbert-base-uncased", num_labels=2,
    id2label={0: "safe", 1: "scam"}, label2id={"safe": 0, "scam": 1})
model.resize_token_embeddings(len(tok))   # make room for the new tag tokens
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
```

The "MISSING: classifier.weight" warning at load time is expected. It just means the new head starts random.

**Why it matters:** for a narrow task, fine-tuning a small pretrained model gets high accuracy in about 15 minutes on a laptop GPU. Each new run starts again from the base model, so runs stay comparable and old mistakes aren't carried over.

Links: [DistilBERT](https://huggingface.co/distilbert/distilbert-base-uncased) · [scam-shield](https://github.com/Mohamedrasheq/scam-shield)
