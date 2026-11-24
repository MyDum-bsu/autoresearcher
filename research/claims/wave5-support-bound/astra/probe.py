"""Fixed four-case support calculations; not a universal theorem checker."""
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'goal/wave-4'))
import m0_check as m0

sys.set_int_max_str_digits(20000)
parents = {}
def read(rel):
    p = ROOT / rel
    raw = p.read_bytes()
    parents[rel] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)

rows = []
for name in ('a4_printed', 'a4_reconstructed_decimal'):
    base = 'artifacts/goal/wave-4/pilot/'
    inp = read(base + 'inputs/' + name + '.json')
    old = read(base + name + '-m0-open-loop.json')
    cert = old['certificate']
    checked = m0.check_certificate(inp, cert)
    bad = dict(cert, objective='0/1')
    try:
        m0.check_certificate(inp, bad)
    except m0.CheckError:
        rejected = True
    else:
        raise ValueError('Corrupted objective accepted')
    dyn = m0.evaluate_dynamics(inp['dynamics'], list(map(F, cert['controls'])), F(inp['constraints']['disturbance_abs_bound']))
    lam, mu = (F(cert['multipliers'][k]) for k in ('lower', 'upper'))
    beta = F(inp['constraints']['control_abs_bound'])
    for r in (67, 104):
        wave4 = read(base + name + '-r' + str(r) + '/certificate.json')
        cols = dyn['columns'][r:]
        hx = beta * sum(abs(x) for x, y in cols)
        hy = beta * sum(abs(y) for x, y in cols)
        hm = beta * sum(abs(y + (lam - mu)*x) for x, y in cols)
        delta = (lam + mu)*hx + hy - hm
        if delta < 0:
            raise ValueError('Negative support defect')
        common = all(x*y >= 0 for x, y in cols)
        corner = [F(1) if x >= 0 else F(-1) for x, y in cols]
        good = all(x*b >= 0 and y*b >= 0 for (x,y),b in zip(cols,corner))
        corner[-1] *= -1
        invalid = not all(x*b >= 0 and y*b >= 0 for (x,y),b in zip(cols,corner))
        if not invalid:
            raise ValueError('Reversed-corner control did not fail')
        rows.append(dict(case=name+'-r'+str(r), m0_valid=checked['certificate_validity'],
            m0_objective=cert['objective'], multipliers=cert['multipliers'],
            delta=str(delta), delta_display=float(delta), zero_defect=delta==0,
            common_xy_corner=common, corner_checked=good, invalid_corner_rejected=invalid,
            invalid_objective_rejected=rejected, suffix_opposite_sign_times=[r+i for i,(x,y) in enumerate(cols) if x*y<0],
            robust_terminal_x=checked['robust_terminal_x'], wave4_fields=sorted(wave4)))
for rel in ('research/sources/A4.pdf','goal/wave-4/m0_check.py','goal/wave-5/astra/contract.md','goal/wave-5/astra/probe.py'):
    parents[rel] = hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
print(json.dumps(dict(scope='four fixed cases; reused M0 arithmetic; general argument not checked', rows=rows, sha256=parents), indent=2))
