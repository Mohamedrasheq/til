# Scoring untrained models first, on the same test

_Learned: 2026-11-24_

**The problem:** "my fine-tuned model scores 0.73" means nothing alone. Is that good? Would a bigger model with no training do better?

**What worked:** before training, I ran several open vision models with no training on the same 100 test receipts, with the same prompt and the same scorer. After training, I re-scored all of their saved answers with the final labels and scorer, so every row in the table is measured the same way.

| Model | Micro F1 | Key fields all right |
|---|---|---|
| **0.8B, fine-tuned** | **0.733** | **57%** |
| 4B, no training | 0.541 | 35% |
| 2B, no training | 0.491 | 18% |
| 0.8B, no training | 0.348 | 2% |

Most of the untrained 0.8B's mistakes were format, not reading: raw dates instead of `YYYY-MM-DD`, full addresses where a city was asked for. Training fixes format cheaply, which is why a small model can pass one five times its size.

**Why it matters:** the untrained baseline shows what training actually added, and the bigger untrained model shows whether a small model is worth training at all.
