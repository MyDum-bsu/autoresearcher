"""Fixed-input exact certificate replay and symbolic scalar proof identities.

Does not certify the general policy-to-scalar reduction or source novelty.
"""

import copy
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "artifacts/goal/wave-4/pilot"
sys.set_int_max_str_digits(30000)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mv(matrix, vector):
    return tuple(sum((a * b for a, b in zip(row, vector, strict=True)), F(0)) for row in matrix)


def forward_data(inp):
    dyn = inp["dynamics"]
    matrix = [list(map(F, row)) for row in dyn["A"]]
    b, e, x0 = (tuple(map(F, dyn[key])) for key in ("B", "E", "x0"))
    controls, disturbances = [], []
    cb, ce, drift = b, e, x0
    for _ in range(dyn["horizon"]):
        controls.append(cb)
        disturbances.append(ce)
        cb, ce, drift = mv(matrix, cb), mv(matrix, ce), mv(matrix, drift)
    return matrix, list(reversed(controls)), list(reversed(disturbances)), drift


def check(inp, cert, r):
    matrix, columns, noise, drift = forward_data(inp)
    bounds = inp["constraints"]
    beta, rho = F(bounds["control_abs_bound"]), F(bounds["disturbance_abs_bound"])
    low, high = map(F, bounds["terminal_x_interval"])
    require(beta >= 0 and rho >= 0 and low <= high, "domain")
    u = list(map(F, cert["controls"]))
    require(len(u) == len(columns), "control length")
    require(all(abs(v) <= beta for v in u), "control box")
    lam, mu = (F(cert["multipliers"][key]) for key in ("lower", "upper"))
    require(lam >= 0 and mu >= 0, "multiplier sign")
    support = tuple(rho * sum((abs(v[j]) for v in noise), F(0)) for j in range(2))
    require(tuple(F(cert["support"][key]) for key in ("x", "y")) == support, "support")
    nominal = tuple(drift[j] + sum((v[j] * a for v, a in zip(columns, u, strict=True)), F(0)) for j in range(2))
    replay = tuple(map(F, inp["dynamics"]["x0"]))
    b = tuple(map(F, inp["dynamics"]["B"]))
    for a in u:
        ax = mv(matrix, replay)
        replay = tuple(ax[j] + b[j] * a for j in range(2))
    require(replay == nominal, "chronological expansion")
    sx, sy = support
    require(nominal[0] - sx >= low, "lower strip")
    require(nominal[0] + sx <= high, "upper strip")
    reward = nominal[1] - sy
    require(reward == F(cert["objective"]), "objective")
    dual = drift[1] - sy + lam * (drift[0] - low - sx) + mu * (high - sx - drift[0])
    dual += beta * sum((abs(y + (lam - mu) * x) for x, y in columns), F(0))
    require(reward == dual, "primal dual equality")
    hx = beta * sum((abs(x) for x, _ in columns[r:]), F(0))
    hy = beta * sum((abs(y) for _, y in columns[r:]), F(0))
    hm = beta * sum((abs(y + (lam - mu) * x) for x, y in columns[r:]), F(0))
    delta = (lam + mu) * hx + hy - hm
    require(delta >= 0, "defect sign")
    return dict(reward=str(reward), dual=str(dual), delta=str(delta), zero=delta == 0,
                strip=[str(nominal[0] - sx), str(nominal[0] + sx)],
                upper_slack=str(high - nominal[0] - sx), columns=columns,
                r=r, lambda_lower=str(lam), mu_upper=str(mu))


def rejected(label, inp, cert, r, reason):
    try:
        check(inp, cert, r)
    except ValueError as error:
        require(str(error) == reason, f"{label}: unexpected rejection {error}")
        return dict(control=label, rejected=True, reason=str(error))
    raise ValueError(f"{label}: invalid control accepted")


