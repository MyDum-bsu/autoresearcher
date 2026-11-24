#!/usr/bin/env python3
"""
Gate G5 validator for research/guides/ study packs (R4 #1160).

Checks:
  1. Active study packs under research/guides/ (excluding TEMPLATE and
     00-source-packet-01) have all 4 required files:
       - 01-intuition-and-map.md
       - 02-propositions-and-chains.md
       - 03-traps-and-counterexamples.md
       - 04-practice-and-attestation.md
  2. Anchor-lint:
     - 100% of inline and reference-style Markdown links (`[t](p)`, `[t][id]`,
       `[id]: p`) resolve to existing files in the repo;
     - Markdown `#anchor` fragments match real ATX headings in the target file;
     - PDF `#page=N` / `#page=N-M` fragments match the real PDF page count;
     - every referenced corpus/ PDF is registered in corpus/MANIFEST.md
       (or resides in corpus/intake/ or corpus/extra/);
     - every referenced BridgeFormalV2.Proofs.<name> exists in both
       expected-theorems-v2.json and verification/lean/BridgeFormalV2/Proofs/;
     - each active pack cites >= 1 verified PDF anchor and >= 1 Lean/code anchor.
  3. LaTeX math syntax: properly ordered and balanced $$, $, \\[/\\], \\(/\\),
     braces inside math, and matching \\begin{env}...\\end{env} pairs (outside
     code blocks and inline code spans).
  4. Mermaid syntax: >= 1 diagram in 01-intuition-and-map.md, valid header,
     no raw HTML tags, balanced quotes/brackets/`|`, no dangling arrows.
  5. Russian technical style check via technical-style-editor
     (`lint_technical_style.py --language ru --json`).
  6. Structural/syntax/style validation of research/guides/README.md and TEMPLATE/.
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
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]
GUIDES_ROOT = ROOT / "research/guides"
REQUIRED_FILES = (
    "01-intuition-and-map.md",
    "02-propositions-and-chains.md",
    "03-traps-and-counterexamples.md",
    "04-practice-and-attestation.md",
)
SKIP_DIRS = {"TEMPLATE", "00-source-packet-01"}
DEFAULT_STYLE_LINTER = (
    pathlib.Path.home()
    / ".agents/skills/technical-style-editor/scripts/lint_technical_style.py"
)
MERMAID_HEADER_RE = re.compile(
    r"^(?:flowchart\s+(?:TD|TB|BT|RL|LR)|graph\s+(?:TD|TB|BT|RL|LR)|"
    r"sequenceDiagram|stateDiagram(?:-v2)?|classDiagram|erDiagram|xychart-beta)\s*$"
)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\n]+)\)")
MD_REF_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(<[^>\n]+>|\S+)(?:\s+.*)?$")
MD_REF_USE_RE = re.compile(r"\[([^\]]+)\]\[([^\]]*)\]")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)(?:\s+#+\s*)?$")
THEMATIC_BREAK_RE = re.compile(r"^\s{0,3}(?:(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,})$")
PDF_PAGE_FRAG_RE = re.compile(r"^page=(\d+)(?:-(\d+))?$", re.IGNORECASE)
LEAN_DECL_RE = re.compile(r"\bBridgeFormalV2\.Proofs\.([A-Za-z0-9_']+)\b")
ENV_RE = re.compile(r"\\(begin|end)\{([A-Za-z0-9_*]+)\}")
HTML_TAG_RE = re.compile(r"<[A-Za-z][^>]*>")
INLINE_CODE_RE = re.compile(r"(`+)[^\n]+?\1")
MERMAID_TRAILING_ARROW_RE = re.compile(
    r"(?:--+>?|-\.+->|==+>?|<-->|o--o|--[ox])\s*(?:\|[^|]*\|\s*)?$"
)
MERMAID_LEADING_ARROW_RE = re.compile(r"^(?:--+>?|-\.+->|==+>?|<-->|o--o|--[ox])(?:\s|$|\|)")

_PDF_PAGE_CACHE: dict[pathlib.Path, int | None] = {}
_MD_ANCHOR_CACHE: dict[pathlib.Path, set[str]] = {}


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(f"Self-test failed: {msg}")


def load_known_corpus_files(repo_root: pathlib.Path) -> set[str]:
    known: set[str] = set()
    manifest = repo_root / "corpus/MANIFEST.md"
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if len(s) > 66 and s[64:66] == "  ":
                known.add(s[66:])
    for sub in ("corpus/intake", "corpus/extra"):
        d = repo_root / sub
        if d.is_dir():
            for f in d.rglob("*"):
                if f.is_file():
                    known.add(f.relative_to(repo_root).as_posix())
    return known


def load_known_lean_decls(repo_root: pathlib.Path) -> set[str]:
    """Return declarations present in both expected-theorems-v2.json and Lean sources."""
    inv = repo_root / "verification/lean/manifests/expected-theorems-v2.json"
    if not inv.is_file():
        return set()
    data = json.loads(inv.read_text(encoding="utf-8"))
    manifest_decls: set[str] = set()
    for target in data.get("targets", []):
        decl = target.get("declaration", "")
        if decl.startswith("BridgeFormalV2.Proofs."):
            manifest_decls.add(decl.split(".")[-1])

    proofs_dir = repo_root / "verification/lean/BridgeFormalV2/Proofs"
    if not proofs_dir.is_dir():
        return set()
    source_text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted(proofs_dir.glob("*.lean"))
    )
    verified: set[str] = set()
    for name in manifest_decls:
        pattern = rf"\b(?:theorem|lemma|def)\s+{re.escape(name)}\b"
        if re.search(pattern, source_text):
            verified.add(name)
    return verified


def split_fenced_blocks(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (prose_without_fences, list_of_(lang, block_body))."""
    lines = text.splitlines()
    prose: list[str] = []
    blocks: list[tuple[str, str]] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    lang = ""
    buf: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if not in_fence:
            m = re.match(r"^(`{3,}|~{3,})\s*([A-Za-z0-9_-]*)\s*$", stripped)
            if m:
                in_fence = True
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                lang = m.group(2).lower()
                buf = []
                continue
            prose.append(line)
        else:
            is_close = (
                stripped.startswith(fence_char * fence_len)
                and stripped.strip(fence_char).strip() == ""
            )
            if is_close:
                blocks.append((lang, "\n".join(buf)))
                prose.append("")
                in_fence = False
                continue
            buf.append(line)
    if in_fence:
        blocks.append(("__unclosed__", "\n".join(buf)))
    return "\n".join(prose), blocks


