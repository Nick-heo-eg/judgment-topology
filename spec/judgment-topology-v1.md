# Judgment Topology v1.0 — Specification

## Core Principle
Uncertainty must be representable as a system state.
Undefined judgment must not transition into execution.

## States
```
ALLOW          — judgment defined; execution permitted
HOLD           — judgment pending; additional information required
INDETERMINATE  — judgment undefined; no decision can be derived
STOP           — irreversible boundary; execution permanently blocked
```

## Transition Rules

### Allowed
```
HOLD → ALLOW
HOLD → STOP
INDETERMINATE → HOLD
INDETERMINATE → STOP
ALLOW → STOP
STOP → (none)
```

### Forbidden
```
INDETERMINATE → ALLOW
STOP → (any state)
```

## Formal Claim

> Any AI system that allows undefined judgment to transition into execution is structurally incomplete.
