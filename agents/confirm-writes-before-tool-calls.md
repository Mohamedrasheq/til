# Confirming every write before the tool actually runs

_Learned: 2025_

**The problem:** once a tool-calling agent can create, update, or delete records, a bad parse or a bad target becomes a real write. Letting the model both propose and execute those tools in the same turn is hard to undo.

**What worked:** write tools don't run when the model first calls them. The server records a pending action, the client shows a preview, and the tool only executes after the user confirms. Read tools (search, fetch) still run immediately.

```python
WRITE_TOOLS = {"create_item", "update_item", "delete_item"}

def handle_tool_call(name, args, *, confirmed: bool):
    if name in WRITE_TOOLS and not confirmed:
        return {"status": "needs_confirmation", "tool": name, "args": args}
    return execute(name, args)
```

Follow-up messages like "yes" or "confirm that" attach to the pending preview, not to a new model guess. If the user edits the preview first, I execute the edited args.

**Why it matters:** the model can still draft the change, but durable state only changes after a human says yes.

Links: [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling)
