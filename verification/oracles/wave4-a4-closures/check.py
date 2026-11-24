"""Exact, solver-free wave-4 checker and state-to-block policy, no status promotion."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import m0_check as m0

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifacts/goal/wave-4/pilot'
INFO = 'exact_current_state_then_whole_suffix_no_later_measurements'
FIELDS = {'schema','case','r','input_sha256','contract_sha256','information','vertices',
          'prefix_signs','first_block','suffix_blocks','multipliers','lower','upper'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x,y in zip(a,b,strict=True)), F(0))


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


def sub(a,b):
    return tuple(x-y for x,y in zip(a,b,strict=True))


def vec(values, length):
    require(isinstance(values,list) and len(values)==length,'Vector dimension mismatch')
    return list(map(m0._number, values))


def text(x):
    return str(x.numerator)+'/'+str(x.denominator)


def interpolate(V, blocks, v):
    """Deterministic fan interpolation on the EXACT reachable polygon."""
    for i, point in enumerate(V):
        if tuple(v) == tuple(point):
            return blocks[i].copy()
    p = sub(v,V[0])
    for i in range(1,len(V)-1):
        a,b = sub(V[i],V[0]),sub(V[i+1],V[0])
        det = cross(a,b)
        require(det>0,'Degenerate or unordered fan triangle')
        beta,gamma = cross(p,b)/det,cross(a,p)/det
        alpha = 1-beta-gamma
        if min(alpha,beta,gamma)>=0:
            return [alpha*x+beta*y+gamma*z for x,y,z in zip(blocks[0],blocks[i],blocks[i+1],strict=True)]
    raise ValueError('Measured state outside certified reachable domain')


def state_to_block(manifest,certificate,state):
    """Only measured state and frozen certificate are inputs, never disturbance history."""
    A = [[F(x) for x in row] for row in manifest['dynamics']['A']]
    r = certificate['r']
    a = list(map(F,certificate['first_block']))
    z = tuple(map(F,state))
    nominal = tuple(map(F,manifest['dynamics']['x0']))
    B = tuple(map(F,manifest['dynamics']['B']))
    for u in a:
        nominal = (dot(A[0],nominal)+B[0]*u,dot(A[1],nominal)+B[1]*u)
    v = sub(z,nominal)
    for _ in range(120-r):
        v = (dot(A[0],v),dot(A[1],v))
    return interpolate([list(map(F,v)) for v in certificate['vertices']],
                       [list(map(F,b)) for b in certificate['suffix_blocks']],v)


def check(manifest,cert):
    digest = m0.validate_input(manifest)
    require(isinstance(cert,dict) and cert.keys()==FIELDS,'Certificate fields differ')
    require(type(cert['schema']) is int and cert['schema']==1,'Schema mismatch')
    contract_path = ROOT/'goal/wave-4/contract.json'
    contract = m0.parse_json(contract_path.read_text())
    require(cert['contract_sha256']==hashlib.sha256(contract_path.read_bytes()).hexdigest(),'Contract binding mismatch')
    r = cert['r']
    require(type(r) is int and r in (67,104),'Closure time outside contract')
    case = f"{manifest['coefficient_set_id']}-r{r}"
    require(cert['case']==case and case in contract['cases'],'Case binding mismatch')
    require(cert['input_sha256']==digest,'Input binding mismatch')
    require(cert['information']==INFO,'Incorrect information/policy class')
    require(hashlib.sha256((ROOT/'research/sources/A4.pdf').read_bytes()).hexdigest()==contract['source_sha256'],'Source binding mismatch')
    A = [[F(x) for x in row] for row in manifest['dynamics']['A']]
    require(A[0][0]*A[1][1]-A[0][1]*A[1][0]!=0,'Singular state transformation')
    B,E,x0 = (list(map(F,manifest['dynamics'][k])) for k in ('B','E','x0'))
    C,d = m0._effects(A,B,x0,120)
    D,_ = m0._effects(A,E,[F(0),F(0)],120)
    g = [tuple(x/2 for x in v) for v in D[:r]]
    n,m = 120-r,2*r
    require(isinstance(cert['vertices'],list) and len(cert['vertices'])==m,'Missing/extra vertices')
    V = [tuple(vec(v,2)) for v in cert['vertices']]
    require(len(set(V))==m,'Duplicate vertices')
    require(isinstance(cert['prefix_signs'],list) and len(cert['prefix_signs'])==m,'Missing prefix realizations')
    for v,signs in zip(V,cert['prefix_signs'],strict=True):
        require(isinstance(signs,list) and len(signs)==r and all(type(s) is int and s in (-1,1) for s in signs),'Invalid prefix realization')
        actual = tuple(sum((a[j]*s for a,s in zip(g,signs,strict=True)),F(0)) for j in range(2))
        require(actual==v,'Vertex not bound to attainable prefix disturbance')
    for i,v in enumerate(V):
        edge = sub(V[(i+1)%m],v)
        next_edge = sub(V[(i+2)%m],V[(i+1)%m])
        require(cross(edge,next_edge)>0,'Polygon not strictly counterclockwise')
        normal = (edge[1],-edge[0])
        support = sum((abs(dot(normal,a)) for a in g),F(0))
        require(dot(normal,v)==support and dot(normal,V[(i+1)%m])==support,'Polygon edge is not exact zonotope support')
    a = vec(cert['first_block'],r)
    require(all(abs(x)<=1 for x in a),'First block outside box')
    require(isinstance(cert['suffix_blocks'],list) and len(cert['suffix_blocks'])==m,'Suffix block count mismatch')
    blocks = [vec(b,n) for b in cert['suffix_blocks']]
    require(all(abs(x)<=1 for b in blocks for x in b),'Suffix control outside box')
    sx,sy = (sum((abs(v[j])/2 for v in D[r:]),F(0)) for j in range(2))
    base = tuple(d[j]+sum((c[j]*u for c,u in zip(C[:r],a,strict=True)),F(0)) for j in range(2))
    rewards, margins = [],[]
    for v,b in zip(V,blocks,strict=True):
        terminal = tuple(base[j]+v[j]+sum((c[j]*u for c,u in zip(C[r:],b,strict=True)),F(0)) for j in range(2))
        require(terminal[0]-sx>=2,'Robust lower terminal row violated')
        require(terminal[0]+sx<=10,'Robust upper terminal row violated')
        rewards.append(terminal[1]-sy)
        margins.extend([terminal[0]-sx-2,10-sx-terminal[0]])
    lower = m0._number(cert['lower'])
    require(lower==min(rewards),'False lower reward')
    lam = vec(cert['multipliers'],3*m)
    require(min(lam)>=0,'Negative certificate multiplier')
    require(sum(lam[2::3],F(0))==1,'Objective coefficient not normalized')
    common = [F(0)]*r
    bound = F(0)
    suffix_residual = F(0)
    for i,v in enumerate(V):
        # Explicit three row coefficient combinations, independent of numerical arrays.
        lo,hi,obj = lam[3*i:3*i+3]
        bound += lo*(d[0]+v[0]-2-sx)+hi*(10-sx-d[0]-v[0])+obj*(d[1]+v[1]-sy)
        for t,c in enumerate(C[:r]):
            common[t] += -lo*c[0]+hi*c[0]-obj*c[1]
        for c in C[r:]:
            suffix_residual += abs(-lo*c[0]+hi*c[0]-obj*c[1])
    upper = bound+sum(map(abs,common),F(0))+suffix_residual
    require(m0._number(cert['upper'])==upper,'False dual upper bound')
    require(lower<=upper,'Reversed bounds')
    # Concrete in-case policy checks: every vertex, center and one edge midpoint.
    for i,v in enumerate(V):
        require(interpolate(V,blocks,v)==blocks[i],'Vertex interpolation mismatch')
    for v in ((F(0),F(0)),tuple((x+y)/2 for x,y in zip(V[0],V[1],strict=True))):
        b = interpolate(V,blocks,v)
        require(all(abs(x)<=1 for x in b),'Interpolated policy outside box')
        x,y = (base[j]+v[j]+sum((c[j]*u for c,u in zip(C[r:],b,strict=True)),F(0)) for j in range(2))
        require(x-sx>=2 and x+sx<=10 and y-sy>=lower,'Interpolated terminal row fails')
    # Actual closure-state interface at zero prefix disturbance (not an extra case).
    nominal = tuple(x0)
    for u in a:
        nominal = (dot(A[0],nominal)+B[0]*u,dot(A[1],nominal)+B[1]*u)
    require(state_to_block(manifest,cert,nominal)==interpolate(V,blocks,(F(0),F(0))),'State-only interface mismatch')
    return {'case':case,'arithmetic':'exact_rational','certificate_validity':'valid',
            'lower':text(lower),'upper':text(upper),'gap':text(upper-lower),
            'lower_display':float(lower),'upper_display':float(upper),'gap_display':float(upper-lower),
            'vertices':m,'min_terminal_margin':text(min(margins)),
            'general_reduction':'written_argument_not_formalized','goalAchieved':False}


def controls(manifest,cert):
    result = [{'control':'positive','result':check(manifest,cert)}]
    mutations = ['incorrect_information','violated_terminal','false_objective','negative_multiplier',
                 'input_binding','closure_binding','missing_vertex']
    for name in mutations:
        bad = copy.deepcopy(cert)
        if name=='incorrect_information': bad['information']='suffix_disturbance_observed'
        elif name=='violated_terminal': bad['suffix_blocks'][0]=['-1/1']*(120-cert['r'])
        elif name=='false_objective': bad['lower']=text(F(cert['upper'])+1)
        elif name=='negative_multiplier': bad['multipliers'][0]='-1/1'
        elif name=='input_binding': bad['input_sha256']='0'*64
        elif name=='closure_binding': bad['r']=104 if cert['r']==67 else 67
        elif name=='missing_vertex': bad['vertices'].pop()
        try:
            check(manifest,bad)
        except ValueError as error:
            result.append({'control':name,'result':'rejected','reason':str(error)})
        else:
            raise ValueError('Invalid control accepted: '+name)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case')
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    cert=m0.parse_json((OUT/args.case/'certificate.json').read_text())
    name=args.case.rsplit('-r',1)[0]
    manifest=m0.parse_json((OUT/'inputs'/f'{name}.json').read_text())
    result=controls(manifest,cert) if args.controls else check(manifest,cert)
    print(json.dumps(result,sort_keys=True))
