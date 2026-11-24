# Session report — 2026-10-20 — essay on exactness of affine decision rules

> Shift type: W (writing) with an L (literature) front half. Language: English
> per charter seq 6554. Russian summary of owner-facing points is in the chat,
> not here.

## Conclusion

A formal survey essay on the exactness of affine decision rules in two-stage
adaptive robust optimization was written, gated, and rendered to PDF. It states
the problem, separates four inequivalent notions of exactness, identifies five
logical mechanisms that produce exactness, gives the sharp negative families,
states eight open problems in settlable form, and proposes a seven-instance
falsification battery. 18 previously unread corpus papers and 3 intake
preprints were read with page anchors as its evidence base.

Deliverables (revision 2: corpus SHA-256 lines removed from the reference list;
Russian edition added):

- `docs/papers/2026-10-20-essay-exactness-and-open-problems.md`
  (SHA-256 `aefa9bcb3de52ee31f6421641d518c74756e38f9b3b96982b52abaf4d770cee0`)
- `docs/papers/2026-10-20-essay-exactness-and-open-problems.pdf`
  (SHA-256 `ffbec776503e6e83409b0eccee610055b1eed921a5a82e821567a760f7f200d4`, 17 pages)
- `docs/papers/2026-10-20-essay-exactness-and-open-problems.ru.md`
  (SHA-256 `f69173c018f2973f0e977ef3233a760aa94749c818b5fb6c076ed42dc59a2f58`)
- `docs/papers/2026-10-20-essay-exactness-and-open-problems.ru.pdf`
  (SHA-256 `6d53f8d1daf9f4fe589c930f17920ceed5bebdd6a7b533673ccb86ad8a3a694b`, 17 pages)

## Findings

**F1. The literature has no necessary-and-sufficient condition for affine
exactness, and the strongest exactness theorem is explicitly one-sided.**
Georghiou–Tsoukalas–Wiesemann 2025, Theorem 1 gives four conditions whose
conjunction is sufficient and minimal, and their Proposition 1 exhibits an
instance violating all four whose optimal policy is nevertheless affine
[GTW25, p. 10]. Status: confirmed from the source.

**F2. Xu–Burer 2017 supplies the correct formulation of the open problem, not a
solution.** Exactness is copositive cone membership; the affine rule is the
inner cone restriction; the sandwich theorem quantifies the space between
[XB17, `theorem:approximaterlp`, arlp.tex:783]. Status: confirmed from the TeX
source.

**F3. Four distinct mechanisms produce exactness, and they are not
interchangeable.** Constraint-wise decomposition [BGT04, Thm. 2.1];
inverse-positive recourse with dominance [GTW25, Thm. 1]; conic restriction
[XB17]; polyhedral barycentric completion [GTW20, Prop. 1 and Prop. 5;
AP16, Lemma 1]. A fifth class-based route exists [BG14; ZDS18]. Status:
confirmed from sources; the *classification* is this essay's construction and is
offered as such.

**F4. Vertex reasoning is insufficient for affine exactness in three independent
ways.** [BGL15, p. 32] gives a convex, vertex-represented, down-monotone set
with arbitrary static gap; [AP16, pp. 5--6] shows vertex reduction preserves the
adaptive optimum but not the affine one and fails under random recourse;
[DH26, pp. 11, 23] shows vertex incidence structure, not the vertex set, is what
matters. Status: confirmed.

**F5. The bridge class is a positive affine-exactness instance that none of the
five mechanisms certifies.** S5 (576 exact LP points, zero gap) asserts affine
exactness; the uncertainty set is the vertex set of a cube (non-simple for
T ≥ 2), the recourse matrix has both signs, and the system is not
constraint-wise. M4 does apply but yields only a piecewise affine rule.
Status: S5 is survived-falsifier (numerically certified), not proved.

**F6. A prior project claim was mis-cited and is corrected in the essay.** The
full-information closed form `max(max(|S|, 2|d0| − (2u_b − |S|)T), |D|T)` is not
a published theorem from the literature: it was derived inside the project and
lives in `scripts/ladder_forms.py`. The wedge law refutes it as an internal
result. Status: confirmed by the 2026-09-28 briefing, which states this
explicitly.

