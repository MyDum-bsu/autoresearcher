# Original-source comparison for wave 3

## Disposition and reading boundary

Two selections, both closed as first-success routes: unrestricted fixed-normal embedding (W3-S1) and the inherited D2 template's realizable residual class (W3-S2). No claim that the general fixed-normal/grouped classification problem is solved in the literature, and no claim of a remaining literature gap. Source closure here is a scoped research disposition, not an LLM mathematical or novelty verdict. General deductions are written reconstructions awaiting checking if ever used scientifically.

Physical PDF pages below are one-indexed. Full PDF hashes, reading modality, page counts and exact short anchors are in source-manifest.json. All new downloads/extracts/renders stay under artifacts/goal/wave-3/sources. Old PDFs remain read-only and are not admitted to a live corpus. Search records are discovery metadata, never mathematical evidence.

## A4 — N. M. Dmitruk, multiple closure strategy (2022)

Original research/sources/A4.pdf, physical pp2–4, printed pp67–69, newly extracted directly in this wave. Equations (1.1)–(1.3) specify stationary real linear dynamics, fixed control/disturbance boxes, robust terminal constraints and worst signed terminal linear cost. On physical p3 the source explicitly computes directional disturbance estimates and the tightened terminal set; these are not a novel wave-3 support-function observation. On physical p4 the block sets allow all disturbances taking values in the same W at each block time. Assumption 1 orders exact state measurement BEFORE selection of that block's open-loop program.

Short anchors: p2 `x(t + 1) = Ax(t) + Bu(t) + M w(t)`; p3 `линейного терминального критерия качества`; p4 `измерить текущее состояние`.

Comparison: the campaign's supplied finite correlated complete-path sets and rational time-varying matrices are an explicit different model. The D2 template is anchored in the actual campaign data, not claimed to be the printed A4 numerical instance. No alteration of A4's disturbance availability is silently attributed to Dmitruk. A4's box-support tightening already demonstrates why treating each terminal-row offset as an independent free parameter is not automatic for a prescribed channel.

## H1 — Olof Hanner (1956), Intersections of translates of convex bodies

Original published article, Mathematica Scandinavica 4, pp65–87, DOI 10.7146/math.scand.a-10456. Acquired PDF has 23 physical pages. Physical pp1–2 (printed pp65–66) were visually read from new page renders. The PDF is scanned: pdftotext yielded page separators only; Tesseract OCR files are auxiliary searchable derivatives, not substitutes for the visually inspected statement. Pages 3–4 were rendered/OCRed during preparation but no mathematical reading or reliance on them is claimed. The whole proof was not read.

The opening defines a convex body as a compact real convex set with interior. It defines I(K) as the smallest m for which m translates pairwise meet but have empty total intersection, infinity if none. Main Theorem A: I(K) is 3, 4 or infinity. Main Theorem B: I(K)>3 iff K is a convex polyhedron, centrally symmetric, and every two disjoint faces lie in distinct parallel supporting planes. Main Theorem C on p2 states I(K)=infinity iff K is a parallelepiped, attributed there to B. v. Sz. Nagy. We inspected Hanner's published statement; the earlier Nagy original was not acquired and is not represented as freshly read.

Short exact anchors in the printed page images: p1 `K is centrally symmetric, and`; p2 `if and only if K is a parallelepiped`. The Main Theorem is on p1 with continuation on p2. OCR normalization can check these fragments but cannot certify its mathematics.

Comparison: a triangle fails central symmetry, so the theorem already covers the elementary existence of a three-translate pairwise obstruction. D2 with singleton suffixes has exactly translated triangles before clipping, with a common box afterward. Hanner does NOT claim arbitrary translated intersections remain translates after box clipping, nor that I(K) is a Helly number. It is the minimum obstruction size, not a maximum minimal-obstruction size. The old D2 rational witnesses separately handle the box and actual dynamics placement. Hanner's p2 paragraph announces homotheties in section 6; since section 6 was not inspected, we do NOT use its result to assert a theorem about all variable-size D2 triangles. No positive-circuit or grouped-prefix formula is imported from Hanner.

## Z1 — Zhen, den Hertog and Sim, inspected 2018 author manuscript

