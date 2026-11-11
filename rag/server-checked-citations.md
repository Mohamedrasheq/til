# Checking citations on the server before the answer streams

_Learned: 2025_

**The problem:** a RAG answer can look well-sourced and still cite a document that was never retrieved, or cite an id that doesn't exist. If those citations stream straight to the client, the user sees a footnote you cannot stand behind.

**What worked:** the model may only cite ids from the retrieved set, and the server checks that before the answer is streamed. I give the model those ids in the prompt, parse every citation out of the draft, and compare them to the retrieved set. If a citation is missing or unknown, I strip it or regenerate; I don't stream the draft as-is.

```python
import re

def citations_are_valid(answer: str, retrieved_ids: set[str]) -> bool:
    cited = set(re.findall(r"\[(\w+)\]", answer))
    return cited <= retrieved_ids
```

Streaming still happens, but only after this check. The client never gets a source card for an id the server didn't retrieve.

**Why it matters:** citation is a server invariant, not a style request in the prompt. The model can still be wrong about what a passage says, but it can't point at a document you never fetched.
