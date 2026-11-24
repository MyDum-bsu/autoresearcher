"""Exact replay of D1's one frozen two-period construction, not an LP solver."""

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def vector(values):
    return tuple(F(x) for x in values)


def matrix(values):
    return tuple(vector(row) for row in values)


def dot(a, b):
    require(len(a) == len(b), "dot dimension mismatch")
    return sum((x * y for x, y in zip(a, b, strict=True)), F(0))


def mv(a, b):
    return tuple(dot(row, b) for row in a)


def add(*vectors):
    require(len({len(v) for v in vectors}) == 1, "sum dimension mismatch")
    return tuple(sum(xs, F(0)) for xs in zip(*vectors, strict=True))


def combine(rows, terms):
    lhs = (F(0), F(0), F(0))
    rhs = F(0)
    for row_id, multiplier in terms:
        weight = F(multiplier)
        require(weight >= 0, "negative certificate multiplier")
        row, bound = rows[row_id]
        lhs = add(lhs, tuple(weight * x for x in row))
        rhs += weight * bound
    return lhs, rhs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    raw = args.candidate.read_bytes()
    data = json.loads(raw)
    require(data["candidate_id"] == "D1-three-prefix-bound-sensitive-v1", "wrong candidate")
    require(
        (data["T"], data["r"], data["n"], data["m"], data["d"]) == (2, 1, 2, 2, 2),
        "unsupported model",
    )
    A, B, E = (tuple(matrix(v) for v in data[key]) for key in ("A", "B", "E"))
    H, h, c = matrix(data["H"]), vector(data["h"]), vector(data["c"])
    x0, a = vector(data["x_initial"]), vector(data["first_program"])
    lo, hi = tuple(map(vector, data["lower"])), tuple(map(vector, data["upper"]))
    q, d0 = F(data["bound"]), F(data["d0"])
    paths = {p["id"]: tuple(map(vector, p["w"])) for p in data["paths"]}
    require(len(paths) == 4 and len(set(paths.values())) == 4, "path inventory mismatch")
    require(all(lo[0][i] <= a[i] <= hi[0][i] for i in range(2)), "first control outside box")
    labels = data["prefix_labels"]
    require(set(labels) == set(paths), "prefix label inventory mismatch")
    require(
        all((labels[i] == labels[j]) == (paths[i][0] == paths[j][0]) for i in paths for j in paths),
        "prefix grouping is false",
    )

    # Route 1: apply the original two transitions, never a residual inequality.
    def trajectory(path_id, b):
        controls = (a, b)
        x = x0
        states = [x]
        for t in range(2):
            x = add(mv(A[t], x), mv(B[t], controls[t]), mv(E[t], paths[path_id][t]))
            states.append(x)
        return states

    def feasible(path_ids, b, bound, hard_only=False):
        if not all(lo[1][i] <= b[i] <= hi[1][i] for i in range(2)):
            return False
        for path_id in path_ids:
            terminal = trajectory(path_id, b)[-1]
            if not all(dot(row, terminal) <= limit for row, limit in zip(H, h, strict=True)):
                return False
            if not hard_only and dot(c, terminal) + d0 > bound:
                return False
        return True

    observed = {}
    states = {pid: trajectory(pid, (F(0), F(0)))[1] for pid in paths}
    require(len(set(states.values())) == 1, "claimed state merge failed")
    require(len(set(labels.values())) == 3, "expected three prefixes")
    observed["state-cell"] = {"passed": True, "measured_states": states}
    prefix = {key: vector(value) for key, value in data["prefix_policy"].items()}
    prefix_traces = {}
    for pid in paths:
        b = prefix[labels[pid]]
        require(feasible([pid], b, q), "prefix witness failed: " + pid)
        terminal = trajectory(pid, b)[-1]
        prefix_traces[pid] = {"b": b, "states": trajectory(pid, b), "cost": dot(c, terminal) + d0}
    observed["prefix-witnesses"] = {"passed": True, "paths": prefix_traces}
    pairs = []
    for pair in data["pair_witnesses"]:
        pids = [pid for pid in paths if labels[pid] in pair["prefixes"]]
        b = vector(pair["b"])
        require(feasible(pids, b, q), "pair witness failed")
        pairs.append(
            {
                "prefixes": pair["prefixes"],
                "paths": pids,
                "b": b,
                "costs": {pid: dot(c, trajectory(pid, b)[-1]) + d0 for pid in pids},
            }
        )
    require(
        {tuple(sorted(p["prefixes"])) for p in pairs} == {("p0", "p1"), ("p0", "p2"), ("p1", "p2")},
        "incomplete pair inventory",
    )
    observed["pairwise-positive"] = {"passed": True, "pairs": pairs}

    # Route 2: expand the terminal affine map and replay nonnegative row sums.
    # Variables are (b_1,b_2,tau); control boxes are checked in route 1.
    rows = {}
    affine = {}
    for pid, w in paths.items():
        z = add(mv(A[0], x0), mv(B[0], a), mv(E[0], w[0]))
        offset = add(mv(A[1], z), mv(E[1], w[1]))
        response = B[1]
        affine[pid] = {"offset": offset, "response": response}
        for j, (normal, bound) in enumerate(zip(H, h, strict=True)):
            coeff = tuple(
                sum((normal[t] * response[t][i] for t in range(2)), F(0)) for i in range(2)
            )
            rows[f"{pid}:hard:{j}"] = (coeff + (F(0),), bound - dot(normal, offset))
        coeff = tuple(sum((c[t] * response[t][i] for t in range(2)), F(0)) for i in range(2))
        rows[f"{pid}:cost"] = (coeff + (F(-1),), -d0 - dot(c, offset))
    certificates = {}
    for key, cert in data["certificates"].items():
        lhs, rhs = combine(rows, cert["rows"])
        require(
            lhs == vector(cert["expected_lhs"]) and rhs == F(cert["expected_rhs"]),
            "certificate mismatch: " + key,
        )
        certificates[key] = {"lhs": lhs, "rhs": rhs, "rows": cert["rows"]}
    state_lhs, state_rhs = combine(rows, data["certificates"]["state_lower_bound"]["rows"])
    residual = state_rhs - state_lhs[2] * q
    require(state_lhs[:2] == (0, 0) and residual < 0, "not an infeasibility certificate")
    observed["joint-infeasible"] = {
        "passed": True,
        "q": q,
        "constant_contradiction_rhs": residual,
        "certificates": certificates,
    }
    # The independent affine expansion must agree with every directly replayed pair/witness.
    programs = list(prefix.values()) + [vector(p["b"]) for p in data["pair_witnesses"]]
    for pid in paths:
        for b in programs:
            require(
                add(mv(affine[pid]["response"], b), affine[pid]["offset"])
                == trajectory(pid, b)[-1],
                "route disagreement",
            )
    observed["double-route"] = {
        "passed": True,
        "terminal_comparisons": len(paths) * len(programs),
        "expanded_rows": rows,
    }

    state_b = vector(data["state_optimal_witness"])
    require(feasible(list(paths), state_b, F(2)), "state optimum witness failed")
    require(feasible(list(paths), state_b, q, hard_only=True), "hard-only feasibility failed")
    require(
        all(feasible([pid], prefix[labels[pid]], F("1/4")) for pid in paths),
        "prefix optimum witness failed",
    )
    require(
        state_rhs == -2 and certificates["prefix_p1_lower_bound"]["rhs"] == F("-1/4"),
        "wrong optimum lower bounds",
    )
    observed["exact-optima"] = {
        "passed": True,
        "prefix": F("1/4"),
        "state": F(2),
        "state_b": state_b,
        "hard_only_feasible": True,
        "scope": (
            "Witness upper bounds and universal linear-inequality lower bounds, "
            "not action enumeration."
        ),
    }
    require(
        not feasible(list(paths), vector(data["false_state_witness"]), q),
        "false witness incorrectly accepted",
    )
    observed["reject-false-witness"] = {
        "passed": True,
        "reason": "D has second terminal coordinate -1 under b=(1,0).",
    }
    terms = data["certificates"]["state_lower_bound"]["rows"]
    negative = [[row, "-1" if i == 0 else weight] for i, (row, weight) in enumerate(terms)]
    rejected = False
    try:
        combine(rows, negative)
    except ValueError as exc:
        require(str(exc) == "negative certificate multiplier", "unexpected mutation error")
        rejected = True
    require(rejected, "negative multiplier accepted")
    observed["reject-negative-multiplier"] = {"passed": True}
    sign_rows = dict(rows)
    original_cost = rows["A:cost"]
    # Mutate c to -c in the cost row while retaining tau's coefficient -1.
    sign_rows["A:cost"] = (
        tuple(-x for x in original_cost[0][:2]) + (F(-1),),
        -original_cost[1] - 2 * d0,
    )
    require(combine(sign_rows, terms) != (state_lhs, state_rhs), "cost sign mutation undetected")
    observed["reject-cost-sign-mutation"] = {
        "passed": True,
        "mutated_sum": combine(sign_rows, terms),
    }
    anticipative = {pid: vector(b) for pid, b in data["anticipative_path_policy"].items()}
    require(
        all(feasible([pid], anticipative[pid], F(0)) for pid in paths),
        "anticipative control not pathwise feasible",
    )
    consistent = all(
        anticipative[i] == anticipative[j] for i in paths for j in paths if labels[i] == labels[j]
    )
    require(not consistent, "anticipative policy accidentally prefix measurable")
    require(not feasible(["B", "C"], prefix["p1"], F(0)), "future suffix leaked")
    require(feasible(["B", "C"], prefix["p1"], F("1/4")), "legal robust prefix program failed")
    observed["timing-correlation"] = {
        "passed": True,
        "anticipative_pathwise_q0": True,
        "anticipative_prefix_policy_admissible": False,
        "same_prefix_paths": ["B", "C"],
        "legal_p1_costs": [prefix_traces[pid]["cost"] for pid in ("B", "C")],
    }
    require(
        not all(
            prefix[labels[i]] == prefix[labels[j]]
            for i in paths
            for j in paths
            if states[i] == states[j]
        ),
        "prefix policy accidentally state measurable",
    )
    observed["reject-prefix-as-state-policy"] = {"passed": True}
    print(
        json.dumps(
            {
                "schema_version": 1,
                "candidate_id": data["candidate_id"],
                "input_sha256": hashlib.sha256(raw).hexdigest(),
                "status": "passed",
                "check_count": len(observed),
                "checks": observed,
                "scope": (
                    "One rational continuous-box matrix-dynamics construction, exact witnesses "
                    "and linear certificates. No general theorem, Lean result or novelty verdict."
                ),
            },
            default=lambda x: str(x) if isinstance(x, F) else x,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
