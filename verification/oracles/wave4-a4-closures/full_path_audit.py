"""Additional positive in-case diagnostic, frozen by this file before execution.

Exactly three full chronological paths per existing scientific case, at the
certificate's first worst-reward vertex: suffix x-min, x-max, y-min. No extra
model/case or sampled grid. Replays original recurrence and actual state policy.
This diagnostic supplements, never replaces, universal support certificates.
"""
from fractions import Fraction as F
import json
from pathlib import Path

import check as checker


def audit(case):
    cert=checker.m0.parse_json((checker.OUT/case/'certificate.json').read_text())
    name=case.rsplit('-r',1)[0]
    m=checker.m0.parse_json((checker.OUT/'inputs'/f'{name}.json').read_text())
    r=cert['r']
    A=[list(map(F,row)) for row in m['dynamics']['A']]
    B,E,x0=(list(map(F,m['dynamics'][k])) for k in ('B','E','x0'))
    C,d=checker.m0._effects(A,B,x0,120)
    D,_=checker.m0._effects(A,E,[F(0),F(0)],120)
    a=list(map(F,cert['first_block']))
    blocks=[list(map(F,b)) for b in cert['suffix_blocks']]
    V=[list(map(F,v)) for v in cert['vertices']]
    sy=sum((abs(v[1])/2 for v in D[r:]),F(0))
    base=d[1]+sum((c[1]*u for c,u in zip(C[:r],a,strict=True)),F(0))
    rewards=[base+v[1]+sum((c[1]*u for c,u in zip(C[r:],b,strict=True)),F(0))-sy for v,b in zip(V,blocks,strict=True)]
    i=min(range(len(V)),key=lambda j:rewards[j])
    def step(state,u,w):
        return tuple(checker.dot(row,state)+b*u+e*w for row,b,e in zip(A,B,E,strict=True))
    state=tuple(x0)
    for u,s in zip(a,cert['prefix_signs'][i],strict=True):state=step(state,u,F(s,2))
    chosen=checker.state_to_block(m,cert,state)
    checker.require(chosen==blocks[i],'Actual nonzero prefix path selected wrong state policy')
    answer=[]
    for label,coordinate,direction in [('suffix_x_min',0,-1),('suffix_x_max',0,1),('suffix_y_min',1,-1)]:
        terminal=state
        for u,column in zip(chosen,D[r:],strict=True):
            sign=1 if column[coordinate]>=0 else -1
            terminal=step(terminal,u,F(direction*sign,2))
        checker.require(2<=terminal[0]<=10,'Full-path terminal strip violated')
        checker.require(terminal[1]>=F(cert['lower']),'Full-path reward below certificate')
        if coordinate==1:checker.require(terminal[1]==F(cert['lower']),'Worst full path did not attain claimed lower')
        answer.append({'path':label,'terminal':[checker.text(x) for x in terminal]})
    return {'case':case,'worst_vertex':i,'state_policy_matches':True,'paths':answer,'result':'valid'}


if __name__=='__main__':
    for case in json.loads((checker.ROOT/'goal/wave-4/contract.json').read_text())['cases']:
        print(json.dumps(audit(case),sort_keys=True),flush=True)