def strip_inline_code(prose: str) -> str:
    return INLINE_CODE_RE.sub(" ", prose)


def _strip_escaped_chars(text: str, targets: str) -> str:
    """Remove backslash-escaped target chars while preserving '\\\\' pairs."""
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "\\" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "\\" or nxt in targets:
                out.append("  ")
                i += 2
                continue
        out.append(text[i])
        i += 1
    return "".join(out)


def _scan_latex_math(clean: str, label: str) -> tuple[list[str], list[str]]:
    """Single-pass LaTeX math delimiter scanner for \\[\\], \\(\\), $$, and $."""
    errors: list[str] = []
    math_blocks: list[str] = []
    mode: str | None = None
    buf: list[str] = []
    i = 0
    n = len(clean)

    while i < n:
        ch = clean[i]
        if ch == "\\" and i + 1 < n:
            nxt = clean[i + 1]
            if nxt in ("\\", "$"):
                if mode is not None:
                    buf.append(clean[i : i + 2])
                i += 2
                continue
            if nxt in ("[", "]", "(", ")"):
                tok = "\\" + nxt
                if mode is None:
                    if nxt in ("[", "("):
                        mode = tok
                        buf = []
                    else:
                        errors.append(f"{label}: unmatched {tok} outside math mode")
                elif (mode == r"\[" and nxt == "]") or (mode == r"\(" and nxt == ")"):
                    math_blocks.append("".join(buf))
                    mode = None
                    buf = []
                else:
                    errors.append(f"{label}: unexpected {tok} inside {mode} math block")
                i += 2
                continue
        if ch == "$":
            is_double = i + 1 < n and clean[i + 1] == "$"
            tok = "$$" if is_double else "$"
            step = 2 if is_double else 1
            if mode is None:
                mode = tok
                buf = []
            elif mode == tok:
                math_blocks.append("".join(buf))
                mode = None
                buf = []
            else:
                errors.append(f"{label}: unexpected {tok} inside {mode} math block")
            i += step
            continue
        if ch == "\n" and mode == "$":
            errors.append(f"{label}: unclosed inline $ math delimiter before newline")
            mode = None
            buf = []
            i += 1
            continue
        if mode is not None:
            buf.append(ch)
        i += 1

    if mode is not None:
        errors.append(f"{label}: unclosed {mode} math delimiter")
    return math_blocks, errors


def check_latex(prose: str, label: str) -> list[str]:
    clean = strip_inline_code(prose)
    math_blocks, errors = _scan_latex_math(clean, label)

    # Check braces & \begin{env}...\end{env} inside every extracted math block
    for idx, mb in enumerate(math_blocks, 1):
        no_esc_b = _strip_escaped_chars(mb, "{}")
        depth = 0
        for ch in no_esc_b:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    errors.append(f"{label}: unmatched '}}' in math block #{idx}")
                    break
        if depth > 0:
            errors.append(f"{label}: unclosed '{{' in math block #{idx}")

        env_stack: list[str] = []
        for em in ENV_RE.finditer(mb):
            kind, name = em.group(1), em.group(2)
            if kind == "begin":
                env_stack.append(name)
            elif not env_stack or env_stack[-1] != name:
                errors.append(f"{label}: mismatched \\end{{{name}}} in math block #{idx}")
                break
            else:
                env_stack.pop()
        if env_stack:
            errors.append(f"{label}: unclosed \\begin{{{env_stack[-1]}}} in math block #{idx}")

    return errors


def _strip_quoted_strings(line: str) -> str:
    return re.sub(r'"[^"]*"', '""', line)


