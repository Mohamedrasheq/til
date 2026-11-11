# Pose estimation in the browser vs on a serverless GPU

_Learned: 2025_

**The problem:** I needed pose landmarks in two very different settings: an interactive page that should respond immediately, and a heavier video job that can run asynchronously. Running the same stack in both places was a poor fit.

**What worked:** I split them. In the browser I use MediaPipe's Pose Landmarker (or a TensorFlow.js model) so frames stay on the device, the first result is a short round-trip, and I can show landmarks as the camera runs. For longer or heavier video, I send the file to a serverless GPU worker, run detection and tracking there, and return measurements. That path can use a larger model and a ReID tracker, at the cost of upload time and a possible cold start.

```text
Browser:  camera/video -> MediaPipe Pose Landmarker -> landmarks in the page
GPU job:  uploaded video -> detector + tracker + pose -> measurements JSON
```

I don't upload a live interactive session unless I have to. I don't try to run multi-person ReID tracking in the browser if the worker already does it better.

**Why it matters:** the constraint is usually privacy and interactivity in one case, and model weight and batch throughput in the other. Pick the runtime for the constraint, not for a single preferred library.

Links: [MediaPipe Pose Landmarker for the web](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/web_js), [TensorFlow.js](https://www.tensorflow.org/js)
