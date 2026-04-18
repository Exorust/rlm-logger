# Eval Harness

A case file can carry a `ground_truth` block. When present, the `GroundTruthDiff`
viewer panel computes two gates and renders pass/fail badges:

## The gates

### `evidence_overlap ≥ 0.5`

Jaccard similarity between the report's evidence `event_id`s and `ground_truth.evidence_event_ids`.
Catches "the agent solved it but cited the wrong events." In the reference fixture,
the ideal trajectory scores 1.0 (all 5 ground-truth events cited).

### `distractor_hits == 0`

Distractors are ground-truth-flagged red herrings: events that look plausible but
aren't causal. If the agent marks any of them `is_key: true`, the run fails the eval,
regardless of whether it got the root cause right. This catches overconfident pattern
matching.

## The reference fixture

`examples/checkout-incident/` is a 72-row 5-service fixture: a Stripe API key rotation
that lands a checkout worker on a stale secret version and cascades to 5xx.

- 5 ground-truth events (vault rotation, first 401, caller-side 401, 5xx spike, queue lag)
- 5 distractors (redis replica blip, db pool pressure, feature-flag reload, subscription-
  worker retry, unrelated 429)
- Ideal trajectory: `schema → top_errors → search("invalid_api_key_version") → around(rotation_ts) → trace(tr_0003) → submit`

Run it:

```bash
pytest eval/test_checkout_fixture.py -v
```

## Writing your own eval

Add a `ground_truth.json` to `examples/<your-incident>/` with the same shape as the
checkout one, then parametrize `eval/test_checkout_fixture.py` or copy it. The MockLM
pattern keeps tests hermetic; for real-LLM runs, set `RLM_EVAL_REAL=1` and budget accordingly.
