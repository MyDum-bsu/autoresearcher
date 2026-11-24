# Style diagnostic disposition

After the delivery/source check, the optional technical-style diagnostic ran once:

    timeout 30 python3 -B ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py goal/wave-3/realizability.md --language en

Observed exit code: 1. Raw output: style.stdout and style.stderr in this directory. It flagged one `not-just` passage at realizability.md line 81: the requirement that a subsequent consequence be not merely an interval/product, translation-Helly, elimination or positive-dependence restatement.

Manual editorial disposition: retain the passage. It expresses the scientific acceptance exclusion specified by the assignment, rather than a promotional contrast. The diagnostic match is recorded, not suppressed or reported as a zero-finding pass. No dossier bytes changed after delivery verification. This note is supplementary and is not included retroactively in the pre-verification result bindings. No scientific verdict follows from either style or delivery checks.
