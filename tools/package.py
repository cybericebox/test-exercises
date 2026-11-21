#!/usr/bin/env python3
"""Build reproducible cib-exercise/1 archives: one zip per task (task at the zip root) and one bundle with a folder per task.

Every archive carries a single root manifest.json with SHA-256 sums."""

import hashlib, json, pathlib, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def archive(files, destination):
    manifest = {
        "version": 1,
        "checksums": {
            n: hashlib.sha256(v).hexdigest() for n, v in sorted(files.items())
        },
    }
    files = {
        **files,
        "manifest.json": (
            json.dumps(manifest, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
        ).encode(),
    }
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, value in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, value)


def main():
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    bundle = {}
    for name in ["static", "dynamic"]:
        folder = ROOT / name
        files = {"exercise.json": (folder / "exercise.json").read_bytes()}
        if (folder / "files").exists():
            files.update(
                {
                    p.relative_to(folder).as_posix(): p.read_bytes()
                    for p in (folder / "files").rglob("*")
                    if p.is_file()
                }
            )
        archive(files, out / f"{name}.zip")
        bundle.update({name + "/" + n: v for n, v in files.items()})
    archive(bundle, out / "test-exercises.zip")
    (out / "SHA256SUMS").write_text(
        "".join(
            hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n"
            for p in sorted(out.glob("*.zip"))
        )
    )


if __name__ == "__main__":
    main()
