"""Read-only exact ARO row interpretation of frozen wave-4 certificates (v2 layout)."""
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.set_int_max_str_digits(20000)
ROOT = Path(__file__).resolve().parents[3]
WAVE4_DIR = ROOT / "verification/oracles/wave4-a4-closures"
CERT_DIR = WAVE4_DIR / "certificates"
INPUTS_DIR = ROOT / "verification/oracles/m0/pilot/inputs"
CONTRACT_PATH = Path(__file__).resolve().parent / "case-contract.json"

sys.path.insert(0, str(WAVE4_DIR))
spec = importlib.util.spec_from_file_location("wave4_check", WAVE4_DIR / "check.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


class _V2LegacyRoot:
    """Read-only path adapter for frozen wave-4/check.py without altering its SHA-256."""

    _MAP = {
        "goal/wave-4/contract.json": WAVE4_DIR / "contract.json",
        "research/sources/A4.pdf": ROOT / "corpus/our_papers/A4_Дмитрук_2022.pdf",
    }

    def __truediv__(self, rel: str) -> Path:
        if rel in self._MAP:
            return self._MAP[rel]
        raise FileNotFoundError(f"Unmapped legacy wave-4 path: {rel}")


legacy.ROOT = _V2LegacyRoot()

# Mapping from frozen historical campaign paths in case-contract.json to v2/clean-base paths
V2_FROZEN_INPUTS = {
    "artifacts/goal/wave-4/pilot/a4_printed-r67/certificate.json": CERT_DIR / "a4_printed-r67/certificate.json",
    "artifacts/goal/wave-4/pilot/a4_reconstructed_decimal-r67/certificate.json": CERT_DIR / "a4_reconstructed_decimal-r67/certificate.json",
    "artifacts/goal/wave-4/pilot/a4_printed-r104/certificate.json": CERT_DIR / "a4_printed-r104/certificate.json",
    "artifacts/goal/wave-4/pilot/a4_reconstructed_decimal-r104/certificate.json": CERT_DIR / "a4_reconstructed_decimal-r104/certificate.json",
    "artifacts/goal/wave-4/pilot/inputs/a4_printed.json": INPUTS_DIR / "a4_printed.json",
    "artifacts/goal/wave-4/pilot/inputs/a4_reconstructed_decimal.json": INPUTS_DIR / "a4_reconstructed_decimal.json",
    "goal/wave-4/check.py": WAVE4_DIR / "check.py",
    "goal/wave-4/m0_check.py": WAVE4_DIR / "m0_check.py",
    "goal/wave-4/contract.json": WAVE4_DIR / "contract.json",
}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ft(x):
    return str(x.numerator) + "/" + str(x.denominator)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), F(0))


def mv(A, v):
    return tuple(dot(row, v) for row in A)


def add(*vs):
    return tuple(sum(col, F(0)) for col in zip(*vs, strict=True))


def chronological_columns(A, B, E, x0, T):
    # Impulse propagation, not the reused backward-adjoint effects builder.
    C, D = [], []
    for t in range(T):
        b, e = tuple(B), tuple(E)
        for _ in range(T - 1 - t):
            b, e = mv(A, b), mv(A, e)
        C.append(b)
        D.append(e)
    d = tuple(x0)
    for _ in range(T):
        d = mv(A, d)
    return C, D, d


def fibre_check(records):
    seen = {}
    for state, future, block in records:
        key = tuple(state)
        value = tuple(block)
        require(
            key not in seen or seen[key] == value,
            "same observed state received different whole suffix blocks",
        )
        seen[key] = value
    # Future coordinates are intentionally not part of the information key.


def rejected(name, action):
    try:
        action()
    except ValueError as exc:
        return {"control": name, "observation": "rejected", "reason": str(exc)}
    raise ValueError("invalid control accepted: " + name)


