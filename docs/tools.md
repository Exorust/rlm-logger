# Tools

Five read-only query primitives plus two side channels, all available to the agent
inside its sandboxed REPL.

## The five

### `schema()`
Describes the event store: distinct services, levels, row count, time window. Usually
the agent's first call.

### `top_errors(limit=20)`
Ranks error/warn events by frequency. Good for surfacing the loudest failure mode.

### `search(pattern, limit=10)`
Case-insensitive substring match across `msg` and `raw`. Results ordered by time.

### `around(ts, window_s=60, service=None)`
Pulls events within ±`window_s` of a timestamp. Use it to see what happened around
a specific event, optionally filtered to one service.

### `trace(trace_id)`
Matches any event whose `raw.trace_id` or `raw.request_id` equals the given id.
Best way to follow a single request through a multi-service call chain.

## Side channels

### `llm_query(question, context="")`
Dispatches a free-form question to a secondary LLM. Use sparingly: it counts against
`max_llm_calls`. Good for "is this stack trace characteristic of a GC pause or a lock
contention?" style judgement calls.

### `submit_incident_report(report: dict)`
Terminal. Validates `report` against the `IncidentReport` schema and ends the run.
Anything missing or malformed raises a validation error the agent will see; on success
the case file is sealed and written.