**F7. Two literature-wide gaps are now precisely stated.** There is no
complexity result for choosing *schedules* (as opposed to policy counts K), and
no paper in the read corpus relates the two [Kur25 vs A4/A5]. There is also no
"price of adaptivity" definition for two-stage ARO; the term exists only in
adjacent literatures and that lead is unverified. Status: statement-level
absence claim, scoped to the read corpus.

## Verified

- `pandoc` → `lualatex` build: **0 errors, 0 overfull boxes, 0 missing
  characters**, 17 pages. Two passes for references. Fonts: Latin Modern for
  text and math, DejaVu Sans Mono for paths and hashes (Latin Modern Mono has no
  Cyrillic, which blanked the A1–A5 filenames on the first build).
- Citation resolution: all 30 bracket keys in the body resolve to reference
  entries; no defined entry is uncited.
- Page-anchor discipline: every literature claim carries a file name and a PDF
  page, printed page, or TeX line number. Intake SHA-256 values computed with
  `sha256sum`; manifest hashes cross-checked.
- Russian edition parity: identical heading count (32), identical equation tags
  (2.1, 3.1, 5.1–5.4), identical reference keys (35), identical body citation set
  (24 keys), identical battery table (7 rows). Term base is `docs/GLOSSARY.md`;
  untranslatable terms stay English (plateau, valley, floor, closure set, fixed
  recourse, ADR/LDR, naming of Lean theorems and judge artifacts).
- Both PDF builds: 0 errors, 0 overfull boxes, 0 missing glyphs.
- `technical-style-editor` lint (`--language en`): 10 passages reviewed, 5 stylistic
  contrasts rewritten, 5 remaining flags are technical uses (`suboptimal`,
  mathematical `unique`, a boundary the linter prescribes keeping).
- `make check`: **all steps green except `lean_axioms.py`**, which fails with
  `unknown module prefix 'Mathlib'` because Mathlib has never been built in this
  checkout (`lean/aroform/.lake/packages/mathlib/.lake` is empty; `git status
  lean` clean). Journal intact at 6591 events with a converging chain;
  anchor-lint 0, statement-lint 0, falsify-first 0, blueprint-sync 187 nodes
  0 violations, graph-sync agree, manifest 42 files 0 problems, dual-route 6
  agreed.

## Not covered

- **Lean axiom gate.** Not run to completion: requires a Mathlib build
  (~5 GB) into 7.4 GB free disk at 95% usage. Deliberately not attempted; a
  full disk is a worse failure than a red gate. Remedy:
  `cd lean/aroform && lake exe cache get && lake build`.
- **Visual acceptance by `pdf:visual-judge`.** The subagent provider was
  unavailable (`provider-not-found`). Pages were inspected directly instead;
  the defects found and fixed this way were hash overflow on p. 16, Cyrillic
  filenames rendering as blanks on p. 14–15, and two marginal overfull boxes.
  A genuine visual pass by the dedicated judge is still owed.
- **Recent literature (2023–2026).** Only a leads scan was performed; results
  are parked in `reports/briefings/2026-10-20-essay-literature-leads.md` marked
  UNVERIFIED and are cited nowhere as established. No paper was added to
  `corpus/`.
- **Electronic Companion of Zeng–Zhao 2013.** Not in corpus; that paper is
  statement-level only.
- **Graph registration.** The 18 new reading extracts are proposals
  (`reports/reading/2026-10-20-essay-*.md`); their blocks are **not** registered
  as knowledge nodes. That is a separate L-tick with judge-backed anchors.

## Lesson

Reading for an essay and reading for the graph are different jobs with different
outputs. The essay needed *classification* (which claims are sufficient, which
necessary, which are reformulation-only), and that classification is not
recoverable from the graph's fact/theorem blocks, which record statements
without their logical role. The four-notion distinction in §2.2 came out of
noticing that "exact" meant different things in the copositive, SDP, and vertex
papers; no single paper says this.

## Handoff

- **Branch / commit:** `research/autonomous`, uncommitted. Working tree holds the
  essay (md + pdf), four reading reports, one leads briefing, and gate-written
  journal events 6590–6591 plus `state/science.db`.
- **Done:** survey essay on affine-rule exactness with 8 open problems and a
  falsification battery, built to a clean 17-page PDF.
- **Status changes:** none. No node status was touched; no judge was run for this
  shift's reading.
