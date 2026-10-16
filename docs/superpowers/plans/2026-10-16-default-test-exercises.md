# Default test exercises implementation plan

> For agentic workers: use superpowers:executing-plans to implement this plan task by task.

**Goal:** Publish a ready-to-import static and dynamic demo set.
**Architecture:** Standard archive JSON, one nginx+OpenSSH image, isolated network smoke tests.
**Tech Stack:** Alpine, nginx, OpenSSH, Python stdlib, Docker, GitHub Actions.
**Spec:** docs/superpowers/specs/2026-10-16-default-test-exercises-design.md

## Constraints
Ukrainian challenge copy. Static flag fixed; WEB_FLAG and SSH_FLAG platform templates. No edits to existing platform repos. Public content contains demo credentials only. Stable image pin plus latest tag.

## Review focus
- Template grammar and per-task environment names match the real importer.
- Dynamic addresses use network references; the explicit VPN client pool route is documented for custom installations.
- Runtime values are escaped for HTML and never passed to a shell as code.
- SSH gives a non-root demo shell and fresh host keys.
- Published image and ZIP assets match the tested source commit.

## Tasks
- [x] Write tests and standard exercise descriptors; build checksummed ZIPs and validate with the real daemon codec/domain.
- [x] Implement image, entrypoint and the Ukrainian page; verify both service flags and lifecycle.
- [x] Run isolated proxy/VPN/internet smoke checks and desktop/mobile visual review.
- [x] Configure public GitHub repository and Docker Hub publishing; publish v1.0.0 and verify image/archive downloads.

## Verified release

- Release: https://github.com/cybericebox/test-exercises/releases/tag/v1.0.0
- Source: `58891f85203090cec4fc6b85385f6b825fa00beb`.
- Release workflow: https://github.com/cybericebox/test-exercises/actions/runs/38935904509 (all jobs passed).
- Published image index: `sha256:036d7aeb7485bd61ede07c71d26242663bccb8b852ba939542e432842b24c7c4`; both Linux architectures, `v1.0.0` and `latest` agree.
- Downloaded release archives match local bytes, SHA-256 and the real daemon validator.
- The pulled published image passes proxy HTTP, actual WireGuard HTTP, SSH, non-root identity, internet, flag separation and shutdown checks.
- No production Laboratory deployment was performed.
