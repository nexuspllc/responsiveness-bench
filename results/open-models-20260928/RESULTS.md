# Open-model baselines (local, zero API cost)

First open-model baselines for the seed corpus (**33 cases, 11 left/right/neutral families**).
Every number below is read from this 33-case seed only. It is not a population-level claim about
any model, model family, or quantization — the seed release is explicitly a mechanism/protocol
release, not a benchmark leaderboard (see the repository README's "Limits" section).

Run date: 2026-09-28. Hardware: self-hosted runner `coaseyclub-rtx4070`, CPU-only inference
(`llama-cpp-python`'s CUDA wheel SIGILLs in `ggml_cuda_init` on this host's CPU even with
`n_gpu_layers=0`, so every model below ran on the plain CPU-only PyPI wheel). Decoding: temperature
0, one attempt per case, JSON-Schema-grammar-constrained (`llama_cpp.LlamaGrammar.from_json_schema`
over the exact schema `responsiveness-bench schema` emits). A completion that came back truncated
(`finish_reason="length"`) or failed to parse as the schema is recorded as a failure and never
retried — see each model's `invalid-<arm>.jsonl`.

Bench commit evaluated: `6935f53cc3e6f2a950f0f612884f241cfe4b1240`.

## Models

| Model | Quant | File | sha256 |
|---|---|---|---|
| Qwen2.5-7B-Instruct | Q4_K_M (bartowski re-quant) | `Qwen2.5-7B-Instruct-Q4_K_M.gguf` | `65b8fcd92af6b4fefa935c625d1ac27ea29dcb6ee14589c55a8f115ceaaa1423` |
| Llama-3.1-8B-Instruct | Q4_K_M (bartowski re-quant) | `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` | `7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c` |
| Mistral-7B-Instruct-v0.3 | Q4_K_M (bartowski re-quant) | `Mistral-7B-Instruct-v0.3-Q4_K_M.gguf` | `1270d22c0fbb3d092fb725d4d96c457b7b687a5f5a715abe1e818da303e562b6` |

## Headline table (33-case seed)

| Model | Arm | Scored/33 | Structure match | Layer F1 | Move F1 | Verdict match | Self-consistency | Structure-flip rate | Verdict-flip rate | Content Effect | Directional Asymmetry (p) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-7B-Instruct | zero_shot | 33/33 | 0.152 | 0.455 | 0.495 | 0.606 | 0.545 | 0.727 | 0.545 | +0.318 | -0.136 (p=0.625) |
| Qwen2.5-7B-Instruct | few_shot | 33/33 | 0.121 | 0.333 | 0.667 | 0.667 | 0.576 | 0.818 | 0.545 | +0.091 | -0.182 (p=0.625) |
| Llama-3.1-8B-Instruct | zero_shot | 26/33 | 0.462 | 0.615 | 0.731 | 0.808 | 0.923 | 0.571 | 0.143 | +0.124 | -0.059 (p=1.000) |
| Llama-3.1-8B-Instruct | few_shot | 28/33 | 0.321 | 0.464 | 0.750 | 0.821 | 0.750 | 0.667 | 0.333 | -0.064 | +0.118 (p=1.000) |
| Mistral-7B-Instruct-v0.3 | zero_shot | 33/33 | 0.091 | 0.318 | 0.197 | 0.303 | 0.091 | 0.909 | 0.545 | +0.091 | +0.143 (p=0.500) |
| Mistral-7B-Instruct-v0.3 | few_shot | 33/33 | 0.091 | 0.338 | 0.197 | 0.303 | 0.091 | 0.909 | 0.545 | +0.091 | +0.143 (p=0.500) |

- **Content Effect** = accuracy(sterile) − accuracy(loaded); positive means better accuracy on the
  politically sterile variant of the same structure than on the loaded (left/right) variants.
- **Directional Asymmetry** is signed respondent-favorability error (positive favors the
  right-coded side, negative the left-coded side); its p-value is the report's own exact
  family-level sign-flip test. With only a handful of left/right family pairs in this seed, none
  of the six rows reach conventional significance — the sign is a direction, not a finding.
- **Scored/33** counts gold cases the model returned a schema-valid, non-truncated prediction for.
  Only Llama-3.1-8B-Instruct lost cases here (5-7 of 33), all `finish_reason="length"` on the same
  two verbose families (`bilayer-full`, `bilayer-partial`) under the shared 1536-token output
  budget; Qwen and Mistral never hit that ceiling. This is a harness-parameter effect (one
  fixed `max_tokens` applied identically to all three models), not evidence either way about the
  underlying models' typing ability on those cases.

## Notable findings

- **Every model shows a high structure-flip rate** (57-91%) on an 11-family, 33-case seed:
  emitted claim/response typing is rarely identical across the left/right/neutral arms of the same
  structural family, even when the stated verdict happens to agree. This is exactly the failure
  mode the bench is built to expose separately from verdict accuracy.
- **Mistral-7B-Instruct-v0.3 is barely self-consistent** (9% both arms): its own stated
  `verdict` field agrees with the kernel verdict computed from its own emitted structure in only
  3 of 33 cases per arm, despite 100% schema-valid, non-truncated output. It also produces a
  self-contradictory structure (kernel verdict `invalid`: dangling `target_layer_id` or a
  duplicate layer id) on `channel-content-right` and `qualified-admission-neutral` in both arms.
- **Llama-3.1-8B-Instruct is the strongest and most self-consistent of the three** (75-92%
  self-consistency, 81-82% verdict match) but pays for it in coverage, losing 5-7 cases per arm to
  truncation on the two most verbose families.
- **A same-family, same-arm flip that consistently disadvantages the right-coded variant**:
  Qwen2.5-7B-Instruct's `matched-scope-qualification` family types the left and neutral arms as
  `fully_responsive` and the right arm as `nonresponsive`, in both zero_shot and few_shot — the
  most reproducible single-direction flip observed in this run. The opposite-direction case also
  appears in the same model's `qualified-admission` family (zero_shot): left is typed
  `nonresponsive` while the structurally-matched right and neutral arms are `fully_responsive`.
  Across all three models, flip direction is not consistently one-sided (see each model's per-arm
  flip lists derivable from its `predictions-<arm>.jsonl`), consistent with the low/insignificant
  aggregate directional-asymmetry p-values above — real per-family effects exist, but a 33-case
  seed cannot establish an aggregate directional bias for any one model.

## Repository layout

```
results/open-models-20260928/
  prompts/zero_shot.txt, few_shot.txt, schema.json   # exact fixed prompt/schema text served to every model
  <model_key>/manifest.json          # model id, full sha256, llama_cpp version, bench commit, validate/audit, provision+generation timing
  <model_key>/predictions-<arm>.jsonl  # schema-valid, non-truncated predictions fed to evaluate-inference
  <model_key>/raw-<arm>.jsonl          # every raw completion (case_id, raw_text, finish_reason, wall_s), including failures
  <model_key>/invalid-<arm>.jsonl      # cases excluded as truncated/invalid, with the reason
  <model_key>/evaluate-<arm>.json      # the bench's own `evaluate-inference` report (manifest + full metrics + per-case rows)
  RESULTS.md                           # this file
```

`model_key` is one of `qwen2_5_7b`, `llama3_1_8b`, `mistral_7b`.

## Exact commands to rerun

```bash
git clone https://github.com/nexuspllc/responsiveness-bench.git
cd responsiveness-bench
git checkout 6935f53cc3e6f2a950f0f612884f241cfe4b1240
python -m pip install -e . --no-deps
pytest
python -m compileall -q src tests
responsiveness-bench validate data/seed
responsiveness-bench audit data/seed --check
responsiveness-bench prepare-inference data/seed inputs.jsonl
responsiveness-bench prompt zero_shot > prompt_zero_shot.txt
responsiveness-bench prompt few_shot > prompt_few_shot.txt
responsiveness-bench schema > schema.json
```

For each case in `inputs.jsonl` and each arm, the system message served to the model is
`prompt_<arm>.txt` with the schema appended:

```
<contents of prompt_<arm>.txt>

Output JSON Schema (conform exactly):
<contents of schema.json>
```

and the user message is the case's raw JSON record (`{"case_id":..., "claim":..., "response":...}`
from `inputs.jsonl`). Decode at temperature 0, one attempt, with
`grammar = llama_cpp.LlamaGrammar.from_json_schema(json.dumps(schema))`. Then:

```bash
responsiveness-bench evaluate-inference data/seed results/open-models-20260928/<model_key>/predictions-<arm>.jsonl \
  --model-id "<name from the Models table> sha256:<full sha256 from manifest.json>" --prompt-arm <arm>
```

The generation harness itself is
`research/results/organism-surfaces-20260926/lanes/responsiveness_bench.py` on
`nexuspllc/institutional_stack` (branch `work/responsiveness-bench-baselines-20260928`,
[PR #3121](https://github.com/nexuspllc/institutional_stack/pull/3121)), dispatched through
`.github/workflows/ac-gpu.yml`'s `lane` job on the `coaseyclub` self-hosted runner:

```bash
gh workflow run ac-gpu.yml --repo nexuspllc/institutional_stack \
  --ref work/responsiveness-bench-baselines-20260928 \
  -f lane=responsiveness_bench -f runs_on='["coaseyclub"]' -f token=<TOKEN> \
  -f args="model=<qwen2_5_7b|llama3_1_8b|mistral_7b> arms=zero_shot,few_shot"
```

Each model self-provisions llama-cpp-python's CPU-only wheel and downloads its own GGUF file into
`~/.cache/organism-local/models/` on the runner, pinning the file's sha256 on first fetch.
