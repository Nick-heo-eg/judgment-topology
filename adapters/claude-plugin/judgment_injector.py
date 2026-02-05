#!/usr/bin/env python3
"""
Judgment Injector for Claude Plugins

Intercepts plugin commands and applies judgment rules before execution.
This is a minimal reference implementation demonstrating the concept.
"""

import json
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


class JudgmentState:
    """Judgment topology states"""
    ALLOW = "ALLOW"
    HOLD = "HOLD"
    INDETERMINATE = "INDETERMINATE"
    STOP = "STOP"


class JudgmentInjector:
    """
    Intercepts Claude plugin commands and applies judgment layer.

    Does NOT modify the plugin itself - wraps it with pre-execution judgment.
    """

    def __init__(self, policy_path: str = "stop_policy.yaml"):
        self.policy = self._load_policy(policy_path)
        self.log_path = Path("proof/decision.trace.jsonl")

    def _load_policy(self, path: str) -> Dict[str, Any]:
        """Load stop policy configuration"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def intercept(self, command: str, model_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intercept a plugin command and apply judgment.

        Args:
            command: Plugin command (e.g., "triage-nda")
            model_output: Output from the Claude plugin

        Returns:
            Judgment decision with state, reason, and required actions
        """
        # Check each stop condition
        for condition in self.policy.get('stop_conditions', []):
            if self._matches_condition(command, model_output, condition):
                decision = {
                    'state': condition['decision'],
                    'reason': condition['reason'].strip(),
                    'policy_id': self.policy['policy_id'],
                    'condition_id': condition['id'],
                    'requires': condition.get('requires', []),
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'command': command,
                    'model_output': model_output
                }

                # Log the judgment
                self._log_decision(decision)

                return decision

        # No conditions matched - allow execution
        return {
            'state': JudgmentState.ALLOW,
            'reason': 'No stop conditions matched',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

    def _matches_condition(self, command: str, model_output: Dict[str, Any],
                          condition: Dict[str, Any]) -> bool:
        """Check if a stop condition matches the current context"""
        when = condition.get('when', {})

        # Check command match
        if 'command' in when and when['command'] != command:
            return False

        # Check model output classification
        if 'model_classification' in when:
            output_text = str(model_output)
            if when['model_classification'] not in output_text:
                return False

        # Check for classification keywords
        if 'model_output_contains' in when:
            output_text = str(model_output).upper()
            if not any(keyword in output_text for keyword in when['model_output_contains']):
                return False

        # Check action intent
        if 'action_intent' in when:
            # In real implementation, this would analyze the command context
            # For now, we assume triage commands have implicit approval intent
            if command.startswith('triage'):
                return True

        return True

    def _log_decision(self, decision: Dict[str, Any]) -> None:
        """Log judgment decision to audit trail"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        log_entry = {
            'timestamp': decision['timestamp'],
            'system': 'Echo Judgment Adapter',
            'platform': 'Claude Code',
            'plugin': self.policy['scope']['plugin'],
            'command': decision['command'],
            'model_output': decision['model_output'],
            'judgment': {
                'decision': decision['state'],
                'reason': decision['reason'],
                'policy_id': decision['policy_id'],
                'condition_id': decision['condition_id']
            },
            'required_next_action': decision.get('requires', []),
            'irreversible': decision['state'] == JudgmentState.STOP
        }

        with open(self.log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


def demo_nda_triage():
    """
    Demonstration: Same plugin, different outcomes

    Without judgment layer: GREEN → Approved
    With judgment layer: GREEN → HOLD → Human review required
    """
    injector = JudgmentInjector()

    # Simulate NDA triage command with GREEN classification
    model_output = {
        'classification': 'GREEN',
        'confidence': 0.92,
        'summary': 'Mutual NDA, 3-year term, no residuals clause',
        'recommendation': 'Low risk - proceed'
    }

    decision = injector.intercept('triage-nda', model_output)

    print("=" * 60)
    print("JUDGMENT LAYER DEMO: NDA Triage")
    print("=" * 60)
    print(f"\nModel Output: {model_output['classification']}")
    print(f"Model Recommendation: {model_output['recommendation']}")
    print(f"\nJudgment Decision: {decision['state']}")
    print(f"Reason: {decision['reason']}")

    if decision['state'] == JudgmentState.HOLD:
        print(f"\nRequired Actions:")
        for action in decision.get('requires', []):
            print(f"  - {action}")

    print(f"\nEvidence logged: {injector.log_path}")
    print("=" * 60)


if __name__ == '__main__':
    demo_nda_triage()
