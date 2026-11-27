# A one-off training run on Hugging Face Jobs with a hard stop

_Learned: 2026-11-24_

**The problem:** I needed a GPU for a few hours and couldn't get one on my notebook service. I also didn't want a crashed or stuck run to keep billing.

**What worked:** Hugging Face Jobs runs one script on a rented GPU and bills only while the job runs.

- **One self-contained script.** `uv run` reads the dependencies from the script header, so there's no image to build.
- **A hard stop on every job** (`--timeout`). The job ends on success, on error or at the timeout, whichever comes first.
- **A pilot first** on a smaller GPU: 30 steps on 200 examples, to check memory and the code before the full run.
- **Results go to a private model repo,** so they're safe even if I close the terminal (`--detach`).
- **Peak memory from `max_memory_allocated()`.** The number in the GPU monitor is memory PyTorch has reserved, which is much higher than what it actually uses.

```bash
HF_TOKEN="$(cat ~/.cache/huggingface/token)" hf jobs uv run \
  --flavor "$FLAVOR" --timeout 4h --secrets HF_TOKEN --detach \
  scripts/train.py

hf jobs logs -f <JOB_ID>      # watch
hf jobs cancel <JOB_ID>       # stop early
```

**Why it matters:** with a timeout on every job, the worst-case cost is known before you press enter.
