"""Summarize observed outcomes, retaining the incomplete C2 and original fixture error."""
import json, re, shutil
from pathlib import Path
from replay import ROOT, OUT, load, save, sha, require, run

audit=load('artifacts/bridge/formal-v2/final-review/theorem-audit.json')
require(audit['target_count']==10,'incomplete expected inventory')
for target in audit['targets']:
    require(target['compiler_exit']==0 and bool(target['axioms']),'failed/empty theorem evidence')
    require(set(target['axioms'])<= {'propext','Classical.choice','Quot.sound'},'forbidden axiom')
pre=load('artifacts/bridge/formal-v2/final-review/preflight.json')
post=load('artifacts/bridge/formal-v2/final-review/postflight.json')
require(pre['identity_checks']==post['identity_checks'],'readonly input changed during review')
controls=load('artifacts/bridge/formal-v2/final-review/controls-execution.json')
for name in ('C1','C3','C4','C6'):
    require(controls[name]['exit_code']==0,name+' did not compile')
require(controls['C2']['exit_code']==1,'C2 outcome changed')
require('Unknown constant `Set.eq_empty_iff_forall_not_mem.mpr`' in (OUT/'control-c2.stdout').read_text(),'C2 failure reason changed')
for name,marker in [('C5','Type mismatch'),('C6Negative','Tactic `rfl` failed')]:
    text=(OUT/('control-'+name.lower()+'.stdout')).read_text()
    require(controls[name]['exit_code']==1 and not controls[name]['import_failure'],'invalid rejection '+name)
    require(marker in text and ('c4Reject' if name=='C5' else 'c6Impossible') in text,'unverified rejection reason')
    controls[name]['status']='expected-rejection-confirmed'
controls['C2']['status']='failed-control-implementation'
controls['C2']['mathematical_conclusion']='not-checked'
controls['C2']['reason']='Unknown auxiliary Set lemma at C2.lean:8; no import failure and no mathematical rejection.'
receipts={p.name:json.loads(p.read_text()) for p in OUT.glob('*.json') if p.name.startswith(('replay-','control-')) and 'command' in json.loads(p.read_text())}
minimum=min(r['minimum_free_bytes'] for r in receipts.values())
require(minimum>=600*1024**2,'disk reserve violated')
style=run('briefing-style',['python3','-B',str(Path.home() / '.agents/skills/technical-style-editor/scripts/lint_technical_style.py'),str(ROOT/'reports/briefings/2026-11-13-ogu-aro-formal-v2.md'),'--language','ru','--extended'])
result=dict(task_id='aro-discovery-k4t',review_status='partial',
    exact_target_replay=dict(completed=10,missing=0,expanded_types_and_axioms='replay-inventory.stdout:3319-3371',allowed_axioms=['propext','Classical.choice','Quot.sound']),
    frozen_identities_unchanged=True,unique_identity_checks=len(pre['identity_checks']),fresh_import_modules=3318,
    controls=controls,failed_scaffold=dict(file='ControlData.lean',exit_code=1,reason='Concrete fixture dependent-type elaboration; preserved, not intentional rejection',replacement='ControlFixture.lean (exit 0); no reviewed source/proof change'),
    incomplete_controls=['C2'],not_run_controls=[],missing_nodes=['F3','F4'],unrestricted_source_policy_comparison='unproved',
    whole_transfer_accepted=False,live_scientific_status_changed=False,attestation=False,novelty_claim=False,
    dependency_source_rebuild='not-run',comparator='not-run; no isolation bypass',
    minimum_observed_free_bytes=minimum,disk_reserve_bytes=600*1024**2,
    actual_billing='unknown',provider_native_retries='unknown',full_os_containment='not-established',
    briefing_style_exit=style,prior_histories='readonly; scoped seals/imports rechecked before and after',
    next_action='No automatic repair/continuation; C2 and separate F3/F4/source-policy obligations require a new explicit assignment.')
