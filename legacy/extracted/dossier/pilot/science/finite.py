"""Small trusted adapter to the imported independent checker, never submitted code."""

import hashlib
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from pilot.checkers import finite_bellman
from pilot.science.contracts import decode, require

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_SHA256 = "e9b141955d00fb0bc68a9bff1869fdcd2b65ef519f12c41a4a82b36d6a92d71f"
CHECKER_SHA256 = "e041bb9bc99eb72ec7b29f5821d798b43179a62db6f8d9c8d96ac897780b8523"


def snapshot_integrity():
    path = ROOT / "artifacts/research-pilot-m0/finite-snapshot.json"
    require(
        hashlib.sha256(path.read_bytes()).hexdigest() == SNAPSHOT_SHA256,
        "snapshot identity changed",
    )
    snapshot = decode(path.read_text())
    for name, entry in snapshot["files"].items():
        require(
            hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == entry["sha256"],
            f"baseline integrity mismatch: {name}",
        )


@dataclass(frozen=True)
class CheckedEvidence:
    id: str
    claim: str
    claim_sha256: str
    instance: str
    normalized_input_sha256: str
    checker_sha256: str
    modes: tuple[str, ...]
    values: tuple[str, ...]
    conclusion: str


def check(evidence, claim, instance):
    require(evidence.claim_sha256 == claim.identity, "stale claim identity")
    require(evidence.checker_sha256 == CHECKER_SHA256, "wrong checker identity")
    data = decode(instance.normalized_json)
    if claim.scope.restriction == "nonzero-prefix-gain":
        require(Fraction(data["prefix_gain"]) != 0, "counterexample/test outside claim premises")
    results = []
    for mode, certificate in zip(claim.scope.modes, evidence.certificates, strict=True):
        result = finite_bellman.check_result(data, mode, decode(certificate))
        require(
            result["result"] == "optimal", "numeric equality does not support typed infeasibility"
        )
        results.append(result)
    values = tuple(item["value"] for item in results)
    conclusion = (
        "holds-on-instance"
        if Fraction(values[0]) == Fraction(values[1])
        else "checked-counterexample"
    )
    return CheckedEvidence(
        evidence.id,
        claim.id,
        claim.identity,
        instance.id,
        results[0]["normalized_input_sha256"],
        CHECKER_SHA256,
        claim.scope.modes,
        values,
        conclusion,
    )
