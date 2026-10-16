import base64, importlib.util, pathlib, tempfile, unittest

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

    def test_packet_recovers_the_runtime_flag_without_exposing_ssh(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory)
            runtime.materialize(
                {
                    "WEB_FLAG": "ICE{web_<demo>}",
                    "SSH_FLAG": "ICE{ssh_abcdef}",
                    "VPN_ADDRESS": '10.128.1.10"><script>',
                },
                path,
                ROOT / "dynamic/site",
            )
            packet = (path / "site/files/packet.txt").read_text()
            self.assertEqual(
                base64.b64decode(packet.splitlines()[-1]).decode(), "ICE{web_<demo>}"
            )
            for asset in (path / "site").rglob("*"):
                if asset.is_file():
                    self.assertNotIn(b"ICE{web_<demo>}", asset.read_bytes())
                    self.assertNotIn(b"ICE{ssh_abcdef}", asset.read_bytes())
            self.assertEqual((path / "flag.txt").read_text(), "ICE{ssh_abcdef}\n")
            index = (path / "site/index.html").read_text()
            self.assertIn("10.128.1.10&quot;&gt;&lt;script&gt;", index)
            self.assertIn('href="/message.html"', index)
            self.assertIn(
                'href="/files/packet.txt"', (path / "site/message.html").read_text()
            )


if __name__ == "__main__":
    unittest.main()