def check_mermaid(blocks: list[tuple[str, str]], label: str, require_diagram: bool) -> list[str]:
    errors: list[str] = []
    for lang, _ in blocks:
        if lang == "__unclosed__":
            errors.append(f"{label}: unclosed fenced code block")
    mermaid_blocks = [body for lang, body in blocks if lang == "mermaid"]
    if require_diagram and not mermaid_blocks:
        errors.append(f"{label}: expected at least one mermaid diagram")
    for idx, body in enumerate(mermaid_blocks, 1):
        lines = [
            ln.strip()
            for ln in body.splitlines()
            if ln.strip() and not ln.strip().startswith("%%")
        ]
        if not lines:
            errors.append(f"{label}: empty mermaid diagram #{idx}")
            continue
        if not MERMAID_HEADER_RE.match(lines[0]):
            errors.append(f"{label}: unsupported mermaid header '{lines[0]}' in diagram #{idx}")
        is_flow = lines[0].startswith(("flowchart", "graph"))
        for ln in lines[1:]:
            if HTML_TAG_RE.search(ln):
                errors.append(f"{label}: raw HTML tag forbidden in mermaid diagram #{idx}: {ln}")
            if ln.count('"') % 2 != 0:
                errors.append(f"{label}: unbalanced quotes in mermaid diagram #{idx}: {ln}")
                continue
            outside = _strip_quoted_strings(ln)
            for opener, closer in (("[", "]"), ("(", ")"), ("{", "}")):
                if outside.count(opener) != outside.count(closer):
                    errors.append(
                        f"{label}: unbalanced '{opener}{closer}' in mermaid diagram #{idx}: {ln}"
                    )
            if outside.count("|") % 2 != 0:
                errors.append(f"{label}: unbalanced '|' label in mermaid diagram #{idx}: {ln}")
            if is_flow:
                for stmt in outside.split(";"):
                    s = stmt.strip()
                    if not s:
                        continue
                    if MERMAID_TRAILING_ARROW_RE.search(s):
                        errors.append(
                            f"{label}: dangling mermaid arrow (missing target) "
                            f"in diagram #{idx}: {ln}"
                        )
                    if MERMAID_LEADING_ARROW_RE.search(s):
                        errors.append(
                            f"{label}: dangling mermaid arrow (missing source) "
                            f"in diagram #{idx}: {ln}"
                        )
    return errors


def _parse_md_target(raw_target: str) -> str:
    s = raw_target.strip()
    if s.startswith("<") and ">" in s:
        return s[1 : s.index(">")].strip()
    m = re.match(r'^(\S+)\s+["\'].*["\']$', s)
    if m:
        return m.group(1)
    return s


def _slugify_heading(title: str) -> str:
    # Strip markdown links [text](url) -> text and inline formatting
    cleaned = MD_LINK_RE.sub(r"\1", title)
    cleaned = re.sub(r"[`*_~]", "", cleaned).strip().lower()
    out: list[str] = []
    for ch in cleaned:
        if ch.isalnum() or ch in (" ", "-"):
            out.append(ch)
    return "".join(out).replace(" ", "-")


def _strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?(?:-->|\Z)", "", text, flags=re.S)


def _strip_indented_code_blocks(text: str) -> str:
    """Remove CommonMark indented code blocks (4 spaces / tab outside open paragraphs)."""
    out: list[str] = []
    can_start_indented = True
    in_indented = False
    for line in text.splitlines():
        if not line.strip():
            out.append("")
            can_start_indented = True
            continue
        is_indented = line.startswith(("    ", "\t"))
        if is_indented and (can_start_indented or in_indented):
            in_indented = True
            can_start_indented = False
            continue
        in_indented = False
        out.append(line)
        # Leaf blocks (ATX heading, thematic break, ref def) cannot be continued by paragraphs
        if (
            HEADING_RE.match(line)
            or THEMATIC_BREAK_RE.match(line)
            or MD_REF_DEF_RE.match(line)
        ):
            can_start_indented = True
        else:
            can_start_indented = False
    return "\n".join(out)


def _strip_html_tags(text: str) -> str:
    """Strip HTML tags respecting quoted attribute values containing '>'."""
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "<" and i + 1 < n and (text[i + 1].isalpha() or text[i + 1] in ("!", "/")):
            j = i + 2
            quote: str | None = None
            closed = False
            while j < n:
                ch = text[j]
                if quote is not None:
                    if ch == quote:
                        quote = None
                elif ch in ('"', "'"):
                    quote = ch
                elif ch == ">":
                    closed = True
                    break
                j += 1
            if closed:
                out.append(" ")
                i = j + 1
                continue
        out.append(text[i])
        i += 1
    return "".join(out)


def _norm_ref_label(raw: str) -> str:
    return re.sub(r"\s+", " ", raw.strip()).casefold()


def _markdown_heading_anchors(md_path: pathlib.Path) -> set[str]:
    key = md_path.resolve()
    if key in _MD_ANCHOR_CACHE:
        return _MD_ANCHOR_CACHE[key]
    prose, _ = split_fenced_blocks(key.read_text(encoding="utf-8"))
    prose = _strip_indented_code_blocks(_strip_html_comments(prose))
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in prose.splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = _slugify_heading(m.group(2))
        if not base:
            continue
        seen = counts.get(base, 0)
        anchors.add(base if seen == 0 else f"{base}-{seen}")
        counts[base] = seen + 1
    _MD_ANCHOR_CACHE[key] = anchors
    return anchors


def _pdf_page_count(pdf_path: pathlib.Path) -> int | None:
    key = pdf_path.resolve()
    if key in _PDF_PAGE_CACHE:
        return _PDF_PAGE_CACHE[key]
    count: int | None = None
    try:
        import pypdf  # type: ignore[import-not-found]

        reader = pypdf.PdfReader(str(key))
        count = len(reader.pages)
    except Exception:
        count = None
    if count is None:
        try:
            proc = subprocess.run(
                ["pdfinfo", str(key)], capture_output=True, text=True, check=False
            )
            if proc.returncode == 0:
                m = re.search(r"^Pages:\s+(\d+)\s*$", proc.stdout, flags=re.M)
                if m:
                    count = int(m.group(1))
        except FileNotFoundError:
            count = None
    _PDF_PAGE_CACHE[key] = count
    return count


