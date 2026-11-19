import hashlib, json
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def inspect_project(root):
    if not root.exists() or not root.is_dir():
        raise ValueError("root must be an existing local directory")
    names = {p.name.lower(): p for p in root.rglob("*") if p.is_file()}
    readme = next((p for p in names.values() if p.name.lower().startswith("readme")), None)
    manifests = [n for n in ("pyproject.toml","requirements.txt","environment.yml","environment.yaml","renv.lock","package-lock.json","poetry.lock") if n in names]
    licenses = [n for n in ("license","license.txt","license.md","copying") if n in names]
    text = (readme.read_text("utf-8", errors="replace") if readme else "")
    seed_terms = any(w in text.lower() for w in ("seed","random state","random_seed"))
    provenance_terms = any(w in text.lower() for w in ("provenance","input data","source data","doi","checksum"))
    output_terms = any(w in text.lower() for w in ("output","artifact","result"))
    code_license = bool(licenses)
    artifact_manifest = next((p for p in names.values() if "manifest" in p.name.lower() or "checksums" in p.name.lower()), None)
    checks = [
        {"category":"README run instructions","present":[str(readme.relative_to(root))] if readme and any(x in text.lower() for x in ("install","run","python")) else [], "missing":[] if readme and any(x in text.lower() for x in ("install","run","python")) else ["README or documented install/run instructions"]},
        {"category":"data/code licenses","present":["LICENSE file found"] if code_license else [], "missing":[] if code_license else ["data and code license or license field"]},
        {"category":"environment manifest","present":[m for m in manifests], "missing":[] if manifests else ["Python/R/environment lock or manifest"]},
        {"category":"seeds","present":["seed documentation in README"] if seed_terms else [], "missing":[] if seed_terms else ["document random seeds or state"]},
        {"category":"input provenance","present":["provenance/source language in README"] if provenance_terms else [], "missing":[] if provenance_terms else ["input data sources, versions, and provenance"]},
        {"category":"outputs/artifact checksums","present":[str(artifact_manifest.relative_to(root))] if artifact_manifest else [], "missing":[] if artifact_manifest else ["output/artifact manifest with SHA-256 checksums"]},
    ]
    recommendations = []
    for c in checks:
        if c["missing"]: recommendations.extend(c["missing"])
    return {"tool":"reproducible-research-preflight","root":str(root),"independent_reproduction_claim":False,"checks":checks,"recommendations":recommendations,"artifact_checksums":{str(p.relative_to(root)):sha256(p) for p in root.rglob("*") if p.is_file() and not any(x in str(p).lower() for x in ("venv",".git","__pycache__"))}}
