# Offline scientific dossier

This standard-library module parses an explicit offline submission, independently
checks M0 finite certificates and exports a handoff. It does not publish science,
write a journal, call `ro`, choose a research campaign or evaluate arbitrary prose.
The only CLI output destination is stdout; diagnostics go to stderr and a rejected
submission exits 2 without a successful packet. Use Python with bytecode disabled.

## Reproduce the illustrative example

From the worktree root:

```sh
PYTHONDONTWRITEBYTECODE=1 timeout 30 python3 -m pilot.science --input pilot/examples/offline-dossier-v1.json --format json
PYTHONDONTWRITEBYTECODE=1 timeout 30 python3 -m pilot.science --input pilot/examples/offline-dossier-v1.json --format markdown
```

`pilot/examples/offline-dossier-v1.packet.json` and
`pilot/examples/offline-dossier-v1.dossier.md` are generated exports of that input.
They are illustrative offline artifacts, not another authoritative journal.
No timestamp, absolute checkout path, conversation history or random seed enters
the output. JSON uses sorted keys, ASCII escaping, compact separators and one
trailing newline. Markdown has a concise outcome list and the entire canonical
handoff context as indented data, preserving all evidence and proposed decisions.
Input array order is retained except for M0 mathematical sets, which the checker
normalizes. Identical input gives identical bytes across fresh processes.

## Closed schema and immutable records

The supported entry point is `contracts.parse(json_text)` followed by
`packet.build(submission)`; dataclass constructors are internal typed containers,
not an alternative untrusted-input admission interface. Every array becomes a
tuple. Nested instances and certificates become canonical JSON strings owned by
the record; no caller-owned mutable dictionary survives parsing. All records are
frozen dataclasses. No floating point is used.

The fixture gives a complete schema example. Every field listed below is required;
unknown fields and duplicate JSON keys are errors, including inside certificates.
Record identifiers must be globally unique across record kinds, and text arrays
may not contain duplicate entries. Every ID and ID reference, including instance
and certificate IDs and case inventory IDs, must match
`[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}` (1..128 ASCII characters). Whitespace,
newlines and Markdown metacharacters outside that grammar are rejected at parsing,
not stripped or repaired. Explanatory text remains unrestricted nonempty text;
canonical JSON escaping keeps it literal in the indented Markdown context.
Versions/limits must be positive integers, never bools.

- Submission: `schema_version` exactly integer 2; nonempty arrays `claims`,
  `instances`, `evidence`, `actions`, `attempts`.
- Claim: `id`, `version`, `parent` (ID or null), `scope`, nonempty `cases`
  (complete declared test inventory), explanatory `statement`. Each case is a
  closed object `{"id":"strict_gain","normalized_input_sha256":"<64 lowercase hex>"}`,
  never an unbound ID string. Case IDs are unique within each claim; the immutable
  tuple of frozen case records is sorted by ID. Its binding hash is SHA-256 of
  canonical JSON of the unchanged checker's `validate_instance` output, including
  the instance ID. Build independently normalizes and hashes every expected
  instance and compares it with the binding before admitting evidence. Supplied
  hashes and recomputed valid certificates alone cannot change a frozen case.
  Claim identity is SHA-256 of canonical JSON of the parsed claim, including text
  and the complete bound inventory. A legitimate case revision requires a new
  claim identity and refreshed action/evidence hashes; stale references reject.
  New valid versioned cases are allowed within the existing model and lineage
  rules. Mathematical set ordering does not change the normalized input binding.
  Schema 1 and old string-only case lists are rejected without compatibility fallback.
  The exported packet also uses schema 2; imported M0 instances/certificates retain
  their unchanged schema 1.
- Scope: `model="m0-two-period-v1"`, `relation="equal-values"`,
  `modes=["state","prefix"]`, `restriction="all"` or
  `"nonzero-prefix-gain"`. Nothing in `statement` executes as a predicate.
- Instance: exactly the imported M0 instance schema. Nonempty rational action
  sets (at most five each), one to eight complete two-component paths, rational
  prefix gain and optional hard terminal interval. Reduced canonical rationals
  have absolute numerator <=1000 and denominator <=1000. Details and arithmetic
  belong to `pilot/baseline/README.md` and the independent checker.