def _validate_fragment(
    resolved: pathlib.Path, fragment: str, label: str, raw_target: str
) -> list[str]:
    frag = urllib.parse.unquote(fragment).strip()
    if not frag:
        return []
    suffix = resolved.suffix.lower()
    if suffix == ".md":
        anchors = _markdown_heading_anchors(resolved)
        if frag.lower() not in anchors:
            return [
                f"{label}: broken markdown anchor fragment '#{frag}' in {raw_target}"
            ]
        return []
    if suffix == ".pdf":
        m = PDF_PAGE_FRAG_RE.match(frag)
        if not m:
            return [
                f"{label}: unsupported PDF fragment '#{frag}' in {raw_target} "
                "(expected #page=N or #page=N-M)"
            ]
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) is not None else start
        if start < 1 or end < start:
            return [f"{label}: invalid PDF page range '#{frag}' in {raw_target}"]
        pages = _pdf_page_count(resolved)
        if pages is None:
            return [f"{label}: unable to read page count of PDF {resolved.name}"]
        if end > pages:
            return [
                f"{label}: PDF page fragment '#{frag}' exceeds page count "
                f"({pages}) in {resolved.name}"
            ]
    return []


def _validate_link_target(
    raw_target: str,
    fpath: pathlib.Path,
    label: str,
    repo_root: pathlib.Path,
    known_corpus: set[str],
) -> tuple[list[str], int, int]:
    errors: list[str] = []
    pdf_anchors = 0
    code_anchors = 0

    target = _parse_md_target(raw_target)
    if target.startswith(("http://", "https://", "mailto:")):
        return [], 0, 0

    if "#" in target:
        path_part, frag_part = target.split("#", 1)
    else:
        path_part, frag_part = target, ""

    target_no_frag = urllib.parse.unquote(path_part)
    resolved = fpath.resolve() if not target_no_frag else (fpath.parent / target_no_frag).resolve()

    try:
        rel_repo = resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return [f"{label}: link escapes repository root: {raw_target}"], 0, 0

    omitted_meta_path = repo_root / "corpus/public-omitted-pdfs.json"
    omitted_pdfs = json.loads(omitted_meta_path.read_text(encoding="utf-8")) if omitted_meta_path.is_file() else {}
    is_omitted_pub = not resolved.exists() and rel_repo in omitted_pdfs

    if not resolved.exists() and not is_omitted_pub:
        return [f"{label}: broken anchor link -> {raw_target} ({rel_repo})"], 0, 0

    if frag_part:
        if is_omitted_pub:
            m_pg = re.match(r"^page=(\d+)$", frag_part)
            if m_pg:
                pg = int(m_pg.group(1))
                max_pg = int(omitted_pdfs[rel_repo]["page_count"])
                if pg < 1 or pg > max_pg:
                    errors.append(f"{label}: PDF page {pg} exceeds page count {max_pg} -> {raw_target}")
        else:
            errors.extend(_validate_fragment(resolved, frag_part, label, raw_target))

    if rel_repo.startswith("corpus/") and resolved.suffix.lower() == ".pdf":
        if rel_repo not in known_corpus:
            errors.append(
                f"{label}: PDF not registered in corpus/MANIFEST.md: {rel_repo}"
            )
        else:
            pdf_anchors += 1
    if rel_repo.startswith(
        ("verification/", "research/counterexamples/", "research/claims/")
    ):
        code_anchors += 1

    return errors, pdf_anchors, code_anchors


def run_style_linter(
    fpath: pathlib.Path, label: str, style_linter: pathlib.Path
) -> list[str]:
    errors: list[str] = []
    proc = subprocess.run(
        [sys.executable, "-B", str(style_linter), "--language", "ru", "--json", str(fpath)],
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 1):
        errors.append(
            f"{label}: style linter crashed (exit {proc.returncode}): {proc.stderr.strip()}"
        )
        return errors
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON from style linter: {exc}")
        return errors

    if isinstance(payload, list):
        findings = payload
    elif isinstance(payload, dict) and isinstance(payload.get("findings"), list):
        findings = payload["findings"]
    else:
        errors.append(
            f"{label}: unexpected JSON shape from style linter ({type(payload).__name__})"
        )
        return errors

    for finding in findings:
        if not isinstance(finding, dict):
            errors.append(f"{label}: style finding -> {finding}")
            continue
        line_no = finding.get("line", "?")
        rule = finding.get("rule") or finding.get("match") or finding.get("phrase") or "unknown"
        excerpt = finding.get("excerpt") or finding.get("message") or ""
        errors.append(f"{label}:{line_no}: style finding [{rule}] -> {excerpt}")

    if proc.returncode == 1 and not findings:
        errors.append(f"{label}: style linter returned exit 1 with no parsed findings")
    return errors


