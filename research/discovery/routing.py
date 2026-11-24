"""Declarative and verifiable model & reasoning routing matrix (R12 #1275).

Enforces strict routing and separation-of-duties invariants:
  - Engineering / scripts / tests / builds: `pi/sol (medium)`, `opencode-go/deepseek-*`,
    or `swe-2-high`; strictly ZERO `zcode`, and strictly DeepSeek-only under `opencode-go`.
  - Creative mathematics (Atlas, conjectures, decomposition, proof & literature synthesis):
    `google/gemini-4-neon (high)`.
  - Hard math review & Semantic Alignment Audit: independent cross-family reviewer
    (`author_family != reviewer_family`, verified against canonical family inference so
    `family` cannot be spoofed), plus `pi/sol` and the Lean 4 formal kernel; surgical
    `anthropic/opus-5.5 (high)` is permitted ONLY with explicit `surgical_trigger=True`
    and `opus_quota_remaining > 0`.
  - Formal kernel verdicts (Lean 4 `0 sorry`, `0 custom axioms`, intact frozen `AroCore/`)
    cannot be bypassed or substituted by LLM approval.
"""

from __future__ import annotations

import dataclasses
import re
from typing import Any

from research.discovery import (
    ALLOWED_LEAN_AXIOMS,
    ALLOWED_REASONING_LEVELS,
    ALLOWED_ROLES,
    PIPELINE_STAGES,
)

_DEEPSEEK_MODEL_RE = re.compile(r"^deepseek-[a-z0-9._-]+$", re.IGNORECASE)
_ZCODE_RE = re.compile(r"zcode", re.IGNORECASE)


class RoutingPolicyError(RuntimeError):
    """Raised when a model specification, route, or reviewer assignment violates policy."""


class FormalGateViolationError(RuntimeError):
    """Raised when formal Lean 4 / frozen-core / alignment promotion gates are violated."""


def infer_model_family(provider: str, model: str) -> str:
    """Deterministically infer canonical model family to prevent family-spoofing bypasses."""
    prov = provider.strip().lower()
    mod = model.strip().lower()
    combined = f"{prov}/{mod}"

    if _ZCODE_RE.search(combined):
        raise RoutingPolicyError(f"Banned provider/model 'zcode' detected in {combined!r}")

    if "deepseek" in mod:
        return "deepseek"
    if "gemini" in mod or prov == "google":
        return "gemini"
    if "opus" in mod or "claude" in mod or "sonnet" in mod or prov == "anthropic":
        return "anthropic"
    if prov == "pi" or mod == "sol":
        return "pi"
    if mod.startswith("swe-") or prov == "swe":
        return "swe"
    if prov == "openai" or mod.startswith(("gpt-", "o1", "o3", "o4", "codex")):
        return "openai"
    raise RoutingPolicyError(f"Unable to infer canonical model family for {combined!r}")


@dataclasses.dataclass(frozen=True)
class ModelSpec:
    provider: str
    model: str
    reasoning_level: str
    family: str
    surgical_only: bool = False

    @property
    def canonical_id(self) -> str:
        return f"{self.provider.strip().lower()}/{self.model.strip().lower()}"

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ModelSpec:
        if not isinstance(data, dict):
            raise RoutingPolicyError("ModelSpec payload must be a JSON object")
        required = ("provider", "model", "reasoning_level", "family")
        for key in required:
            if not isinstance(data.get(key), str) or not str(data[key]).strip():
                raise RoutingPolicyError(f"ModelSpec missing non-empty string field {key!r}")
        spec = cls(
            provider=str(data["provider"]).strip(),
            model=str(data["model"]).strip(),
            reasoning_level=str(data["reasoning_level"]).strip().lower(),
            family=str(data["family"]).strip().lower(),
            surgical_only=bool(data.get("surgical_only", False)),
        )
        validate_model_spec(spec)
        return spec


@dataclasses.dataclass(frozen=True)
class StageRoute:
    stage: str
    role: str
    primary: ModelSpec
    fallbacks: tuple[ModelSpec, ...] = ()
    requires_lean_kernel: bool = False
    requires_cross_family_review: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "role": self.role,
            "primary": self.primary.to_dict(),
            "fallbacks": [fb.to_dict() for fb in self.fallbacks],
            "requires_lean_kernel": self.requires_lean_kernel,
            "requires_cross_family_review": self.requires_cross_family_review,
        }


