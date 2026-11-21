# A training run on a cloud notebook that survives a disconnect

_Learned: 2026-11-21_

**The problem:** a multi-hour run on a Colab GPU. The machine is wiped on disconnect, and it keeps billing while idle after the run ends.

**What worked:**

- **Code in Drive, data on the machine's own disk.** A 50 KB zip of the scripts lives in Drive; the data is downloaded and encoded on the runtime's local disk each session (fast from Hugging Face, and much faster to read than Drive).
- **Checkpoints to Drive, written atomically.** Model + optimizer + step every 500 steps; the same command resumes from it.
- **A speed test first.** 30 steps give real tokens per second, memory use and the full-run time before committing. The first steps are slow while `torch.compile` warms up, so skip them in the average.
- **Shut down when done.** The runtime doesn't stop when the cell ends.

```python
def save(path, obj):
    tmp = path.with_suffix(".tmp")
    torch.save(obj, tmp)
    os.replace(tmp, path)          # a disconnect mid-save never leaves a broken checkpoint

if ckpt_path.exists():             # same command = resume
    ck = torch.load(ckpt_path, weights_only=True)
    model.load_state_dict(ck["model"]); opt.load_state_dict(ck["opt"]); step = ck["step"]
```

```python
!python train.py --out /content/drive/MyDrive/run
from google.colab import runtime
runtime.unassign()                 # stop the runtime (and the billing) when training ends
```

**Why it matters:** the worst case after a disconnect becomes "lose a few minutes and re-run four cells", not "start again".

Links: [mini-gpt/step10_colab.ipynb](https://github.com/Mohamedrasheq/mini-gpt/blob/v1.1.0/step10_colab.ipynb)
