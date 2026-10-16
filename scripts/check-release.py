#!/usr/bin/env python3
"""A release tag must match the image pinned in the portable descriptor."""

import json, os, pathlib, re

root = pathlib.Path(__file__).resolve().parents[1]
tag = os.environ["RELEASE_TAG"]
if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
    raise SystemExit("Only stable vX.Y.Z releases are supported")
descriptor = json.loads((root / "dynamic/exercise.json").read_text())
images = {
    device["image"]
    for version in descriptor["versions"]
    for variant in version["Variants"]
    for device in variant["topology"]["devices"]
}
expected = {"cybericebox/test-exercises:" + tag}
if images != expected:
    raise SystemExit(f"Descriptor image pin {images} does not match {expected}")
print("Release tag matches descriptor image pin")
