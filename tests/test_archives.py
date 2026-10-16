import hashlib, json, pathlib, re, subprocess, unittest, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Archives(unittest.TestCase):
    def test_import_archives_and_flags(self):
        subprocess.run(["python3", str(ROOT / "scripts/package.py")], check=True)
        for name in ["static", "dynamic"]:
            with zipfile.ZipFile(ROOT / "dist" / f"{name}.zip") as z:
                manifest = json.loads(z.read("manifest.json"))
                self.assertEqual(manifest["version"], 1)
                for path, digest in manifest["checksums"].items():
                    self.assertEqual(hashlib.sha256(z.read(path)).hexdigest(), digest)
                data = json.loads(z.read("exercise.json"))
                self.assertEqual(data["format"], "cib-exercise/v1")
                variant = data["versions"][0]["Variants"][0]
                if name == "static":
                    task = variant["tasks"][0]
                    self.assertFalse(task.get("linked_device_id"))
                    source = z.read(
                        "files/" + task["attachments"][0]["file_id"] + "/welcome.go"
                    ).decode()
                    self.assertNotIn(task["flag"][0], source)
                    mask = int(
                        re.search(r"const mask byte = (0x[0-9a-f]+)", source).group(1),
                        16,
                    )
                    values = re.search(
                        r"var packet = \[\]byte\{(.*?)\}", source, re.S
                    ).group(1)
                    restored = bytes(
                        int(n, 16) ^ mask for n in re.findall(r"0x[0-9a-f]+", values)
                    ).decode()
                    self.assertEqual(restored, task["flag"][0])
                else:
                    self.assertEqual(len(variant["tasks"]), 2)
                    self.assertTrue(
                        all(
                            t["flag"][0].startswith("template:ICE{")
                            for t in variant["tasks"]
                        )
                    )
                    self.assertEqual(
                        {t["device_flag_var"] for t in variant["tasks"]},
                        {"WEB_FLAG", "SSH_FLAG"},
                    )
                    topo = variant["topology"]
                    self.assertTrue(topo["vpn"]["enabled"])
                    self.assertTrue(topo["internet"]["enabled"])
                    self.assertEqual(len(topo["devices"]), 1)
                    self.assertEqual(
                        topo["devices"][0]["external"],
                        {"port": 8080, "protocol": "http"},
                    )
                    self.assertTrue(
                        any(
                            i["ip"].get("gateway_ref", {}).get("network") == "internet"
                            for i in topo["devices"][0]["interfaces"]
                        )
                    )

    def test_reproducible_archives(self):
        subprocess.run(["python3", str(ROOT / "scripts/package.py")], check=True)
        before = {p.name: p.read_bytes() for p in (ROOT / "dist").glob("*.zip")}
        subprocess.run(["python3", str(ROOT / "scripts/package.py")], check=True)
        self.assertTrue(
            all((ROOT / "dist" / n).read_bytes() == v for n, v in before.items())
        )


if __name__ == "__main__":
    unittest.main()