def check_markdown_file(
    fpath: pathlib.Path,
    label: str,
    repo_root: pathlib.Path,
    known_corpus: set[str],
    known_lean: set[str],
    style_linter: pathlib.Path | None,
    *,
    require_diagram: bool = False,
    check_links: bool = True,
) -> tuple[list[str], int, int]:
    errors: list[str] = []
    pdf_anchors = 0
    code_anchors = 0

    text = fpath.read_text(encoding="utf-8")
    if not text.strip():
        return [f"{label}: file is empty"], 0, 0

    prose, blocks = split_fenced_blocks(text)
    errors.extend(check_latex(prose, label))
    errors.extend(check_mermaid(blocks, label, require_diagram=require_diagram))

    if check_links:
        # Parse reference-style link definitions `[id]: target` outside HTML comments / code
        prose_visible = _strip_indented_code_blocks(_strip_html_comments(prose))
        ref_defs: dict[str, str] = {}
        ref_counts: dict[str, tuple[int, int]] = {}
        body_lines: list[str] = []
        for line in prose_visible.splitlines():
            rm = MD_REF_DEF_RE.match(line)
            if rm:
                ref_id = _norm_ref_label(rm.group(1))
                ref_target = rm.group(2).strip()
                ref_defs[ref_id] = ref_target
                link_errs, p_cnt, c_cnt = _validate_link_target(
                    ref_target, fpath, label, repo_root, known_corpus
                )
                errors.extend(link_errs)
                # Count PDF/code anchors only when the reference is actually used in text
                ref_counts[ref_id] = (p_cnt, c_cnt)
            else:
                body_lines.append(line)

        prose_no_code = strip_inline_code("\n".join(body_lines))

        # Check inline links `[text](target)`
        for m in MD_LINK_RE.finditer(prose_no_code):
            link_errs, p_cnt, c_cnt = _validate_link_target(
                m.group(2), fpath, label, repo_root, known_corpus
            )
            errors.extend(link_errs)
            pdf_anchors += p_cnt
            code_anchors += c_cnt

        # Strip inline links and HTML tags/attributes before scanning reference usages
        prose_for_refs = _strip_html_tags(MD_LINK_RE.sub(" ", prose_no_code))
        used_refs: set[str] = set()

        # Check full `[text][id]` and collapsed `[text][]` reference usages
        for um in MD_REF_USE_RE.finditer(prose_for_refs):
            ref_key = _norm_ref_label(um.group(2) or um.group(1))
            if ref_key not in ref_defs:
                errors.append(
                    f"{label}: unresolved reference-style link [{um.group(1)}][{um.group(2)}]"
                )
            else:
                used_refs.add(ref_key)

        # Also recognize shortcut reference usages `[id]` matching a defined reference
        prose_after_full = MD_REF_USE_RE.sub(" ", prose_for_refs)
        for sm in re.finditer(r"\[([^\]]+)\]", prose_after_full):
            ref_key = _norm_ref_label(sm.group(1))
            if ref_key in ref_defs:
                used_refs.add(ref_key)

        for ref_key in used_refs:
            p_cnt, c_cnt = ref_counts.get(ref_key, (0, 0))
            pdf_anchors += p_cnt
            code_anchors += c_cnt

    # Verify every cited BridgeFormalV2.Proofs.<name> declaration
    for dm in LEAN_DECL_RE.finditer(text):
        short = dm.group(1)
        if short not in known_lean:
            errors.append(
                f"{label}: unknown Lean declaration BridgeFormalV2.Proofs.{short} "
                "(not verified in expected-theorems-v2.json + BridgeFormalV2/Proofs)"
            )
        else:
            code_anchors += 1

    if style_linter is not None:
        errors.extend(run_style_linter(fpath, label, style_linter))

    return errors, pdf_anchors, code_anchors


def check_pack(
    pack_dir: pathlib.Path,
    repo_root: pathlib.Path,
    known_corpus: set[str],
    known_lean: set[str],
    style_linter: pathlib.Path | None,
    *,
    is_template: bool = False,
) -> list[str]:
    errors: list[str] = []
    pdf_anchors = 0
    code_anchors = 0

    for fname in REQUIRED_FILES:
        fpath = pack_dir / fname
        label = f"{pack_dir.name}/{fname}"
        if not fpath.is_file():
            errors.append(f"{label}: missing required guide file")
            continue
        file_errors, p_cnt, c_cnt = check_markdown_file(
            fpath,
            label,
            repo_root,
            known_corpus,
            known_lean,
            style_linter,
            require_diagram=(fname == "01-intuition-and-map.md"),
            check_links=not is_template,
        )
        errors.extend(file_errors)
        pdf_anchors += p_cnt
        code_anchors += c_cnt

    if not is_template:
        if pdf_anchors == 0:
            errors.append(
                f"{pack_dir.name}: pack must cite at least one verified corpus/ PDF anchor"
            )
        if code_anchors == 0:
            errors.append(
                f"{pack_dir.name}: pack must cite at least one verified Lean/code anchor"
            )
    return errors


def resolve_style_linter(arg_path: str | None, require_style: bool) -> pathlib.Path | None:
    candidate = (
        pathlib.Path(arg_path)
        if arg_path
        else pathlib.Path(os.environ.get("ARO_STYLE_LINTER", str(DEFAULT_STYLE_LINTER)))
    )
    if candidate.is_file():
        return candidate
    if require_style:
        raise FileNotFoundError(f"Required style linter not found: {candidate}")
    return None