def check_case(case):
    cert = load(CERT_DIR / case / "certificate.json")
    manifest = load(INPUTS_DIR / (case.rsplit("-r", 1)[0] + ".json"))
    original = legacy.check(manifest, cert)
    A = [list(map(F, row)) for row in manifest["dynamics"]["A"]]
    B, E, x0 = (list(map(F, manifest["dynamics"][k])) for k in ("B", "E", "x0"))
    a = list(map(F, cert["first_block"]))
    r, T = cert["r"], 120
    C, D, d = chronological_columns(A, B, E, x0, T)
    V = [tuple(map(F, v)) for v in cert["vertices"]]
    blocks = [list(map(F, b)) for b in cert["suffix_blocks"]]
    sx, sy = (sum((abs(v[j]) / 2 for v in D[r:]), F(0)) for j in range(2))
    base = add(
        d,
        tuple(sum((v[j] * u for v, u in zip(C[:r], a, strict=True)), F(0)) for j in range(2)),
    )
    q = F(cert["lower"])
    residuals = []
    nominals = []
    for v, b in zip(V, blocks, strict=True):
        h = add(
            base,
            v,
            tuple(sum((cc[j] * u for cc, u in zip(C[r:], b, strict=True)), F(0)) for j in range(2)),
        )
        nominals.append(h)
        # Standard ARO <=0 rows, signed cost c=-e2 and eta=-q.
        residuals.append((-h[0] + sx + 2, h[0] + sx - 10, -h[1] + sy + q))
    require(max(max(row) for row in residuals) <= 0, "standard ARO robust row violated")
    require(min(h[1] - sy for h in nominals) == q, "reward epigraph offset mismatch")
    bad_sign = lambda: require(
        max(h[1] + sy + q for h in nominals) <= 0,
        "signed objective row changed from -x2 to +x2",
    )
    bad_row = lambda: require(
        max(h[0] + sx + 2 for h in nominals) <= 0,
        "lower terminal row direction reversed",
    )
    controls = [
        {"control": "positive_mapping", "observation": "accepted"},
        {"control": "robust_terminal_and_signed_cost", "observation": "accepted"},
        rejected("cost_sign_error", bad_sign),
        rejected("terminal_row_error", bad_row),
    ]
    bad = copy.deepcopy(cert)
    bad["information"] = "suffix_disturbance_observed"
    controls.append(rejected("information_metadata_error", lambda: legacy.check(manifest, bad)))
    state = tuple(x0)
    for u in a:
        state = add(mv(A, state), tuple(x * u for x in B))
    future_minus = [F(-1, 2)] * (T - r)
    future_plus = [F(1, 2)] * (T - r)
    bminus = legacy.state_to_block(manifest, cert, state)
    bplus = legacy.state_to_block(manifest, cert, state)
    fibre_check([(state, future_minus, bminus), (state, future_plus, bplus)])
    controls.append({"control": "state_only_timing", "observation": "accepted"})
    # Explicit hostile table: same actual observation, different future, different control.
    hostile = list(bplus)
    hostile[0] = F(1) if bplus[0] != 1 else F(-1)
    controls.append(
        rejected(
            "future_information_semantic_error",
            lambda: fibre_check([(state, future_minus, bminus), (state, future_plus, hostile)]),
        )
    )
    # Replay the same entire valid suffix against two future paths; no later measurement.
    trajectories = []
    for future in (future_minus, future_plus):
        x = state
        for u, w in zip(bminus, future, strict=True):
            x = add(mv(A, x), tuple(v * u for v in B), tuple(v * w for v in E))
        require(2 <= x[0] <= 10 and x[1] >= q, "chronological terminal replay failed")
        trajectories.append([ft(z) for z in x])
    controls.append({"control": "chronological_replay", "observation": "accepted"})
    expected = load(CONTRACT_PATH)["controls"]
    require({c["control"]: c["observation"] for c in controls} == expected, "control inventory mismatch")
    N, k = len(V), T - r
    return {
        "case": case,
        "existing_certificate_check": original,
        "standard_aro": {
            "first_stage_variables": r + 1,
            "recourse_variables": N * k,
            "total_variables": r + 1 + N * k,
            "terminal_cost_rows": 3 * N,
            "box_rows": 2 * r + 2 * N * k,
            "max_residual_by_row": [ft(max(v[j] for v in residuals)) for j in range(3)],
            "cost_interval": [ft(-F(cert["upper"])), ft(-q)],
        },
        "controls": controls,
        "replayed_terminal_states": trajectories,
        "coverage": "four fixed instances; finite information diagnostics, not arbitrary-policy certification",
    }


def main():
    contract = load(CONTRACT_PATH)
    for hist_path, v2_path in V2_FROZEN_INPUTS.items():
        expected_sha = contract["readonly_sha256"][hist_path]
        require(digest(v2_path) == expected_sha, f"frozen scientific input changed: {v2_path}")
    results = [check_case(case) for case in contract["cases"]]
    print(
        json.dumps(
            {
                "status": "checks_completed",
                "results": results,
                "formalProof": False,
                "scientificAttestation": False,
                "novelContributionClaimed": False,
                "firstScientificSuccessAchieved": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
