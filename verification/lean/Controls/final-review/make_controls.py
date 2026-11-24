"""Materialize separate frozen semantic control evidence, then execute once per file."""
from pathlib import Path
import json
from replay import OUT, compile_file, save
unfold='Data.sourceTrajectory, Data.prefixState, Data.run, Data.step, Data.blockAt, Data.sourceSuffix, D, B, E, a, pi'
files={
'C1':r'''import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV2.Proofs

def c1Terminal (wm wp : D.NoiseBlock 1) :
    D.sourceTrajectory a pi wm wp 2 =
      fun i => if i = 0 then 2 else wm.val 0 0 + wm.val 0 1 + wp.val 0 0 + wp.val 0 1 := by
  ext i
  fin_cases i <;> simp [UNFOLD] <;> ring

def c1Source : D.SourceBound a pi (-2) := by
  intro wm wp
  rw [show D.r + D.q = 2 from rfl, c1Terminal]
  constructor
  · intro i
    fin_cases i
    · norm_num [D]
    · have h00 := wm.property 0 0
      have h01 := wm.property 0 1
      have h10 := wp.property 0 0
      have h11 := wp.property 0 1
      change (-1 ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1) at h00
      change (-1 ≤ wm.val 0 1 ∧ wm.val 0 1 ≤ 1) at h01
      change (-1 ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1) at h10
      change (-1 ≤ wp.val 0 1 ∧ wp.val 0 1 ≤ 1) at h11
      change -4 ≤ wm.val 0 0 + wm.val 0 1 + wp.val 0 0 + wp.val 0 1 ∧
        wm.val 0 0 + wm.val 0 1 + wp.val 0 0 + wp.val 0 1 ≤ 4
      constructor <;> linarith [h00.1,h00.2,h01.1,h01.2,h10.1,h10.2,h11.1,h11.2]
  · norm_num [D]

example : D.AROBound a y (-2) := by
  have hr : D.Related a pi y := ⟨by intros; rfl, by intros; rfl⟩
  exact ((preserves_of_related D a pi y hr).2.2.2 (-2)).mp c1Source

#print axioms c1Terminal
#print axioms c1Source
end
end FinalReviewControls
''',
'C2':r'''import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data
example : Nonempty (badD.ControlBlock 1) ∧ Nonempty (badD.NoiseBlock 1) :=
  BridgeFormalV2.Proofs.nonempty_blocks badD 1
example : badD.sourceLevels = ∅ := by
  apply Set.eq_empty_iff_forall_not_mem.mpr
  intro eta h
  obtain ⟨a0, policy, hb⟩ := h
  have h5 := ((hb zeroNoise zeroNoise).1 (1 : Fin 2)).1
  norm_num [Data.sourceTrajectory, Data.prefixState, Data.run, Data.step,
    Data.blockAt, badD, D, B, E, zeroNoise, noise] at h5
end
end FinalReviewControls
''',
'C3':r'''import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data
example (policy : D.StatePolicy a) :
    D.sourceSuffix a policy wPlus = D.sourceSuffix a policy wMinus ∧
    (fun (_ : D.NoiseBlock D.q) => D.sourceSuffix a policy wPlus) futurePlus =
      (fun (_ : D.NoiseBlock D.q) => D.sourceSuffix a policy wMinus) futureMinus := by
  have hs : D.prefixState a wPlus = D.prefixState a wMinus := by
    ext i
    fin_cases i <;> norm_num [Data.prefixState, Data.run, Data.step,
      Data.blockAt, D, B, E, a, wPlus, wMinus, noise]
  have he := BridgeFormalV2.Proofs.observation_fibre D a policy wPlus wMinus hs
  exact ⟨he,he⟩
example : futurePlus.val 0 0 = 1 ∧ futureMinus.val 0 0 = -1 := ⟨rfl,rfl⟩
end
end FinalReviewControls
''',
'C4':r'''import C1
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data
example (wm wp : D.NoiseBlock 1) :
    D.Rows (-2) (D.sourceTrajectory a pi wm wp 2) := c1Source wm wp

def c4Reject : ¬ D.SourceBound a pi (-3) := by
  intro h
  have hc := (h zeroNoise zeroNoise).2
  rw [show D.r + D.q = 2 from rfl, c1Terminal] at hc
  norm_num [D] at hc

example : ¬ D.Rows (-3) (D.sourceTrajectory a pi zeroNoise zeroNoise 2) := by
  intro h
  have hc := h.2
  rw [c1Terminal] at hc
  norm_num [D] at hc

example : ¬ positiveD.SourceBound positiveA positivePi (-2) := by
  intro h
  have hc := (h zeroNoise zeroNoise).2
  norm_num [Data.sourceTrajectory, Data.prefixState, Data.run, Data.step,
    Data.blockAt, Data.sourceSuffix, positiveD, positiveA, positivePi, D, B, E,
    a, zeroNoise, noise] at hc
#print axioms c4Reject
end
end FinalReviewControls
''',
'C5':r'''import C4
open FinalReviewControls
#check c4Reject
-- Deliberately false signed-bound target. Imports must succeed first.
example : D.SourceBound a pi (-3) := by
  exact c1Source
''',
'C6':r'''import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data
-- Positive impossibility check for the same observation under independent futures.
def c6Impossible : ¬ ∃ policy : D.StatePolicy a, FutureDemand policy := by
  rintro ⟨policy,h⟩
  have hplus := (h futurePlus).1 (show futurePlus.val 0 0 = 1 from rfl)
  have hminus := (h futureMinus).2 (show futureMinus.val 0 0 = -1 from rfl)
  have he : a = minus := hplus.symm.trans hminus
  have hc : (1 : ℝ) = -1 := congrArg (fun b : D.ControlBlock D.q => b.val 0 0) he
  norm_num at hc
#print axioms c6Impossible
end
end FinalReviewControls
''',
'C6Negative':r'''import C6
open FinalReviewControls
#check c6Impossible
example : ∃ policy : D.StatePolicy a, FutureDemand policy := by
  refine ⟨pi, ?_⟩
  intro wp
  constructor
  · intro _; rfl
  · intro _; rfl
'''
}
plan={
'C1':{'expected':'compile','meaning':'Actual C1 real data, bounded controls/noise, measurable constant witness, SourceBound -2 and corresponding AROBound -2'},
'C2':{'expected':'compile','meaning':'Nonempty uncertainty/controls, nonempty terminal intervals [5,5], empty sourceLevels via zero disturbances'},
'C3':{'expected':'compile','meaning':'Two distinct cancelling prefix histories give equal observation and arbitrary-policy suffix; independently varied futures'},
'C4':{'expected':'compile','meaning':'All terminal Rows -2, zero-disturbance rejection of -3, opposite signed criterion violates -2'},
'C5':{'expected':'reject','meaning':'False -3 target rejected for bound mismatch after imported c4Reject proves zero-disturbance contradiction'},
'C6':{'expected':'compile','meaning':'No single state policy obeys incompatible future-conditioned suffix demands'},
'C6Negative':{'expected':'reject','meaning':'Constant-policy construction of forbidden future demand rejected at incompatible control equality'}
}
for name,content in files.items():
    path=OUT/(name+'.lean')
    if path.exists(): raise RuntimeError('no implicit rerun: '+name)
    path.write_text(content.replace('UNFOLD',unfold))
save('controls-plan.json',plan)
results={}
for name in files:
    dependencies={'C4':['C1'],'C5':['C4'],'C6Negative':['C6']}.get(name,[])
    if any(results[d]['exit_code']!=0 for d in dependencies):
        results[name]=dict(status='not-run',reason='prerequisite control did not compile',dependencies=dependencies,exit_code=None)
        continue
    code=compile_file('control-'+name.lower(),OUT/(name+'.lean'),name)
    stdout=(OUT/('control-'+name.lower()+'.stdout')).read_text()
    stderr=(OUT/('control-'+name.lower()+'.stderr')).read_text()
    import_failure=any(s in stdout+stderr for s in ('unknown module prefix','does not exist','object file','failed to open file','unknown package'))
    expected=plan[name]['expected']
    status='compiled' if code==0 and expected=='compile' else 'failed'
    if expected=='reject' and code!=0 and not import_failure:
        status='rejected-needs-reason-inspection'
    results[name]=dict(status=status,exit_code=code,import_failure=import_failure,expected=expected)
save('controls-execution.json',results)
print(json.dumps(results,indent=2))
