# Returning interactive cards from an agent instead of plain text

_Learned: 2025_

**The problem:** some agent turns need the user to pick, confirm, or edit something. A paragraph of markdown is a poor UI for that, and letting the model write HTML is a poor idea.

**What worked:** the model (or a tool result) returns a small, schema-checked card payload: a type plus the data the UI needs. The client maps each type to a React component. The model never sends markup, and unknown types render as a fallback instead of failing the chat.

```tsx
type Card =
  | { type: "confirm"; title: string; fields: Record<string, string> }
  | { type: "list"; items: { id: string; label: string }[] };

function ChatCard({ card }: { card: Card }) {
  if (card.type === "confirm") return <ConfirmCard {...card} />;
  if (card.type === "list") return <ListCard items={card.items} />;
  return null;
}
```

Clicks on a card go back as structured user input (the selected id, or a confirmation), not as a free-text recount of what was on screen. The AI SDK's generative UI docs describe the same idea: render tool output as UI, not as prose.

**Why it matters:** the chat can collect a precise action without making the user type it back, and you stay in control of the interface.

Links: [AI SDK generative user interfaces](https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces)