def _write_two_page_pdf(path: pathlib.Path) -> None:
    try:
        import pypdf  # type: ignore[import-not-found]

        writer = pypdf.PdfWriter()
        writer.add_blank_page(width=200, height=200)
        writer.add_blank_page(width=200, height=200)
        with path.open("wb") as fh:
            writer.write(fh)
        return
    except Exception:
        pass
    # Minimal valid 2-page PDF fallback
    path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n"
        b"2 0 obj<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>endobj\n"
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] >>endobj\n"
        b"4 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] >>endobj\n"
        b"xref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n"
        b"0000000058 00000 n \n0000000120 00000 n \n0000000190 00000 n \n"
        b"trailer<< /Size 5 /Root 1 0 R >>\nstartxref\n260\n%%EOF\n"
    )


def _build_fake_repo(base: pathlib.Path) -> tuple[pathlib.Path, set[str], set[str]]:
    (base / "corpus").mkdir(parents=True)
    _write_two_page_pdf(base / "corpus/demo.pdf")
    _write_two_page_pdf(base / "corpus/unregistered.pdf")
    (base / "corpus/MANIFEST.md").write_text(
        f"{'0' * 64}  corpus/demo.pdf\n", encoding="utf-8"
    )
    (base / "verification/lean/manifests").mkdir(parents=True)
    (base / "verification/lean/manifests/expected-theorems-v2.json").write_text(
        json.dumps({"targets": [{"declaration": "BridgeFormalV2.Proofs.expansion"}]}),
        encoding="utf-8",
    )
    (base / "verification/lean/BridgeFormalV2/Proofs").mkdir(parents=True)
    (base / "verification/lean/BridgeFormalV2/Proofs/Dynamics.lean").write_text(
        "theorem expansion : True := trivial\n", encoding="utf-8"
    )
    (base / "research/guides").mkdir(parents=True)
    return base, load_known_corpus_files(base), load_known_lean_decls(base)


def _write_valid_fake_pack(pack_dir: pathlib.Path) -> None:
    pack_dir.mkdir(parents=True, exist_ok=True)
    (pack_dir / "01-intuition-and-map.md").write_text(
        "# Тема\n\n"
        "## Раздел 1\n\n"
        "<!--\n## Hidden\n-->\n\n"
        "Ссылки: [demo][PDF  ref], [якорь](#раздел-1). "
        "Код-пример `[ignored](does-not-exist.md)`.\n\n"
        "[pdf ref]: ../../../corpus/demo.pdf#page=1-2\n\n"
        "```mermaid\nflowchart LR\n    A[\"x\"] --> B[\"y\"]; B --> C[\"z\"];\n```\n\n"
        "Формула $x = 1$, блок $$\\begin{aligned} a &= b \\\\ c &= d \\end{aligned}$$.\n",
        encoding="utf-8",
    )
    for fn in REQUIRED_FILES[1:]:
        (pack_dir / fn).write_text(
            "# Тема\n\nОпора: `BridgeFormalV2.Proofs.expansion`.\n",
            encoding="utf-8",
        )


