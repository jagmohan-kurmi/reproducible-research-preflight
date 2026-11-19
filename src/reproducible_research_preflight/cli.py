import argparse, json, sys
from pathlib import Path
from .preflight import inspect_project

def main(argv=None):
    p = argparse.ArgumentParser(prog="reproducible-research-preflight")
    p.add_argument("root", nargs="?", default=".", help="Local project directory")
    p.add_argument("--json", action="store_true", help="Write machine-readable JSON")
    args = p.parse_args(argv)
    result = inspect_project(Path(args.root).resolve())
    print(json.dumps(result, indent=2) if args.json else "\n".join(
        ("PASS" if not i["missing"] else "CHECK") + ": " + i["category"] + " — " + "; ".join(i["missing"] or i["present"])
        for i in result["checks"]
    ))
    print("\n" + "\n".join("- " + x for x in result["recommendations"]))
    return 0
