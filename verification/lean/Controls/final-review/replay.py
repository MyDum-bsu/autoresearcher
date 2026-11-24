"""Independent offline, disk-guarded replay. No network or source mutation."""
import hashlib, json, os, re, shutil, signal, subprocess, sys, time
from pathlib import Path
ROOT = Path(os.environ.get('ARO_CAMPAIGN_ROOT', '.')).resolve()
OUT = ROOT / 'artifacts/bridge/formal-v2/final-review'
PROJECT = ROOT / 'bridge/formal-env-v2/lean'
RESERVE = 600 * 1024**2
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', MATHLIB_NO_CACHE_ON_UPDATE='1', LEAN_NUM_THREADS='2', GIT_TERMINAL_PROMPT='0')
for key in ('TMPDIR','TMP','TEMP','XDG_CACHE_HOME','MATHLIB_CACHE_DIR','LAKE_CACHE_DIR'):
    ENV[key] = str(OUT / ('scratch' if key in ('TMPDIR','TMP','TEMP') else key.lower()))
    Path(ENV[key]).mkdir(parents=True, exist_ok=True)
def require(ok, message):
    if not ok: raise RuntimeError(message)
def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()
def load(path): return json.loads((ROOT/path).read_text())
def save(name, value): (OUT/name).write_text(json.dumps(value, indent=2)+'\n')
def identities(label):
    require(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT),'wrong worktree')
    require(subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD'],cwd=ROOT,text=True).strip()=='task/aro-discovery-k4t-campaign','wrong branch')
    candidate = 'artifacts/bridge/formal-env-v2/candidate-seal-v2.json'
    reviewed = 'artifacts/bridge/formal-v2/statement-review/reviewed-target-identity.json'
    proof = load('artifacts/bridge/formal-v2/proof/proof-seal.json')
    check = {}
    def verify(p,h):
        actual=sha(ROOT/p); require(actual==h,'identity mismatch: '+p); check[p]=actual
    verify(candidate,proof['candidate_seal_sha256'])
    verify(reviewed,proof['reviewed_identity_sha256'])
    verify('bridge/formal-env-v2/expected-theorems-v2.json',proof['inventory_sha256'])
    for e in load(candidate)['files']: verify(e['path'],e['sha256'])
    for p,h in proof['proof_files'].items(): verify(p,h)
    for p,h in proof['build_files'].items(): verify(p,h)
    inventory=load('bridge/formal-env-v2/expected-theorems-v2.json')
    require(len(inventory['targets'])==10 and len({e['declaration'] for e in inventory['targets']})==10,'empty/duplicate/wrong target inventory')
    require(inventory['targets']==load(reviewed)['targets'],'reviewed targets changed')
    closures=[('artifacts/bridge/formal-v2/statement-review/actual-import-closure.json',load(reviewed)['actual_import_closure_sha256']),('artifacts/bridge/formal-v2/proof/actual-proof-import-closure.json',proof['actual_proof_import_closure_sha256'])]
    counts=[]
    for p,h in closures:
        verify(p,h); entries=load(p)['modules']; require(bool(entries),'empty import closure')
        for e in entries:
            verify(e['source_path'],e['source_sha256'])
            for binary,digest in e['compiled_files'].items(): verify(binary,digest)
        counts.append(len(entries))
    tools=load('artifacts/bridge/formal-v1/setup/trusted-seal.json')['tools']
    for tool,e in tools.items(): verify(shutil.which(tool),e['sha256'])
    require(shutil.disk_usage(ROOT).free>=RESERVE,'disk reserve')
    save(label+'.json',dict(identity_checks=check,closure_counts=counts,target_count=len(inventory['targets']),free_bytes=shutil.disk_usage(ROOT).free))
    print(label,counts,len(check),'identities checked')
def run(label,args):
    require(not (OUT/(label+'.json')).exists(),'operation already exists: '+label)
    require(shutil.disk_usage(ROOT).free>=RESERVE,'disk reserve')
    start=time.monotonic(); minimum=shutil.disk_usage(ROOT).free; stop=None
    with (OUT/(label+'.stdout')).open('wb') as stdout, (OUT/(label+'.stderr')).open('wb') as stderr:
        p=subprocess.Popen(args,cwd=PROJECT,env=ENV,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,start_new_session=True)
        while p.poll() is None:
            minimum=min(minimum,shutil.disk_usage(ROOT).free)
            if minimum<RESERVE: stop='disk-reserve'
            if time.monotonic()-start>240: stop='timeout'
            if stop:
                os.killpg(p.pid,signal.SIGTERM)
                try: p.wait(timeout=5)
                except subprocess.TimeoutExpired: os.killpg(p.pid,signal.SIGKILL); p.wait()
                break
            time.sleep(.2)
    receipt=dict(command=args,cwd=str(PROJECT),exit_code=p.returncode,stop_reason=stop,elapsed_seconds=time.monotonic()-start,minimum_free_bytes=minimum,environment={k:ENV[k] for k in ('TMPDIR','TMP','TEMP','XDG_CACHE_HOME','MATHLIB_CACHE_DIR','LAKE_CACHE_DIR','MATHLIB_NO_CACHE_ON_UPDATE','LEAN_PATH') if k in ENV})
    save(label+'.json',receipt); print(label,'exit',p.returncode,'seconds',round(receipt['elapsed_seconds'],2))
    return p.returncode
BUILD=OUT/'build'
def set_path(): ENV['LEAN_PATH']=str(BUILD)+':'+(OUT/'lean-path.stdout').read_text().strip()
def compile_file(label,source,module):
    set_path(); dest=BUILD/(module.replace('.','/')+'.olean'); dest.parent.mkdir(parents=True,exist_ok=True)
    root = OUT if Path(source).is_relative_to(OUT) else PROJECT
    return run(label,['lean','--root='+str(root),'-o',str(dest),str(source)])
def audit():
    output=(OUT/'replay-inventory.stdout').read_text()
    inventory=load('bridge/formal-env-v2/expected-theorems-v2.json')
    axioms={n:re.findall(r'[A-Za-z_][A-Za-z_0-9.]*',a) for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output)}
    records=[]
    for e in inventory['targets']:
        n=e['declaration']; require(n in axioms,'missing axiom output: '+n)
        require(bool(axioms[n]),'empty axiom output requires explicit audit, not pass: '+n)
        require(set(axioms[n])<=set(inventory['axiomAllowlist']),'forbidden axiom: '+n)
        require(re.search(re.escape(n)+r'\s*:\s*'+re.escape(e['type']),output) is not None,'wrong/missing type: '+n)
        require('def '+e['type'] in output,'missing expanded goal: '+n)
        records.append(dict(**e,axioms=axioms[n],compiler_exit=0))
    modules=re.findall(r'^IMPORT\|([^\n]+)$',output,re.M)
    require(bool(modules) and len(modules)==len(set(modules)),'empty/duplicate imports')
    old=load('artifacts/bridge/formal-v2/proof/actual-proof-import-closure.json')['modules']
    require(set(modules)=={e['module'] for e in old},'fresh import closure differs')
    path=(OUT/'lean-path.stdout').read_text().strip().split(':')
    prefix=Path(subprocess.check_output(['lean','--print-prefix'],env=ENV,text=True).strip())
    roots=[BUILD]+[PROJECT/p for p in path if p]+[prefix/'lib/lean']
    sources=[PROJECT]+list((PROJECT/'.lake/packages').iterdir())+[prefix/'src/lean']
    entries=[]
    for m in modules:
        relative=Path(m.replace('.','/'))
        src=next((r/relative.with_suffix('.lean') for r in sources if (r/relative.with_suffix('.lean')).is_file()),None)
        obj=next((r/relative.with_suffix('.olean') for r in roots if (r/relative.with_suffix('.olean')).is_file()),None)
        require(src is not None and obj is not None,'unresolved module '+m)
        binaries={str(obj.resolve()):sha(obj)}
        for suffix in ('.private','.server'):
            p=Path(str(obj)+suffix)
            if p.is_file(): binaries[str(p.resolve())]=sha(p)
        entries.append(dict(module=m,source_path=str(src.resolve()),source_sha256=sha(src),compiled_files=binaries))
    save('actual-import-closure.json',dict(module_count=len(entries),modules=entries))
    save('theorem-audit.json',dict(target_count=len(records),targets=records,missing_nodes=['F3','F4'],unrestricted_source_policy_comparison='unproved',whole_transfer_accepted=False))
    print('Audited',len(records),'targets;',len(entries),'fresh imports')
if __name__=='__main__':
    action=sys.argv[1]
    if action=='replay':
        identities('preflight')
        require(run('lean-path',['lake','env','printenv','LEAN_PATH'])==0,'lake environment failure')
        for module in ('Model','Goals','Proofs/Dynamics','Proofs/Policies','Proofs/Inventory'):
            require(compile_file('replay-'+module.replace('/','-').lower().replace('proofs-inventory','inventory'),PROJECT/'BridgeFormalV2'/(module+'.lean'),'BridgeFormalV2.'+module.replace('/','.'))==0,'compile failure '+module)
        audit()
    elif action=='control':
        sys.exit(compile_file(sys.argv[2],OUT/(sys.argv[3]+'.lean'),sys.argv[3]))
    elif action=='identities': identities('postflight')
    else: raise RuntimeError('unknown operation')
