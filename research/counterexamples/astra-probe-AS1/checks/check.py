import itertools
import json
from fractions import Fraction as F

# Frozen candidate data; no search and no imports from predecessor checks.
ZERO = ((0, 0), (0, 0))
IDENTITY = ((1, 0), (0, 1))
DATA = {
    "positive": {"q": -1, "paths": [((0, 0), (-1, 0)), ((1, 0), (0, -1)), ((0, 1), (0, 0)), ((0, 1), (1, 1))]},
    "separated": {"q": -3, "paths": [((0, 0), (-1, 0)), ((1, 0), (0, -1)), ((0, 1), (0, 0)), ((0, 1), (1, 1))]},
    "timing": {"q": -1, "paths": [((0, 0), (-1, 0)), ((0, 0), (3, 0))]},
    "triangle": {"q": 1, "paths": [((0, 0), (-1, 0)), ((1, 0), (0, -1)), ((0, 1), (0, 0))]},
}
H = [(-1, 0), (0, -1), (1, 0), (0, 1)]
h = [0, 0, 4, 4]
c = (-1, 0)
observations = []


def require(ok, name):
    if not ok:
        raise RuntimeError(name)
    observations.append(name)


def dot(a, b):
    return sum((F(x) * F(y) for x, y in zip(a, b)), F(0))


def mv(a, b):
    return tuple(dot(row, b) for row in a)


def transition(a, x, b, u, e, w):
    terms = (mv(a, x), mv(b, u), mv(e, w))
    return tuple(sum((v[i] for v in terms), F(0)) for i in range(2))


def specification(name):
    if name == "triangle":
        return H[:2], h[:2], (1, 1), 2
    return H, h, c, 5


def trajectory_ok(name, path, action):
    hard, rhs, cost, box = specification(name)
    p, s = path
    x1 = transition(ZERO, (0, 0), ZERO, (0, 0), ZERO, p)
    x2 = transition(ZERO, x1, IDENTITY, action, IDENTITY, s)
    return (all(0 <= v <= box for v in action)
            and all(dot(row, x2) <= bound for row, bound in zip(hard, rhs))
            and dot(cost, x2) <= DATA[name]["q"])


def rows(name, path_index):
    hard, rhs, cost, box = specification(name)
    suffix = DATA[name]["paths"][path_index][1]
    return [(tuple(map(F, row)), F(bound) - dot(row, suffix))
            for row, bound in zip(hard + [cost], rhs + [DATA[name]["q"]])]


def certificate_ok(name, entries):
    lhs = [F(0), F(0)]
    rhs = F(0)
    for path, row, weight in entries:
        weight = F(weight)
        if weight < 0:
            return False
        a, b = rows(name, path)[row]
        lhs = [lhs[i] + weight * a[i] for i in range(2)]
        rhs += weight * b
    return lhs == [0, 0] and rhs < 0


def intervals(name):
    result = {}
    for index, (p, s) in enumerate(DATA[name]["paths"]):
        if p not in result:
            result[p] = [[F(0), F(5)], [F(0), F(5)]]
        for row, rhs in rows(name, index):
            used = [i for i in range(2) if row[i]]
            if len(used) != 1:
                raise ValueError("not coordinate-separable")
            i = used[0]
            bound = rhs / row[i]
            side = 1 if row[i] > 0 else 0
            op = min if side else max
            result[p][i][side] = op(result[p][i][side], bound)
    return result


# 4 cases, at most 4 paths, 3 prefixes, 7 nonempty subsets.
# No unbounded loops; at most 28 positive subset/path trajectory checks.
for name, data in DATA.items():
    states = [transition(ZERO, (0, 0), ZERO, (0, 0), ZERO, p) for p, s in data["paths"]]
    require(all(z == (0, 0) for z in states), name + ":equal_measured_states")
    require(len(set(data["paths"])) == len(data["paths"]), name + ":distinct_complete_paths")

L = H + [c]
require(L[0][0] * L[1][1] - L[0][1] * L[1][0] == 1, "rank_two_minor")
require(all(sum(v != 0 for v in row) == 1 for row in L), "coordinate_support")
pos = intervals("positive")
require(list(pos.values()) == [[[2, 5], [0, 4]], [[1, 4], [1, 5]], [[1, 3], [0, 3]]], "positive_exact_rectangles")
require(all(lo < hi for rectangle in pos.values() for lo, hi in rectangle), "positive_full_dimensional_individual_sets")
prefixes = list(pos)
for size in (1, 2, 3):
    for subset in itertools.combinations(prefixes, size):
        action = tuple(max(pos[p][i][0] for p in subset) for i in range(2))
        require(all(trajectory_ok("positive", path, action) for path in DATA["positive"]["paths"] if path[0] in subset), "positive_subset:" + str(subset))
require(all(trajectory_ok("positive", path, (F(5, 2), 2)) for path in DATA["positive"]["paths"]), "interior_common_action")
require(not trajectory_ok("positive", DATA["positive"]["paths"][0], (0, 0)), "reject_false_action")
require(not trajectory_ok("positive", DATA["positive"]["paths"][0], (6, 1)), "reject_box_violation")
# Positive nonzero objective is a sign error for this frozen signed cost.
require(not dot((1, 0), (1, 1)) <= -1, "reversed_cost_sign_rejects_valid_trajectory")
sep = intervals("separated")
require(list(sep.values()) == [[[4, 5], [0, 4]], [[3, 4], [1, 5]], [[3, 3], [0, 3]]], "separated_exact_rectangles")
for p, rectangle in sep.items():
    action = tuple(a[0] for a in rectangle)
    require(all(trajectory_ok("separated", path, action) for path in DATA["separated"]["paths"] if path[0] == p), "separated_individual:" + str(p))
require(certificate_ok("separated", [(0, 4, 1), (3, 2, 1)]), "separated_pair_certificate_0_le_minus1")
require(not certificate_ok("separated", [(0, 4, -1), (3, 2, 1)]), "reject_negative_certificate_multiplier")
require(certificate_ok("timing", [(0, 4, 1), (1, 2, 1)]), "timing_certificate_0_le_minus1")
clairvoyant = [(2, 0), (0, 0)]
require(all(trajectory_ok("timing", path, b) for path, b in zip(DATA["timing"]["paths"], clairvoyant)), "clairvoyant_actions_individually_feasible")
policy = {}
consistent = True
for path, action in zip(DATA["timing"]["paths"], clairvoyant):
    if path[0] in policy and policy[path[0]] != action:
        consistent = False
    policy[path[0]] = action
require(not consistent, "reject_suffix_oracle_as_prefix_policy")
require(intervals("timing")[(0, 0)][0] == [2, 1], "timing_singleton_prefix_empty")
for pair, action in [((0, 1), (1, 1)), ((0, 2), (1, 0)), ((1, 2), (0, 1))]:
    require(all(trajectory_ok("triangle", DATA["triangle"]["paths"][i], action) for i in pair), "triangle_pair:" + str(pair))
require(certificate_ok("triangle", [(0, 0, 1), (1, 1, 1), (2, 2, 1)]), "triangle_joint_certificate_0_le_minus1")
require(sum(v != 0 for v in specification("triangle")[2]) == 2, "triangle_outside_subclass")
print(json.dumps({"scope": "four frozen finite cases, not a general theorem", "checks_passed": len(observations), "observations": observations, "positive_joint_box": [[2, 3], [1, 3]], "positive_common_action": [2, 1], "positive_terminal_states": [[1, 1], [2, 0], [2, 1], [3, 2]], "positive_signed_costs": [-1, -2, -2, -3]}, indent=2))