Original corpus/21_Zhen_denHertog_Sim_2018.pdf, freshly extracted physical pp7–8, printed manuscript pp6–7. Algorithm 1 eliminates one bounded adjustable variable by pairing its upper and lower constraints, retaining zero-coefficient rows. Theorem 1 states `X = X` with the eliminated-variable superscript; the following proof reconstructs the eliminated variable as a convex combination of the maximum lower and minimum upper bounds. On p8 the manuscript explicitly says the elimination can be repeated for all linear adjustable variables.

Short anchors: p7 `Algorithm 1 Fourier-Motzkin Elimination for two-stage problems.`; p7 `Theorem 1.`; p8 `one can repeatedly apply Algorithm 1`.

Comparison: generic exact elimination of a common-continuation residual LP is already available. To transfer the algebra, stack ALL actual suffix rows belonging to one observed cell under ONE variable b before eliminating it. The uncertainty-dependent function y(z) in the source does not authorize dependence on the campaign's hidden prefix or suffix. The paper does not by the inspected theorem characterize our max-closure of a frozen disturbance image; our at-most-one-witness-per-row observation is elementary and not an established scientific delta from it. No final-journal page equivalence is claimed for this manuscript.

## DL — De Loera, La Haye, Oliveros and Roldan-Pensado (2015)

Original arXiv:1508.02380v1, Helly numbers of algebraic subsets of R^d, old goal-local PDF read through its original direct extraction on physical pp1–3; a fresh pp1–3 extraction is included in this wave's packet. Physical p1 states ordinary convex Helly; p2 defines the Helly number and explicitly gives h(F^d)=d+1 for any subfield F of R. Physical p3 states the one-dimensional bound at most two. These are background within this original research paper, not its new contribution. Historical Helly/Radon originals were not read here.

Short anchor p2 `any subfield of R`. This supplies a generic rational planar upper bound for finite convex residuals, not a sharp dynamics-restricted improvement. For families smaller than the claimed Helly number, individual/full small-family feasibility must be included; no vacuity shortcut is allowed. No need to reprove interval or coordinate-product geometry for first success.

## Focused discovery record and unavailable leads

One Searcharvester query returned no tool output; it establishes nothing about literature coverage. A Google request returned a script/challenge page. A distinct arXiv API request for the exact phrase Helly dimension ended with RemoteDisconnected; the error was saved. Crossref title discovery returned Hanner, Kincses's classification of 3- and 4-Helly-dimensional bodies, and Baladze–Boltyanskii's Belt bodies and Helly dimension. These latter papers were not acquired/read; no theorem is attributed to them and no priority claim is made.

The Crossref Hanner `article/view/2863/2862` link returned HTML, not PDF. Following the journal's actual landing-page citation_pdf_url (the distinct `article/download/2863/2862` endpoint) obtained the published scan. The HTML response and landing metadata are preserved; no blind retry of a failed command, insecure TLS, proxy change, credential, package install or provider fallback was used. This is direct source acquisition, not external-system testing.

A dedicated sharp fixed-normal positive-dependence/grouped-infeasibility classification was not acquired. That limits any broad literature conclusion. It does not block rejection of an elementary embedding or of a template refinement that already retains the familiar triangle obstruction. No unexplored lead is renamed an open gap, and no positive target is selected on search silence.

## Selection record

| Selection | Mechanism | Source-to-model comparison | Disposition |
|---|---|---|---|
| W3-S1 | Arbitrary RHS families via erased prefixes and independent terminal disturbance coordinates | Actual common-matrix LPs contain the generic geometry; Z1 already gives exact elimination | Elementary embedding/reconstruction; no proof target |
| W3-S2 | Max-closure of the existing D2 row-image plane | Fixed q=1 bounds triangle scale but retains scale-1 translate obstruction; H1 covers its familiar geometric mechanism, DL supplies only the generic upper bound | Genuine template restriction, no non-elementary compatibility delta; no proof target |

No mathematical experiments ran. No finite test establishes any universal characterization written in realizability.md. Source identity/delivery checks are the only new executable checks in this wave and are explicitly non-scientific.
