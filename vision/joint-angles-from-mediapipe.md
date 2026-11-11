# Measuring joint angles from MediaPipe world landmarks

_Learned: 2025_

**The problem:** I needed joint angles from a pose, and it's easy to get them wrong. MediaPipe's image landmarks are normalized by width and height separately, so computing an angle in that space distorts anything that isn't a square frame.

**What worked:** I use the Pose Landmarker’s world landmarks, which are in metres with the mid-hip as the origin, and measure the angle at the middle of three points. For the left elbow that's shoulder (11), elbow (13), and wrist (15). I also skip the angle if visibility on those landmarks is low.

```python
import numpy as np

LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST = 11, 13, 15

def angle_at(a, b, c) -> float:
    ba = np.array([a.x, a.y, a.z]) - np.array([b.x, b.y, b.z])
    bc = np.array([c.x, c.y, c.z]) - np.array([b.x, b.y, b.z])
    cos = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))

# result.pose_world_landmarks[0] is the first pose, in metres
lm = result.pose_world_landmarks[0]
elbow = angle_at(lm[LEFT_SHOULDER], lm[LEFT_ELBOW], lm[LEFT_WRIST])
```

This returns an unsigned 0–180° angle, which is enough for how bent a joint is. It does not tell you which way the joint is bending.

**Why it matters:** world coordinates keep the geometry in real space. Image-normalized x and y will quietly skew the same angle.

Links: [MediaPipe Pose Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)
