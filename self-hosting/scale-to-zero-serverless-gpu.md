# Scale-to-zero serverless GPU: living with cold starts

_Learned: 2025_

**The problem:** I wanted to run an open-weight model on a GPU without paying for a worker that sits idle. Serverless endpoints can scale to zero, but the next request then waits while a worker starts and the model loads into VRAM.

**What worked:** I used a serverless GPU endpoint (I used Runpod Serverless) with a minimum of zero workers for traffic that can wait, and I treated cold start as a product fact, not a surprise. The worker image preloads what it can, but the first request after idle still pays for boot plus model load. For paths where that wait isn't acceptable, the lever is to keep at least one worker warm, knowing it bills even when idle.

```python
import runpod

# min workers = 0: the endpoint can scale to zero
# a warm start only happens if a worker is already up
endpoint = runpod.Endpoint("ENDPOINT_ID")
result = endpoint.run_sync({"prompt": prompt})
```

I don't have a single number for cold-start time or cost that I trust across models and GPU types, so I measure them on the actual endpoint rather than quoting a vendor average.

**Why it matters:** scale-to-zero is a cost choice. It fits batch or infrequent jobs; a user-facing chat path may need a warm worker.

Links: [Runpod Serverless overview](https://docs.runpod.io/serverless/overview), [endpoint settings](https://docs.runpod.io/serverless/endpoints/endpoint-configurations)
