"""Verify identities and disposition of this G3 reading packet, not mathematics."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
expected_root = Path('<workspace>/aro-discovery-campaign')
if root != expected_root:
    raise RuntimeError(f'Wrong packet root: {root}')
for args, expected in [
    (['git', 'rev-parse', '--show-toplevel'], str(expected_root)),
    (['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 'task/aro-discovery-k4t-campaign'),
]:
    value = subprocess.check_output(args, cwd=root, text=True, timeout=5).strip()
    if value != expected:
        raise RuntimeError(f'Workspace mismatch: {value}')

manifest = json.loads((root / 'goal/wave-1/source-manifest.json').read_text())
contract = json.loads((root / 'goal/wave-1/claim-contract.json').read_text())
count = 0
for group in ['sources', 'inputs', 'derivatives', 'outputs', 'initial_selection_records']:
    for entry in manifest[group]:
        path = root / entry['path']
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise RuntimeError(f'Identity mismatch: {entry["path"]}')
        if len(data) != entry['size_bytes']:
            raise RuntimeError(f'Size mismatch: {entry["path"]}')
        count += 1
binding = contract['source_manifest']
if hashlib.sha256((root / binding['path']).read_bytes()).hexdigest() != binding['sha256']:
    raise RuntimeError('Contract does not bind this source manifest')
old_pool = json.loads((root / 'research/resource-manifest.json').read_text())
for entry in old_pool['sources']:
    if hashlib.sha256((root / entry['copy_path']).read_bytes()).hexdigest() != entry['sha256']:
        raise RuntimeError(f'Inherited PDF changed: {entry["copy_path"]}')
if contract['actionableTarget'] is not False or contract['target'] is not None:
    raise RuntimeError('No actionable target was justified by this audit')
if contract['goal_achieved'] is not False or contract['proof_authorized'] is not False:
    raise RuntimeError('Source audit cannot authorize proof or declare first success')
if len(contract['selections']) > 2 or not manifest['unavailable_or_uninspected_sources']:
    raise RuntimeError('Missing selection bound or source-gap disclosure')
print(json.dumps({
    'status': 'passed',
    'scope': 'artifact identities, workspace, inherited six PDF identities and negative target disposition only',
    'packet_identities_checked': count,
    'inherited_pdf_identities_checked': len(old_pool['sources']),
    'actionableTarget': False,
    'mathematical_or_novelty_verdict': False,
}, indent=2))
