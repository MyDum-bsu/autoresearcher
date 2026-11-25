.PHONY: verify verify-all verify-migration verify-corpus verify-m0 verify-transfer verify-counterexamples verify-falsifiers verify-lean verify-lean-compile verify-claim verify-atlas verify-literature verify-discovery verify-remote verify-run02 verify-guides verify-learn verify-public-hygiene

PYTHON ?= python3

verify: verify-claim

verify-all: verify-migration verify-corpus verify-m0 verify-transfer verify-counterexamples verify-falsifiers verify-lean verify-claim verify-atlas verify-literature verify-discovery verify-remote verify-run02 verify-guides verify-learn verify-public-hygiene

verify-migration:
	@$(PYTHON) -B verification/gates/verify_baseline.py migration
	@$(PYTHON) -B -O verification/gates/verify_baseline.py migration

verify-corpus:
	@$(PYTHON) -B verification/gates/verify_baseline.py corpus
	@$(PYTHON) -B -O verification/gates/verify_baseline.py corpus

verify-m0:
	@cd verification/oracles/m0 && $(PYTHON) -B -m unittest discover -s pilot/baseline -p 'test_*.py'
	@cd verification/oracles/m0 && $(PYTHON) -B -m unittest discover -s pilot/checkers -p 'test_*.py'
	@cd verification/oracles/m0 && $(PYTHON) -B -O -m unittest discover -s pilot/baseline -p 'test_*.py'
	@cd verification/oracles/m0 && $(PYTHON) -B -O -m unittest discover -s pilot/checkers -p 'test_*.py'

verify-transfer:
	@$(PYTHON) -B -O -c 'import json, subprocess, sys; \
	a = subprocess.check_output(["$(PYTHON)", "-B", "research/claims/bridge-transfer-v1/check.py"], text=True); \
	b = subprocess.check_output(["$(PYTHON)", "-B", "-O", "research/claims/bridge-transfer-v1/check.py"], text=True); \
	(a == b) or sys.exit("normal vs -O stdout mismatch"); \
	d = json.loads(a); \
	(d["status"] == "checks_completed" and len(d["results"]) == 4) or sys.exit("unexpected transfer-v1 summary"); \
	tot = sum(len(r["controls"]) for r in d["results"]); \
	acc = sum(1 for r in d["results"] for c in r["controls"] if c["observation"] == "accepted"); \
	rej = sum(1 for r in d["results"] for c in r["controls"] if c["observation"] == "rejected"); \
	((tot, acc, rej) == (32, 16, 16)) or sys.exit(f"unexpected counts: {(tot, acc, rej)}"); \
	print(f"BRIDGE TRANSFER-V1 OK: 4 cases, {tot} controls ({acc} accepted, {rej} rejected), -B/-O byte-identical")'

verify-counterexamples:
	@$(PYTHON) -B research/counterexamples/D1-baseline/checks/check_candidate_v2.py research/counterexamples/D1-baseline/checks/candidate-v1.json >/dev/null && echo "COUNTEREXAMPLE D1 OK"
	@$(PYTHON) -B research/counterexamples/D2-structured/checks/certificate_check_v2.py >/dev/null && echo "COUNTEREXAMPLE D2-cert OK"
	@$(PYTHON) -B research/counterexamples/D2-structured/checks/trajectory_check_v2.py >/dev/null && echo "COUNTEREXAMPLE D2-traj OK"
	@$(PYTHON) -B research/counterexamples/E-rank1/checks/rank_one_check.py >/dev/null && echo "COUNTEREXAMPLE E-rank1 OK"
	@$(PYTHON) -B research/counterexamples/astra-probe-AS1/checks/check.py >/dev/null && echo "ASTRA PROBE A-S1 (38 checks) OK"
	@$(PYTHON) -B research/counterexamples/O8-sion-gap/checks/check_o8_gap.py >/dev/null && echo "COUNTEREXAMPLE O8-sion-gap (-B) OK"
	@$(PYTHON) -B -O research/counterexamples/O8-sion-gap/checks/check_o8_gap.py >/dev/null && echo "COUNTEREXAMPLE O8-sion-gap (-B -O) OK"
	@$(PYTHON) -B research/counterexamples/O4-supermodular-synergy/checks/check_o4_synergy.py >/dev/null && echo "COUNTEREXAMPLE O4-supermodular-synergy (-B) OK"
	@$(PYTHON) -B -O research/counterexamples/O4-supermodular-synergy/checks/check_o4_synergy.py >/dev/null && echo "COUNTEREXAMPLE O4-supermodular-synergy (-B -O) OK"
	@$(PYTHON) -B research/counterexamples/O1-fullrank-shear-gap/checks/check_o1_shear_gap.py >/dev/null && echo "COUNTEREXAMPLE O1-fullrank-shear-gap (-B) OK"
	@$(PYTHON) -B -O research/counterexamples/O1-fullrank-shear-gap/checks/check_o1_shear_gap.py >/dev/null && echo "COUNTEREXAMPLE O1-fullrank-shear-gap (-B -O) OK"

