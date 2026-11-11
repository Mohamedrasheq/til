# A two-pass multimodal pipeline: observe, then summarise and tag

_Learned: 2025_

**The problem:** when I asked a vision-capable model to read a page and its images and also write a summary and tags in one go, it often skimmed. Tags drifted toward generic labels, and details that only appeared in an image didn't always make it into the summary.

**What worked:** I split the job. Pass one only observes: it extracts visible text, what's in each image, and named entities, as structured data, with no summary yet. Pass two is a text-only model that writes the summary and tags from that observation object, not from the raw page again.

```python
observations = client.chat.completions.create(
    model=VISION_MODEL,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Extract visible text, image content, and entities. Do not summarise."},
            {"type": "image_url", "image_url": {"url": image_url}},
        ],
    }],
)

summary = client.chat.completions.create(
    model=TEXT_MODEL,
    messages=[{
        "role": "user",
        "content": "Write a short summary and tags from these observations only:\n"
                   + observations.choices[0].message.content,
    }],
)
```

If the first pass fails, I retry that pass; I don't ask the second model to invent a summary from an empty extract.

**Why it matters:** observation and writing are different jobs. Separating them makes each step easier to inspect and retry.

Links: [OpenAI images and vision](https://platform.openai.com/docs/guides/images-vision)