save('validation.json',result)
lines=['# Independent formal-v2 final replay','',
'C2 is incomplete: the control implementation failed at an unknown auxiliary Set lemma. F3/F4 and unrestricted-source-policy comparison remain unproved. Whole-transfer acceptance is false.','',
'All ten exact frozen prerequisite/F1/F2 targets were freshly compiled with exit 0. Expanded goal types and nonempty transitive axiom outputs were inspected; each uses only propext, Classical.choice and Quot.sound. No reviewed mathematical source or proof was changed.','',
'## Evidence and reproduction','',
'- `timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/replay.py replay`: exit 0; fresh Model, Goals, Dynamics, Policies and exact Inventory compilation.',
'- `timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/make_controls.py`: driver exit 0, distinct compiler results below; not an all-controls pass.',
'- `timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/replay.py identities`: exit 0; identical pre/post frozen inputs.',
'- Operation IDs are one-shot: existing receipt labels refuse rerun. A future reproduction must use a separately authorized new evidence directory rather than overwrite this history.',
'- `theorem-audit.json` and `replay-inventory.stdout:3319-3371`: actual printed types and transitive axioms, not author booleans.',
'- `actual-import-closure.json`: 3318 fresh compiler-reported imports and their source/binary identities; no dependency rebuild/source-binary reproducibility claim.',
'- `preflight.json` / `postflight.json`: 13286 unique file identities match; both old 3316/3318 closures, candidate/review/proof seals, exact inventory, binaries and tool identities checked.',
'- Russian owner report: `reports/briefings/2026-11-13-ogu-aro-formal-v2.md`.','',
'## Exact target coverage','',
'All declaration names below have prefix `BridgeFormalV2.Proofs.`; goal names have prefix `BridgeFormalV2.`. Every row has compiler exit 0 and the same permitted foundation set `{propext, Classical.choice, Quot.sound}`. Data assumptions and full per-node claim/remaining-obligation table are in the Russian report.','',
'| Node | Goal | Declaration |','|---|---|---|']
for e in audit['targets']: lines.append('| '+e['node']+' | `'+e['type']+'` | `'+e['declaration']+'` |')
lines+=['','F1 derives the recurrence expansion, prefix split and actual source chronology. F2 constructs both measurable reachable-state/deviation translations, preserves actual controls/trajectories/all signed bounds and equates the two Borel epigraph-level sets. This is not equality with arbitrary unrestricted source strategies, extended-value/attainment, support elimination or a finite vertex/selection theorem.','',
'## Semantic controls','',
'| Control | Compiler result | Interpretation |','|---|---|---|',
'| C1 | 0 | Real continuous fixture, admissible measurable witness, SourceBound and corresponding AROBound at -2 |',
'| C2 | 1 | Failed at `C2.lean:8`: unknown `Set.eq_empty_iff_forall_not_mem.mpr`; empty sourceLevels not checked, not an intended rejection |',
'| C3 | 0 | Two cancelling histories, one observation, arbitrary policy suffix equality under independently varied futures |',
'| C4 | 0 | Rows -2 for all witness terminal states, zero-noise rejection of -3, opposite signed criterion violates -2 |',
'| C5 | 1 expected | Working imports and printed c4Reject, then -2/-3 SourceBound type mismatch at the deliberately false target |',
'| C6 | 0; negative 1 expected | Positive impossibility of incompatible future demands; false construction rejected at suffix/minus equality, not import failure |','',
'The first new `ControlData.lean` fixture also failed elaboration. Its file/output remain immutable. The separately compiled `ControlFixture.lean` makes only concrete fixture Data abbreviations transparent and uses numeric index values; no sealed definitions or reviewed proofs were repaired. C2 was not repaired or rerun. All six declared controls were attempted; no not-run outcome is relabelled as a rejection.','',
'## Remaining coverage and authority','',
'- F3: missing sealed proposition/proof for universal future-box support equivalence, including signed criterion and both terminal directions.',
'- F4: missing finite fixed-recourse reduction and measurable real-state implementation, including relative dimension/degenerate images.',
'- Unrestricted source policies: missing existence/level comparison with the Borel convention; no arbitrary-policy bijection claimed.',
'- C2: incomplete semantic nonvacuity/infeasibility control due to the test implementation error; not a counterexample to the ten checked targets.',
'- No source/proof repair, new scientific theorem, download, global install, full Mathlib build/import, comparator bypass, live journal/blueprint/corpus/glossary/config write, attestation, commit/push, nested worker/workflow or new objective.',
'- Python -B and explicit task-local TMP/cache variables, MATHLIB_NO_CACHE_ON_UPDATE=1, bounded processes and a 600 MiB disk guard were used. Minimum observed free bytes: '+str(minimum)+'. Actual billing/native provider retries/full OS containment remain unknown.',
'- First-scientific-success and whole-transfer acceptance remain unmet. This is a scoped compiler/hash/axiom audit, not a general scientific success flag.','']
(OUT/'report.md').write_text('\n'.join(lines))
index={str(p.relative_to(ROOT)):dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='evidence-index.json'}
brief=ROOT/'reports/briefings/2026-11-13-ogu-aro-formal-v2.md'
index[str(brief.relative_to(ROOT))]=dict(sha256=sha(brief),bytes=brief.stat().st_size)
save('evidence-index.json',dict(files=index,scope='New final-review evidence and the named Russian briefing only. The index does not hash itself.'))
print(json.dumps(dict(review_status='partial',targets=10,incomplete_controls=['C2'],expected_rejections=['C5','C6Negative'],minimum_free_bytes=minimum,missing_nodes=['F3','F4'],evidence_files=len(index),style_exit=style)))
