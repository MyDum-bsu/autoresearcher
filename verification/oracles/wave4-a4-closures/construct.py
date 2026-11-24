"""Wave-4 proposal generator. Floating LP is not the certificate checker."""
import argparse
from fractions import Fraction as F
from functools import cmp_to_key
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

import m0_generator as m0

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'artifacts/goal/wave-4/pilot'


def txt(x):
    return str(x.numerator) + '/' + str(x.denominator)


def save(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def apply(A, v):
    return tuple(sum((a*b for a, b in zip(row, v)), F(0)) for row in A)


def columns(A, v, T):
    out = []
    for _ in range(T):
        out.append(v)
        v = apply(A, v)
    return out[::-1]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def vertices(g):
    oriented = []
    for t, (x, y) in enumerate(g):
        if not (x or y):
            raise ValueError('Zero generator unsupported')
        s = 1 if y > 0 or (y == 0 and x > 0) else -1
        oriented.append((x*s, y*s, t, s))
    def compare(a, b):
        cross = a[0]*b[1]-a[1]*b[0]
        return -1 if cross > 0 else (1 if cross < 0 else 0)
    oriented.sort(key=cmp_to_key(compare))
    for a, b in zip(oriented, oriented[1:]):
        if a[0]*b[1] == a[1]*b[0]:
            raise ValueError('Parallel generators require grouping, not supported here')
    signs = [0]*len(g)
    for _, _, t, s in oriented:
        signs[t] = -s
    v = tuple(sum((a[j]*s for a, s in zip(g, signs)), F(0)) for j in range(2))
    points, realizations = [], []
    for direction in (1, -1):
        for x, y, t, s in oriented:
            points.append(v)
            realizations.append(signs.copy())
            v = (v[0]+2*direction*x, v[1]+2*direction*y)
            signs[t] = direction*s
    if v != points[0]:
        raise ValueError('Zonotope walk did not close')
    return points, realizations


def repair(b, C, base, low, high):
    x = base + sum((c[0]*u for c, u in zip(C, b)), F(0))
    target = min(max(x, low), high)
    need = target-x
    for t, c in enumerate(C):
        if not need:
            break
        cx = c[0]
        if not cx:
            continue
        endpoint = F(1) if need*cx > 0 else F(-1)
        capacity = cx*(endpoint-b[t])
        gain = min(abs(need), abs(capacity)) * (1 if need > 0 else -1)
        b[t] += gain/cx
        need -= gain
    if need or any(abs(u) > 1 for u in b):
        raise ValueError('Exact suffix repair lacks terminal capacity')
    return b


def run(name, r):
    case = f'{name}-r{r}'
    folder = OUT / case
    folder.mkdir(exist_ok=False)
    manifest = m0.parse_input((OUT/'inputs'/f'{name}.json').read_text())
    A = [list(map(F, row)) for row in manifest['dynamics']['A']]
    B, E, d = (tuple(map(F, manifest['dynamics'][k])) for k in ('B', 'E', 'x0'))
    C, D = columns(A, B, 120), columns(A, E, 120)
    for _ in range(120):
        d = apply(A, d)
    V, signs = vertices([tuple(a/F(2) for a in v) for v in D[:r]])
    n, m = 120-r, len(V)
    s = tuple(sum((abs(v[j])/2 for v in D[r:]), F(0)) for j in range(2))
    K = r+m*n
    M = lil_matrix((3*m, K+1))
    rhs = []
    for i, v in enumerate(V):
        for j, sign in ((0, -1), (0, 1), (1, -1)):
            row = len(rhs)
            M[row, :r] = [float(sign*c[j]) for c in C[:r]]
            M[row, r+i*n:r+(i+1)*n] = [float(sign*c[j]) for c in C[r:]]
            if row % 3 == 2:
                M[row, K] = 1
                rhs.append(float(d[1]+v[1]-s[1]))
            elif sign == -1:
                rhs.append(float(d[0]+v[0]-2-s[0]))
            else:
                rhs.append(float(10-s[0]-d[0]-v[0]))
    objective = np.zeros(K+1)
    objective[-1] = -1
    start = time.monotonic()
    result = linprog(objective, A_ub=M.tocsr(), b_ub=rhs,
                     bounds=[(-1, 1)]*K+[(None, None)], method='highs',
                     options={'time_limit': 60})
    proposal = {'case': case, 'elapsed_seconds': time.monotonic()-start,
                'status': int(result.status), 'message': result.message,
                'success_is_not_certification': bool(result.success),
                'variables': K+1, 'rows': 3*m,
                'x': result.x.tolist() if result.x is not None else None,
                'inequality_marginals': result.ineqlin.marginals.tolist()
                if result.ineqlin.marginals is not None else None}
    save(folder/'proposal.json', proposal)
    print(json.dumps({k: v for k, v in proposal.items() if k not in ('x','inequality_marginals')}), flush=True)
    if not result.success:
        raise ValueError('Numerical proposal failed; no retry')
    denom = 10**10
    controls = [F(round(float(u)*denom), denom) for u in result.x[:-1]]
    a = controls[:r]
    base = tuple(d[j]+sum((c[j]*u for c, u in zip(C[:r], a)), F(0)) for j in range(2))
    blocks, rewards = [], []
    for i, v in enumerate(V):
        b = repair(controls[r+i*n:r+(i+1)*n], C[r:], base[0]+v[0], 2+s[0], 10-s[0])
        blocks.append(b)
        rewards.append(base[1]+v[1]+sum((c[1]*u for c, u in zip(C[r:], b)), F(0))-s[1])
    lam = [F(max(0, round(-float(x)*10**12)), 10**12) for x in result.ineqlin.marginals]
    norm = sum(lam[2::3], F(0))
    if norm <= 0:
        raise ValueError('No positive objective-row dual mass')
    lam = [x/norm for x in lam]
    # This producer expression is checked by a separately assembled backward-adjoint route.
    rx = [lam[3*i+1]-lam[3*i] for i in range(m)]
    ry = [-lam[3*i+2] for i in range(m)]
    rhs_exact = []
    for v in V:
        rhs_exact.extend([d[0]+v[0]-2-s[0], 10-s[0]-d[0]-v[0], d[1]+v[1]-s[1]])
    residual = sum((abs(sum(rx,F(0))*c[0]+sum(ry,F(0))*c[1]) for c in C[:r]), F(0))
    residual += sum((abs(rx[i]*c[0]+ry[i]*c[1]) for i in range(m) for c in C[r:]), F(0))
    upper = dot(lam, rhs_exact)+residual
    cert = {'schema': 1, 'case': case, 'r': r, 'input_sha256': m0.validate_input(manifest),
            'contract_sha256': hashlib.sha256((ROOT/'goal/wave-4/contract.json').read_bytes()).hexdigest(),
            'information': 'exact_current_state_then_whole_suffix_no_later_measurements',
            'vertices': [[txt(x) for x in v] for v in V], 'prefix_signs': signs,
            'first_block': list(map(txt,a)), 'suffix_blocks': [list(map(txt,b)) for b in blocks],
            'multipliers': list(map(txt,lam)), 'lower': txt(min(rewards)), 'upper': txt(upper)}
    save(folder/'certificate.json', cert)
    print(json.dumps({'case': case, 'lower_float_display_only': float(min(rewards)),
                      'upper_float_display_only': float(upper), 'gap_float_display_only': float(upper-min(rewards)),
                      'vertices': m, 'certificate_bytes': (folder/'certificate.json').stat().st_size}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', choices=['a4_printed','a4_reconstructed_decimal'])
    parser.add_argument('r', type=int, choices=[67,104])
    args = parser.parse_args()
    run(args.name, args.r)