# Canonical approved model specifications
MODEL_PI_SOL = ModelSpec(
    provider="pi",
    model="sol",
    reasoning_level="medium",
    family="pi",
)
MODEL_OPENCODE_DEEPSEEK_R1 = ModelSpec(
    provider="opencode-go",
    model="deepseek-r1",
    reasoning_level="medium",
    family="deepseek",
)
MODEL_OPENCODE_DEEPSEEK_V3 = ModelSpec(
    provider="opencode-go",
    model="deepseek-v3",
    reasoning_level="medium",
    family="deepseek",
)
MODEL_SWE_2_HIGH = ModelSpec(
    provider="swe",
    model="swe-2-high",
    reasoning_level="high",
    family="swe",
)
MODEL_GEMINI_4_NEON = ModelSpec(
    provider="google",
    model="gemini-4-neon",
    reasoning_level="high",
    family="gemini",
)
MODEL_OPUS_5_5_SURGICAL = ModelSpec(
    provider="anthropic",
    model="opus-5.5",
    reasoning_level="high",
    family="anthropic",
    surgical_only=True,
)


STAGE_ROUTING_MATRIX: dict[str, StageRoute] = {
    "SELECT_OPEN_NODE": StageRoute(
        stage="SELECT_OPEN_NODE",
        role="creative_math",
        primary=MODEL_GEMINI_4_NEON,
    ),
    "NOVELTY_CHECK": StageRoute(
        stage="NOVELTY_CHECK",
        role="creative_math",
        primary=MODEL_GEMINI_4_NEON,
    ),
    "CONJECTURE_PROPOSAL": StageRoute(
        stage="CONJECTURE_PROPOSAL",
        role="creative_math",
        primary=MODEL_GEMINI_4_NEON,
    ),
    "FALSIFY_FIRST": StageRoute(
        stage="FALSIFY_FIRST",
        role="engineering",
        primary=MODEL_PI_SOL,
        fallbacks=(MODEL_OPENCODE_DEEPSEEK_R1, MODEL_OPENCODE_DEEPSEEK_V3, MODEL_SWE_2_HIGH),
    ),
    "SUBGOAL_DECOMPOSITION": StageRoute(
        stage="SUBGOAL_DECOMPOSITION",
        role="creative_math",
        primary=MODEL_GEMINI_4_NEON,
    ),
    "LEAN4_BLUEPRINT_VERIFY": StageRoute(
        stage="LEAN4_BLUEPRINT_VERIFY",
        role="engineering",
        primary=MODEL_PI_SOL,
        fallbacks=(MODEL_OPENCODE_DEEPSEEK_R1, MODEL_SWE_2_HIGH),
        requires_lean_kernel=True,
    ),
    "SEMANTIC_ALIGNMENT_AUDIT": StageRoute(
        stage="SEMANTIC_ALIGNMENT_AUDIT",
        role="semantic_alignment_audit",
        primary=MODEL_PI_SOL,
        fallbacks=(MODEL_GEMINI_4_NEON, MODEL_OPUS_5_5_SURGICAL),
        requires_lean_kernel=True,
        requires_cross_family_review=True,
    ),
    "PACK_FOR_LEARNHARNESS": StageRoute(
        stage="PACK_FOR_LEARNHARNESS",
        role="engineering",
        primary=MODEL_PI_SOL,
        fallbacks=(MODEL_OPENCODE_DEEPSEEK_V3, MODEL_SWE_2_HIGH),
    ),
}


