# Locking onto one person with re-identification tracking

_Learned: 2025_

**The problem:** a pose model will happily return landmarks for every person in the frame. In a multi-person video I needed to follow one target across frames. Tracking by overlap alone (IoU) loses the person when they cross, turn, or get briefly occluded.

**What worked:** I detect people first, then run a ReID-capable tracker so each box also gets a persistent id from appearance, not just motion. I used YOLOv8 for the detections and BoxMOT's `BotSort` for tracking. Once the user (or a first-frame rule) picks a target id, later frames keep only that id's box and landmarks.

```python
from boxmot import BotSort

tracker = BotSort()
# dets: N x 6 — x1, y1, x2, y2, confidence, class
tracks = tracker.update(dets, frame)
# tracks include a persistent id in column 4
ids = tracks[:, 4].astype(int)

target = tracks[tracks[:, 4] == target_id]
```

If the target id is missing for a few frames, I wait rather than silently switching to the nearest remaining person.

**Why it matters:** identity has to survive a crossing or a brief occlusion, or every downstream pose metric is about the wrong body.

Links: [BoxMOT](https://github.com/mikel-brostrom/boxmot), [Ultralytics YOLOv8](https://docs.ultralytics.com/models/yolov8/)
