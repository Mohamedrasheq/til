# TIL: Today I Learned

Short notes on things I figure out while building with LLMs: agents, tool calling, MCP, RAG, evals, self-hosted models, voice and vision.

Each note is one small finding: the problem, the fix and a snippet. This README is rebuilt automatically on every push.

<!-- index starts -->
**43 notes so far.**

## Most recent

- [Choosing a BPE vocabulary size for a tiny dataset](training/bpe-vocab-size-for-a-tiny-dataset.md) · training · 2026-11-19
- [Keeping the best checkpoint, not the last one](training/keep-the-best-checkpoint-not-the-last.md) · training · 2026-11-19
- [Reading perplexity as "how many choices the model is torn between"](training/perplexity-as-number-of-choices.md) · training · 2026-11-19
- [Scoring the test set in one fixed pass, then explaining the gap](training/score-the-test-set-in-one-fixed-pass.md) · training · 2026-11-19
- [Splitting a text corpus by position, not by random lines](training/split-a-text-corpus-by-position.md) · training · 2026-11-19

## agents

- [Asking a clarifying question instead of guessing a date or target](agents/ask-instead-of-guess.md) · 2025
- [Cancelling in-flight agent work when the user keeps talking](agents/cancel-stale-requests.md) · 2025
- [Classifying the message before picking a model](agents/classify-then-route.md) · 2025
- [Confirming every write before the tool actually runs](agents/confirm-writes-before-tool-calls.md) · 2025
- [Returning interactive cards from an agent instead of plain text](agents/dynamic-cards-in-chat.md) · 2025
- [A reviewer agent that only opens a PR after a checklist passes](agents/reviewer-agent-validated-prs.md) · 2025
- [One chat agent, different tools per user role](agents/role-based-tool-access.md) · 2025
- [Letting code resolve targets after the model extracts actions](agents/structured-actions-resolved-in-code.md) · 2025

## evals

- [Dropping invented facts with a post-generation code check](evals/code-checks-for-invented-facts.md) · 2025
- [Re-running a live phrase suite before shipping an agent](evals/live-phrase-checks.md) · 2025
- [Scoring free-text answers with a rubric and an LLM grader](evals/rubric-scoring-with-an-llm-grader.md) · 2025
- [Comparing a commercial model to an open-weight one with rule-based checks](evals/rule-based-eval-open-vs-commercial.md) · 2025
- [A fresh test set from a different AI showed my 99% was really 91%](evals/a-fresh-test-set-from-a-different-ai.md) · 2026-11-16

## extraction

- [Sending low-confidence fields to human review instead of guessing](extraction/human-review-for-low-confidence-fields.md) · 2025
- [Schema-driven extraction with a confidence score per field](extraction/schema-extraction-with-confidence.md) · 2025

## fine-tuning

- [Full fine-tuning a small BERT model into a text classifier](fine-tuning/full-fine-tuning-a-small-classifier.md) · 2026-11-12
- [Using the model's own doubts to find wrong labels](fine-tuning/finding-label-noise-with-the-model.md) · 2026-11-16
- [Freezing the validation and test sets between training runs](fine-tuning/freeze-val-and-test-between-runs.md) · 2026-11-16
- [Masking links made my scam detector blind to fake domains](fine-tuning/masking-can-hide-the-clue.md) · 2026-11-16
- [Synthetic data teaches, real data judges](fine-tuning/synthetic-data-for-training-only.md) · 2026-11-16

## rag

- [Hybrid search in Postgres with pgvector and full-text ranks](rag/hybrid-search-pgvector.md) · 2025
- [Checking citations on the server before the answer streams](rag/server-checked-citations.md) · 2025
- [Staying inside retrieved passages and keeping figures as written](rag/stay-inside-retrieved-passages.md) · 2025
- [Translating a regional-language question into search terms first](rag/translate-queries-before-retrieval.md) · 2025
- [A two-pass multimodal pipeline: observe, then summarise and tag](rag/two-pass-multimodal-summaries.md) · 2025

## self-hosting

- [When I'd use Ollama vs vLLM](self-hosting/ollama-vs-vllm.md) · 2025
- [Prompt-tuning a smaller open model against a commercial baseline](self-hosting/prompt-tuning-open-models.md) · 2025
- [Scale-to-zero serverless GPU: living with cold starts](self-hosting/scale-to-zero-serverless-gpu.md) · 2025
- [Getting reliable JSON out of a self-hosted model on vLLM](self-hosting/structured-json-from-vllm.md) · 2025

## training

- [Choosing a BPE vocabulary size for a tiny dataset](training/bpe-vocab-size-for-a-tiny-dataset.md) · 2026-11-19
- [Keeping the best checkpoint, not the last one](training/keep-the-best-checkpoint-not-the-last.md) · 2026-11-19
- [Reading perplexity as "how many choices the model is torn between"](training/perplexity-as-number-of-choices.md) · 2026-11-19
- [Scoring the test set in one fixed pass, then explaining the gap](training/score-the-test-set-in-one-fixed-pass.md) · 2026-11-19
- [Splitting a text corpus by position, not by random lines](training/split-a-text-corpus-by-position.md) · 2026-11-19
- [Temperature and top-k when sampling from a small model](training/temperature-and-top-k.md) · 2026-11-19

## vision

- [Detecting key movement events from pose landmarks](vision/detecting-events-from-pose-landmarks.md) · 2025
- [Measuring joint angles from MediaPipe world landmarks](vision/joint-angles-from-mediapipe.md) · 2025
- [Pose estimation in the browser vs on a serverless GPU](vision/pose-in-the-browser-vs-gpu.md) · 2025
- [Locking onto one person with re-identification tracking](vision/reid-tracking-in-multi-person-video.md) · 2025
- [Turning vision metrics into a structured, safety-checked LLM report](vision/structured-llm-reports-from-vision-metrics.md) · 2025

## voice

- [Ignoring background noise and garbled speech before the agent replies](voice/ignoring-noise-and-garbled-speech.md) · 2025
- [Carrying per-user memory across voice sessions](voice/per-user-memory-across-voice-sessions.md) · 2025
- [Streaming STT and TTS so a voice agent doesn't pause mid-reply](voice/streaming-stt-tts-without-gaps.md) · 2025

<!-- index ends -->
