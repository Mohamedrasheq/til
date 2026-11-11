# Ignoring background noise and garbled speech before the agent replies

_Learned: 2025_

**The problem:** a live voice agent will happily answer a transcript of chair scrape, a half-word, or someone talking in the background. Once that transcript reaches the LLM, you get a spoken reply to something the user never said.

**What worked:** I put a gate in front of the agent. Incoming audio has to look like speech (a voice-activity check), and the transcript has to pass a minimum length and, when the STT provides it, a minimum confidence. Anything below that is ignored and the agent keeps listening. I also don't start a turn on a partial transcript; I wait for the final one.

```python
def should_ignore(transcript: str, confidence: float | None) -> bool:
    if not transcript.strip():
        return True
    if confidence is not None and confidence < MIN_CONFIDENCE:
        return True
    if len(transcript.split()) < MIN_WORDS:
        return True
    return False
```

The thresholds are settings I tuned on real recordings, not universal values. When in doubt, I ignore the clip; a missed "um" is better than an answer to noise.

**Why it matters:** the cheapest way to stop a bad voice turn is to never start it.
