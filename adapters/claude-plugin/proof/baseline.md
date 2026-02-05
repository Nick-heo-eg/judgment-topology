# Baseline: Legal Plugin Without Judgment Layer

This document shows the original behavior of the Anthropic legal plugin.

## Environment

- **Platform:** Claude Code
- **Plugin:** Anthropic legal plugin (standard installation)
- **Version:** Current production
- **Judgment Layer:** OFF (baseline behavior)

## Scenario: NDA Triage

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

### Model Processing

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

### System Response

```
✓ NDA Classification: GREEN (Low Risk)

Based on the analysis, this NDA follows standard industry patterns
and contains no unusual risk factors.

Next Steps:
→ Proceed with approval
→ Route to authorized signatory
→ Standard processing timeline applies

Status: APPROVED for standard workflow
```

## Key Observations

1. **Model provides classification:** GREEN with 92% confidence
2. **System interprets as approval:** "APPROVED for standard workflow"
3. **Implicit execution authority:** Classification drives next steps
4. **No explicit human gate:** Human review is optional, not required
5. **No audit trail:** Decision reasoning not formally logged

## What Happens Next

In typical workflow:
1. Document routed to signing queue
2. Authorized signatory reviews (if they check queue)
3. Potential for auto-routing to esignature system
4. NDA executed based on AI classification

## The Assumption

**GREEN = GO**

The system assumes that:
- Model classification is reliable enough for action
- Low risk = automatic approval authority
- Human review is a optimization, not a requirement

## Why This Matters

This is **not** a flaw in the plugin design. Anthropic's legal plugin does exactly what it's supposed to do: provide expert analysis and classification.

The question is: **Should classification automatically drive execution in production legal workflows?**

---

**Note:** This baseline is provided for comparison purposes. It represents standard plugin behavior without additional governance layers.
