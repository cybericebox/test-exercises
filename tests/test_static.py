import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class StaticRecovery(unittest.TestCase):
    def test_go_attachment_restores_the_configured_flag(self):
        exercise = json.loads((ROOT / "static/exercise.json").read_text())
        task = exercise["versions"][0]["variants"][0]["tasks"][0]
        source = ROOT / "static" / task["attachments"][0]["file"]
        with tempfile.TemporaryDirectory() as directory:
            folder = pathlib.Path(directory)
            shutil.copy(source, folder / "welcome.go")
            (folder / "go.mod").write_text("module demo\n\ngo 1.27.0\n")
            (folder / "welcome_test.go").write_text(
                'package main\nimport "testing"\n'
                "func TestRecover(t *testing.T) { if got := restore(packet); got != "
                + json.dumps(task["flag"][0])
                + ' { t.Fatalf("restored unexpected flag: %q", got) } }\n'
            )
            result = subprocess.run(
                ["go", "test", "-count=1", "."],
                cwd=folder,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            default = subprocess.run(
                ["go", "run", "welcome.go"],
                cwd=folder,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertNotIn(task["flag"][0], default.stdout)
