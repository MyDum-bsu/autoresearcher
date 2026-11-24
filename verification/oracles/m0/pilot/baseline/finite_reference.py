"""Offline exact finite policy enumeration; not an approved scientific judge."""

import argparse
import hashlib
import itertools
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

MODES = ("open", "state", "prefix")
FIELDS = {
    "schema_version",
    "instance_id",
    "first_actions",
    "second_actions",
    "paths",
    "prefix_gain",
    "terminal_interval",
}


class ReferenceError(ValueError):
    def __init__(self, message, code="invalid_input"):
        super().__init__(f"{code}: {message}")
        self.code = code


def _require(condition, message, code="invalid_input"):
    if not condition:
        raise ReferenceError(message, code)


def _rational(text, bounded=False):
    _require(
        isinstance(text, str) and re.fullmatch(r"-?(0|[1-9][0-9]*)/[1-9][0-9]*", text),
        "expected canonical rational n/d",
    )
    if bounded:
        numerator, denominator = text.split("/")
        _require(
            len(numerator.lstrip("-")) <= 4 and len(denominator) <= 4,
            "rational exceeds numerator/denominator limits",
            "unsupported_scope",
        )
    try:
        value = Fraction(text)
    except ValueError as error:
        raise ReferenceError("invalid rational integer") from error
    _require(text == _text(value), "rational must be reduced; zero must be 0/1")
    if bounded:
        _require(
            abs(value.numerator) <= 1000 and value.denominator <= 1000,
            "rational exceeds numerator/denominator limits",
            "unsupported_scope",
        )
    return value


def _text(value):
    return f"{value.numerator}/{value.denominator}"


def canonical_json(data):
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _no_float(text):
    raise ReferenceError(f"noninteger JSON number is forbidden: {text}")


def parse_instance(text):
    """Decode strict JSON and return a normalized, validated JSON-shaped instance."""
    _require(isinstance(text, str), "JSON input must be text")
    try:
        data = json.loads(
            text, object_pairs_hook=_object, parse_float=_no_float, parse_constant=_no_float
        )
    except (ValueError, RecursionError) as error:
        if isinstance(error, ReferenceError):
            raise
        raise ReferenceError("malformed JSON") from error
    return validate_instance(data)


def validate_instance(data):
    """Validate closed schema and reference limits; sort arrays by rational value."""
    _require(type(data) is dict and set(data) == FIELDS, "expected exactly the instance fields")
    _require(
        type(data["schema_version"]) is int and data["schema_version"] == 1,
        "unsupported schema_version",
    )
    _require(
        isinstance(data["instance_id"], str) and bool(data["instance_id"]),
        "instance_id must be nonempty text",
    )
    normalized = dict(data)
    for field, limit in (("first_actions", 5), ("second_actions", 5), ("paths", 8)):
        array = data[field]
        _require(type(array) is list and bool(array), f"{field} must be a nonempty array")
        _require(len(array) <= limit, f"{field} exceeds {limit}", "unsupported_scope")
        if field == "paths":
            _require(all(type(p) is list and len(p) == 2 for p in array), "paths must be pairs")
            values = [tuple(_rational(x, True) for x in p) for p in array]
            normalized[field] = [[_text(x) for x in p] for p in sorted(values)]
        else:
            values = [_rational(x, True) for x in array]
            normalized[field] = [_text(x) for x in sorted(values)]
        _require(len(set(values)) == len(values), f"repeated element in {field}")
    _rational(data["prefix_gain"], True)
    interval = data["terminal_interval"]
    if interval is not None:
        _require(
            type(interval) is list and len(interval) == 2,
            "terminal_interval must be null or a pair",
        )
        lower, upper = (_rational(x, True) for x in interval)
        _require(lower <= upper, "inverted terminal interval")
        normalized["terminal_interval"] = list(interval)
    return normalized


def _cells(data, mode, first):
    _require(mode in MODES, "unknown information mode")
    gain = Fraction(data["prefix_gain"])
    keys = [
        "open"
        if mode == "open"
        else (Fraction(p) if mode == "prefix" else first + gain * Fraction(p))
        for p, q in data["paths"]
    ]
    return sorted(set(keys)), keys


def _outcomes(data, first, keys, actions):
    outcomes = []
    interval = data["terminal_interval"]
    for path, key in zip(data["paths"], keys, strict=True):
        p, q = map(Fraction, path)
        x1 = first + Fraction(data["prefix_gain"]) * p
        x2 = x1 + actions[key] + q
        if interval is not None and not Fraction(interval[0]) <= x2 <= Fraction(interval[1]):
            return None
        outcomes.append(
            {"path": list(path), "x1": _text(x1), "x2": _text(x2), "cost": _text(abs(x2))}
        )
    return outcomes


