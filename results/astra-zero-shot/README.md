# Astra zero-shot seed predictions

- Surface: ChatGPT, Work Mode.
- Model/run label: Astra, as requested by the operator. The exact model name displayed in the user's UI is not exposed to this runtime and has not been independently verified.
- Date: 2026-09-28 (America/New_York).
- Source: `main` at `6935f53cc3e6f2a950f0f612884f241cfe4b1240`.
- Prompt arm: `zero_shot`.
- Packaged prompt SHA-256: `945ab5441ad55e758ebc8080546e634350f068e3cb6b1296d6ee667d2b7812d4`.
- Predictions SHA-256: `bfba336d08aa02aa1ca1e511b1d4a61b8e0dd18eb3a039b273b92128aa5b15e2`.

The harness's `prepare-inference` generated all 33 inputs. Only `case_id`, `claim`, and `response` were displayed for each item, together with the verbatim packaged zero-shot prompt and the previously read schema and annotation guide. Cases were presented individually in a deterministic shuffled order (Python `random.Random(20260928).shuffle`); the JSONL preserves that order. Each answer was made as an independent judgment of that exchange and frozen before the next case appeared. No answer was revised, no family comparison was performed, and no gold labels or answer annotations were displayed to the model. Preparation code processed the source corpus without displaying its annotations.

**Isolation limitation:** all judgments were produced in one ChatGPT conversation. Earlier cases remained in conversation history; this run does not establish fresh-context independence. Retain this disclosure when comparing with isolated per-request runs. Exact UI model identity also remains unverified.

Validation checked the packaged JSON schema, 33 unique case IDs matching the prepared inputs, and valid target references. No evaluator, gold comparison, score calculation, or gold-reading test suite was run. Deterministic scoring is left to Hibari.
