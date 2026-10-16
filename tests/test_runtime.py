import importlib.util, pathlib, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("runtime", ROOT / "dynamic/runtime.py")
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class Runtime(unittest.TestCase):
    def test_flags_are_required(self):
        for env in [
            {},
            {"WEB_FLAG": "ICE{web}"},
            {"WEB_FLAG": "template:ICE{web}", "SSH_FLAG": "ICE{ssh}"},
        ]:
            with self.assertRaises(ValueError):
                runtime.materialize(
                    env, pathlib.Path(tempfile.mkdtemp()), ROOT / "dynamic/site"
                )

    def test_flags_are_escaped_and_kept_in_their_channels(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory)
            runtime.materialize(
                {"WEB_FLAG": "ICE{web_<demo>}", "SSH_FLAG": "ICE{ssh_abcdef}"},
                path,
                ROOT / "dynamic/site",
            )
            page = (path / "site/index.html").read_text()
            self.assertIn("ICE{web_&lt;demo&gt;}", page)
            self.assertNotIn("ICE{ssh_abcdef}", page)
            self.assertEqual((path / "flag.txt").read_text(), "ICE{ssh_abcdef}\n")


if __name__ == "__main__":
    unittest.main()
