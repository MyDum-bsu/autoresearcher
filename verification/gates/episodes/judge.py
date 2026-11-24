"""PUBLIC offline episode judges. No journal, status promotion or candidate execution."""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

from pilot.episodes.vendor import finite_bellman as finite

ROOT = Path(__file__).resolve().parent
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}", re.ASCII)


class Rejected(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Rejected(reason)


def fields(data, names):
    require(type(data) is dict and set(data) == set(names.split()), "closed schema mismatch")


def decode(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def bad(_value):
        raise Rejected("noninteger JSON number forbidden")

    return json.loads(text, object_pairs_hook=pairs, parse_float=bad, parse_constant=bad)


def integrity():
    identities = decode((ROOT / "reference-identities.json").read_text())
    require(
        set(identities) == {"trusted/inputs.json", "trusted/target.lean.txt"},
        "trusted inventory mismatch",
    )
    for name, digest in identities.items():
        require(
            hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, "trusted input drift"
        )
    provenance = decode((ROOT / "provenance.json").read_text())
    for item in provenance["files"]:
        require(
            hashlib.sha256((ROOT / item["destination"]).read_bytes()).hexdigest() == item["sha256"],
            "vendor drift",
        )


def inputs():
    return decode((ROOT / "trusted/inputs.json").read_text())


def certs(case, data):
    fields(data, "state prefix")
    outcomes = [
        finite.check_result(inputs()[case], mode, data[mode]) for mode in ("state", "prefix")
    ]
    require(
        all(x["result"] == "optimal" for x in outcomes), "finite equality needs feasible optima"
    )
    return tuple(Fraction(x["value"]) for x in outcomes)


def implementable(instance, certificate):
    """Check equality of assignment on actual measured-state fibers."""
    assignments = dict(certificate["policy"])
    a, k = Fraction(certificate["first_action"]), Fraction(instance["prefix_gain"])
    fibers = {}
    for p, _ in instance["paths"]:
        x = a + k * Fraction(p)
        b = assignments[p]
        if x in fibers and fibers[x] != b:
            return False
        fibers[x] = b
    return True


def model(data):
    fields(
        data,
        "episode schema_version certificates state_implementable injective_implementable collision",
    )
    certs("hidden", data["certificates"])
    actual = implementable(inputs()["hidden"], data["certificates"]["prefix"])
    other = finite.solve(inputs()["injective"], "prefix")
    require(
        type(data["state_implementable"]) is bool and data["state_implementable"] == actual,
        "state/prefix confusion",
    )
    require(
        type(data["injective_implementable"]) is bool
        and data["injective_implementable"] == implementable(inputs()["injective"], other),
        "paired information confusion",
    )
    collision = data["collision"]
    require(
        type(collision) is list
        and len(collision) == 2
        and all(p in inputs()["hidden"]["paths"] for p in collision),
        "invalid collision paths",
    )
    p, q = collision
    require(p != q, "collision must use distinct paths")
    a = Fraction(data["certificates"]["prefix"]["first_action"])
    k = Fraction(inputs()["hidden"]["prefix_gain"])
    policy = dict(data["certificates"]["prefix"]["policy"])
    require(
        a + k * Fraction(p[0]) == a + k * Fraction(q[0]) and policy[p[0]] != policy[q[0]],
        "not a conflicting observation fiber",
    )


def falsify(data):
    fields(data, "episode schema_version parent parent_outcome witness certificates child")
    require(
        data["parent"] == "equal-all-v1" and data["parent_outcome"] == "refuted",
        "parent must remain refuted",
    )
    require(
        type(data["witness"]) is str and data["witness"] in ("hidden", "shift"), "unfrozen witness"
    )
    left, right = certs(data["witness"], data["certificates"])
    require(left != right, "not a counterexample")
    child = data["child"]
    fields(child, "id parent restriction outcome case certificates")
    require(
        child["id"] == "equal-nonzero-v2" and child["parent"] == data["parent"],
        "child lineage mismatch",
    )
    require(
        child["restriction"] == "nonzero-prefix-gain" and child["outcome"] == "finite-survival",
        "unsupported child scope/conclusion",
    )
    require(
        child["case"] == "injective" and Fraction(inputs()[child["case"]]["prefix_gain"]) != 0,
        "outside child premise",
    )
    a, b = certs(child["case"], child["certificates"])
    require(a == b, "child failed finite check")


def research(data):
    fields(data, "episode schema_version stages continuation")
    stages = data["stages"]
    require(type(stages) is list and len(stages) == 2, "two ordered evidence stages required")
    for stage in stages:
        fields(stage, "stage evidence decision")
    require(
        stages[0]["stage"] == "contradiction" and stages[0]["decision"] == "stop-parent-proof",
        "must respond to contradiction",
    )
    evaluate(stages[0]["evidence"], nested=True)
    require(stages[0]["evidence"]["episode"] == "F", "wrong staged evidence kind")
    require(stages[1]["stage"] == "restricted-check", "missing restricted stage")
    a, b = certs("injective", stages[1]["evidence"])
    require(a == b, "restricted stage not surviving")
    packet = data["continuation"]
    fields(
        packet,
        "parent parent_outcome child child_outcome next_action depends_on "
        "obligation consequences excluded human_review",
    )
    for key, expected in [
        ("parent", "equal-all-v1"),
        ("parent_outcome", "refuted"),
        ("child", "equal-nonzero-v2"),
        ("child_outcome", "finite-survival"),
        ("human_review", "pending"),
    ]:
        require(packet[key] == expected, "continuation scope/history mismatch")
    options = {
        "prove-injectivity": "fiber-injectivity",
        "compare-source-and-park": "source-assumptions",
    }
    action = packet["next_action"]
    require(
        type(action) is str and action in options and stages[1]["decision"] == action,
        "inadmissible continuation action",
    )
    require(packet["obligation"] == options[action], "action does not address its uncertainty")
    require(
        packet["depends_on"] == ["contradiction", "restricted-check"],
        "missing continuation dependencies",
    )
    require(
        packet["consequences"]
        == {
            "positive": "prepare-human-review",
            "negative": "revise-child",
            "inconclusive": "park-child",
        },
        "outcome consequences mismatch",
    )
    require(
        packet["excluded"] == ["universal-proof", "novelty", "attestation"], "missing exclusions"
    )


def proof(data):
    fields(data, "episode schema_version target proof")
    require(data["target"] == "observation_factorization", "wrong statement")
    body = data["proof"]
    require(type(body) is str and 0 < len(body) <= 8000, "proof size/type")
    # A deliberately small tactic/term language, not an arbitrary Lean executor.
    dotted = {"Classical.choose", "Classical.choose_spec", "False.elim"}
    forbidden = {
        "axiom",
        "sorry",
        "admit",
        "unsafe",
        "opaque",
        "def",
        "theorem",
        "example",
        "import",
        "set_option",
        "run_tac",
        "macro",
        "elab",
        "syntax",
        "instance",
        "initialize",
        "include",
        "omit",
        "section",
        "namespace",
        "end",
        "partial",
        "termination_by",
        "where",
        "native_decide",
    }
    require(
        not any(x in body for x in ("#", '"', "--", "/-", "\\", "`", "@")),
        "unsupported proof syntax",
    )
    require(
        re.fullmatch(r"[A-Za-z0-9_ .,:=()\[\]{}<>?\n→∃⟨⟩·↔]+", body) is not None,
        "unsupported proof characters",
    )
    tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*", body)
    for token in tokens:
        require(
            token not in forbidden and not any(part in forbidden for part in token.split(".")),
            "unsupported axiom/command",
        )
        if "." in token:
            require(
                token in dotted or all(x in {"symm", "trans"} for x in token.split(".") if x),
                "unsupported dependency",
            )
    version = subprocess.run(
        ["lean", "--version"], capture_output=True, text=True, timeout=10, check=True
    ).stdout
    require(version.startswith("Lean (version 4.35.0-rc2,"), "unpinned Lean version")
    source = (ROOT / "trusted/target.lean.txt").read_text().replace("{{PROOF}}", body)
    # Scratch remains in this worktree and is removed on success or failure.
    with tempfile.TemporaryDirectory(prefix="lean-", dir=ROOT) as directory:
        path = Path(directory) / "Check.lean"
        path.write_text(source)
        run = subprocess.run(["lean", str(path)], capture_output=True, text=True, timeout=30)
    require(run.returncode == 0, "Lean rejected fixed target: " + run.stdout + run.stderr)
    require("warning:" not in run.stdout, "Lean warning is not a clean proof")
    found = re.fullmatch(
        r"'observation_factorization' depends on axioms: \[(.*?)\]\s*", run.stdout, re.DOTALL
    )
    require(found is not None, "missing/nonunique transitive axiom report")
    axioms = {x.strip() for x in found[1].split(",") if x.strip()}
    require(axioms <= {"propext", "Classical.choice", "Quot.sound"}, "unsupported transitive axiom")
    return sorted(axioms)


def evaluate(data, nested=False):
    require(type(data) is dict, "submission must be object")
    require(
        type(data.get("schema_version")) is int and data["schema_version"] == 1,
        "schema version must be integer 1",
    )
    episode = data.get("episode")
    require(
        type(episode) is str
        and ID.fullmatch(episode) is not None
        and episode in ("M", "F", "P", "R"),
        "unknown/invalid episode identifier",
    )
    require(not nested or episode == "F", "nested evidence must be F")
    integrity()
    axioms = None
    if episode == "M":
        model(data)
    elif episode == "F":
        falsify(data)
    elif episode == "R":
        research(data)
    else:
        axioms = proof(data)
    result = {
        "episode": episode,
        "objective_checks": "pass",
        "human_review": "pending",
        "scientific_status_change": False,
    }
    if axioms is not None:
        result["axioms"] = axioms
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = evaluate(decode(args.input.read_text()))
    except (
        Rejected,
        finite.CheckerError,
        OSError,
        ValueError,
        subprocess.SubprocessError,
    ) as error:
        print(json.dumps({"objective_checks": "rejected", "reason": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
