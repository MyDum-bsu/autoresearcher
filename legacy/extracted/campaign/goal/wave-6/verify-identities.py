from pathlib import Path
import hashlib, json, subprocess
r = Path.cwd()
m = json.loads(Path("goal/wave-6/source-manifest.json").read_text())
root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
print("ROOT", root)
print("BRANCH", branch)
if root != m["root"] or branch != m["branch"]:
    raise SystemExit("workspace identity mismatch")
def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for s in m["sources"]:
    actual = digest(s["path"])
    print("SOURCE", s["id"], actual, s["path"], "MATCH", actual == s["sha256"])
    if actual != s["sha256"]:
        raise SystemExit("source identity mismatch")
    if "comparePath" in s:
        same = digest(s["comparePath"]) == actual
        print("CORPUS_COPY_MATCH", s["id"], same)
        old = json.loads(Path(s["parentManifest"]).read_text())
        pinned = next(x["sha256"] for x in old["sources"] if x["id"] == s["id"])
        print("FROZEN_PARENT_MATCH", s["id"], actual == pinned)
        if not same or actual != pinned:
            raise SystemExit("prior source identity mismatch")
for item in m["parentInputs"] + m["derivedEvidence"]:
    actual = digest(item["path"])
    print("BOUND_FILE", actual, item["path"], "MATCH", actual == item["sha256"])
    if actual != item["sha256"]:
        raise SystemExit("bound file identity mismatch")
for s in m["sources"]:
    meta = subprocess.check_output(["pdfinfo",s["path"]],text=True)
    print("PDFINFO",s["id"])
    for line in meta.splitlines():
        if line.startswith(("Title:","Pages:","File size:","PDF version:")):
            print(line)
print("IDENTITY_CHECK_PASS: 4 primary PDFs; A3 corpus and prior manifest match. File identity only; no scientific verdict.")
