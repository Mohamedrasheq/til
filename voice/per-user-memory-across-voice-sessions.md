# Carrying per-user memory across voice sessions

_Learned: 2025_

**The problem:** a voice agent that only sees the current session forgets preferences, names, and earlier decisions the next time the same person talks to it. Dumping the entire history into the next prompt doesn't scale, and it's easy to mix one user's memory with another's.

**What worked:** I store memory scoped to a `user_id` and retrieve only that user's entries at the start of a turn. I used Mem0 for this: `add` after a turn, `search` before the next one, always filtered by `user_id`. The search result is a short list of memories I drop into the system prompt, not the raw session log.

```python
from mem0 import Memory

memory = Memory()
memory.add(messages, user_id=user_id)

hits = memory.search(user_message, filters={"user_id": user_id})
# pass hits into the next turn's system prompt, for this user only
```

I never search without that filter. A missing `user_id` is a bug, not a "search everyone" fallback.

**Why it matters:** cross-session memory is only useful if it's scoped. The filter is the isolation boundary.

Links: [Mem0 Python quickstart](https://docs.mem0.ai/open-source/python-quickstart)
