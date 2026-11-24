"""Emit deterministic PUBLIC reference/control validation evidence to stdout."""

import json

from pilot.episodes import judge
from pilot.episodes.vendor import finite_bellman

# Evaluator-owned completeness and family bindings, not candidate-provided metadata.
REFERENCES = {
    "M-reference.json": "M",
    "M-alternative.json": "M",
    "F-reference.json": "F",
    "F-alternative.json": "F",
    "P-reference.json": "P",
    "P-alternative.json": "P",
    "R-reference.json": "R",
    "R-alternative.json": "R",
}
CONTROLS = {
    "M-wrong-information.json": "M",
    "F-erased-refutation.json": "F",
    "P-wrong-statement.json": "P",
    "P-unsupported-axiom.json": "P",
    "R-ignore-contradiction.json": "R",
}


def inventory(directory, expected):
    root = judge.ROOT / directory
    judge.require(root.is_dir(), f"Missing inventory directory: {directory}")
    entries = {path.name: path for path in root.iterdir()}
    missing = sorted(set(expected) - set(entries))
    unexpected = sorted(set(entries) - set(expected))
    judge.require(
        not missing and not unexpected,
        f"{directory} inventory mismatch: missing={missing}, unexpected={unexpected}",
    )
    submissions = {}
    for name, family in sorted(expected.items()):
        path = entries[name]
        judge.require(path.is_file(), f"Inventory entry is not a file: {directory}/{name}")
        data = judge.decode(path.read_text())
        judge.require(
            type(data) is dict and data.get("episode") == family,
            f"Inventory family mismatch: {directory}/{name} must be {family}",
        )
        submissions[name] = data
    return submissions


def main():
    # Integrity must run even when no submissions can be discovered or evaluated.
    judge.integrity()
    references = inventory("references", REFERENCES)
    controls = inventory("controls", CONTROLS)
    results = {
        "public": True,
        "scientific_status_change": False,
        "references": {},
        "negative_controls": {},
        "finite_values": {},
    }
    for name, data in references.items():
        results["references"][name] = judge.evaluate(data)
    for name, data in controls.items():
        try:
            judge.evaluate(data)
        except (judge.Rejected, finite_bellman.CheckerError) as error:
            results["negative_controls"][name] = {
                "objective_checks": "rejected",
                "reason": str(error),
            }
        else:
            raise RuntimeError(f"Known invalid control accepted: {name}")
    for name, instance in judge.inputs().items():
        results["finite_values"][name] = {
            mode: finite_bellman.solve(instance, mode)["value"] for mode in ("state", "prefix")
        }
    print(json.dumps(results, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
