"""Independent A4 certificate verifier: backward adjoints and chronological replay."""

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

INPUT_DIGESTS = {
    "a4_printed": "154b1a0181c5a9f29bcc20d64bc111220cbb4193b3560387b543d2c31fe32602",
    "a4_reconstructed_decimal": "77dca22ff207f2d7176fe103c2f38552c7a40e1d60cd39d10f1958bc06f1a869",
}
CERTIFICATE_FIELDS = {
    "schema_version",
    "certificate_type",
    "coefficient_set_id",
    "input_sha256",
    "scope",
    "method",
    "coverage",
    "arithmetic",
    "controls",
    "objective",
    "support",
    "multipliers",
}
RATIONAL = re.compile(r"(?:0|-?[1-9][0-9]*)/[1-9][0-9]*", re.ASCII)


class CheckError(ValueError):
    """Invalid data or certificate; no scientific/project status is implied."""


def canonical_json(data):
    return json.dumps(
        data, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def _rtext(number):
    return f"{number.numerator}/{number.denominator}"


def _number(text):
    if not isinstance(text, str) or RATIONAL.fullmatch(text) is None:
        raise CheckError("Expected a reduced rational n/d string")
    number = Fraction(text)
    if _rtext(number) != text:
        raise CheckError("Rational string is not canonical/reduced")
    return number


def _fields(data, expected, label):
    if not isinstance(data, dict) or data.keys() != expected:
        raise CheckError(f"{label}: missing or unknown fields")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CheckError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_number(_text):
    raise CheckError("Floating point and nonfinite JSON numbers are forbidden")


def parse_json(text):
    try:
        return json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_float=_reject_number,
            parse_constant=_reject_number,
        )
    except json.JSONDecodeError as error:
        raise CheckError(f"Malformed JSON: {error.msg}") from error


def validate_input(manifest):
    if not isinstance(manifest, dict) or not isinstance(manifest.get("coefficient_set_id"), str):
        raise CheckError("Expected pinned input manifest with coefficient_set_id")
    digest = hashlib.sha256(canonical_json(manifest).encode("utf-8")).hexdigest()
    if INPUT_DIGESTS.get(manifest["coefficient_set_id"]) != digest:
        raise CheckError("Input identity/schema/source/coefficients do not match a pinned manifest")
    return digest


def _effects(matrix, vector, x0, horizon):
    """Row costates travel backward from terminal coordinates, never forward powers."""
    px, py = (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))
    columns = [None] * horizon
    for t in range(horizon - 1, -1, -1):
        columns[t] = (px[0] * vector[0] + px[1] * vector[1], py[0] * vector[0] + py[1] * vector[1])
        px = (
            px[0] * matrix[0][0] + px[1] * matrix[1][0],
            px[0] * matrix[0][1] + px[1] * matrix[1][1],
        )
        py = (
            py[0] * matrix[0][0] + py[1] * matrix[1][0],
            py[0] * matrix[0][1] + py[1] * matrix[1][1],
        )
    drift = (px[0] * x0[0] + px[1] * x0[1], py[0] * x0[0] + py[1] * x0[1])
    return columns, drift


def evaluate_dynamics(dynamics, controls, disturbance_radius):
    """Unpinned arithmetic helper, NOT input/certificate validation; used for sensitivity tests."""
    matrix = [[_number(v) for v in row] for row in dynamics["A"]]
    b, e, x0 = ([_number(v) for v in dynamics[key]] for key in ("B", "E", "x0"))
    horizon = dynamics["horizon"]
    if len(controls) != horizon:
        raise CheckError("Control vector must cover the full chronological horizon")
    columns, drift = _effects(matrix, b, x0, horizon)
    # Disturbance support uses E independently; equality E=B is never substituted.
    disturbance_columns, _ = _effects(matrix, e, (Fraction(0), Fraction(0)), horizon)
    support = tuple(
        disturbance_radius * sum((abs(v[j]) for v in disturbance_columns), Fraction(0))
        for j in range(2)
    )
    x, y = x0
    for control in controls:
        x, y = (
            matrix[0][0] * x + matrix[0][1] * y + b[0] * control,
            matrix[1][0] * x + matrix[1][1] * y + b[1] * control,
        )
    expanded = tuple(
        drift[j] + sum((v[j] * u for v, u in zip(columns, controls, strict=True)), Fraction(0))
        for j in range(2)
    )
    if (x, y) != expanded:
        raise CheckError("Chronological replay disagrees with backward adjoint expansion")
    return {
        "columns": columns,
        "drift": drift,
        "support": support,
        "nominal": (x, y),
        "reward": y - support[1],
    }


