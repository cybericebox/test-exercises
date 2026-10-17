import hashlib, json, pathlib, re, subprocess, unittest, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def linked_files(data):
    return {
        a["file"]
        for version in data["versions"]
        for variant in version["variants"]
        for task in variant.get("tasks", [])
        for a in task.get("attachments", [])
    }


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
                self.assertEqual(data["schema"], "cib-exercise/1")
                self.assertNotIn("format", data)
                variant = data["versions"][0]["variants"][0]
                self.assertEqual(
                    linked_files(data),
                    {n for n in z.namelist() if n not in ("exercise.json", "manifest.json")},
                )
                if name == "static":
                    task = variant["tasks"][0]
                    self.assertFalse(task.get("linked_device_id"))
                    self.assertEqual(
                        task["attachments"], [{"file": "files/welcome.go"}]
                    )
                    source = z.read(task["attachments"][0]["file"]).decode()
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

    def test_bundle_has_task_folders_and_one_root_manifest(self):
        subprocess.run(["python3", str(ROOT / "scripts/package.py")], check=True)
        with zipfile.ZipFile(ROOT / "dist/test-exercises.zip") as z:
            names = z.namelist()
            self.assertEqual([n for n in names if n.endswith("manifest.json")], ["manifest.json"])
            self.assertEqual(
                {n.split("/")[0] for n in names if "/" in n}, {"static", "dynamic"}
            )
            self.assertEqual(
                {n for n in names if n.endswith("exercise.json")},
                {"static/exercise.json", "dynamic/exercise.json"},
            )
            self.assertFalse([n for n in names if re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-", n)])
            checks = json.loads(z.read("manifest.json"))["checksums"]
            self.assertEqual(set(checks), {n for n in names if n != "manifest.json"})
            for path, digest in checks.items():
                self.assertEqual(hashlib.sha256(z.read(path)).hexdigest(), digest)
            static = json.loads(z.read("static/exercise.json"))
            self.assertEqual(
                linked_files(static),
                {n[len("static/"):] for n in names if n.startswith("static/files/")},
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
