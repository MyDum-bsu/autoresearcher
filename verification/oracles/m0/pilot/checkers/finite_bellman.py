"""Independent exact finite Bellman solver and P1 witness checker (stdlib only)."""

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path


class CheckerError(ValueError):
    """An explicit validation error, never mathematical infeasibility."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


INPUT_FIELDS = {
    "schema_version",
    "instance_id",
    "first_actions",
    "second_actions",
    "paths",
    "prefix_gain",
    "terminal_interval",
}
RESULT_FIELDS = {
    "schema_version",
    "instance_id",
    "information",
    "normalized_input_sha256",
    "result",
    "value",
    "first_action",
    "policy",
    "outcomes",
}
MODES = ("open", "state", "prefix")
RATIONAL = re.compile(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)/[1-9][0-9]*", re.ASCII)


def canonical_json(data):
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


def _text(value):
    return f"{value.numerator}/{value.denominator}"


def _rational(value, *, bounded=True, code="invalid_input"):
    if not isinstance(value, str) or RATIONAL.fullmatch(value) is None:
        raise CheckerError(code, "Expected a canonical rational string")
    numerator, denominator = value.split("/")
    if bounded and (len(numerator.lstrip("-")) > 4 or len(denominator) > 4):
        raise CheckerError("unsupported_scope", "Input rational exceeds 1000 limit")
    try:
        number = Fraction(value)
    except ValueError as error:
        raise CheckerError(code, "Rational exceeds integer parsing capacity") from error
    if _text(number) != value:
        raise CheckerError(code, "Rational must be reduced")
    if bounded and (abs(number.numerator) > 1000 or number.denominator > 1000):
        raise CheckerError("unsupported_scope", "Input rational exceeds 1000 limit")
    return number


def _fields(data, fields, code):
    if not isinstance(data, dict) or data.keys() != fields:
        raise CheckerError(code, "Missing or unknown fields")


def _array(data, cap):
    if not isinstance(data, list) or not data:
        raise CheckerError("invalid_input", "Expected a nonempty array")
    if len(data) > cap:
        raise CheckerError("unsupported_scope", "Input set exceeds finite size limit")


def validate_instance(data):
    """Independently validate and normalize the documented P1 input contract."""
    _fields(data, INPUT_FIELDS, "invalid_input")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise CheckerError("invalid_input", "Expected schema_version integer 1")
    if not isinstance(data["instance_id"], str) or not data["instance_id"]:
        raise CheckerError("invalid_input", "Expected nonempty instance_id")
    normalized = {"schema_version": 1, "instance_id": data["instance_id"]}
    for field in ("first_actions", "second_actions"):
        _array(data[field], 5)
        numbers = [_rational(item) for item in data[field]]
        if len(set(numbers)) != len(numbers):
            raise CheckerError("invalid_input", "Duplicate actions")
        normalized[field] = [_text(number) for number in sorted(numbers)]
    _array(data["paths"], 8)
    paths = []
    for pair in data["paths"]:
        if not isinstance(pair, list) or len(pair) != 2:
            raise CheckerError("invalid_input", "Each path must be a pair")
        paths.append(tuple(_rational(item) for item in pair))
    if len(set(paths)) != len(paths):
        raise CheckerError("invalid_input", "Duplicate paths")
    normalized["paths"] = [[_text(p), _text(q)] for p, q in sorted(paths)]
    normalized["prefix_gain"] = _text(_rational(data["prefix_gain"]))
    interval = data["terminal_interval"]
    if interval is not None:
        if not isinstance(interval, list) or len(interval) != 2:
            raise CheckerError("invalid_input", "Expected null or a terminal interval pair")
        lower, upper = (_rational(item) for item in interval)
        if lower > upper:
            raise CheckerError("invalid_input", "Reversed terminal interval")
        interval = [_text(lower), _text(upper)]
    normalized["terminal_interval"] = interval
    return normalized


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CheckerError("invalid_input", "Duplicate JSON key")
        result[key] = value
    return result


def _reject_number(_value):
    raise CheckerError("invalid_input", "Noninteger JSON number is forbidden")


def parse_instance(text):
    try:
        data = json.loads(
            text,
            object_pairs_hook=_json_object,
            parse_float=_reject_number,
            parse_constant=_reject_number,
        )
    except CheckerError:
        raise
    except json.JSONDecodeError as error:
        raise CheckerError("invalid_input", f"Invalid JSON: {error.msg}") from error
    except (ValueError, RecursionError) as error:
        raise CheckerError("invalid_input", f"Invalid JSON: {error}") from error
    return validate_instance(data)


def _mode(information):
    if information not in MODES:
        raise CheckerError("invalid_input", "Expected information open, state or prefix")


def _record(data, information):
    return {
        "schema_version": 1,
        "instance_id": data["instance_id"],
        "information": information,
        "normalized_input_sha256": hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest(),
        "result": "infeasible",
        "value": None,
        "first_action": None,
        "policy": [],
        "outcomes": [],
    }


def solve(instance, information):
    """Min_a max_cell min_b max_path; no enumeration of full policies."""
    data = validate_instance(instance)
    _mode(information)
    result = _record(data, information)
    paths = [tuple(Fraction(item) for item in pair) for pair in data["paths"]]
    gain = Fraction(data["prefix_gain"])
    terminal = data["terminal_interval"]
    bounds = None if terminal is None else tuple(Fraction(item) for item in terminal)
    best_value = None
    for first in map(Fraction, data["first_actions"]):
        groups = {}
        for p, q in paths:
            state = first + gain * p
            observation = (
                None if information == "open" else (state if information == "state" else p)
            )
            groups.setdefault(observation, []).append((state, q))
        policy = []
        cell_values = []
        for observation in sorted(groups):
            candidates = []
            for second in map(Fraction, data["second_actions"]):
                terminals = [state + second + q for state, q in groups[observation]]
                if bounds is not None and any(
                    end < bounds[0] or end > bounds[1] for end in terminals
                ):
                    continue
                candidates.append((max(abs(end) for end in terminals), second))
            if not candidates:
                break  # This first action cannot cover a reachable cell.
            value, second = min(candidates)
            cell_values.append(value)
            policy.append(["open" if observation is None else _text(observation), _text(second)])
        else:
            value = max(cell_values)
            if best_value is not None and value >= best_value:
                continue
            best_value = value
            assignments = {key: Fraction(action) for key, action in policy}
            outcomes = []
            for p, q in paths:
                state = first + gain * p
                key = (
                    "open"
                    if information == "open"
                    else _text(state if information == "state" else p)
                )
                end = state + assignments[key] + q
                outcomes.append(
                    {
                        "path": [_text(p), _text(q)],
                        "x1": _text(state),
                        "x2": _text(end),
                        "cost": _text(abs(end)),
                    }
                )
            result.update(
                result="optimal",
                value=_text(value),
                first_action=_text(first),
                policy=policy,
                outcomes=outcomes,
            )
    return result


def check_witness(instance, information, witness):
    """Replay a full feasible P1 record; do not certify its optimality label."""
    data = validate_instance(instance)
    _mode(information)
    code = "invalid_witness"
    _fields(witness, RESULT_FIELDS, code)
    expected = _record(data, information)
    for field in ("schema_version", "instance_id", "information", "normalized_input_sha256"):
        if type(witness[field]) is not type(expected[field]) or witness[field] != expected[field]:
            raise CheckerError(code, f"Witness metadata mismatch: {field}")
    if witness["result"] != "optimal":
        raise CheckerError(code, "Replay requires a feasible optimal-shaped witness")
    first = _rational(witness["first_action"], bounded=False, code=code)
    if _text(first) not in data["first_actions"]:
        raise CheckerError(code, "Disallowed first action")
    _rational(witness["value"], bounded=False, code=code)
    if not isinstance(witness["policy"], list):
        raise CheckerError(code, "Expected policy array")
    actions = {}
    ordered_keys = []
    for entry in witness["policy"]:
        if not isinstance(entry, list) or len(entry) != 2:
            raise CheckerError(code, "Expected observation/action pair")
        key, action = entry
        if information == "open":
            if key != "open":
                raise CheckerError(code, "Open policy must have only the open key")
            order_key = "open"
        else:
            order_key = _rational(key, bounded=False, code=code)
        second = _rational(action, bounded=False, code=code)
        if action not in data["second_actions"]:
            raise CheckerError(code, "Disallowed second action")
        if key in actions:
            raise CheckerError(code, "Duplicate observation cell")
        actions[key] = second
        ordered_keys.append(order_key)
    if ordered_keys != sorted(ordered_keys):
        raise CheckerError(code, "Policy cells must be numerically sorted")
    gain = Fraction(data["prefix_gain"])
    terminal = data["terminal_interval"]
    bounds = None if terminal is None else [Fraction(item) for item in terminal]
    reached = set()
    outcomes = []
    costs = []
    for pair in data["paths"]:
        p, q = map(Fraction, pair)
        measured = first + gain * p
        if information == "state":
            key = _text(measured)
        elif information == "prefix":
            key = _text(p)
        else:
            key = "open"
        reached.add(key)
        if key not in actions:
            raise CheckerError(code, "Missing reachable observation cell")
        end = measured + actions[key] + q
        if bounds is not None and not bounds[0] <= end <= bounds[1]:
            raise CheckerError(code, "Hard terminal interval violated")
        costs.append(abs(end))
        outcomes.append(
            {"path": list(pair), "x1": _text(measured), "x2": _text(end), "cost": _text(abs(end))}
        )
    if set(actions) != reached:
        raise CheckerError(code, "Extra observation cells")
    expected.update(
        result="optimal",
        value=_text(max(costs)),
        first_action=_text(first),
        policy=witness["policy"],
        outcomes=outcomes,
    )
    if witness != expected:
        raise CheckerError(code, "Incorrect exact value or per-path outcomes")
    return expected


def check_result(instance, information, result):
    """Replay feasible certificates and independently certify the Bellman value."""
    optimum = solve(instance, information)
    if isinstance(result, dict) and result.get("result") == "optimal":
        replayed = check_witness(instance, information, result)
        if optimum["result"] != "optimal" or replayed["value"] != optimum["value"]:
            raise CheckerError("invalid_witness", "Witness is feasible but not optimal")
        return replayed
    _fields(result, RESULT_FIELDS, "invalid_witness")
    if type(result["schema_version"]) is not int or result != optimum:
        raise CheckerError("invalid_witness", "Incorrect infeasibility record")
    return optimum


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--information", required=True, choices=MODES)
    args = parser.parse_args(argv)
    try:
        instance = parse_instance(args.input.read_text(encoding="utf-8"))
        result = solve(instance, args.information)
    except (OSError, UnicodeError, CheckerError) as error:
        code = error.code if isinstance(error, CheckerError) else "input_io_error"
        print(f"{code}: {error}", file=sys.stderr)
        return 2
    print(canonical_json(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
