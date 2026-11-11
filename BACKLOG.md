# Note ideas from past work

Topics to write up from the last two years. Write a few a week, pick the folder and fill in a rough "Learned" period.

## agents
- [ ] Turning one user message into several structured actions, then letting code (not the model) resolve the targets (2025)
- [ ] "Ask instead of guess": making an agent ask a clarifying question when a date or target is ambiguous (2025)
- [ ] Human confirmation before every write action in a tool-calling agent (2025)
- [ ] Role-based tool access: one chat agent, different tools per user role (2025)
- [ ] Dynamic cards in chat: letting an agent return interactive UI instead of plain text (2025)
- [ ] A reviewer agent that mines session logs and opens validated pull requests (2025)
- [ ] Classifying each message first (chat vs action vs request) before routing to a model (2025)
- [ ] Cancelling stale requests when the user keeps talking (2025)

## rag
- [ ] Citations checked on the server before the answer is streamed (2025)
- [ ] Hybrid search with pgvector: combining keyword and vector scores (2025)
- [ ] Translating regional-language questions into search terms before retrieval (2025)
- [ ] Never answering beyond the retrieved passages and keeping figures exactly as written (2025)
- [ ] Two-pass multimodal pipeline: read the page and its images, then summarise and tag (2025)

## evals
- [ ] A rule-based eval to compare a commercial model with an open-weight one (2025)
- [ ] Code checks that drop invented facts after generation (2025)
- [ ] Live phrase checks: running the same 100+ inputs three times in a row before shipping (2025)
- [ ] Scoring free-text answers against a rubric with an LLM grader (2025)

## self-hosting
- [ ] Scale-to-zero serverless GPU for an open-weight model: cold starts and costs (2025)
- [ ] Prompt-tuning a smaller open model to match a bigger commercial one (2025)
- [ ] Ollama vs vLLM: when I'd use each (2025)

## extraction
- [ ] Schema-driven extraction with confidence scores per field (2025)
- [ ] Sending low-confidence fields to human review instead of guessing (2025)

## voice
- [ ] Streaming STT and TTS for a voice agent without awkward gaps (2025)
- [ ] Ignoring background noise and garbled speech in a live voice agent (2025)
- [ ] Per-user memory across voice sessions (2025)

## vision
- [ ] Detecting key events in a movement from pose landmarks (2025)
- [ ] Measuring joint angles from MediaPipe landmarks (2025)
- [ ] Locking onto one person in a multi-person video with re-identification tracking (2025)
- [ ] Running pose estimation in the browser vs on a serverless GPU (2025)
- [ ] Turning vision metrics into a structured, safety-checked LLM report (2025)
