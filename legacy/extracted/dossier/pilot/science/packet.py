"""Lineage, action eligibility and scope-bound offline outcomes."""

from dataclasses import asdict

from pilot.checkers.finite_bellman import validate_instance
from pilot.science.contracts import canonical, decode, digest, require, unique
from pilot.science.finite import check, snapshot_integrity


def lineage(claims):
    for claim in claims.values():
        seen = {claim.id}
        current = claim
        while current.parent is not None:
            require(current.parent in claims, "missing parent")
            require(current.parent not in seen, "cyclic lineage")
            seen.add(current.parent)
            parent = claims[current.parent]
            require(current.version > parent.version, "child version must increase")
            require(
                (current.scope.model, current.scope.relation, current.scope.modes)
                == (parent.scope.model, parent.scope.relation, parent.scope.modes),
                "changed parent scope/relation",
            )
            require(
                parent.scope.restriction == "all"
                and current.scope.restriction == "nonzero-prefix-gain",
                "unsupported child restriction",
            )
            current = parent


def eligible(action, claims, checked):
    require(action.claim in claims, "action missing claim")
    claim = claims[action.claim]
    require(action.claim_sha256 == claim.identity, "stale action claim identity")
    require(len(claim.cases) <= action.max_cases, "inventory exceeds action budget")
    allowed = {claim.id, claim.parent}
    for prerequisite in action.prerequisites:
        require(prerequisite in checked, "missing prerequisite evidence")
        require(checked[prerequisite].claim in allowed, "wrong prerequisite binding")
    if claim.parent is not None:
        require(
            any(
                checked[item].claim == claim.parent
                and checked[item].conclusion == "checked-counterexample"
                for item in action.prerequisites
            ),
            "child requires checked parent counterexample",
        )


def attempt_result(attempt, actions, claims, checked):
    require(attempt.action in actions, "attempt missing action")
    action = actions[attempt.action]
    claim = claims[action.claim]
    require(all(item in checked for item in attempt.evidence), "missing attempt evidence")
    evidence = [checked[item] for item in attempt.evidence]
    require(all(item.claim == claim.id for item in evidence), "attempt evidence wrong claim")
    if attempt.outcome != "completed":
        return {**asdict(attempt), "claim": claim.id, "scientific_outcome": "none"}
    require(
        len(evidence) == len(claim.cases)
        and {item.instance for item in evidence} == {item.id for item in claim.cases},
        "incomplete/duplicate test inventory",
    )
    outcome = (
        "checked-counterexample"
        if any(item.conclusion == "checked-counterexample" for item in evidence)
        else "survived-finite-inventory"
    )
    return {
        **asdict(attempt),
        "claim": claim.id,
        "scientific_outcome": outcome,
        "coverage": [item.id for item in claim.cases],
        "universal_proof": False,
    }


def build(submission):
    snapshot_integrity()
    claims, instances = unique(submission.claims), unique(submission.instances)
    lineage(claims)
    for claim in claims.values():
        for case in claim.cases:
            require(case.id in instances, "missing expected instance")
            normalized = validate_instance(decode(instances[case.id].normalized_json))
            require(
                digest(normalized) == case.normalized_input_sha256,
                "inventory input identity mismatch",
            )
    checked = {}
    for evidence in submission.evidence:
        require(
            evidence.claim in claims and evidence.instance in instances, "missing evidence binding"
        )
        require(
            evidence.instance in {item.id for item in claims[evidence.claim].cases},
            "evidence outside claim inventory",
        )
        checked[evidence.id] = check(evidence, claims[evidence.claim], instances[evidence.instance])
    actions = unique(submission.actions)
    for action in actions.values():
        eligible(action, claims, checked)
    outcomes = [attempt_result(item, actions, claims, checked) for item in submission.attempts]
    return {
        "schema_version": 2,
        "kind": "illustrative-offline-handoff",
        "scientific_status_change": False,
        "model_definition": {
            "id": "m0-two-period-v1",
            "dynamics": ["x0=0", "x1=a+k*p", "x2=x1+b+q"],
            "timing": "Choose a before p; measure x1 or observe p; choose b before q.",
            "objective": "Minimize max abs(x2) over exactly the supplied complete paths (p,q).",
            "controls": "a and b belong to the supplied finite action sets.",
            "feasibility": "The terminal interval, when present, holds on every complete path.",
            "information": {"state": "exact x1", "prefix": "exact p"},
            "policy": "One second action per reachable observation cell; no unreachable defaults.",
            "comparison": "Equality of independently checked optimal rational values only.",
            "infeasibility": "Typed infeasibility is rejected for numeric comparison.",
            "premises": {
                "all": "No gain restriction.",
                "nonzero-prefix-gain": "k != 0, checked before comparison.",
            },
            "domain": "Exactly the bounded M0 finite input contract, not all control problems.",
        },
        "novelty": "unassessed",
        "human_attestation": "absent",
        "general_statement": (
            "proposed-unreviewed; docs/specs/2026-11-10-single-measurement-statement.md"
        ),
        "input": asdict(submission),
        "checked_evidence": [asdict(item) for item in checked.values()],
        "attempt_results": outcomes,
        "limitations": [
            "Finite survival is not universal proof.",
            "Hashes identify bytes, not producer authority or physical source correspondence.",
            "Action eligibility checks structure and binding, not intellectual quality.",
            "No live publication, formal proof, novelty review or human decision occurred.",
        ],
    }


def markdown(packet):
    # JSON fences preserve all context without interpreting arbitrary explanatory prose as markup.
    lines = [
        "# Illustrative offline scientific dossier",
        "",
        "Novelty: unassessed. Human attestation: absent. No scientific status transition.",
        "",
        "## Outcomes",
        "",
    ]
    for result in packet["attempt_results"]:
        lines.append(f"- {result['claim']}: {result['outcome']} / {result['scientific_outcome']}")
    lines += ["", "## Limitations", ""] + [f"- {item}" for item in packet["limitations"]]
    lines += ["", "## Complete handoff context", "", "    " + canonical(packet), ""]
    return "\n".join(lines)
