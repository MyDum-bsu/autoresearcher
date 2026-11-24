#!/usr/bin/env python3
"""
Lean 4 verifier for BridgeFormalV2 (10 F1/F2 declarations).

Modes:
  --mode=static   Strip Lean comments (-- and nested /- ... -/) AND string literals
                  ("..." with escapes) across all proof and inventory files, then
                  verify: 5/5 modules present, 0 sorry/admit/custom axioms in proofs,
                  and 10/10 expected targets declared & listed in `#print axioms`
                  inside Inventory.lean.
                  (Does NOT run Lean kernel compile; kernel compile is R2 #1156.)
  --mode=compile  Fresh offline `lean --root=... -o` compilation of all 5 modules
                  against hydrated .lake/packages .oleans + strict #print axioms audit.
  --self-test     Run negative unit self-tests proving commented-out declarations,
                  string-hidden declarations, and active `sorry` are all rejected.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "verification/lean"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

MODULES = [
    "BridgeFormalV2/Model.lean",
    "BridgeFormalV2/Goals.lean",
    "BridgeFormalV2/Proofs/Dynamics.lean",
    "BridgeFormalV2/Proofs/Policies.lean",
    "BridgeFormalV2/Proofs/Inventory.lean",
]


_CHAR_LIT_RE = re.compile(r"'(?:\\(?:x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4}|.)|[^'\\\n])'")


def strip_lean_comments_and_strings(text: str) -> str:
    """Strip Lean line comments (`-- ...`), nested block comments (`/- ... -/`),
    char literals (`'x'`, `'\\''`, `'«'`), ordinary string literals (`"..."`),
    Lean 4 raw string literals (`r#*"..."#*`), and French-quoted identifiers (`«...»`)."""
    out: list[str] = []
    i = 0
    n = len(text)
    depth = 0
    in_string = False
    in_guillemet = False
    raw_hashes: int | None = None
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if depth > 0:
            if ch == "/" and nxt == "-":
                depth += 1
                i += 2
            elif ch == "-" and nxt == "/":
                depth -= 1
                i += 2
            elif ch == "\n":
                out.append("\n")
                i += 1
            else:
                i += 1
            continue
        if in_guillemet:
            if ch == "»":
                in_guillemet = False
                out.append("»")
                i += 1
            elif ch == "\n":
                out.append("\n")
                i += 1
            else:
                i += 1
            continue
        if raw_hashes is not None:
            closing = '"' + ("#" * raw_hashes)
            if text.startswith(closing, i):
                out.append('""')
                i += len(closing)
                raw_hashes = None
            elif ch == "\n":
                out.append("\n")
                i += 1
            else:
                i += 1
            continue
        if in_string:
            if ch == "\\" and i + 1 < n:
                if nxt == "\n":
                    out.append("\n")
                i += 2
            elif ch == '"':
                in_string = False
                out.append('"')
                i += 1
            elif ch == "\n":
                out.append("\n")
                i += 1
            else:
                i += 1
            continue
        if ch == "'" and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] in "_'»")):
            m = _CHAR_LIT_RE.match(text, i)
            if m:
                out.append("''")
                i = m.end()
                continue
        if ch == "«":
            in_guillemet = True
            out.append("«")
            i += 1
            continue
        if ch == "r" and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] in "_'")):
            j = i + 1
            while j < n and text[j] == "#":
                j += 1
            if j < n and text[j] == '"':
                raw_hashes = j - (i + 1)
                i = j + 1
                continue
        if ch == '"':
            in_string = True
            out.append('"')
            i += 1
        elif ch == "/" and nxt == "-":
            depth = 1
            i += 2
        elif ch == "-" and nxt == "-":
            while i < n and text[i] != "\n":
                i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def load_expected_targets() -> tuple[list[dict[str, str]], set[str]]:
    expected = json.loads(
        (LEAN_ROOT / "manifests/expected-theorems-v2.json").read_text(encoding="utf-8")
    )
    targets = expected["targets"]
    allowlist = set(expected.get("axiomAllowlist", ALLOWED_AXIOMS))
    return targets, allowlist


def audit_static_contents(
    contents: dict[str, str],
    targets: list[dict[str, str]],
    allowlist: set[str],
) -> list[str]:
    errors: list[str] = []
    if len(targets) != 10:
        errors.append(f"Expected 10 targets, found {len(targets)}")
    if allowlist > ALLOWED_AXIOMS:
        errors.append(f"Unexpected axiomAllowlist: {allowlist}")

    stripped: dict[str, str] = {}
    for rel in MODULES:
        if rel not in contents:
            errors.append(f"Missing Lean module: {rel}")
            continue
        stripped[rel] = strip_lean_comments_and_strings(contents[rel])
    if errors:
        return errors

    for rel in ("BridgeFormalV2/Proofs/Dynamics.lean", "BridgeFormalV2/Proofs/Policies.lean"):
        clean = stripped[rel]
        for forbidden in ("sorry", "admit", "axiom"):
            if re.search(rf"\b{forbidden}\b", clean):
                errors.append(f"Forbidden token '{forbidden}' found in {rel}")

    proofs_blob = (
        stripped["BridgeFormalV2/Proofs/Dynamics.lean"]
        + "\n"
        + stripped["BridgeFormalV2/Proofs/Policies.lean"]
    )
    inv_clean = stripped["BridgeFormalV2/Proofs/Inventory.lean"]

    for t in targets:
        decl = t["declaration"]
        short = decl.split(".")[-1]
        if not re.search(rf"\btheorem\s+{re.escape(short)}\b", proofs_blob):
            errors.append(f"Missing theorem declaration '{short}' for {decl}")
        if (
            not re.search(rf"#print\s+axioms\s+{re.escape(decl)}\b", inv_clean)
            and not re.search(rf"#print\s+axioms\s+{re.escape(short)}\b", inv_clean)
        ):
            errors.append(f"Missing '#print axioms' entry in Inventory.lean for {decl}")
    return errors


def load_module_contents() -> dict[str, str]:
    contents: dict[str, str] = {}
    for rel in MODULES:
        p = LEAN_ROOT / rel
        if p.is_file():
            contents[rel] = p.read_text(encoding="utf-8")
    return contents


def run_static() -> int:
    targets, allowlist = load_expected_targets()
    contents = load_module_contents()
    errors = audit_static_contents(contents, targets, allowlist)
    if errors:
        for err in errors:
            print(f"LEAN STATIC AUDIT FAILED: {err}", file=sys.stderr)
        return 1
    print(
        f"LEAN 4 BRIDGEFORMALV2 STATIC AUDIT OK: {len(MODULES)}/5 modules present, "
        f"0 sorry/admit/custom axioms, {len(targets)}/10 targets declared & audited "
        "(comments & strings stripped; fresh kernel compile deferred to R2 #1156)"
    )
    return 0


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(f"Self-test failed: {msg}")


def run_self_test() -> int:
    targets, allowlist = load_expected_targets()
    base = load_module_contents()
    _expect(audit_static_contents(base, targets, allowlist) == [], "Baseline static audit failed")

    # Negative 1: comment out a theorem declaration with `--`
    c1 = dict(base)
    c1["BridgeFormalV2/Proofs/Dynamics.lean"] = c1["BridgeFormalV2/Proofs/Dynamics.lean"].replace(
        "theorem expansion", "-- theorem expansion", 1
    )
    _expect(
        bool(audit_static_contents(c1, targets, allowlist)),
        "Commented theorem (-- ) accepted!",
    )

    # Negative 2: comment out a theorem declaration inside nested `/- /- ... -/ -/`
    c2 = dict(base)
    c2["BridgeFormalV2/Proofs/Policies.lean"] = c2["BridgeFormalV2/Proofs/Policies.lean"].replace(
        "theorem epigraph_equality", "/- /- nested -/ theorem epigraph_equality -/", 1
    )
    _expect(
        bool(audit_static_contents(c2, targets, allowlist)),
        "Nested block-comment theorem accepted!",
    )

    # Negative 3: comment out `#print axioms` in Inventory.lean
    c3 = dict(base)
    c3["BridgeFormalV2/Proofs/Inventory.lean"] = re.sub(
        r"(#print\s+axioms\s+\S+)", r"-- \1", c3["BridgeFormalV2/Proofs/Inventory.lean"], count=1
    )
    _expect(
        bool(audit_static_contents(c3, targets, allowlist)),
        "Commented #print axioms accepted!",
    )

    # Negative 4: active `sorry` must fail; commented `sorry` must pass
    c4 = dict(base)
    c4["BridgeFormalV2/Proofs/Dynamics.lean"] += "\nprivate lemma bad : True := by sorry\n"
    _expect(bool(audit_static_contents(c4, targets, allowlist)), "Active sorry was accepted!")

    # Negative 5: theorem name hidden inside a string literal (with escaped quotes!) must fail
    c5 = dict(base)
    c5["BridgeFormalV2/Proofs/Dynamics.lean"] = c5["BridgeFormalV2/Proofs/Dynamics.lean"].replace(
        "theorem expansion", 'def fake := "escaped \\" theorem expansion \\""', 1
    )
    _expect(bool(audit_static_contents(c5, targets, allowlist)), "String-hidden theorem accepted!")

    # Negative 6: `#print axioms` hidden inside a string literal must fail
    c6 = dict(base)
    c6["BridgeFormalV2/Proofs/Inventory.lean"] = re.sub(
        r"(#print\s+axioms\s+\S+)",
        r'def fake := "\1"',
        c6["BridgeFormalV2/Proofs/Inventory.lean"],
        count=1,
    )
    _expect(
        bool(audit_static_contents(c6, targets, allowlist)),
        "String-hidden #print axioms accepted!",
    )

    # Negative 7: Lean 4 raw string literals `r#*"..."#*` hiding theorem & `#print axioms` must fail
    c7_raw = dict(base)
    c7_raw["BridgeFormalV2/Proofs/Dynamics.lean"] = c7_raw[
        "BridgeFormalV2/Proofs/Dynamics.lean"
    ].replace("theorem expansion", 'def fakeRaw := r##"inner "# theorem expansion"##', 1)
    _expect(bool(audit_static_contents(c7_raw, targets, allowlist)), "Raw-string theorem accepted!")

    c8_raw = dict(base)
    c8_raw["BridgeFormalV2/Proofs/Inventory.lean"] = re.sub(
        r"(#print\s+axioms\s+\S+)",
        r'def fakeRaw := r#"\1"#',
        c8_raw["BridgeFormalV2/Proofs/Inventory.lean"],
        count=1,
    )
    _expect(
        bool(audit_static_contents(c8_raw, targets, allowlist)),
        "Raw-string #print axioms accepted!",
    )

    # Negative 9: modified axiom (`private axiom` / `protected axiom` / `local axiom`) must fail
    c9_ax = dict(base)
    c9_ax["BridgeFormalV2/Proofs/Dynamics.lean"] += "\nprivate axiom fake_ax : False\n"
    _expect(bool(audit_static_contents(c9_ax, targets, allowlist)), "private axiom was accepted!")

    # Negative 10 & 11: French-quoted `«...»` hiding theorem or `#print axioms` must fail
    c10_guil = dict(base)
    c10_guil["BridgeFormalV2/Proofs/Dynamics.lean"] = c10_guil[
        "BridgeFormalV2/Proofs/Dynamics.lean"
    ].replace("theorem expansion", "def «theorem expansion» := True", 1)
    _expect(
        bool(audit_static_contents(c10_guil, targets, allowlist)),
        "French-quoted theorem accepted!",
    )

    c11_guil = dict(base)
    c11_guil["BridgeFormalV2/Proofs/Inventory.lean"] = re.sub(
        r"(#print\s+axioms\s+\S+)",
        r"def «\1» := True",
        c11_guil["BridgeFormalV2/Proofs/Inventory.lean"],
        count=1,
    )
    _expect(
        bool(audit_static_contents(c11_guil, targets, allowlist)),
        "French-quoted #print accepted!",
    )

    # Negative 12 & 13: char literals `'«'`/`'»'` or `'\"'` must NOT swallow code between them!
    c12_char = dict(base)
    c12_char["BridgeFormalV2/Proofs/Dynamics.lean"] += (
        "\ndef cOpen := '«'\nprivate axiom hidden_by_char : False\ndef cClose := '»'\n"
    )
    _expect(
        bool(audit_static_contents(c12_char, targets, allowlist)),
        "Char '«' hid private axiom!",
    )

    c13_char = dict(base)
    c13_char["BridgeFormalV2/Proofs/Dynamics.lean"] += (
        "\ndef q1 := '\"'\nprivate axiom hidden_by_quote_char : False\ndef q2 := '\"'\n"
    )
    _expect(
        bool(audit_static_contents(c13_char, targets, allowlist)),
        "Char '\"' hid private axiom!",
    )

    # Positive controls: `sorry` inside a comment, string, or raw string + primed id `x'` ok
    c_ok = dict(base)
    c_ok["BridgeFormalV2/Proofs/Dynamics.lean"] += (
        "\n-- sorry in comment\ndef x' := '\\''\n"
        'def msg := "sorry \\"ok\\""\ndef raw := r#"sorry "ok""#\n'
    )
    _expect(audit_static_contents(c_ok, targets, allowlist) == [], "Benign comment/string failed!")

    print(
        "LEAN STATIC AUDIT SELF-TEST OK: 13/13 negative controls rejected "
        "(comments + nested + strings + raw strings + guillemets + char literals + sorry + axiom), "
        "1/1 benign control OK"
    )
    return 0


def build_lean_path(out_lib: pathlib.Path) -> str:
    lake_pkgs = (LEAN_ROOT / ".lake").resolve() / "packages"
    if not lake_pkgs.is_dir():
        raise FileNotFoundError(f"Prebuilt Lean packages not found at {lake_pkgs}")
    parts = [str(out_lib)]
    for pkg in sorted(lake_pkgs.iterdir()):
        lib = pkg / ".lake/build/lib/lean"
        if lib.is_dir():
            parts.append(str(lib))
    sysroot = subprocess.check_output(["lean", "--print-prefix"], text=True).strip()
    parts.append(str(pathlib.Path(sysroot) / "lib/lean"))
    return os.pathsep.join(parts)


def run_compile() -> int:
    targets, allowlist = load_expected_targets()
    with tempfile.TemporaryDirectory(prefix="aro-lean-verify-") as tmp:
        out_lib = pathlib.Path(tmp) / "lib"
        out_lib.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["LEAN_PATH"] = build_lean_path(out_lib)

        inventory_stdout = ""
        for rel in MODULES:
            src = LEAN_ROOT / rel
            olean = out_lib / pathlib.Path(rel).with_suffix(".olean")
            olean.parent.mkdir(parents=True, exist_ok=True)
            proc = subprocess.run(
                ["lean", f"--root={LEAN_ROOT}", "-o", str(olean), str(src)],
                cwd=str(LEAN_ROOT),
                env=env,
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                print(f"LEAN COMPILE FAILED on {rel} (exit {proc.returncode}):", file=sys.stderr)
                print(proc.stdout, file=sys.stderr)
                print(proc.stderr, file=sys.stderr)
                return 1
            if rel.endswith("Inventory.lean"):
                inventory_stdout = proc.stdout

    axioms_by_thm: dict[str, set[str]] = {}
    for line in inventory_stdout.splitlines():
        m = re.match(r"^'([^']+)'\s+depends on axioms:\s+\[([^\]]*)\]", line.strip())
        if m:
            axioms_by_thm[m.group(1)] = {a.strip() for a in m.group(2).split(",") if a.strip()}
        m_none = re.match(r"^'([^']+)'\s+does not depend on any axioms", line.strip())
        if m_none:
            axioms_by_thm[m_none.group(1)] = set()

    if not axioms_by_thm:
        print("LEAN AUDIT FAILED: empty axiom inventory output!", file=sys.stderr)
        return 1

    for t in targets:
        decl = t["declaration"]
        if decl not in axioms_by_thm:
            print(f"Missing theorem in axiom audit: {decl}", file=sys.stderr)
            return 1
        disallowed = axioms_by_thm[decl] - allowlist
        if disallowed:
            print(f"Disallowed axioms on {decl}: {sorted(disallowed)}", file=sys.stderr)
            return 1

    print(
        f"LEAN 4 BRIDGEFORMALV2 COMPILE OK: {len(MODULES)}/5 modules compiled, "
        f"{len(targets)}/10 targets audited, axioms subset of {sorted(allowlist)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("static", "compile"), default="static")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    return run_static() if args.mode == "static" else run_compile()


if __name__ == "__main__":
    sys.exit(main())
