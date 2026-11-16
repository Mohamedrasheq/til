# A fresh test set from a different AI showed my 99% was really 91%

_Learned: 2026-11-16_

**The problem:** my scam classifier scored 98–99% on its held-out test set. But that set had only personal chats as safe messages, and I'd looked at it many times while improving the data. The number no longer told me how the model would do in real life.

**What worked:** I wrote a generic prompt with no mention of my model or its known mistakes, ran it in a **different** AI, and got 400 new messages (half scam, half safe, easy and hard, 18 countries). Before scoring I checked them for duplicates and for overlap with my training data. Then I scored every model version **once** and split the results by difficulty and by "has a link".

| Model | Own test set | New test set |
|---|---|---|
| v1.0.0 | 97.8% | 75.2% |
| v1.1.0 | 98.5% | 91.5% |

The new set also showed where the model breaks: hard messages (81%), and scams whose only clue is the link.

**Why it matters:** a test set you keep looking at slowly turns into training data. Use a fresh, independently written set to decide which model ships, score it once, and don't tune to its mistakes. The next release needs another fresh one.

Links: [scam-shield v1.1.0](https://github.com/Mohamedrasheq/scam-shield/releases/tag/v1.1.0)