def symbolic_checks():
    names = "q dx dy px py L H sx sy hx hy hp hm lam mu"
    q, dx, dy, px, py, low, high, sx, sy, hx, hy, hp, hm, lam, mu = sp.symbols(names, real=True)
    g_lower = dx + px - low - sx + hx
    g_upper = high - sx + hx - dx - px
    g_reward = dy + py + hy - sy - q
    g_prefix = hp - py - (lam - mu) * px
    d0 = dy - sy + lam * (dx - low - sx) + mu * (high - sx - dx) + hp + hm
    delta = (lam + mu) * hx + hy - hm
    decomposition = g_reward + lam * g_lower + mu * g_upper + g_prefix
    require(sp.expand(d0 + delta - q - decomposition) == 0, "symbolic weighted slack identity")
    require(sp.expand(d0 + delta - q - (decomposition - 2 * mu * g_upper)) != 0,
            "wrong upper-slack sign control")
    # For a single coordinate this identity separates the two triangle inequalities.
    x, y, ax, ay, amix, adiff = sp.symbols("x y ax ay amix adiff", real=True)
    coordinate_defect = (lam + mu) * ax + ay - amix
    triangle_split = (lam + mu - adiff) * ax + (ay + adiff * ax - amix)
    require(sp.expand(coordinate_defect - triangle_split) == 0, "triangle decomposition")
    return dict(sympy_version=sp.__version__, weighted_slack_identity=True,
                wrong_upper_slack_sign_rejected=True, triangle_identity=True,
                scope="universal polynomial identities only; nonnegative premises and policy reduction require the written proof")


def main():
    frozen = json.loads((ROOT / "artifacts/goal/wave-5/verification/parents.json").read_text())
    for rel, digest in frozen.items():
        require(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == digest, f"parent changed: {rel}")
    rows, controls = [], []
    for name in ("a4_printed", "a4_reconstructed_decimal"):
        inp = json.loads((BASE / "inputs" / (name + ".json")).read_text())
        cert = json.loads((BASE / (name + "-m0-open-loop.json")).read_text())["certificate"]
        for r in (67, 104):
            result = check(inp, cert, r)
            columns = result.pop("columns")
            require(result["zero"] == (r == 104), "frozen defect discriminator")
            rows.append(dict(case=f"{name}-r{r}", **result))
            if r == 104:
                corner = [F(1) if x >= 0 else F(-1) for x, _ in columns[r:]]
                favorable = lambda c: all(x * b >= 0 and y * b >= 0 for (x, y), b in zip(columns[r:], c, strict=True))
                require(favorable(corner), "positive favorable corner")
                corner[-1] *= -1
                require(not favorable(corner), "flipped corner accepted")
                controls.append(dict(case=name, control="flipped final suffix corner", rejected=True))
            else:
                require(F(result["delta"]) > 0, "invalid r67 zero claim")
                controls.append(dict(case=name, control="r67 exact-zero claim", rejected=True))
        bad = copy.deepcopy(cert)
        bad["objective"] = str(F(cert["objective"]) + 1)
        controls.append(rejected(name + ": objective +1", inp, bad, 104, "objective"))
        bad = copy.deepcopy(cert)
        bad["controls"][0] = "2/1"
        controls.append(rejected(name + ": out-of-box control", inp, bad, 104, "control box"))
        bad = copy.deepcopy(cert)
        bad["multipliers"]["lower"] = "-1/1"
        controls.append(rejected(name + ": negative multiplier", inp, bad, 104, "multiplier sign"))
        bad_input = copy.deepcopy(inp)
        bad_input["constraints"]["disturbance_abs_bound"] = "1/1"
        controls.append(rejected(name + ": changed noise", bad_input, cert, 104, "support"))
        for side, index, offset in (("lower", 0, F(1, 1000)), ("upper", 1, -F(1, 1000))):
            bad_input = copy.deepcopy(inp)
            bad_input["constraints"]["terminal_x_interval"][index] = str(F(rows[-1]["strip"][index]) + offset)
            controls.append(rejected(name + ": tightened " + side, bad_input, cert, 104, side + " strip"))
    astra = json.loads((ROOT / "artifacts/goal/wave-5/astra/probe.stdout.json").read_text())
    for ours, theirs in zip(rows, astra["rows"], strict=True):
        require(ours["case"] == theirs["case"] and F(ours["delta"]) == F(theirs["delta"]), "Astra comparison")
        require(F(ours["reward"]) == F(theirs["m0_objective"]), "Astra objective comparison")
    print(json.dumps(dict(goalAchieved=False, rows=rows, invalid_controls=controls,
                          symbolic=symbolic_checks(), parent_sha256=frozen,
                          scope="four fixed exact certificates; general model reduction is written, not formally checked"), indent=2))


if __name__ == "__main__":
    main()
