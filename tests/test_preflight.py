import tempfile, unittest
from pathlib import Path
from src.reproducible_research_preflight.preflight import inspect_project

class PreflightTests(unittest.TestCase):
    def test_complete_manifest_and_missing_checks(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/"README.md").write_text("Install and run; seed=123; input provenance DOI; output artifact")
            (p/"requirements.txt").write_text("numpy==1.26\n"); (p/"LICENSE").write_text("MIT")
            r=inspect_project(p)
            self.assertFalse(r["independent_reproduction_claim"])
            self.assertTrue(r["artifact_checksums"])
    def test_missing_root(self):
        with self.assertRaises(ValueError): inspect_project(Path("/definitely/not/local"))

if __name__=="__main__": unittest.main()
