# Proof: Judgment Layer for Legal Plugin

This proof demonstrates the same Anthropic legal plugin running on the same Claude Code setup.

**The only difference:** A judgment layer intercepts execution.

## What This Proves

**Claim:** Classification output (GREEN, YELLOW, RED) should not automatically trigger execution.

**Evidence:** Two identical scenarios with different outcomes.

## Setup

- **Platform:** Claude Code
- **Plugin:** Anthropic legal plugin (unchanged)
- **Command:** `/triage-nda`
- **Input:** Mutual NDA, 3-year term, standard clauses
- **Model Output:** `GREEN` (low risk)

## Scenario A: Baseline (No Judgment Layer)

See [baseline.md](./baseline.md)

**Flow:**
```
User: /triage-nda
  ↓
Model: GREEN (low risk)
  ↓
System: Approved ✓
```

**Result:** Automatic approval based on classification

## Scenario B: With Judgment Layer

See [judgment_on.md](./judgment_on.md)

**Flow:**
```
User: /triage-nda
  ↓
Model: GREEN (low risk)
  ↓
Judgment Layer: HOLD
  ↓
System: Human review required
```

**Result:** Execution blocked, human approval required

## Key Difference

| Aspect | Baseline | With Judgment Layer |
|--------|----------|-------------------|
| Model Output | GREEN | GREEN (same) |
| Execution | Automatic | Blocked |
| Human Authority | Optional | Required |
| Audit Trail | None | Full log (decision.trace.jsonl) |
| Legal Risk | AI decides | Human decides |

## Audit Evidence

All judgment decisions are logged to `decision.trace.jsonl` with:
- Timestamp
- Decision state (ALLOW/HOLD/STOP)
- Policy that triggered
- Required next actions
- Full context

See [decision.trace.jsonl](./decision.trace.jsonl) for example logs.

## Visual Comparison

See [comparison.png](./comparison.png) for side-by-side screenshots.

## Running This Proof

```bash
# Install dependencies
pip install pyyaml

# Run the demo
cd adapters/claude-plugin
python judgment_injector.py

# View the audit log
cat proof/decision.trace.jsonl | jq
```

## Implications

This proof shows:

1. **Same plugin, different governance** - No modification to Anthropic's code
2. **Classification ≠ Authority** - GREEN is information, not approval
3. **Auditable decisions** - Every judgment is traceable
4. **Human in the loop** - Legal commitments require human authority

## What This Is NOT

- A criticism of Anthropic's plugin design
- A claim that plugins are "unsafe"
- A recommendation to avoid Claude tools

## What This IS

- A demonstration that production use requires judgment governance
- Evidence that classification and execution are separate concerns
- A reference implementation for adding judgment layers to existing tools

---

**Status:** Private validation (link-restricted)
**Created:** 2026-02-06
**Reference:** [Judgment Topology v1.0](../../../spec/judgment-topology-v1.md)