- Evidence: `id`, `claim`, exact `claim_sha256`, `instance`, exact
  `checker_sha256`, two full `certificates` in state/prefix order. The checker
  recomputes optimality/infeasibility with `finite_bellman.check_result`, not just
  feasible replay. Certificates bind normalized input hash, instance ID,
  information mode, actions and full per-path outcomes. A supplied PASS or hash
  without a matching independently checked certificate cannot support admission.
- Action: `id`, `claim`, `claim_sha256`, `operation="finite-compare"`,
  nonempty `prerequisites` (evidence IDs), `uncertainty`, `rationale`, distinct
  `positive`, `negative`, `inconclusive` consequences, nonempty `exclusions`,
  `max_cases` (1..8), `wall_seconds` (1..120). These are resource declarations
  checked for eligibility, not an OS-enforced sandbox or elapsed-time accounting.
- Attempt: `id`, `action`, `outcome`, `evidence` (IDs), explanatory `reason`.
  Outcomes are `completed`, `inconclusive`, `failed`, `cancelled`,
  `budget-exhausted`. Completed attempts require exactly one evidence record per
  expected case, bound to that action's claim. Every noncompleted outcome yields
  scientific outcome `none`, regardless of any diagnostic evidence retained.

Parents must exist, lineage must be acyclic, and child versions increase. The
only supported revision is restriction from `all` to `nonzero-prefix-gain` with
identical model/relation/modes. A child's action requires independently checked
parent-counterexample evidence. Action prerequisites otherwise must refer to
its own claim or immediate parent. These rules prevent missing/stale/wrong-scope
prerequisites; they do not establish the intellectual quality of a rationale.
Distinct text consequences prevent a trivial identical-outcomes record, not
meaningless paraphrases. Human judgment is still required.

## Executable scope and example interpretation

M0 has x0=0, x1=a+k*p, x2=x1+b+q. The controller chooses a before p and b
before q, minimizing max abs(x2) over the supplied complete paths (p,q).
`state` observes exact x1; `prefix` observes p. They are not relabeled as the
same information. Complete paths can be correlated. Controls are finite sets,
not continuous boxes. The optional terminal interval is robust over those paths.
The numeric comparison rejects typed infeasibility; it never replaces it with
zero or infinity. Premises are checked before evaluating equality/violation.

The inventory was fixed before implementing tests:

1. Parent `prefix-state-equality-v1`, `all`: the existing
   `correlated_hidden_disturbance` has checked state cost 1/1 and prefix cost
   0/1. It is a counterexample to this parent version's equality.
2. Child `prefix-state-equality-v2`, nonzero prefix gain: the existing
   `strict_gain` has checked state/prefix costs 0/1. It survives only this
   one explicitly declared finite test. The zero-gain parent counterexample
   is outside the child's premise and cannot refute it.
3. Four separate illustrative operational attempts show inconclusive, failed,
   cancelled and budget-exhausted outcomes. These are input examples, not
   claims that those incidents occurred during implementation.

The restricted child remains a proposal. The exported finite survival is not a
universal theorem, formal proof, novelty claim or human attestation. The separate
`docs/specs/2026-11-10-single-measurement-statement.md` proposes an exact
bound-witness correspondence statement for later human semantic review; it is
not proved by this example and has a different model/objective.

## Trust boundary and checks

The adapter pins the imported snapshot manifest hash, checks every one of its
eight file identities and requires the independent checker source identity.
This detects byte drift relative to the supplied snapshot. It authenticates
neither the producer nor source/model correspondence and does not freeze files
at the OS level. The checker is trusted reviewed code, imported from a fixed
module, never from a submitted module path. Concurrent source replacement,
hostile Python callers, interpreter compromise and filesystem sandboxing are
outside this offline threat model. There is no claim that a prompt is isolation.

The targeted unittest suite includes strict schema mutation, certificate and
observation tampering, feasible-but-nonoptimal witness rejection, typed
infeasibility, lineage/prerequisites, missing inventories, premises, immutability,
all noncompleted outcomes, twelve parent and seventy-two child set-order variants,
recomputed-valid-certificate data tampering, expected-hash tampering, stale
references, legitimate versioned updates, identifier injection at each parser
boundary, narrative preservation, a planted lost-path defect, two fresh CLI
processes per format, generated-byte
comparison and a before/after worktree file-hash inventory around exports.
It uses bounded standard-library enumeration, without installing Hypothesis.
No source checker is modified by the in-memory planted mutation.

Run the acceptance commands in the implementation report. Tests cannot establish
general mathematical truth, physical meaning, novelty, publication authority or
the proposed formal statement's correspondence to any source paper.
