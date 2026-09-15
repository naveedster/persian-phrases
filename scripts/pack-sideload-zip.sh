#!/bin/bash
# Pack a Sideloadly-ready source zip (no .git, no build products).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/PersianPhrases-ios.zip}"

cd "$ROOT"
rm -f "$OUT"

zip -r "$OUT" . \
  -x '.git/*' \
  -x '.git/**' \
  -x 'DerivedData/*' \
  -x 'DerivedData/**' \
  -x '.build/*' \
  -x '.build/**' \
  -x '**/.DS_Store' \
  -x '**/__pycache__/*' \
  -x '**/*.pyc' \
  -x '*.ipa' \
  -x 'PersianPhrases-ios.zip'

echo "Wrote $OUT"
ls -lh "$OUT"
