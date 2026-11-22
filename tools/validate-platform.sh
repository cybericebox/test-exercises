#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
platform="${BACKEND_SOURCE:?Set BACKEND_SOURCE to the backend checkout (cybericebox/backend, named daemon until 2026-11-22) at e5a275ca0afac653d92b7f436be6d6e7da4ccb98}"
# Validate against a disposable checkout; the owning platform repo is never edited.
# The test imports github.com/cybericebox/backend; a checkout from before the rename declares github.com/cybericebox/daemon.
module="$(awk '$1 == "module" { print $2; exit }' "$platform/go.mod")"
sed "s#\"github.com/cybericebox/backend/#\"$module/#" "$root/tools/platform_contract_test.go" >"$platform/internal/useCase/exercise/demo_contract_test.go"
cd "$platform"
CIB_DEMO_ROOT="$root" go test ./internal/useCase/exercise -run '^TestPortableDemoArtifacts$' -count=1
