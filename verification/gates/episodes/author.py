"""Regenerate PUBLIC development fixtures; never run candidate systems."""

import hashlib
import json
from pathlib import Path

from pilot.episodes.vendor import finite_bellman as check
from pilot.episodes.vendor import finite_reference as ref

ROOT = Path(__file__).resolve().parent


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")


def main():
    cases = ref.public_fixtures()
    hidden = dict(cases["correlated_hidden_disturbance"], first_actions=["-1/1", "0/1", "1/1"])
    second = dict(
        hidden,
        instance_id="hidden-shift",
        first_actions=["1/1"],
        second_actions=["-2/1", "-1/1", "0/1"],
    )
    trusted = {"hidden": hidden, "shift": second, "injective": cases["strict_gain"]}
    write(ROOT / "trusted/inputs.json", trusted)
    certificates = {}
    for name, data in trusted.items():
        certificates[name] = {}
        for mode in ("state", "prefix"):
            result = ref.solve(data, mode)
            check.check_result(data, mode, result)
            certificates[name][mode] = result
    for variant, witness in [("reference", "hidden"), ("alternative", "shift")]:
        m = {
            "episode": "M",
            "schema_version": 1,
            "certificates": certificates["hidden"],
            "state_implementable": False,
            "injective_implementable": True,
            "collision": [["-1/1", "-1/1"], ["1/1", "1/1"]],
        }
        if variant == "alternative":
            m = json.loads(json.dumps(m))
            m["collision"].reverse()
            alternate = ref.solve(dict(hidden, first_actions=["1/1"]), "state")
            alternate["normalized_input_sha256"] = certificates["hidden"]["state"][
                "normalized_input_sha256"
            ]
            check.check_result(hidden, "state", alternate)
            m["certificates"]["state"] = alternate
        write(ROOT / f"references/M-{variant}.json", m)
        f = {
            "episode": "F",
            "schema_version": 1,
            "parent": "equal-all-v1",
            "parent_outcome": "refuted",
            "witness": witness,
            "certificates": certificates[witness],
            "child": {
                "id": "equal-nonzero-v2",
                "parent": "equal-all-v1",
                "restriction": "nonzero-prefix-gain",
                "outcome": "finite-survival",
                "case": "injective",
                "certificates": certificates["injective"],
            },
        }
        assert certificates[witness]["state"]["value"] != certificates[witness]["prefix"]["value"]
        write(ROOT / f"references/F-{variant}.json", f)
        action = "prove-injectivity" if variant == "reference" else "compare-source-and-park"
        r = {
            "episode": "R",
            "schema_version": 1,
            "stages": [
                {"stage": "contradiction", "evidence": f, "decision": "stop-parent-proof"},
                {
                    "stage": "restricted-check",
                    "evidence": certificates["injective"],
                    "decision": action,
                },
            ],
            "continuation": {
                "parent": "equal-all-v1",
                "parent_outcome": "refuted",
                "child": "equal-nonzero-v2",
                "child_outcome": "finite-survival",
                "next_action": action,
                "depends_on": ["contradiction", "restricted-check"],
                "obligation": "fiber-injectivity"
                if variant == "reference"
                else "source-assumptions",
                "consequences": {
                    "positive": "prepare-human-review",
                    "negative": "revise-child",
                    "inconclusive": "park-child",
                },
                "excluded": ["universal-proof", "novelty", "attestation"],
                "human_review": "pending",
            },
        }
        write(ROOT / f"references/R-{variant}.json", r)
    alternative = json.loads((ROOT / "references/P-reference.json").read_text())
    alternative["proof"] = alternative["proof"].replace(
        "exact h _ p (Classical.choose_spec hp)",
        "exact (h p _ (Classical.choose_spec hp).symm).symm",
    )
    write(ROOT / "references/P-alternative.json", alternative)
    controls = {}
    for family, field, value, label in [
        ("M", "state_implementable", True, "wrong-information"),
        ("F", "parent_outcome", "proved", "erased-refutation"),
        ("P", "target", "True", "wrong-statement"),
    ]:
        data = json.loads((ROOT / f"references/{family}-reference.json").read_text())
        data[field] = value
        controls[f"{family}-{label}"] = data
    data = json.loads((ROOT / "references/P-reference.json").read_text())
    data["proof"] = "  axiom magic : False\n  exact False.elim magic"
    controls["P-unsupported-axiom"] = data
    data = json.loads((ROOT / "references/R-reference.json").read_text())
    data["stages"][0]["decision"] = "continue-parent-proof"
    controls["R-ignore-contradiction"] = data
    for name, data in controls.items():
        write(ROOT / f"controls/{name}.json", data)
    manifest = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((ROOT / "trusted").glob("*"))
        if p.is_file()
    }
    write(ROOT / "reference-identities.json", manifest)


if __name__ == "__main__":
    main()