def run_self_test(repo_root: pathlib.Path, style_linter: pathlib.Path | None) -> int:
    # Positive check on real Packet-01
    real_corpus = load_known_corpus_files(repo_root)
    real_lean = load_known_lean_decls(repo_root)
    real_pack = repo_root / "research/guides/01-bridge-packet-01"
    _expect(real_pack.is_dir(), "Missing 01-bridge-packet-01 for self-test")
    real_errs = check_pack(real_pack, repo_root, real_corpus, real_lean, style_linter)
    _expect(real_errs == [], f"Real Packet-01 failed self-test: {real_errs}")

    passed = 0
    skipped: list[str] = []

    with tempfile.TemporaryDirectory(prefix="aro-guides-selftest-") as tmp:
        fake_root, fake_corpus, fake_lean = _build_fake_repo(pathlib.Path(tmp) / "repo")
        _expect("corpus/demo.pdf" in fake_corpus, "fake corpus load")
        _expect("expansion" in fake_lean, "fake lean load")

        # Positive check on isolated fake pack (reference link + #anchor + #page=1-2 + inline code)
        good_pack = fake_root / "research/guides/01-good"
        _write_valid_fake_pack(good_pack)
        good_errs = check_pack(good_pack, fake_root, fake_corpus, fake_lean, None)
        _expect(good_errs == [], f"Valid fake pack failed: {good_errs}")

        # N1: missing required file
        p1 = fake_root / "research/guides/n1-missing"
        _write_valid_fake_pack(p1)
        (p1 / "04-practice-and-attestation.md").unlink()
        e1 = check_pack(p1, fake_root, fake_corpus, fake_lean, None)
        _expect(any("missing required guide file" in e for e in e1), f"N1 failed: {e1}")
        passed += 1

        # N2: broken relative link inside repo
        p2 = fake_root / "research/guides/n2-broken-link"
        _write_valid_fake_pack(p2)
        (p2 / "04-practice-and-attestation.md").write_text(
            "BridgeFormalV2.Proofs.expansion [bad](no-such-file.md)\n", encoding="utf-8"
        )
        e2 = check_pack(p2, fake_root, fake_corpus, fake_lean, None)
        _expect(any("broken anchor link" in e for e in e2), f"N2 failed: {e2}")
        passed += 1

        # N3: link escaping repository root
        p3 = fake_root / "research/guides/n3-escape"
        _write_valid_fake_pack(p3)
        (p3 / "04-practice-and-attestation.md").write_text(
            "BridgeFormalV2.Proofs.expansion [esc](../../../../../etc/hosts)\n",
            encoding="utf-8",
        )
        e3 = check_pack(p3, fake_root, fake_corpus, fake_lean, None)
        _expect(any("escapes repository root" in e for e in e3), f"N3 failed: {e3}")
        passed += 1

        # N4: unregistered corpus PDF
        p4 = fake_root / "research/guides/n4-unregistered-pdf"
        _write_valid_fake_pack(p4)
        (p4 / "02-propositions-and-chains.md").write_text(
            "BridgeFormalV2.Proofs.expansion [ghost](../../../corpus/unregistered.pdf)\n",
            encoding="utf-8",
        )
        e4 = check_pack(p4, fake_root, fake_corpus, fake_lean, None)
        _expect(any("PDF not registered" in e for e in e4), f"N4 failed: {e4}")
        passed += 1

        # N5: unused [PDF] def, HTML attr with '>' (`title="x > [PDF]"`), & indented code blocks
        # immediately after ATX heading, thematic break, fenced block, and blank line
        p5 = fake_root / "research/guides/n5-no-pdf"
        _write_valid_fake_pack(p5)
        (p5 / "01-intuition-and-map.md").write_text(
            "# Тема\n"
            "    [PDF]\n"
            "---\n"
            "    [PDF]\n"
            "<span title=\"x > [PDF]\">text</span>\n\n"
            "    [PDF]\n\n"
            "```mermaid\nflowchart LR\n    A[\"x\"] --> B[\"y\"]\n```\n"
            "    [PDF]\n\n"
            "[PDF]: ../../../corpus/demo.pdf\n",
            encoding="utf-8",
        )
        e5 = check_pack(p5, fake_root, fake_corpus, fake_lean, None)
        _expect(any("at least one verified corpus/ PDF anchor" in e for e in e5), f"N5: {e5}")
        passed += 1

        # N6: unknown Lean declaration
        p6 = fake_root / "research/guides/n6-fake-lean"
        _write_valid_fake_pack(p6)
        (p6 / "02-propositions-and-chains.md").write_text(
            "BridgeFormalV2.Proofs.fake_thm\n", encoding="utf-8"
        )
        e6 = check_pack(p6, fake_root, fake_corpus, fake_lean, None)
        _expect(any("unknown Lean declaration" in e for e in e6), f"N6 failed: {e6}")
        passed += 1

        # N7: broken Markdown #anchor (incl. closed & unclosed HTML comment), bad PDF #page, refs
        p7 = fake_root / "research/guides/n7-fragments-and-refs"
        _write_valid_fake_pack(p7)
        (p7 / "02-propositions-and-chains.md").write_text(
            "# Тема\n\nBridgeFormalV2.Proofs.expansion\n\n<!--\n## UnclosedHidden\n",
            encoding="utf-8",
        )
        (p7 / "03-traps-and-counterexamples.md").write_text(
            "BridgeFormalV2.Proofs.expansion\n"
            "[bad anchor](01-intuition-and-map.md#no-such-heading)\n"
            "[hidden anchor](01-intuition-and-map.md#hidden)\n"
            "[unclosed hidden](02-propositions-and-chains.md#unclosedhidden)\n"
            "[bad page](../../../corpus/demo.pdf#page=99)\n"
            "[bad ref use][missing-ref]\n"
            "[broken-def]: no-such-ref-target.md\n",
            encoding="utf-8",
        )
        e7 = check_pack(p7, fake_root, fake_corpus, fake_lean, None)
        _expect(any("#no-such-heading" in e for e in e7), f"N7a anchor: {e7}")
        _expect(any("#hidden" in e for e in e7), f"N7b hidden HTML comment heading: {e7}")
        _expect(any("#unclosedhidden" in e for e in e7), f"N7c unclosed HTML comment: {e7}")
        _expect(any("exceeds page count" in e for e in e7), f"N7d pdf page: {e7}")
        _expect(any("unresolved reference-style link" in e for e in e7), f"N7e ref use: {e7}")
        _expect(any("broken anchor link -> no-such-ref-target.md" in e for e in e7), f"N7f: {e7}")
        passed += 1

        # N8: LaTeX syntax errors including reversed order & interleaved \[ \) x \( \]
        _expect(bool(check_latex("$$ x = 1\n", "t")), "N8a unbalanced $$")
        _expect(bool(check_latex("$$\\begin{aligned} x = 1$$", "t")), "N8b unclosed begin")
        _expect(bool(check_latex("Broken $x + 1 math", "t")), "N8c unbalanced $")
        _expect(bool(check_latex(r"\[ x = 1", "t")), "N8d unclosed \\[")
        _expect(bool(check_latex(r"\] x = 1 \[", "t")), "N8e reversed \\] ... \\[")
        _expect(bool(check_latex(r"\) x = 1 \(", "t")), "N8f reversed \\) ... \\(")
        _expect(bool(check_latex(r"\[ \) x \( \]", "t")), "N8g interleaved \\[ \\) x \\( \\]")
        _expect(bool(check_latex(r"$x = {1$", "t")), "N8h unclosed brace")
        _expect(bool(check_latex(r"$x = 1}$", "t")), "N8i unmatched brace")
        _expect(
            check_latex("$$a \\\\\\\\$$", "t") == [],
            "N8j double backslash before $$ must be valid",
        )
        passed += 1

        # N9: Mermaid errors (header, HTML, quotes, brackets, dangling arrows incl. `;`, missing)
        _expect(bool(check_mermaid([("mermaid", "gantt\n    title bad")], "t", True)), "N9a")
        _expect(
            bool(check_mermaid([("mermaid", 'flowchart LR\n    A["x<br>y"] --> B["z"]')], "t", 1)),
            "N9b",
        )
        _expect(
            bool(check_mermaid([("mermaid", 'flowchart LR\n    A["unclosed] --> B["z"]')], "t", 1)),
            "N9c",
        )
        _expect(
            bool(check_mermaid([("mermaid", 'flowchart LR\n    A["x" --> B["z"]')], "t", 1)),
            "N9d",
        )
        _expect(
            bool(check_mermaid([("mermaid", 'flowchart LR\n    A["x"] -->')], "t", True)),
            "N9e dangling trailing arrow",
        )
        _expect(
            bool(check_mermaid([("mermaid", 'flowchart LR\n    A["x"] -->;')], "t", True)),
            "N9f dangling arrow before semicolon",
        )
        _expect(
            bool(check_mermaid([("mermaid", 'flowchart LR\n    A["x"] -->|"lbl"|')], "t", True)),
            "N9g dangling labeled arrow",
        )
        _expect(
            bool(check_mermaid([("mermaid", 'flowchart LR\n    --> B["y"]')], "t", True)),
            "N9h dangling leading arrow",
        )
        _expect(bool(check_mermaid([], "t", True)), "N9i missing diagram")
        _expect(bool(check_mermaid([("__unclosed__", "abc")], "t", False)), "N9j unclosed fence")
        passed += 1

        # N10: style linter JSON list finding MUST fail the gate
        stub_linter = pathlib.Path(tmp) / "stub_style_linter.py"
        stub_linter.write_text(
            "import json, sys\n"
            "print(json.dumps([{'line': 1, 'rule': 'rhetorical-negation', 'excerpt': 'bad'}]))\n"
            "sys.exit(1)\n",
            encoding="utf-8",
        )
        e10 = run_style_linter(good_pack / "01-intuition-and-map.md", "stub", stub_linter)
        _expect(any("style finding [rhetorical-negation]" in e for e in e10), f"N10 failed: {e10}")
        passed += 1

        # N11: real RU style linter rejects rhetorical negation (or explicitly reported skipped)
        if style_linter is not None:
            bad_ru = pathlib.Path(tmp) / "bad_ru.md"
            bad_ru.write_text(
                "Метод не требует обратимости матрицы, но ограничен стационарной динамикой.\n",
                encoding="utf-8",
            )
            e11 = run_style_linter(bad_ru, "bad_ru.md", style_linter)
            _expect(any("style finding" in e for e in e11), f"N11 real RU linter: {e11}")
            passed += 1
        else:
            skipped.append("N11 real RU style linter")

    skip_note = f" ({', '.join(skipped)} skipped via --no-style)" if skipped else ""
    print(
        f"GUIDES G5 SELF-TEST OK: {passed}/{passed} negative controls rejected{skip_note} "
        "(structure/links/escape/PDF/no-PDF/Lean/fragments+refs/LaTeX-order/Mermaid-arrows/style)"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style-linter", default=None)
    parser.add_argument("--no-style", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    style_linter = (
        None
        if args.no_style
        else resolve_style_linter(args.style_linter, require_style=True)
    )

    if args.self_test:
        return run_self_test(ROOT, style_linter)

    known_corpus = load_known_corpus_files(ROOT)
    known_lean = load_known_lean_decls(ROOT)

    packs = sorted(
        d for d in GUIDES_ROOT.iterdir() if d.is_dir() and d.name not in SKIP_DIRS
    )
    if not packs:
        print(
            "GUIDES G5 FAILED: no active guide packs found under research/guides/",
            file=sys.stderr,
        )
        return 1

    all_errors: list[str] = []

    guides_readme = GUIDES_ROOT / "README.md"
    if not guides_readme.is_file():
        all_errors.append("research/guides/README.md: missing guides index")
    else:
        readme_errs, _, _ = check_markdown_file(
            guides_readme,
            "research/guides/README.md",
            ROOT,
            known_corpus,
            known_lean,
            style_linter,
        )
        all_errors.extend(readme_errs)

    template_dir = GUIDES_ROOT / "TEMPLATE"
    if not template_dir.is_dir():
        all_errors.append("research/guides/TEMPLATE: missing template directory")
    else:
        all_errors.extend(
            check_pack(
                template_dir,
                ROOT,
                known_corpus,
                known_lean,
                style_linter,
                is_template=True,
            )
        )

    for pack in packs:
        all_errors.extend(check_pack(pack, ROOT, known_corpus, known_lean, style_linter))

    if all_errors:
        print("GUIDES G5 FAILED:", file=sys.stderr)
        for err in all_errors:
            print("  -", err, file=sys.stderr)
        return 1

    print(
        f"GUIDES G5 OK: {len(packs)} active pack(s) verified "
        f"({', '.join(p.name for p in packs)}) + TEMPLATE + README — "
        "4-file schema, 100% anchor-lint, LaTeX, Mermaid, and RU technical style clean"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
