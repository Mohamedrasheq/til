# Cancelling in-flight agent work when the user keeps talking

_Learned: 2025_

**The problem:** in a live chat or voice agent, the user often starts a new turn before the previous one has finished. If I still speak or render the old result, the UI answers a question they already moved on from, and I waste a model call.

**What worked:** each turn gets an `AbortController`. When a new message (or a new utterance) arrives, I abort the in-flight request and ignore any response that arrives afterwards. The LLM, tool calls, and TTS all share the same signal so a cancelled turn doesn't keep talking.

```javascript
let current;

async function handleTurn(text) {
  current?.abort();
  const controller = new AbortController();
  current = controller;

  const result = await runAgent(text, { signal: controller.signal });
  if (controller.signal.aborted) return;
  await speak(result, { signal: controller.signal });
}
```

I also drop late events whose turn id no longer matches, in case something was already in flight when abort landed.

**Why it matters:** cancellation is part of the agent loop, not an afterthought, especially once speech or slow tools are involved.

Links: [MDN AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
