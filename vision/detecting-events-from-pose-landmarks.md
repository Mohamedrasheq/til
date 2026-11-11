# Detecting key movement events from pose landmarks

_Learned: 2025_

**The problem:** a raw stream of pose landmarks is a lot of points and no structure. I needed to mark a few meaningful events in a movement (starts, extrema, transitions) so later steps could score or describe those moments, not every frame.

**What worked:** I derive a simple one-dimensional signal from the landmarks, then detect events as local extrema or threshold crossings in that signal. The signal is something the event is actually about, for example a wrist's vertical position, or a joint angle over time. I only accept a peak if the landmarks for that joint were visible, so a occluded frame doesn't become an event.

```python
import numpy as np

def local_maxima(signal: np.ndarray, min_gap: int) -> list[int]:
    peaks = []
    for i in range(1, len(signal) - 1):
        if signal[i] >= signal[i - 1] and signal[i] >= signal[i + 1]:
            if not peaks or i - peaks[-1] >= min_gap:
                peaks.append(i)
    return peaks

# e.g. signal[t] = world_landmarks[t][LEFT_WRIST].y
```

Event detection stays in code. The model, if I use one, only sees the event list and the measurements around those frames.

**Why it matters:** once events are explicit, everything downstream can talk about a handful of moments instead of a noisy landmark dump.

Links: [MediaPipe Pose Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)
