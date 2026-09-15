# Install on a physical iPhone (free Apple ID)

Use a **rented cloud Mac** only to *build* an `.ipa`. Sign and install on **Windows with Sideloadly** so you do not type your Apple ID on the rental Mac.

No paid Apple Developer Program is required. The app lasts about **7 days**, then Sideloadly-install again.

You need: Windows PC, USB cable, iPhone on **iOS 17+**, [Sideloadly](https://sideloadly.io), and any Mac with **Xcode 15+**.

The on-device name is **Daily Phrases**. Search that name when adding Home Screen or Lock Screen widgets.

---

## A. Cloud Mac — build an unsigned IPA (no Apple ID)

1. Download `PersianPhrases-ios.zip` (see README / repo root) and unzip it.
2. Install Xcode from the App Store if needed. Open it once and accept the license.
3. Double-click `PersianPhrases.xcodeproj`.
4. If asked, **Trust** and let it resolve the local package `PersianPhrasesKit` (File → Packages → Resolve Package Versions).
5. Optional but recommended if the default IDs collide later: select each target → **Signing & Capabilities** / **Build Settings → Product Bundle Identifier**
   - App (`PersianPhrases`): `com.YOURNAME.persianphrases`
   - Widget (`PersianPhrasesWidget`): `com.YOURNAME.persianphrases.widget`
   - App Group (both `.entitlements` files **and** `PhraseSettingsSnapshot.appGroupID` in the kit): keep them in sync, e.g. `group.com.YOURNAME.persianphrases`  
   The widget ID must start with the app ID plus a dot. You can skip this and let Sideloadly change the app ID; if you skip it, leave both IDs as-is. Sideloadly on a free Apple ID often **cannot** provision App Groups — the app still works; language/topic filters then live in standard `UserDefaults` and the widget may not see them until you install with a paid team.
6. In Terminal, from the unzipped folder:

```bash
chmod +x scripts/export-sideloadly-ipa.sh
./scripts/export-sideloadly-ipa.sh
```

That writes `PersianPhrases.ipa` next to the `.xcodeproj`.

**Manual fallback** (same result):

```bash
xcodebuild -scheme PersianPhrases \
  -project PersianPhrases.xcodeproj \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -derivedDataPath ./DerivedData \
  CODE_SIGNING_ALLOWED=NO \
  CODE_SIGNING_REQUIRED=NO \
  CODE_SIGN_IDENTITY="" \
  build

rm -rf /tmp/PersianPhrasesPayload
mkdir -p /tmp/PersianPhrasesPayload/Payload
cp -R DerivedData/Build/Products/Release-iphoneos/PersianPhrases.app \
  /tmp/PersianPhrasesPayload/Payload/
( cd /tmp/PersianPhrasesPayload && zip -yr "$OLDPWD/PersianPhrases.ipa" Payload )
```

7. Confirm `PersianPhrases.app/PlugIns/PersianPhrasesWidget.appex` exists inside the payload (the script prints this).
8. Copy `PersianPhrases.ipa` to your Windows PC (AirDrop, browser download, USB, etc.).

Do **not** use Product → Archive → Distribute → Ad Hoc / Development on a free Apple ID. Those export paths need a paid team. Sideloadly re-signs this unsigned IPA instead.

To refresh the zip from a checkout:

```bash
chmod +x scripts/pack-sideload-zip.sh
./scripts/pack-sideload-zip.sh
```

---

## B. Optional: sign in Xcode with a Personal Team

Only if you are on a Mac you trust (not a rental):

1. Both targets → **Signing & Capabilities** → **Automatically manage signing**.
2. **Team**: your Apple ID (Personal Team). Add the account under Xcode → Settings → Accounts if needed.
3. Enable the **App Groups** capability on both targets with `group.com.persianphrases.app` (or your renamed group).
4. Fix bundle IDs if Xcode says they are taken (same pattern as above).
5. Destination: **Any iOS Device (arm64)**. Product → Build.
6. Still package the `.app` as an IPA with the script or the `zip` steps above (Organizer “Distribute” is usually blocked on a free team).

---

## C. Windows — Sideloadly

1. Install [Sideloadly](https://sideloadly.io) and the **Apple Devices** app (Microsoft Store) or iTunes.
2. On the iPhone: unlock, plug in, **Trust This Computer**.
3. iOS 16+: **Settings → Privacy & Security → Developer Mode** → On → restart.
4. Open Sideloadly. Drag in `PersianPhrases.ipa`.
5. Apple account: **your** Apple ID (the free one).
6. Start the install. If asked, enter an app-specific password from [appleid.apple.com](https://appleid.apple.com) → Sign-In and Security → App-Specific Passwords.
7. iPhone: **Settings → General → VPN & Device Management** → your Apple ID → **Trust**.
8. Open **Daily Phrases** once. Pick a learning language and topics in Settings. Tap the speaker to hear on-device speech (install the language’s iOS voice if it sounds wrong).
9. Home Screen: long-press → **+** → search **Daily Phrases** → Small / Medium / Large → **Add Widget**.
10. Lock Screen: long-press the Lock Screen → **Customize** → **Lock Screen** → tap a widget well → add **Daily Phrases** (circular, rectangular, or inline).

The same IPA works in **AltStore**. When you reinstall, keep app extensions enabled so the widget (Home Screen and Lock Screen) stays available.

Reinstall with Sideloadly or AltStore when the 7-day free cert expires.

---

## Known issues

- This project was written on Linux and has **not** been compiled with Xcode. First open may upgrade the project file or ask to resolve `PersianPhrasesKit`.
- Need **Xcode 15+** and an **iPhone on iOS 17+**.
- `xcodebuild` / Simulator are **not** available in the Linux Cursor environment; the IPA must be produced on a Mac.
- Free signing / Sideloadly: Home Screen **widgets sometimes do not appear** or die after reboot. The companion app should still run. If the widget is missing, open the app once, reboot, and check **+** again. A paid Developer account + Xcode-to-device install is more reliable for WidgetKit.
- Free Apple ID: about **3 sideloaded apps** at a time, **7-day** expiry. App Groups often fail on free signing, so the widget may ignore in-app language/topic filters until you sign with a team that can provision `group.com.persianphrases.app`.
- Default bundle IDs are `com.persianphrases.app` / `com.persianphrases.app.widget`. Change them if signing complains they are in use.
- Both targets must stay a parent/child bundle ID pair and (if you sign in Xcode) the same Team.
- Unsigned `CODE_SIGNING_ALLOWED=NO` builds are **only** for Sideloadly (or similar) to re-sign. They will not launch if you copy the `.app` onto the phone yourself.
- Do not log into a rented Mac with your Apple ID if you can avoid it. Use path A + Sideloadly on your PC.
- On-device TTS quality varies by language. Add voices under **Settings → Accessibility → Spoken Content → Voices**.
