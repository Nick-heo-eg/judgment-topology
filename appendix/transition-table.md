# State Transition Table

| FROM \ TO      | ALLOW | HOLD | INDETERMINATE | STOP |
|----------------|:-----:|:----:|:-------------:|:----:|
| **ALLOW**        |   –   |  –   |       –       |  ✓   |
| **HOLD**         |   ✓   |  –   |       –       |  ✓   |
| **INDETERMINATE**|   ✗   |  ✓   |       –       |  ✓   |
| **STOP**         |   ✗   |  ✗   |       ✗       |  –   |

**Legend**
- ✓ : Allowed transition
- ✗ : Forbidden transition
- – : Not applicable

This table defines permitted state transitions only; it does not prescribe decision logic.