def validate_model_spec(
    spec: ModelSpec,
    *,
    role: str | None = None,
    surgical_trigger: bool = False,
    opus_quota_remaining: int = 0,
) -> None:
    """Validate a single ModelSpec against hard R12 routing policies (zero `assert`)."""
    if not isinstance(spec, ModelSpec):
        raise RoutingPolicyError(f"Expected ModelSpec, got {type(spec).__name__}")

    prov = spec.provider.strip().lower()
    mod = spec.model.strip().lower()
    fam = spec.family.strip().lower()
    reasoning = spec.reasoning_level.strip().lower()

    if not prov or not mod or not fam:
        raise RoutingPolicyError(f"ModelSpec fields must be non-empty: {spec!r}")

    if _ZCODE_RE.search(prov) or _ZCODE_RE.search(mod) or _ZCODE_RE.search(fam):
        raise RoutingPolicyError(
            f"Policy violation: 'zcode' is strictly forbidden ({spec.canonical_id})"
        )

    if prov == "opencode-go" and not _DEEPSEEK_MODEL_RE.match(mod):
        raise RoutingPolicyError(
            f"Policy violation: provider 'opencode-go' is strictly DeepSeek-only; "
            f"rejected {spec.canonical_id!r}"
        )

    if reasoning not in ALLOWED_REASONING_LEVELS:
        raise RoutingPolicyError(
            f"Invalid reasoning_level {spec.reasoning_level!r}; "
            f"allowed: {sorted(ALLOWED_REASONING_LEVELS)}"
        )

    inferred = infer_model_family(prov, mod)
    if fam != inferred:
        raise RoutingPolicyError(
            f"Model family mismatch for {spec.canonical_id!r}: "
            f"declared {fam!r}, canonical {inferred!r}"
        )

    is_opus = "opus" in mod
    if is_opus and not spec.surgical_only:
        raise RoutingPolicyError(
            f"Model {spec.canonical_id!r} must be flagged surgical_only=True"
        )

    if role is not None:
        if role not in ALLOWED_ROLES:
            raise RoutingPolicyError(f"Unknown routing role {role!r}")
        if role == "creative_math" and (
            spec.canonical_id != "google/gemini-4-neon" or reasoning != "high"
        ):
            raise RoutingPolicyError(
                f"Role 'creative_math' requires google/gemini-4-neon (high); got {spec!r}"
            )
        if role == "engineering":
            allowed_eng = (
                (spec.canonical_id == "pi/sol" and reasoning in {"medium", "high"})
                or (prov == "opencode-go" and bool(_DEEPSEEK_MODEL_RE.match(mod)))
                or (mod == "swe-2-high" and reasoning == "high")
            )
            if not allowed_eng:
                raise RoutingPolicyError(
                    f"Model {spec.canonical_id!r} (reasoning={reasoning!r}) "
                    "is not permitted for role 'engineering'"
                )
        if role in {"hard_math_review", "semantic_alignment_audit"}:
            allowed_review = (
                (spec.canonical_id == "google/gemini-4-neon" and reasoning == "high")
                or (spec.canonical_id == "pi/sol" and reasoning in {"medium", "high"})
                or (spec.canonical_id == "anthropic/opus-5.5" and reasoning == "high")
            )
            if not allowed_review:
                raise RoutingPolicyError(
                    f"Model {spec.canonical_id!r} (reasoning={reasoning!r}) "
                    f"is not permitted for role {role!r}"
                )
        if is_opus:
            if role not in {"hard_math_review", "semantic_alignment_audit"}:
                raise RoutingPolicyError(
                    f"Surgical {spec.canonical_id!r} is only allowed for hard math review / "
                    f"semantic alignment audit, not role {role!r}"
                )
            if not surgical_trigger or opus_quota_remaining <= 0:
                raise RoutingPolicyError(
                    f"Surgical {spec.canonical_id!r} requires surgical_trigger=True and "
                    f"opus_quota_remaining > 0 (got trigger={surgical_trigger}, "
                    f"quota={opus_quota_remaining})"
                )


def validate_review_separation(
    author: ModelSpec,
    reviewer: ModelSpec,
    *,
    surgical_trigger: bool = False,
    opus_quota_remaining: int = 0,
) -> None:
    """Enforce strict cross-family review invariant: author_family != reviewer_family."""
    validate_model_spec(author)
    validate_model_spec(
        reviewer,
        role="semantic_alignment_audit",
        surgical_trigger=surgical_trigger,
        opus_quota_remaining=opus_quota_remaining,
    )
    author_fam = infer_model_family(author.provider, author.model)
    reviewer_fam = infer_model_family(reviewer.provider, reviewer.model)
    if author_fam == reviewer_fam:
        raise RoutingPolicyError(
            f"Self-acceptance forbidden: author ({author.canonical_id}, family={author_fam!r}) "
            f"and reviewer ({reviewer.canonical_id}, family={reviewer_fam!r}) share the same family"
        )


def select_reviewer_route(
    author: ModelSpec,
    *,
    surgical_trigger: bool = False,
    opus_quota_remaining: int = 0,
    prefer_surgical_opus: bool = False,
) -> ModelSpec:
    """Select a policy-compliant independent cross-family reviewer for `author`."""
    validate_model_spec(author)
    author_fam = infer_model_family(author.provider, author.model)

    if prefer_surgical_opus:
        # Fail closed if caller explicitly requests Opus without trigger or quota
        validate_review_separation(
            author,
            MODEL_OPUS_5_5_SURGICAL,
            surgical_trigger=surgical_trigger,
            opus_quota_remaining=opus_quota_remaining,
        )
        return MODEL_OPUS_5_5_SURGICAL

    if surgical_trigger and opus_quota_remaining > 0 and author_fam != "anthropic":
        validate_review_separation(
            author,
            MODEL_OPUS_5_5_SURGICAL,
            surgical_trigger=True,
            opus_quota_remaining=opus_quota_remaining,
        )
        return MODEL_OPUS_5_5_SURGICAL

    if author_fam != "gemini":
        validate_review_separation(author, MODEL_GEMINI_4_NEON)
        return MODEL_GEMINI_4_NEON

    validate_review_separation(author, MODEL_PI_SOL)
    return MODEL_PI_SOL