- **Queue now (top 3):**
  1. Register the 18 essay reading extracts as knowledge blocks (L-tick,
     judge-backed) — they are the evidence base of a submitted document and
     currently exist only as proposals.
  2. O1: state the cone-membership exactness question for the bridge class and
     test whether the IA face admits a certificate there (T-tick on S5).
  3. O4: complexity of schedule selection, using the tail sum (5.4) as the
     decision oracle — the only place in the corpus where the schedule
     objective is closed-form.
- **Blocked:** `make check` on the Lean axiom step (Mathlib unbuilt, disk
  constrained); `pdf:visual-judge` provider unavailable.
- **Next shift:** T — take S5 (full-prefix affine exactness, survived-falsifier)
  and attempt an analytic proof, since it is the load-bearing claim that the
  essay's battery turns on, and its proof route is already identified.
- **Cost:** ~105 M subagent tokens across 5 reading agents (two of them large),
  ~1 h wall clock, ~250 k main-thread tokens.

## Russian summary for the owner

Эссе написано и собрано в PDF (17 страниц, сборка чистая). Главное содержательно:
в литературе нет необходимого и достаточного условия точности аффинных правил;
самая сильная теорема точности (GTW-2025) явно односторонняя; вопрос корректно
формулируется как принадлежность копозитивному конусу (Xu–Burer). Пять
механизмов точности в литературе логически различны, и наш мост-класс не
покрывается ни одним из них — это делает его хорошим тестом. Отдельно исправлена
ошибка атрибуции: «опубликованная форма» полной информации на самом деле наша
собственная формула из `scripts/ladder_forms.py`, и клин-закон её опровергает
внутри себя. Гейт красный ровно в одном месте — Lean-аксиомы, потому что Mathlib
в этом чекауте никогда не собирался; на диске 7.4 ГБ свободно, качать 5 ГБ я не
стал.

## Revision 3 — v2 with Part II, Part III, figures and clickable links

Owner asked for a completeness assessment and a second version: clickable
references, variables explained inside their problem, the state of the art in
theory with theorems, guarantees and conditions, the Dmitruk problem stated, and
the bridge treated mathematically beyond $n=2$ (including A5).

Delivered: `docs/papers/2026-10-20-essay-exactness-v2.md` and `.pdf`
(SHA-256 `fd4251f0...`, `a2385219...`; 23 pages, 10 049 words, 10 sections,
25 subsections, 8 tables, 5 figures, 26 clickable links — 24 DOI verified
against Crossref, 2 arXiv).

Structural changes over v1: Part I (ARO, with a state-of-the-art table by
question rather than by paper), Part II (Dmitruk general theory: model,
polyhedral closing sets, the affine-in-$\alpha$ representation, one LP per
closure, parametric-LP support tracing, approximating sets, the two-sided
a posteriori certificate, cost profile, declared-open schedule), Part III (the
bridge: dictionary table, rotation, ladder ends, wedge figure, schedule figures,
block fold and tail sum, the defect below, and why the class is a test case),
Part IV (eight open problems), the battery, non-coverage, Appendix A (symbols
with the problem each belongs to), Appendix B (verification ledger).

**A defect was found while writing v2 and is reported in the essay (§III.6).**
The project's S2/S3/S4 closed forms were certified on grids in the symmetric
row regime ($e_1=e_2$) and in regimes where the difference floor $|D|T$
dominates. Checked against the exact per-path LP oracle at $T=5$ with
$e=(3/2,1/2)$:

- symmetric rows, $D=0$: 0 mismatches in 4 one-closure points;
- asymmetric rows, $D=1$: 3 mismatches in 4 (LP 9/8/7/8 vs form 8/6/6/8).

The mechanism is the one Part III states: the adversary picks one path, so
$\max_w \max(|s_T|,|D\,W|) \neq \max(\max_w|s_T|, \max_w|D\,W|)$. The
certificates remain valid on their own domain; the general statement in
`docs/THESES.md` is phrased too broadly and should be narrowed. No node status
was changed in this session; the finding is recorded here and in the essay for
the next L/T tick.

Figures are generated by `docs/papers/figs/make_figures.py` from exact rational
LP (`judges/numerical/bridge.py`), not from invented data; the script prints its
cross-check. Note: the script needs the system `python3` for matplotlib, the
project `.venv` has no matplotlib.
