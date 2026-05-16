import subprocess
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "day05" / "check_insertion.py"
PLASMID = ROOT / "day05" / "ROZMAN_D6Y_1_lentiv2_zim3_pLann.dna"
PCR = ROOT / "day05" / "4212_100_1-guideRNAseqF" / "4212_100_1-guideRNAseqF.fasta"
INSERT = "CGGCGGCCCGCTCGCTCGGG"


class CheckInsertionCliTests(unittest.TestCase):
    def run_script(self, enzyme):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--plasmid",
                str(PLASMID),
                "--pcr",
                str(PCR),
                "--enzyme",
                enzyme,
                "--insert",
                INSERT,
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

    def test_expected_enzyme_succeeds(self):
        result = self.run_script("BsmBI")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("SUCCESS", result.stdout)
        self.assertIn("Insert touches a restriction cut: True", result.stdout)

    def test_wrong_enzyme_fails(self):
        result = self.run_script("bstbi")
        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("FAIL", result.stdout)
        self.assertIn("Insert touches a restriction cut: False", result.stdout)

    def test_other_wrong_enzyme_fails(self):
        result = self.run_script("EcoRI")
        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()