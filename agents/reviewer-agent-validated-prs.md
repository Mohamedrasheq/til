# A reviewer agent that only opens a PR after a checklist passes

_Learned: 2025_

**The problem:** I wanted an agent that reads session logs, suggests prompt or tool changes, and opens a pull request. If it can push a branch on its own, a noisy finding becomes an unreviewed change.

**What worked:** the reviewer is allowed to draft a diff, but a PR is only opened when a checklist in code all returns true. The checks are things I can compute: the diff is limited to allowed paths, tests still run, and the change includes a short rationale tied to the session evidence. Failures stay as notes; they never become pull requests.

```python
def maybe_open_pr(proposal, github):
    checks = [
        proposal.paths_allowed(),
        proposal.tests_passed(),
        proposal.has_rationale(),
    ]
    if not all(checks):
        return None
    return github.pulls.create(
        title=proposal.title,
        head=proposal.branch,
        base="main",
        body=proposal.rationale,
    )
```

A person still reviews and merges the PR. The agent proposes; it does not land the change.

**Why it matters:** log mining is useful, but "validated" has to mean a real gate, not a hopeful sentence in the agent's prompt.

Links: [GitHub API: create a pull request](https://docs.github.com/en/rest/pulls/pulls#create-a-pull-request)