def _result(data, mode, first=None, actions=None, outcomes=None):
    return {
        "schema_version": 1,
        "instance_id": data["instance_id"],
        "information": mode,
        "normalized_input_sha256": hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest(),
        "result": "infeasible" if first is None else "optimal",
        "value": None if outcomes is None else _text(max(Fraction(o["cost"]) for o in outcomes)),
        "first_action": None if first is None else _text(first),
        "policy": []
        if actions is None
        else [[k if k == "open" else _text(k), _text(v)] for k, v in actions.items()],
        "outcomes": [] if outcomes is None else outcomes,
    }


def solve(instance, information):
    """Exhaust all finite policies. Equal values retain the first canonical policy."""
    data = validate_instance(instance)
    _require(information in MODES, "unknown information mode")
    best, best_value = _result(data, information), None
    for first in map(Fraction, data["first_actions"]):
        cells, keys = _cells(data, information, first)
        for choices in itertools.product(map(Fraction, data["second_actions"]), repeat=len(cells)):
            actions = dict(zip(cells, choices, strict=True))
            outcomes = _outcomes(data, first, keys, actions)
            if outcomes is not None:
                value = max(Fraction(o["cost"]) for o in outcomes)
                if best_value is None or value < best_value:
                    best, best_value = _result(data, information, first, actions, outcomes), value
    return best


def replay(instance, information, witness):
    """Validate a feasible result-shaped witness, not its claimed optimality."""
    data = validate_instance(instance)
    _require(
        type(witness) is dict and witness.get("information") == information,
        "information-mode mismatch",
    )
    first = _rational(witness.get("first_action"))
    _require(_text(first) in data["first_actions"], "first action outside allowed set")
    cells, keys = _cells(data, information, first)
    policy = witness.get("policy")
    _require(
        type(policy) is list and all(type(pair) is list and len(pair) == 2 for pair in policy),
        "invalid policy pairs",
    )
    labels = [key if key == "open" else _text(key) for key in cells]
    _require(
        [pair[0] for pair in policy] == labels,
        "policy must cover exactly the sorted reachable cells",
    )
    actions = {key: _rational(pair[1]) for key, pair in zip(cells, policy, strict=True)}
    _require(
        all(_text(v) in data["second_actions"] for v in actions.values()),
        "second action outside allowed set",
    )
    outcomes = _outcomes(data, first, keys, actions)
    _require(outcomes is not None, "witness violates terminal interval")
    expected = _result(data, information, first, actions, outcomes)
    _require(
        canonical_json(witness) == canonical_json(expected),
        "witness metadata/value/outcomes mismatch",
    )
    return expected


def public_fixtures():
    """Public inputs only; every result is computed by solve."""
    actions = ["-1/1", "0/1", "1/1"]
    cases = {}
    for name in (
        "strict_gain",
        "correlated_hidden_disturbance",
        "independent_hidden_disturbance",
        "terminal_feasibility",
    ):
        hidden = "hidden" in name
        paths = [["-1/1", "-1/1"], ["1/1", "1/1"]] if hidden else [["-1/1", "0/1"], ["1/1", "0/1"]]
        if name == "independent_hidden_disturbance":
            paths = [list(p) for p in itertools.product(["-1/1", "1/1"], repeat=2)]
        cases[name] = {
            "schema_version": 1,
            "instance_id": name,
            "first_actions": ["0/1"] if hidden else list(actions),
            "second_actions": list(actions),
            "paths": paths,
            "prefix_gain": "0/1" if hidden else "1/1",
            "terminal_interval": ["0/1", "0/1"] if name == "terminal_feasibility" else None,
        }
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--public-fixtures", action="store_true")
    group.add_argument("--input")
    parser.add_argument("--information", choices=MODES)
    args = parser.parse_args()
    if (args.input is not None) != (args.information is not None):
        parser.error("--input requires --information; --public-fixtures takes neither")
    try:
        if args.public_fixtures:
            result = {
                "schema_version": 1,
                "cases": {
                    name: {mode: solve(data, mode) for mode in MODES}
                    for name, data in public_fixtures().items()
                },
            }
        else:
            with Path(args.input).open(encoding="utf-8") as source:
                result = solve(parse_instance(source.read()), args.information)
        print(canonical_json(result))
    except (ReferenceError, OSError, UnicodeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
