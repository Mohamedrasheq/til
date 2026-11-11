# Streaming STT and TTS so a voice agent doesn't pause mid-reply

_Learned: 2025_

**The problem:** if you wait for the full transcript, then the full model answer, then the full audio file, a voice agent goes quiet for a long time before it speaks. That gap makes the conversation feel broken even when the eventual answer is fine.

**What worked:** I streamed every stage and overlapped them. Speech-to-text emits partial, then final, transcripts. As soon as a final user utterance is ready, the agent starts generating. As the model streams tokens, I split off complete sentences and send each one to text-to-speech without waiting for the rest of the answer. Audio starts while generation is still in progress.

```javascript
let buffer = "";
for await (const token of llmStream) {
  buffer += token;
  const sentence = splitOffSentence(buffer); // flush on '.', '?', '!'
  if (sentence) {
    await tts.speak(sentence); // start audio before the full answer exists
  }
}
if (buffer.trim()) await tts.speak(buffer);
```

I also share an abort signal with TTS so a new user utterance can stop audio that's already playing.

**Why it matters:** in voice, time-to-first-audio is the latency people feel, not time-to-full-answer.

Links: [MDN AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
