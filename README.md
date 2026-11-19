# reproducible-research-preflight

Local-only structural preflight for sharing code and data. It does not execute project code and does not prove independent reproduction.

## Install
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Run
```powershell
reproducible-research-preflight C:\path\to\project
reproducible-research-preflight C:\path\to\project --json
python -m unittest discover -s tests -v
```
