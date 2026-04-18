# Case File Protocol v0.1

A case file is a single JSON document. One run = one case file.

## Top-level shape

```jsonc
{
  "version": "0.1",
  "question": "why did checkout fail around 3am?",
  "model": { "provider": "anthropic", "name": "claude-sonnet-4-6", "temperature": 0.2 },
  "logs_manifest": { "files": [...], "time_window": {...}, "total_rows": 72 },
  "trajectory": [ /* Step[] */ ],
  "report": { /* IncidentReport | null */ },
  "termination_reason": "submitted",  // or max_iterations, max_llm_calls, max_wall_clock, aborted, error
  "usage": { "llm_calls": 7, "tool_calls": 6, "wall_clock_s": 42, "input_tokens": 18200, "output_tokens": 2100 },
  "ground_truth": null  // optional, for eval
}
```

## EvidenceLine

Every evidence citation carries up to ±3 surrounding lines of context so the viewer can
show what happened around the cited event without re-reading the source logs:

```jsonc
{
  "event_id": "vault-rotate-stripe-2026-04-17T02:58:04Z",
  "file": "logs/vault.log.jsonl",
  "line": 3,
  "ts": "2026-04-17T02:58:04Z",
  "service": "vault",
  "level": "info",
  "text_redacted": "secret rotated old_version=6 new_version=7",
  "context_before": [],   // up to 3 redacted lines
  "context_after": [],    // up to 3 redacted lines
  "why": "the rotation is the precipitating event",
  "is_key": true
}
```

`text_redacted` and `context_*` have already been through the secret redactor. No raw
Bearer tokens, Stripe keys, AWS access keys, JWTs, or private keys should ever appear
in a case file.

## Breaking changes

The `version` field is a string literal (`"0.1"`). Any change that alters field names,
types, required-ness, or meaning bumps this. The Python pydantic model and the TypeScript
zod schema in the viewer are kept in lock-step.
