# Default test exercises

Public repository cybericebox/test-exercises. No platform repository changes.

- static/: Ukrainian title/description and a downloadable Go source file containing one fixed demo flag. Standard cib-exercise/v1 JSON and checksummed import ZIP.
- dynamic/: one small container, nginx HTTP on port 8080 and SSH on 2222. Two independent platform-generated template flags injected through WEB_FLAG and SSH_FLAG. A Ukrainian illustrated connection desk page shows the web flag; the SSH account reads its own flag file.
- Network: VPN interface eth0, internet interface eth1 and the standard Laboratory internet gateway; HTTP proxy exposure and VPN access. No custom gateway image or privileged application container.
- Public demo SSH credentials are documented and provide a non-root shell for reading the flag and checking internet access. Runtime SSH host keys are generated per container.
- Publish linux/amd64 and linux/arm64 images to cybericebox/test-exercises. Stable tags vX.Y.Z plus latest; import JSON pins the stable tag. No credentials or generated runtime flags in Git.
- GitHub Actions test, validate archives against the pinned production daemon model, build/publish and attach import ZIPs/checksums to release v1.0.0.
- Verify local HTTP, SSH, flag injection, missing/invalid flags, health and shutdown. Test proxy and WireGuard access in an isolated Docker network. Distinguish that network smoke test from an actual deployed Laboratory run.