def check_certificate(manifest, certificate):
    digest = validate_input(manifest)
    _fields(certificate, CERTIFICATE_FIELDS, "certificate")
    expected = {
        "schema_version": 1,
        "certificate_type": "a4_open_loop_primal_dual",
        "coefficient_set_id": manifest["coefficient_set_id"],
        "input_sha256": digest,
        "scope": "a4_example_1_open_loop_rectangular_disturbances_exact_rational",
        "method": "forward_power_columns_fractional_cost_adjustment_v1",
        "coverage": "all_120_controls_and_all_independent_continuous_box_disturbances",
        "arithmetic": "exact_rational",
    }
    for key, value in expected.items():
        if type(certificate[key]) is not type(value) or certificate[key] != value:
            raise CheckError(f"Certificate binding mismatch: {key}")
    _fields(certificate["support"], {"x", "y"}, "support")
    _fields(certificate["multipliers"], {"lower", "upper"}, "multipliers")
    if not isinstance(certificate["controls"], list) or len(certificate["controls"]) != 120:
        raise CheckError("Expected 120 controls in chronological order")
    controls = [_number(value) for value in certificate["controls"]]
    bound = _number(manifest["constraints"]["control_abs_bound"])
    if any(abs(u) > bound for u in controls):
        raise CheckError("Control box bound violated")
    lower_multiplier = _number(certificate["multipliers"]["lower"])
    upper_multiplier = _number(certificate["multipliers"]["upper"])
    if lower_multiplier < 0 or upper_multiplier < 0:
        raise CheckError("Terminal slab dual multipliers must be nonnegative")
    computed = evaluate_dynamics(
        manifest["dynamics"], controls, _number(manifest["constraints"]["disturbance_abs_bound"])
    )
    sx, sy = computed["support"]
    if (_number(certificate["support"]["x"]), _number(certificate["support"]["y"])) != (sx, sy):
        raise CheckError("Disturbance support mismatch")
    low, high = map(_number, manifest["constraints"]["terminal_x_interval"])
    x, y = computed["nominal"]
    if x - sx < low:
        raise CheckError("Robust lower terminal bound violated")
    if x + sx > high:
        raise CheckError("Robust upper terminal bound violated")
    dx, dy = computed["drift"]
    # For feasible u, add lambda*(x-L)+mu*(H-x) >= 0 to its reward.
    # Maximizing this affine expression on |u_t|<=bound gives the box support below.
    dual = (
        dy
        - sy
        + lower_multiplier * (dx - low - sx)
        + upper_multiplier * (high - sx - dx)
        + bound
        * sum(
            (
                abs(cy + (lower_multiplier - upper_multiplier) * cx)
                for cx, cy in computed["columns"]
            ),
            Fraction(0),
        )
    )
    reward = computed["reward"]
    if _number(certificate["objective"]) != reward:
        raise CheckError("Claimed objective differs from chronological replay reward")
    if reward != dual:
        raise CheckError("Exact primal reward does not equal the valid dual upper bound")
    return {
        "schema_version": 1,
        "certificate_validity": "valid",
        "input_sha256": digest,
        "coefficient_set_id": manifest["coefficient_set_id"],
        "scope": expected["scope"],
        "coverage": expected["coverage"],
        "arithmetic": "exact_rational",
        "numerical_input_validity": "pinned_manifest_match",
        "source_page_verification": "not_performed_by_numeric_checker",
        "exact_reward": _rtext(reward),
        "dual_upper_bound": _rtext(dual),
        "nominal_terminal": [_rtext(x), _rtext(y)],
        "robust_terminal_x": [_rtext(x - sx), _rtext(x + sx)],
        "support": {"x": _rtext(sx), "y": _rtext(sy)},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--certificate", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = parse_json(args.input.read_text(encoding="utf-8"))
        certificate = parse_json(args.certificate.read_text(encoding="utf-8"))
        result = check_certificate(manifest, certificate)
        output = canonical_json(result)
    except (OSError, ValueError, TypeError, RecursionError) as error:
        print(f"a4_check: {error}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
