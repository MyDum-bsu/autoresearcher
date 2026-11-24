"""Independent inequality/certificate replay for the fixed D2 candidates.

This route uses explicit scalar terminal formulas, not trajectory_check imports.
The exact model equalities below bind those formulas to instances.json.
"""

import copy
import json
from fractions import Fraction as F
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows_for(path, q):
    s, t = map(F, path["w"][1])
    return {
        "hard-0": ([-F(1), F(0)], s),
        "hard-1": ([F(0), -F(1)], t),
        "cost": ([F(1), F(1)], F(q) - s - t),
    }


def combine(paths, terms, q):
    lhs = [F(0), F(0)]
    rhs = F(0)
    for term in terms:
        weight = F(term["lambda"])
        require(weight >= 0, "nonnegative certificate multiplier")
        row, bound = rows_for(paths[term["path"]], q)[term["row"]]
        lhs = [x + weight * y for x, y in zip(lhs, row)]
        rhs += weight * bound
    return lhs, rhs


def contradiction(paths, terms, q):
    lhs, rhs = combine(paths, terms, q)
    return lhs == [0, 0] and rhs < 0


def main():
    data = json.loads(Path(__file__).with_name("instances.json").read_text())
    zero = [[0, 0], [0, 0]]
    identity = [[1, 0], [0, 1]]
    for key, expected in {
        "A": [zero, zero],
        "B": [zero, identity],
        "E": [zero, identity],
        "x_initial": [0, 0],
        "first_program": [0, 0],
        "H": [[-1, 0], [0, -1]],
        "h": [0, 0],
        "c": [1, 1],
        "d0": 0,
        "boxes": [[[0, 0], [0, 0]], [[0, 0], [2, 2]]],
    }.items():
        require(data[key] == expected, "scalar formula/model binding: " + key)
    paths = {p["id"]: p for p in data["paths"]}
    require(len(paths) == 3, "three-row source paths")
    certificate = data["joint_certificate_at_q1"]
    require(contradiction(paths, certificate, 1), "joint rational contradiction")
    lhs, rhs = combine(paths, certificate, 1)
    require(rhs == -1, "strict contradiction magnitude")
    at_zero = combine(paths, certificate, 0)
    at_one = combine(paths, certificate, 1)
    require(at_zero == ([0, 0], -2) and at_one == ([0, 0], -1), "affine RHS identity q-2")
    require(combine(paths, certificate, 2) == ([0, 0], 0), "boundary q2 is not contradiction")
    bad = copy.deepcopy(certificate)
    bad[2]["lambda"] = 0
    require(not contradiction(paths, bad, 1), "reject missing cost-row certificate")
    sign_error = copy.deepcopy(certificate)
    sign_error[0]["lambda"] = -1
    negative_rejected = False
    try:
        combine(paths, sign_error, 1)
    except ValueError as exc:
        require(str(exc) == "nonnegative certificate multiplier", "specific intended rejection")
        negative_rejected = True
    require(negative_rejected, "negative multiplier must be rejected")
    timing = data["timing_control"]
    timing_paths = {p["id"]: p for p in timing["paths"]}
    timing_terms = timing["certificate_at_q0"]
    require(contradiction(timing_paths, timing_terms, 0), "same-prefix timing contradiction")
    require(combine(timing_paths, timing_terms, 0) == ([0, 0], -1), "timing RHS q-1")
    require(combine(timing_paths, timing_terms, 1) == ([0, 0], 0), "timing boundary")
    signatures = {
        name: [str(rows_for(path, 2)[key][1]) for key in ["hard-0", "hard-1", "cost"]]
        for name, path in paths.items()
    }
    require(
        len({tuple(s) for s in signatures.values()}) == 3, "three different residual signatures"
    )
    print(
        json.dumps(
            {
                "check_id": "D2-certificates",
                "disposition": "passed",
                "joint_q1_sum": {"lhs": list(map(str, lhs)), "rhs": str(rhs)},
                "joint_bound_identity": "0 <= q - 2",
                "timing_q0_sum": {"lhs": ["0", "0"], "rhs": "-1"},
                "timing_bound_identity": "0 <= q - 1",
                "controls": {
                    "missing_row_certificate_rejected": True,
                    "negative_multiplier_rejected": True,
                    "q2_not_refuted": True,
                },
                "residual_RHS_at_q2": signatures,
                "scope": "Sound rational nonnegative combinations of the actual candidate inequalities; no general dual completeness, general geometry theorem, Lean or novelty verdict.",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
