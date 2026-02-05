# Judgment Layer for Claude Plugins

This adapter adds a **judgment layer** on top of existing Claude plugins without modifying them.

## What This Does

Claude plugins (like Anthropic's legal plugin) provide powerful domain-specific capabilities. However, when these plugins generate classifications or recommendations, there's often an implicit assumption that these outputs can directly drive execution.

This adapter intercepts plugin commands **before execution** and applies judgment rules to determine whether the action should proceed, be held for human review, or be stopped.

## Core Principle

> **Classification ≠ Execution Authority**

A model's output (GREEN, YELLOW, RED) is advisory information, not an execution decision. The judgment layer enforces this separation.

## Architecture

```
[User Command]
    ↓
[Judgment Layer] ← stop_policy.yaml
    ↓
[Claude Plugin] (unchanged)
    ↓
[Execution] (only if judgment = ALLOW)
```

## Why This Matters

In domains like legal, finance, and compliance:
- **GREEN** does not mean "automatically approve"
- **Advisory output** should not become **binding action**
- **Irreversible commitments** require explicit human authority

## Relationship to Anthropic's Work

This project deeply respects Anthropic's plugin architecture. We do not:
- Fork their repositories
- Modify their plugin code
- Reimplement their functionality

Instead, we add a **pre-execution judgment layer** that works with existing plugins. This is complementary work focused on production governance, not a critique of the underlying tools.

## Files

- `stop_policy.yaml` - Defines judgment rules for legal plugin (NDA triage)
- `judgment_injector.py` - Minimal reference implementation
- `proof/` - Demonstration showing same plugin, different outcomes

## Usage

See `proof/README.md` for a complete demonstration of this adapter in action.

## References

- [Judgment Topology Spec](../../spec/judgment-topology-v1.md)
- [Anthropic Claude](https://www.anthropic.com/claude)
