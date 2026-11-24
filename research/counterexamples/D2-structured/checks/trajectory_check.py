"""Direct exact trajectory checks for the frozen D2 two-period candidates."""

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATA = Path(__file__).with_name("instances.json")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    require(len(a) == len(b), "dot dimension")
    return sum((F(x) * F(y) for x, y in zip(a, b)), F(0))


def mv(matrix, vector):
    return [dot(row, vector) for row in matrix]


def trajectory(data, path, continuation):
    state = list(map(F, data["x_initial"]))
    states = [state]
    for t, control in enumerate([data["first_program"], continuation]):
        lo, hi = data["boxes"][t]
        require(all(F(l) <= F(u) <= F(h) for l, u, h in zip(lo, control, hi)), "box")
        terms = [mv(data["A"][t], state), mv(data["B"][t], control), mv(data["E"][t], path["w"][t])]
        state = [sum(values, F(0)) for values in zip(*terms)]
        states.append(state)
    return states


def feasible(data, path, b, q):
    terminal = trajectory(data, path, b)[-1]
    hard = all(dot(row, terminal) <= F(h) for row, h in zip(data["H"], data["h"]))
    cost = dot(data["c"], terminal) + F(data["d0"])
    return hard and cost <= F(q), cost


def main():
    data = json.loads(DATA.read_text())
    require(
        (data["T"], data["r"], data["n"], data["m"], data["d"]) == (2, 1, 2, 2, 2),
        "fixed candidate dimensions",
    )
    paths = {p["id"]: p for p in data["paths"]}
    require(set(paths) == {"p1", "p2", "p3"}, "nonempty exact path inventory")
    require(len({tuple(p["w"][0]) for p in paths.values()}) == 3, "three distinct prefixes")
    observations = {name: trajectory(data, p, [0, 0])[1] for name, p in paths.items()}
    require(all(z == [0, 0] for z in observations.values()), "one merged state cell")
    prefix_costs = {}
    for name, b in data["prefix_witnesses"].items():
        ok, cost = feasible(data, paths[name], b, 0)
        require(ok, "prefix witness at zero")
        prefix_costs[name] = str(cost)
    expected_pairs = set(itertools.combinations(sorted(paths), 2))
    supplied_pairs = {tuple(entry["prefixes"]) for entry in data["pair_witnesses_at_q1"]}
    require(expected_pairs == supplied_pairs and len(supplied_pairs) == 3, "all pairs exactly once")
    pair_costs = []
    for entry in data["pair_witnesses_at_q1"]:
        costs = []
        for name in entry["prefixes"]:
            ok, cost = feasible(data, paths[name], entry["b"], 1)
            require(ok, "pair witness")
            costs.append(str(cost))
        pair_costs.append({"prefixes": entry["prefixes"], "b": entry["b"], "costs": costs})
    for path in paths.values():
        require(feasible(data, path, data["joint_witness_at_q2"], 2)[0], "joint witness at two")
    false_results = {
        name: feasible(data, p, data["false_joint_witness_at_q1"], 1)[0]
        for name, p in paths.items()
    }
    require(
        false_results == {"p1": True, "p2": True, "p3": False},
        "false joint witness must fail exactly p3",
    )
    timing = data["timing_control"]
    require(len({tuple(p["w"][0]) for p in timing["paths"]}) == 1, "timing control one prefix")
    clairvoyant = timing["illegal_clairvoyant_witnesses_at_q0"]
    for path in timing["paths"]:
        require(
            feasible(data, path, clairvoyant[path["id"]], 0)[0], "clairvoyant path-local witness"
        )
        require(
            feasible(data, path, timing["common_witness_at_q1"], 1)[0],
            "legal common timing witness",
        )
    consistent = len({tuple(b) for b in clairvoyant.values()}) == 1
    require(not consistent, "reject suffix revelation as prefix policy")
    signature = data["signature_control"]
    for path in paths.values():
        require(
            feasible(data, path, signature["common_witness"], signature["q"])[0],
            "unequal-signature common witness",
        )
    print(
        json.dumps(
            {
                "check_id": "D2-trajectories",
                "disposition": "passed",
                "observations": {k: list(map(str, v)) for k, v in observations.items()},
                "prefix_costs_at_q0": prefix_costs,
                "pair_witnesses_at_q1": pair_costs,
                "joint_witness_q2": data["joint_witness_at_q2"],
                "false_joint_witness_q1_path_feasibility": false_results,
                "timing_control": {
                    "pathwise_q0_feasible": True,
                    "prefix_consistent": consistent,
                    "legal_q1_feasible": True,
                },
                "signature_control_q2_feasible": True,
                "scope": "Exact rational trajectories and listed witnesses only; no action enumeration, general theorem, novelty or Lean verdict.",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
