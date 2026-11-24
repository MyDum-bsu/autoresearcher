"""Closed offline contracts. Text explains decisions; it never defines predicates."""

import hashlib
import json
import re
from dataclasses import asdict, dataclass, fields
from typing import Literal


class ContractError(ValueError):
    """Invalid or unsupported offline submission."""


def require(condition, message):
    if not condition:
        raise ContractError(message)


def canonical(data):
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


def digest(data):
    return hashlib.sha256(canonical(data).encode()).hexdigest()


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_number(value):
    raise ContractError(f"noninteger JSON number: {value}")


def decode(text):
    try:
        return json.loads(
            text,
            object_pairs_hook=object_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (ValueError, RecursionError) as error:
        raise ContractError(f"invalid JSON: {error}") from error


def closed(data, names):
    require(
        type(data) is dict and set(data) == set(names), f"expected exactly fields: {sorted(names)}"
    )
    return data


def text(value):
    require(type(value) is str and bool(value.strip()), "expected nonempty text")
    return value


def texts(value):
    require(type(value) is list, "expected text array")
    result = tuple(text(item) for item in value)
    require(len(set(result)) == len(result), "duplicate array entry")
    return result


def identifier(value):
    require(
        type(value) is str and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}", value),
        "invalid identifier: expected 1..128 ASCII letters/digits/_.:-, starting alphanumeric",
    )
    return value


def identifiers(value):
    return tuple(identifier(item) for item in texts(value))


def sha256(value):
    require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "invalid SHA-256")
    return value


def positive(value):
    require(type(value) is int and value > 0, "expected positive integer, not boolean")
    return value


@dataclass(frozen=True)
class Scope:
    model: Literal["m0-two-period-v1"]
    relation: Literal["equal-values"]
    modes: tuple[str, ...]
    restriction: Literal["all", "nonzero-prefix-gain"]


@dataclass(frozen=True)
class Case:
    id: str
    normalized_input_sha256: str


@dataclass(frozen=True)
class Claim:
    id: str
    version: int
    parent: str | None
    scope: Scope
    cases: tuple[Case, ...]
    statement: str

    @property
    def identity(self):
        return digest(asdict(self))


@dataclass(frozen=True)
class Instance:
    id: str
    normalized_json: str


@dataclass(frozen=True)
class Evidence:
    id: str
    claim: str
    claim_sha256: str
    instance: str
    checker_sha256: str
    certificates: tuple[str, ...]


@dataclass(frozen=True)
class Action:
    id: str
    claim: str
    claim_sha256: str
    operation: Literal["finite-compare"]
    prerequisites: tuple[str, ...]
    uncertainty: str
    rationale: str
    positive: str
    negative: str
    inconclusive: str
    exclusions: tuple[str, ...]
    max_cases: int
    wall_seconds: int


@dataclass(frozen=True)
class Attempt:
    id: str
    action: str
    outcome: Literal["completed", "inconclusive", "failed", "cancelled", "budget-exhausted"]
    evidence: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class Submission:
    schema_version: int
    claims: tuple[Claim, ...]
    instances: tuple[Instance, ...]
    evidence: tuple[Evidence, ...]
    actions: tuple[Action, ...]
    attempts: tuple[Attempt, ...]


def record(data, cls):
    return closed(data, (field.name for field in fields(cls)))


def parse_scope(data):
    record(data, Scope)
    require(data["model"] == "m0-two-period-v1", "unsupported model scope")
    require(data["relation"] == "equal-values", "unsupported relation")
    require(data["modes"] == ["state", "prefix"], "unsupported observation semantics")
    require(data["restriction"] in ("all", "nonzero-prefix-gain"), "unsupported premise")
    return Scope(data["model"], data["relation"], tuple(data["modes"]), data["restriction"])


def parse_claim(data):
    record(data, Claim)
    parent = data["parent"]
    if parent is not None:
        identifier(parent)
    require(type(data["cases"]) is list and data["cases"], "empty/invalid test inventory")
    cases = []
    for item in data["cases"]:
        record(item, Case)
        cases.append(Case(identifier(item["id"]), sha256(item["normalized_input_sha256"])))
    unique(cases)
    return Claim(
        identifier(data["id"]),
        positive(data["version"]),
        parent,
        parse_scope(data["scope"]),
        tuple(sorted(cases, key=lambda item: item.id)),
        text(data["statement"]),
    )


def parse_action(data):
    record(data, Action)
    require(data["operation"] == "finite-compare", "unsupported operation")
    require(
        len({text(data[key]) for key in ("positive", "negative", "inconclusive")}) == 3,
        "outcome consequences must differ",
    )
    values = dict(data)
    for key in ("id", "claim"):
        values[key] = identifier(data[key])
    values["claim_sha256"] = sha256(data["claim_sha256"])
    for key in ("uncertainty", "rationale"):
        values[key] = text(data[key])
    for key in ("prerequisites", "exclusions"):
        values[key] = identifiers(data[key]) if key == "prerequisites" else texts(data[key])
        require(values[key], f"missing {key}")
    for key in ("max_cases", "wall_seconds"):
        values[key] = positive(data[key])
    require(
        values["max_cases"] <= 8 and values["wall_seconds"] <= 120, "unsupported resource limits"
    )
    return Action(**values)


def parse_evidence(data):
    record(data, Evidence)
    values = {key: identifier(data[key]) for key in ("id", "claim", "instance")}
    for key in ("claim_sha256", "checker_sha256"):
        values[key] = sha256(data[key])
    require(
        type(data["certificates"]) is list and len(data["certificates"]) == 2,
        "expected state and prefix certificates",
    )
    for item in data["certificates"]:
        require(type(item) is dict and "instance_id" in item, "missing certificate instance ID")
        identifier(item["instance_id"])
    return Evidence(**values, certificates=tuple(canonical(item) for item in data["certificates"]))


def parse_attempt(data):
    record(data, Attempt)
    require(
        data["outcome"] in ("completed", "inconclusive", "failed", "cancelled", "budget-exhausted"),
        "unknown operational outcome",
    )
    return Attempt(
        identifier(data["id"]),
        identifier(data["action"]),
        data["outcome"],
        identifiers(data["evidence"]),
        text(data["reason"]),
    )


def unique(records):
    result = {item.id: item for item in records}
    require(len(result) == len(records), "duplicate record ID")
    return result


def parse(text_input):
    # The checker owns all finite arithmetic and finite input limits.
    from pilot.checkers.finite_bellman import validate_instance

    data = record(decode(text_input), Submission)
    require(
        type(data["schema_version"]) is int and data["schema_version"] == 2,
        "invalid schema version",
    )
    for key in ("claims", "instances", "evidence", "actions", "attempts"):
        require(type(data[key]) is list and data[key], f"missing {key}")
    for item in data["instances"]:
        require(type(item) is dict and "instance_id" in item, "missing instance ID")
        identifier(item["instance_id"])
    instances = tuple(validate_instance(item) for item in data["instances"])
    submission = Submission(
        2,
        tuple(map(parse_claim, data["claims"])),
        tuple(Instance(identifier(item["instance_id"]), canonical(item)) for item in instances),
        tuple(map(parse_evidence, data["evidence"])),
        tuple(map(parse_action, data["actions"])),
        tuple(map(parse_attempt, data["attempts"])),
    )
    unique(
        submission.claims
        + submission.instances
        + submission.evidence
        + submission.actions
        + submission.attempts
    )
    return submission
