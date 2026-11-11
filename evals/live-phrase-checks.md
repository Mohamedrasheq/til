# Re-running a live phrase suite before shipping an agent

_Learned: 2025_

**The problem:** unit tests caught broken parsers, but they didn't catch a tool-calling agent that fails only on some phrasings, or that fails the same phrasing only some of the time. I wanted a check that felt closer to what people actually type or say.

**What worked:** I keep a fixed suite of live phrases: real, in-distribution requests with an expected action or an expected clarification. Before a release, I run the full agent (tools included) against every phrase, more than once, in the same environment I'd ship. A case fails if the action doesn't match, or if the result flips between runs.

```python
def run_suite(cases, agent, runs=3):
    failures = []
    for n in range(runs):
        for case in cases:
            output = agent(case["input"])
            if not matches(output, case["expect"]):
                failures.append((n, case["id"], output))
    return failures
```

I add a phrase to the suite when I see a new wording in real use, rather than inventing a huge synthetic set. The suite is a regression net, not a proof that the agent is generally correct.

**Why it matters:** agents are non-deterministic. Running the same phrases more than once is how I notice a flake before users do.
