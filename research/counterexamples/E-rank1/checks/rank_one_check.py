"""Exact controls for six frozen rank-one continuation boundary instances."""

import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(left, right):
    return sum((x * y for x, y in zip(left, right, strict=True)), F(0))


def rows_for(case, subset):
    lo, hi = case["lower"], case["upper"]
    rows = [
        ([F(1), F(0)], hi[0], "box-upper-0"),
        ([F(-1), F(0)], -lo[0], "box-lower-0"),
        ([F(0), F(1)], hi[1], "box-upper-1"),
        ([F(0), F(-1)], -lo[1], "box-lower-1"),
    ]
    response = case["B1"]
    for prefix in subset:
        suffix = case["suffixes"][prefix]
        rows.append(([-x for x in response], suffix, f"hard-{prefix}"))
        rows.append((response, case["q"] - suffix, f"cost-{prefix}"))
    return rows


def obeys(point, rows):
    return all(dot(coeff, point) <= rhs for coeff, rhs, _ in rows)


def vertex_route(rows):
    points = set()
    for first, second in combinations(rows, 2):
        (a, b), rhs, _ = first
        (c, d), other, _ = second
        determinant = a * d - b * c
        if determinant:
            point = ((rhs * d - b * other) / determinant, (a * other - rhs * c) / determinant)
            if obeys(point, rows):
                points.add(point)
    return sorted(points)


def scalar_route(case, subset):
    response = case["B1"]
    minus = [
        lo if value >= 0 else hi
        for value, lo, hi in zip(response, case["lower"], case["upper"], strict=True)
    ]
    plus = [
        hi if value >= 0 else lo
        for value, lo, hi in zip(response, case["lower"], case["upper"], strict=True)
    ]
    image_low, image_high = dot(response, minus), dot(response, plus)
    lower = max([image_low] + [-case["suffixes"][p] for p in subset])
    upper = min([image_high] + [case["q"] - case["suffixes"][p] for p in subset])
    if lower > upper:
        return None, (lower, upper)
    if image_low == image_high:
        point = minus
    else:
        alpha = (lower - image_low) / (image_high - image_low)
        point = [(1 - alpha) * x + alpha * y for x, y in zip(minus, plus, strict=True)]
    require(dot(response, point) == lower, "section misses chosen scalar")
    return point, (lower, upper)


def certificate(rows, weights):
    require(all(weight >= 0 for weight in weights.values()), "negative multiplier")
    lookup = {name: (coeff, rhs) for coeff, rhs, name in rows}
    require(set(weights) <= set(lookup), "certificate names missing row")
    left = [sum((weights[name] * lookup[name][0][j] for name in weights), F(0)) for j in range(2)]
    right = sum((weight * lookup[name][1] for name, weight in weights.items()), F(0))
    require(left == [0, 0] and right < 0, "not a strict contradiction")
    return {
        "weights": {key: str(value) for key, value in weights.items()},
        "weighted_left": list(map(str, left)),
        "weighted_right": str(right),
    }


def contradiction_for(case, rows):
    if case["id"] == "E-separated":
        weights = {"hard-0": F(1), "cost-2": F(1)}
    elif case["id"] == "E-singleton-r1-empty":
        weights = {"hard-0": F(1), "box-upper-0": F(1), "box-lower-1": F(1)}
    elif case["id"] == "E-singleton-r0-empty":
        weights = {"hard-0": F(1)}
    else:
        raise ValueError("unexpected infeasible case")
    return certificate(rows, weights)


def normalize(raw):
    result = dict(raw)
    for key in ["B1", "lower", "upper", "suffixes"]:
        result[key] = list(map(F, raw[key]))
    result["q"] = F(raw["q"])
    require(
        len(result["B1"]) == len(result["lower"]) == len(result["upper"]) == 2,
        "two continuation coordinates required",
    )
    require(
        all(lo <= hi for lo, hi in zip(result["lower"], result["upper"], strict=True)), "empty box"
    )
    return result


def main():
    packet = json.loads((HERE / "instances.json").read_text())
    require(len(packet["cases"]) == 6, "fixed six-case inventory changed")
    observations = []
    for raw in packet["cases"]:
        case = normalize(raw)
        count = len(case["suffixes"])
        require(1 <= count <= 3, "prefix cap")
        subsets = [
            subset for size in range(1, count + 1) for subset in combinations(range(count), size)
        ]
        checks = []
        for subset in subsets:
            rows = rows_for(case, subset)
            point, interval = scalar_route(case, subset)
            vertices = vertex_route(rows)
            feasible = point is not None
            require(feasible == bool(vertices), "scalar and vertex routes disagree")
            item = {
                "prefixes": list(subset),
                "feasible": feasible,
                "scalar_interval": list(map(str, interval)),
                "vertex_count": len(vertices),
            }
            if feasible:
                require(obeys(point, rows), "section violates original rows")
                terminals = []
                for prefix in subset:
                    # x1=0; choose the same action before the suffix enters.
                    x1 = F(0)
                    terminal = dot(case["B1"], point) + case["suffixes"][prefix]
                    require(
                        x1 == 0 and terminal >= 0 and terminal <= case["q"],
                        "direct trajectory violates hard/cost bounds",
                    )
                    terminals.append(str(terminal))
                item.update(witness=list(map(str, point)), terminal_states=terminals)
            else:
                item["contradiction"] = contradiction_for(case, rows)
            checks.append(item)
        singles = all(item["feasible"] for item in checks if len(item["prefixes"]) == 1)
        pairs = all(item["feasible"] for item in checks if len(item["prefixes"]) == 2)
        joint = checks[-1]["feasible"]
        require([singles, pairs, joint] == raw["expected"], "unexpected case outcome")
        require(not (singles and pairs) or joint, "repaired child violated on fixed case")
        observations.append(
            {
                "case_id": case["id"],
                "measured_states": ["0"] * count,
                "rank_L": int(any(case["B1"])),
                "individual_feasible": singles,
                "distinct_pairs_feasible": pairs,
                "joint_feasible": joint,
                "subsets": checks,
            }
        )

    common = normalize(packet["cases"][0])
    require(
        not obeys([F(0), F(0)], rows_for(common, (0, 1, 2))), "false witness accidentally accepted"
    )
    # Reversing -t<=s to t>=s admits t=-1 for s=-1, q=2.
    require(not obeys([F(0), F(1)], rows_for(common, (0,))), "sign mutation accidentally accepted")
    rejected_negative = False
    try:
        certificate(rows_for(common, (0,)), {"hard-0": F(-1)})
    except ValueError as error:
        require(str(error) == "negative multiplier", "unrelated rejection")
        rejected_negative = True
    require(rejected_negative, "negative multiplier accepted")
    print(
        json.dumps(
            {
                "check_id": "E-rank-one-exact",
                "cases": observations,
                "controls": {
                    "false_witness_rejected": True,
                    "sign_mutation_rejected": True,
                    "negative_multiplier_rejected": True,
                    "singleton_vacuity_observed": True,
                },
                "scope": "six fixed rational systems; not a general rank-one proof",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
