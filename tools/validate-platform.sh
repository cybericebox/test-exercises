#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
platform="${DAEMON_SOURCE:?Set DAEMON_SOURCE to the daemon checkout at e5a275ca0afac653d92b7f436be6d6e7da4ccb98}"
# Validate against a disposable checkout; the owning platform repo is never edited.
cp "$root/scripts/platform_contract_test.go" "$platform/internal/useCase/exercise/demo_contract_test.go"
cd "$platform"
CIB_DEMO_ROOT="$root" go test ./internal/useCase/exercise -run '^TestPortableDemoArtifacts$' -count=1
