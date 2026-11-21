# test-exercises

Two small example tasks for the Cyber&nbsp;ICE&nbsp;Box platform. They show what a task archive looks like and give a
fresh installation something to import, start and solve, so that every part of the path (flag check, web through the
proxy and VPN, SSH, internet access) can be tried end to end.

## The examples

| Example | Kind | What the participant does |
|---|---|---|
| `static` ("Загублений пакет") | Static task with an attachment | Reads `welcome.go`, recovers a masked message and submits the flag |
| `dynamic` ("Журнал зв’язку: веб і SSH") | Task with a running machine | Opens a web page through the proxy or the VPN and recovers a message, then connects over SSH for a second flag |

The dynamic example runs one container image. Its two flags are templates; the platform passes the real values when
the lab starts. Flags always have the form `ICE{...}`.

## Layout

| Path | Contents |
|---|---|
| `static/` | `exercise.json` and `files/welcome.go` |
| `dynamic/` | `exercise.json`, `Dockerfile`, nginx and sshd config, `runtime.py`, `site/` (the web pages) |
| `scripts/package.py` | Builds the import archives |
| `scripts/smoke.py` | Runs the image in isolated Docker networks with a real WireGuard tunnel, an HTTP proxy and SSH |
| `scripts/validate-platform.sh` | Checks the archives against the platform's exercise validator |
| `scripts/check-release.py` | Checks that a release tag matches the image pinned in the descriptor |
| `tests/` | Unit tests for the archives, the runtime and the static task |

## Build the archives

```bash
mise run package
```

This writes to `dist/` (not tracked):

| File | Contents |
|---|---|
| `static.zip`, `dynamic.zip` | One task each, with `exercise.json` at the zip root |
| `test-exercises.zip` | Both tasks, one folder per task |
| `SHA256SUMS` | Checksums of the zip files |

Every archive carries a `manifest.json` with SHA-256 sums of its files. The build is reproducible: the same sources
give the same bytes.

## Import into the platform

Import the zip through the platform's exercise import: `static.zip` or `dynamic.zip` for one task, or
`test-exercises.zip` for both. Then start the task in a test lab or add it to an event.

The dynamic task needs the container image named in `dynamic/exercise.json` (`cybericebox/test-exercises`). A release
publishes it for `linux/amd64` and `linux/arm64`.

## Development commands

| Command | What it does |
|---|---|
| `mise run test` | Python unit tests, and runs `welcome.go` to check the static flag |
| `mise run package` | Builds the archives into `dist/` |
| `mise run build` | Builds the dynamic image as `cybericebox/test-exercises:local` (needs Docker) |
| `mise run smoke` | Builds the test-tools image and runs `scripts/smoke.py` (needs Docker) |

`mise run test` needs Python 3 and Go.

## Releases

A tag `vX.Y.Z` runs the checks, publishes the image and attaches the archives and `SHA256SUMS` to the GitHub release
(`.github/workflows/release.yml`). The text of the release page is `RELEASE_NOTES.md`.

## License

See [LICENSE](LICENSE). The font in `dynamic/site/fonts` has its own license, in `dynamic/site/fonts/OFL.txt`.