def validate_formal_kernel_verdict(verdict: dict[str, Any] | None) -> None:
    """Enforce that Lean 4 kernel checks passed with zero sorry/custom axioms & intact core.

    LLM approval alone can NEVER satisfy or bypass this check.
    """
    if not isinstance(verdict, dict):
        raise FormalGateViolationError(
            "Missing Lean 4 kernel verdict; LLM approval cannot substitute for formal verification"
        )
    if verdict.get("lean_verified") is not True:
        raise FormalGateViolationError(
            "Lean 4 kernel verification did not pass: "
            f"lean_verified={verdict.get('lean_verified')!r}"
        )
    sorry_count = verdict.get("sorry_count")
    if not isinstance(sorry_count, int) or isinstance(sorry_count, bool) or sorry_count != 0:
        raise FormalGateViolationError(
            f"Formal gate violation: sorry_count must be 0, got {sorry_count!r}"
        )
    if verdict.get("frozen_core_intact") is not True:
        raise FormalGateViolationError(
            "Formal gate violation: frozen AroCore/BridgeFormalV2 integrity check failed"
        )
    custom_axioms = verdict.get("custom_axioms")
    if not isinstance(custom_axioms, list) or len(custom_axioms) > 0:
        raise FormalGateViolationError(
            f"Formal gate violation: custom axioms forbidden, got {custom_axioms!r}"
        )
    used_axioms = verdict.get("used_axioms", [])
    if not isinstance(used_axioms, list):
        raise FormalGateViolationError("Formal gate violation: 'used_axioms' must be a list")
    disallowed = sorted({str(ax) for ax in used_axioms} - ALLOWED_LEAN_AXIOMS)
    if disallowed:
        raise FormalGateViolationError(
            f"Formal gate violation: disallowed Lean axioms detected: {disallowed}"
        )
    verified_decls = verdict.get("verified_decls")
    if (
        not isinstance(verified_decls, list)
        or not verified_decls
        or not all(isinstance(d, str) and d.strip() for d in verified_decls)
    ):
        raise FormalGateViolationError(
            "Formal gate violation: 'verified_decls' must be a non-empty list of declarations"
        )


def validate_routing_matrix(matrix: dict[str, StageRoute] = STAGE_ROUTING_MATRIX) -> dict[str, Any]:
    """Audit the entire stage routing matrix for completeness and policy compliance."""
    missing = [s for s in PIPELINE_STAGES if s not in matrix]
    extra = [s for s in matrix if s not in PIPELINE_STAGES]
    if missing or extra:
        raise RoutingPolicyError(
            f"Routing matrix stage mismatch: missing={missing}, extra={extra}"
        )

    for stage in PIPELINE_STAGES:
        route = matrix[stage]
        if route.stage != stage:
            raise RoutingPolicyError(f"Route key {stage!r} != route.stage {route.stage!r}")
        if route.role not in ALLOWED_ROLES:
            raise RoutingPolicyError(f"Stage {stage!r} has invalid role {route.role!r}")
        validate_model_spec(route.primary, role=route.role)
        for fb in route.fallbacks:
            is_surgical_fb = "opus" in fb.model.lower()
            validate_model_spec(
                fb,
                role=route.role,
                surgical_trigger=is_surgical_fb,
                opus_quota_remaining=1 if is_surgical_fb else 0,
            )

    # Verify Lean 4 kernel mandatory stages
    if not matrix["LEAN4_BLUEPRINT_VERIFY"].requires_lean_kernel:
        raise RoutingPolicyError("LEAN4_BLUEPRINT_VERIFY must require Lean 4 kernel")
    if not matrix["SEMANTIC_ALIGNMENT_AUDIT"].requires_lean_kernel:
        raise RoutingPolicyError("SEMANTIC_ALIGNMENT_AUDIT must require Lean 4 kernel")
    if not matrix["SEMANTIC_ALIGNMENT_AUDIT"].requires_cross_family_review:
        raise RoutingPolicyError("SEMANTIC_ALIGNMENT_AUDIT must require cross-family review")

    # Verify default author vs default reviewer are strictly cross-family
    validate_review_separation(
        matrix["CONJECTURE_PROPOSAL"].primary,
        matrix["SEMANTIC_ALIGNMENT_AUDIT"].primary,
    )
    return {
        "stages": len(matrix),
        "creative_math_primary": matrix["CONJECTURE_PROPOSAL"].primary.canonical_id,
        "engineering_primary": matrix["FALSIFY_FIRST"].primary.canonical_id,
        "alignment_primary": matrix["SEMANTIC_ALIGNMENT_AUDIT"].primary.canonical_id,
    }