verify-falsifiers:
	@$(PYTHON) -B -m verification.falsifiers.battery_t1_t7
	@$(PYTHON) -B -O -m verification.falsifiers.battery_t1_t7
	@$(PYTHON) -B -m unittest discover -s verification/falsifiers/tests -p 'test_*.py'
	@$(PYTHON) -B -O -m unittest discover -s verification/falsifiers/tests -p 'test_*.py'

verify-lean:
	@$(PYTHON) -B verification/gates/verify_lean.py --mode=static
	@$(PYTHON) -B verification/gates/verify_lean.py --self-test
	@$(PYTHON) -B -O verification/gates/verify_lean.py --mode=static
	@$(PYTHON) -B -O verification/gates/verify_lean.py --self-test

verify-lean-compile:
	@$(PYTHON) -B verification/gates/verify_lean.py --mode=compile

verify-claim:
	@$(PYTHON) -B verification/gates/verify_claim.py --gate=all
	@$(PYTHON) -B verification/gates/verify_claim.py --self-test
	@$(PYTHON) -B -O verification/gates/verify_claim.py --gate=g2
	@$(PYTHON) -B -O verification/gates/verify_claim.py --self-test

verify-atlas:
	@$(PYTHON) -B research/atlas/verify_atlas.py
	@$(PYTHON) -B research/atlas/verify_atlas.py --self-test
	@$(PYTHON) -B -O research/atlas/verify_atlas.py
	@$(PYTHON) -B -O research/atlas/verify_atlas.py --self-test

verify-literature:
	@$(PYTHON) -B research/literature/verify_literature.py
	@$(PYTHON) -B research/literature/verify_literature.py --self-test
	@$(PYTHON) -B -m unittest discover -s research/literature/tests -p 'test_*.py'
	@$(PYTHON) -B -O research/literature/verify_literature.py
	@$(PYTHON) -B -O research/literature/verify_literature.py --self-test
	@$(PYTHON) -B -O -m unittest discover -s research/literature/tests -p 'test_*.py'

verify-discovery:
	@$(PYTHON) -B research/discovery/verify_discovery.py
	@$(PYTHON) -B research/discovery/verify_discovery.py --self-test
	@$(PYTHON) -B -m unittest discover -s research/discovery/tests -p 'test_*.py'
	@$(PYTHON) -B -O research/discovery/verify_discovery.py
	@$(PYTHON) -B -O research/discovery/verify_discovery.py --self-test
	@$(PYTHON) -B -O -m unittest discover -s research/discovery/tests -p 'test_*.py'

verify-remote:
	@$(PYTHON) -B research/remote/verify_remote.py
	@$(PYTHON) -B research/remote/verify_remote.py --self-test
	@$(PYTHON) -B -O research/remote/verify_remote.py
	@$(PYTHON) -B -O research/remote/verify_remote.py --self-test

verify-run02:
	@$(PYTHON) -B research/discovery/significance_gate.py --self-test
	@$(PYTHON) -B -O research/discovery/significance_gate.py --self-test
	@$(PYTHON) -B research/discovery/run02/run02_falsify.py
	@$(PYTHON) -B -O research/discovery/run02/run02_falsify.py

verify-guides:
	@$(PYTHON) -B verification/gates/verify_guides.py
	@$(PYTHON) -B verification/gates/verify_guides.py --self-test
	@$(PYTHON) -B -O verification/gates/verify_guides.py
	@$(PYTHON) -B -O verification/gates/verify_guides.py --self-test

verify-learn:
	@$(PYTHON) -B -m unittest discover -s learn/tests -p 'test_*.py' -v
	@$(PYTHON) -B -O -m unittest discover -s learn/tests -p 'test_*.py' -v

verify-public-hygiene:
	@$(PYTHON) -B verification/gates/verify_public_hygiene.py
	@$(PYTHON) -B verification/gates/verify_public_hygiene.py --self-test
	@$(PYTHON) -B -O verification/gates/verify_public_hygiene.py
	@$(PYTHON) -B -O verification/gates/verify_public_hygiene.py --self-test
