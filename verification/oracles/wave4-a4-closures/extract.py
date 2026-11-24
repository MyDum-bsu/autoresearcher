"""Deliberate exact extraction from preserved LP output; NEVER invokes a solver.

Original generation failed at a saturated suffix after rounding the common prefix.
The changed evidence is that the exact prefix viability interval was omitted.
Repair that interval first. Keep original proposal and raw failure immutable.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import construct as p


def extract(case):
    folder=p.OUT/case
    require_new=folder/'certificate.json'
    if require_new.exists():
        raise ValueError('Refusing to overwrite a certificate')
    proposal=json.loads((folder/'proposal.json').read_text())
    if proposal['status']!=0 or proposal['x'] is None:
        raise ValueError('No usable preserved proposal; no retry')
    name,r=case.rsplit('-r',1)
    r=int(r)
    manifest=p.m0.parse_input((p.OUT/'inputs'/f'{name}.json').read_text())
    A=[list(map(F,row)) for row in manifest['dynamics']['A']]
    B,E,d=(tuple(map(F,manifest['dynamics'][k])) for k in ('B','E','x0'))
    C,D=p.columns(A,B,120),p.columns(A,E,120)
    for _ in range(120):d=p.apply(A,d)
    V,signs=p.vertices([tuple(x/2 for x in v) for v in D[:r]])
    n,m=120-r,len(V)
    sx,sy=(sum((abs(v[j])/2 for v in D[r:]),F(0)) for j in range(2))
    prefix_support=sum((abs(v[0])/2 for v in D[:r]),F(0))
    suffix_capacity=sum((abs(v[0]) for v in C[r:]),F(0))
    u=[F(round(float(x)*10**10),10**10) for x in proposal['x'][:-1]]
    old_a=u[:r]
    a=p.repair(old_a.copy(),C[:r],d[0],2+sx+prefix_support-suffix_capacity,
               10-sx-prefix_support+suffix_capacity)
    base=tuple(d[j]+sum((c[j]*v for c,v in zip(C[:r],a)),F(0)) for j in range(2))
    blocks,rewards=[],[]
    for i,v in enumerate(V):
        b=p.repair(u[r+i*n:r+(i+1)*n],C[r:],base[0]+v[0],2+sx,10-sx)
        blocks.append(b)
        rewards.append(base[1]+v[1]+sum((c[1]*x for c,x in zip(C[r:],b)),F(0))-sy)
    lam=[F(max(0,round(-float(x)*10**12)),10**12) for x in proposal['inequality_marginals']]
    norm=sum(lam[2::3],F(0))
    if norm<=0:raise ValueError('Objective normalization unavailable')
    lam=[x/norm for x in lam]
    rx=[lam[3*i+1]-lam[3*i] for i in range(m)]
    ry=[-lam[3*i+2] for i in range(m)]
    rhs=[]
    for v in V:rhs.extend([d[0]+v[0]-2-sx,10-sx-d[0]-v[0],d[1]+v[1]-sy])
    residual=sum((abs(sum(rx,F(0))*c[0]+sum(ry,F(0))*c[1]) for c in C[:r]),F(0))
    residual+=sum((abs(rx[i]*c[0]+ry[i]*c[1]) for i in range(m) for c in C[r:]),F(0))
    upper=p.dot(lam,rhs)+residual
    cert={'schema':1,'case':case,'r':r,'input_sha256':p.m0.validate_input(manifest),
          'contract_sha256':hashlib.sha256((p.ROOT/'goal/wave-4/contract.json').read_bytes()).hexdigest(),
          'information':'exact_current_state_then_whole_suffix_no_later_measurements',
          'vertices':[[p.txt(x) for x in v] for v in V],'prefix_signs':signs,
          'first_block':list(map(p.txt,a)),'suffix_blocks':[list(map(p.txt,b)) for b in blocks],
          'multipliers':list(map(p.txt,lam)),'lower':p.txt(min(rewards)),'upper':p.txt(upper)}
    p.save(require_new,cert)
    p.save(folder/'extraction-record.json',{'proposal_sha256':hashlib.sha256((folder/'proposal.json').read_bytes()).hexdigest(),
           'extraction_contract_sha256':hashlib.sha256((p.ROOT/'goal/wave-4/extraction-contract.json').read_bytes()).hexdigest(),
           'prefix_change_l1':p.txt(sum((abs(x-y) for x,y in zip(a,old_a)),F(0))),
           'prefix_viability_interval':[p.txt(2+sx+prefix_support-suffix_capacity),p.txt(10-sx-prefix_support+suffix_capacity)]})
    print(json.dumps({'case':case,'action':'exact_extraction_no_solver_rerun','lower_display':float(min(rewards)),
                      'upper_display':float(upper),'gap_display':float(upper-min(rewards))}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case')
    extract(parser.parse_args().case)
