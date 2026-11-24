"""Exact open-loop certificates for two pinned A4 decimal datasets; stdlib only."""

import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

PINNED_INPUTS = {
    "a4_printed": "154b1a0181c5a9f29bcc20d64bc111220cbb4193b3560387b543d2c31fe32602",
    "a4_reconstructed_decimal": "77dca22ff207f2d7176fe103c2f38552c7a40e1d60cd39d10f1958bc06f1a869",
}
SCOPE = "a4_example_1_open_loop_rectangular_disturbances_exact_rational"
METHOD = "forward_power_columns_fractional_cost_adjustment_v1"
COVERAGE = "all_120_controls_and_all_independent_continuous_box_disturbances"


def canonical_json(data):
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


def rational_text(number):
    return f"{number.numerator}/{number.denominator}"


def _object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f"Duplicate JSON key: {key}")
        data[key] = value
    return data


def _noninteger(_value):
    raise ValueError("Floating point and nonfinite JSON numbers are forbidden")


def parse_input(text):
    data = json.loads(
        text, object_pairs_hook=_object, parse_float=_noninteger, parse_constant=_noninteger
    )
    validate_input(data)
    return data


def validate_input(data):
    """Pin the entire manifest, including identities, provenance and all numbers."""
    if not isinstance(data, dict) or not isinstance(data.get("coefficient_set_id"), str):
        raise ValueError("Expected an A4 input manifest with coefficient_set_id")
    digest = hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()
    if PINNED_INPUTS.get(data["coefficient_set_id"]) != digest:
        raise ValueError("Input is not a pinned A4 manifest (identity, schema or data mismatch)")
    return digest


def _apply(matrix, vector):
    return tuple(sum((a * b for a, b in zip(row, vector, strict=True)), F(0)) for row in matrix)


def make_certificate(manifest):
    digest = validate_input(manifest)
    dynamics = manifest["dynamics"]
    matrix = [list(map(F, row)) for row in dynamics["A"]]
    control = tuple(map(F, dynamics["B"]))
    disturbance = tuple(map(F, dynamics["E"]))
    initial = tuple(map(F, dynamics["x0"]))
    control_columns, disturbance_columns = [], []
    for _ in range(dynamics["horizon"]):
        control_columns.append(control)
        disturbance_columns.append(disturbance)
        control = _apply(matrix, control)
        disturbance = _apply(matrix, disturbance)
        initial = _apply(matrix, initial)
    # Forward powers are indexed by lag. Exported actions must instead be time-indexed.
    control_columns.reverse()
    disturbance_columns.reverse()
    radius = F(manifest["constraints"]["disturbance_abs_bound"])
    sx, sy = (radius * sum((abs(v[j]) for v in disturbance_columns), F(0)) for j in range(2))
    low, high = map(F, manifest["constraints"]["terminal_x_interval"])
    lower, upper = low + sx, high - sx
    if lower > upper or any(y == 0 for _, y in control_columns):
        raise ValueError("Unsupported generator assumptions: empty slab or zero y column")
    actions = [F(1) if y > 0 else F(-1) for _, y in control_columns]
    nominal_x = initial[0] + sum(
        (x * u for (x, _), u in zip(control_columns, actions, strict=True)), F(0)
    )
    needed = lower - nominal_x
    if needed <= 0:
        raise ValueError("Unsupported generator assumptions: lower slab must initially be violated")
    options = sorted(
        (abs(y / x), t)
        for t, ((x, y), u) in enumerate(zip(control_columns, actions, strict=True))
        if x * u < 0
    )
    multiplier = None
    for price, t in options:
        x = control_columns[t][0]
        gain = min(needed, 2 * abs(x))
        actions[t] += gain / x
        needed -= gain
        if needed == 0:
            multiplier = price
            break
    if needed != 0 or multiplier is None:
        raise ValueError("Unsupported generator assumptions: insufficient x-gain capacity")
    nominal_x = initial[0] + sum(
        (x * u for (x, _), u in zip(control_columns, actions, strict=True)), F(0)
    )
    reward = (
        initial[1]
        - sy
        + sum((y * u for (_, y), u in zip(control_columns, actions, strict=True)), F(0))
    )
    dual = (
        initial[1]
        - sy
        + multiplier * (initial[0] - lower)
        + sum((abs(y + multiplier * x) for x, y in control_columns), F(0))
    )
    if any(abs(u) > 1 for u in actions) or not lower <= nominal_x <= upper:
        raise ValueError("Generated controls violate the box or robust terminal slab")
    if multiplier < 0 or reward != dual:
        raise ValueError("Generated primal and dual do not match exactly")
    return {
        "schema_version": 1,
        "certificate_type": "a4_open_loop_primal_dual",
        "coefficient_set_id": manifest["coefficient_set_id"],
        "input_sha256": digest,
        "scope": SCOPE,
        "method": METHOD,
        "coverage": COVERAGE,
        "arithmetic": "exact_rational",
        "controls": list(map(rational_text, actions)),
        "objective": rational_text(reward),
        "support": {"x": rational_text(sx), "y": rational_text(sy)},
        "multipliers": {"lower": rational_text(multiplier), "upper": "0/1"},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        certificate = make_certificate(parse_input(args.input.read_text(encoding="utf-8")))
        output = canonical_json(certificate)
    except (OSError, ValueError, TypeError, RecursionError) as error:
        print(f"a4_certificate: {error}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
