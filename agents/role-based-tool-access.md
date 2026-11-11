# One chat agent, different tools per user role

_Learned: 2025_

**The problem:** I wanted a single chat agent that several kinds of users could talk to, without giving every role the same powers. A system prompt that says "don't delete if the user is a viewer" is not a real control: the model can still emit the tool call.

**What worked:** I built one agent loop, then filtered the tool list on the server from the signed-in user's role before the request went to the model. A role that shouldn't delete never receives the delete tool, so there is no way for the model to call it. The same screens that those roles already use stay available; the chat just talks to a subset of the same backend functions.

```python
def tools_for(role: str):
    tools = [search_items, get_item]
    if role in {"editor", "admin"}:
        tools += [create_item, update_item]
    if role == "admin":
        tools += [delete_item]
    return tools

completion = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools_for(user.role),
)
```

I still authorize the underlying API with the same role checks, so a forged tool call wouldn't get through either.

**Why it matters:** authorization belongs in the tool list and the API, not in the prompt.

Links: [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling)
