#!/bin/bash
# Build an unsigned IPA on macOS for Sideloadly to re-sign.
# Run from the folder that contains PersianPhrases.xcodeproj.
set -euo pipefail

if ! command -v xcodebuild >/dev/null 2>&1; then
  echo "xcodebuild not found. Run this script on a Mac with Xcode 15+." >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

DERIVED="$ROOT/DerivedData"
APP="$DERIVED/Build/Products/Release-iphoneos/PersianPhrases.app"
IPA="$ROOT/PersianPhrases.ipa"

echo "Building unsigned Release (generic iOS device)…"
xcodebuild -scheme PersianPhrases \
  -project "$ROOT/PersianPhrases.xcodeproj" \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -derivedDataPath "$DERIVED" \
  CODE_SIGNING_ALLOWED=NO \
  CODE_SIGNING_REQUIRED=NO \
  CODE_SIGN_IDENTITY="" \
  build

if [[ ! -d "$APP" ]]; then
  echo "Build finished but $APP is missing." >&2
  exit 1
fi

WIDGET="$APP/PlugIns/PersianPhrasesWidget.appex"
if [[ -d "$WIDGET" ]]; then
  echo "Widget extension found: $WIDGET"
else
  echo "WARNING: Widget .appex not found under PlugIns. The app may still sideload without a Home Screen widget." >&2
fi

STAGE="$(mktemp -d)"
mkdir -p "$STAGE/Payload"
cp -R "$APP" "$STAGE/Payload/"
rm -f "$IPA"
( cd "$STAGE" && zip -yr "$IPA" Payload )
rm -rf "$STAGE"

echo "Wrote $IPA"
ls -lh "$IPA"
