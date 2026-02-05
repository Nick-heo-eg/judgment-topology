# With Judgment Layer: Same Plugin, Different Outcome

This document shows the **same legal plugin** with a judgment layer added.

## Environment

- **Platform:** Claude Code
- **Plugin:** Anthropic legal plugin (unchanged)
- **Version:** Same as baseline
- **Judgment Layer:** ON (using stop_policy.yaml)

## Scenario: NDA Triage (Identical Input)

### Input

```
/triage-nda

File: mutual_nda_techcorp_2026.pdf

Key Terms:
- Mutual confidentiality agreement
- 3-year term
- Standard confidentiality obligations
- No non-compete clause
- No residuals clause
- Governing law: Delaware
```

### Model Processing (Same as Baseline)

```
Analyzing document...

Classification: GREEN
Confidence: 92%

Risk Assessment:
✓ Standard mutual NDA format
✓ Reasonable term length (3 years)
✓ No unusual obligations
✓ Common governing law jurisdiction
✓ No identified red flags

Recommendation: Low risk - proceed with standard approval process
```

### Judgment Layer Intercept

```
⚠️  JUDGMENT LAYER ACTIVE

Model Output: GREEN (Low Risk)
Policy Check: LEGAL_EXECUTION_STOP_V1

[HOLD]

Legal classification is advisory output, not execution authority.
Model assessment (GREEN/YELLOW/RED) provides information but does not
constitute legal approval. Human review required before any binding action.

Policy ID: LEGAL_EXECUTION_STOP_V1
Condition: NDA_APPROVAL_ATTEMPT
State: HOLD
```

### System Response

```
Status: HOLD (Execution Blocked)

Model Classification: GREEN (Low Risk)
↓
Judgment Decision: HOLD
↓
Required Actions:
  ✓ Legal counsel review
  ✓ Authorized signatory approval

Reason:
NDA classified as GREEN (low risk) by model. However, classification
does not equal approval authority. Even low-risk NDAs require human
judgment before signing or commitment.

Evidence Logged:
→ proof/decision.trace.jsonl
→ Timestamp: 2026-02-06T09:41:12Z
→ Authority: judgment-gate:v1

Next Steps:
1. Route to legal counsel for review
2. Obtain explicit approval from authorized signatory
3. Document approval rationale
4. Re-submit with human authorization
```

## Key Differences from Baseline

| Aspect | Baseline | With Judgment Layer |
|--------|----------|-------------------|
| Model Output | GREEN | GREEN (identical) |
| Automatic Approval | Yes | No (blocked) |
| Human Authority | Optional | Required |
| Audit Trail | None | Full (JSONL) |
| Decision Authority | AI classification | Human judgment |
| Execution State | APPROVED | HOLD |

## What Changed?

**Nothing about the plugin.** The legal plugin still:
- Analyzes the document correctly
- Provides accurate classification
- Generates helpful recommendations

**What changed is governance:**
- Classification is information, not authority
- Execution requires explicit human approval
- All decisions are logged and auditable
- Even "safe" (GREEN) outputs don't auto-execute

## The Principle

**GREEN ≠ GO**

The judgment layer enforces that:
- Model output is advisory
- Binding commitments require human authority
- Classification and execution are separate concerns
- Uncertainty is represented as a system state (HOLD)

## Audit Trail

Every judgment decision generates a complete audit log:

```json
{
  "timestamp": "2026-02-06T09:41:12Z",
  "system": "Echo Judgment Adapter",
  "platform": "Claude Code",
  "plugin": "legal",
  "command": "triage-nda",
  "model_output": {"classification": "GREEN", ...},
  "judgment": {
    "decision": "HOLD",
    "reason": "Legal classification used for execution",
    "policy_id": "LEGAL_EXECUTION_STOP_V1"
  },
  "required_next_action": ["legal_counsel_review", "authorized_signatory_approval"],
  "irreversible": false
}
```

## Production Impact

With judgment layer:
1. **Legal review is mandatory** (not optional)
2. **Approval authority is explicit** (not implicit)
3. **Decisions are auditable** (logged with evidence)
4. **Risk is bounded** (classification ≠ commitment)

## What This Proves

Same environment. Same plugin. Same input. Same model output.

**Different decision about execution.**

The judgment layer adds governance without modifying Anthropic's tools.

---

**Status:** Proof of concept (private validation)
**Policy:** LEGAL_EXECUTION_STOP_V1
**Reference:** [stop_policy.yaml](../stop_policy.yaml)
