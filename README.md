# Persian Phrases

An iOS 17+ widget that shows a small everyday Persian phrase whenever you glance at your phone — on the **Home Screen** or the **Lock Screen**. Each phrase has Persian text, English, Latin transliteration, and a word-by-word breakdown. The companion **Persian Phrases** app explains how to add the widgets and lets you browse the full catalog.

This repository was authored on Linux. **Building, running, and adding the widget require Xcode on macOS.** The widget was not executed on a simulator in this environment.

## What you get

- **Home Screen widget** (Small, Medium, Large) via WidgetKit
- **Lock Screen widgets** (circular, rectangular, and inline)
- A **rotating phrase** queued every 5 minutes (`TimelineProvider`)
- Optional **category filter** (greetings, polite, food, travel, daily life, shopping, emergency, time, weather, feelings, work, family, health)
- **1,000+ curated everyday phrases** with word breakdowns
- A bilingual host app: browse, search, and open full detail (tap a widget to jump to that phrase)

iOS decides when a widget actually refreshes. Timeline entries are spaced a few minutes apart so looking at the Home Screen often shows something new — not literally on every unlock.

**Physical iPhone, no Mac of your own:** see [DEVICE-INSTALL.md](DEVICE-INSTALL.md) (cloud Mac build + Sideloadly on Windows, free Apple ID). Download `PersianPhrases-ios.zip` from the repo root.

## Open in Xcode

1. On a Mac, install **Xcode 15 or later** (iOS 17 SDK).
2. Open `PersianPhrases.xcodeproj`.
3. Select the **PersianPhrases** scheme and an iPhone simulator or a signed device.
4. In the PersianPhrases and PersianPhrasesWidget targets, set **Signing & Capabilities → Team** to your Apple Developer team (or your Personal Team).
5. Press **Run** (⌘R). The host app launches; the widget extension is embedded automatically.

Bundle IDs default to `com.persianphrases.app` and `com.persianphrases.app.widget`. Change them in the target **Build Settings** if they collide with an existing app.

## Add the widget to the Home Screen

On a simulator or device where the app is installed:

1. Long-press an empty area of the Home Screen until the icons jiggle.
2. Tap **+** in the corner.
3. Search for **Persian Phrases**.
4. Choose **Small**, **Medium**, or **Large**, then **Add Widget**.
5. Optional: long-press the widget → **Edit Widget** to filter by category.

On the Simulator you may need **Device → Trigger Screenshot** / go Home (**⌘⇧H**) to see the Home Screen.

Tapping the widget opens that phrase in the app (`persianphrases://phrase/<id>`).

## Add a Lock Screen widget

1. Wake the iPhone and **long-press the Lock Screen**.
2. Tap **Customize**, then **Lock Screen**.
3. Tap a widget well above or below the clock (or the inline area around the date).
4. Search for **Persian Phrases** and add **circular**, **rectangular**, or **inline**.
5. Tap **Done**. You can still **Edit Widget** to pick a category.

StandBy uses the Home Screen small widget; Lock Screen uses the accessory families.

## Project layout

```
PersianPhrases.xcodeproj     Xcode project (app + widget)
App/                         SwiftUI host app
Widget/                      WidgetKit extension
PersianPhrasesKit/           Shared Swift package (model, catalog, colors)
  Sources/PersianPhrasesKit/Resources/phrases.json
scripts/                     Helpers to regenerate JSON / app icon
```

The app and widget both depend on **PersianPhrasesKit**. Phrase data lives in one JSON file so you never duplicate the catalog.

## Add more phrases

Edit `PersianPhrasesKit/Sources/PersianPhrasesKit/Resources/phrases.json`, or update `scripts/generate_phrases.py` and run:

```bash
python3 scripts/generate_phrases.py
```

Each entry needs:

```json
{
  "id": "unique-kebab-id",
  "category": "greetings | polite | food | travel | daily | shopping | emergency | time | weather | feelings | work | family | health",
  "formality": "formal | informal | null",
  "persian": "سلام",
  "english": "Hello (informal / everyday)",
  "transliteration": "salām",
  "words": [
    { "persian": "سلام", "transliteration": "salām", "english": "hello / peace" }
  ]
}
```

Keep `id` unique. Prefer natural Persian (including ZWNJ in prefixes such as `می‌خواهم`). Lightly mark formality in `english` when it helps a learner.

After changing JSON, rebuild in Xcode. Package tests in `PersianPhrasesKit` check that the catalog decodes, has 1,000+ phrases, unique ids, and a deterministic rotation.

```bash
# On a Mac with Swift installed:
cd PersianPhrasesKit && swift test
```

## How rotation works

`PhraseStore.phrase(for:category:)` maps `floor(date / 5 minutes)` plus the selected category to a stable index in the catalog. The widget timeline emits about three hours of entries (`policy: .atEnd`). WidgetKit may coalesce refreshes when the device is idle; that is expected.

## Design notes

- Persian is set to RTL (`layoutDirection` + `fa` locale); English and transliteration stay LTR.
- Small widgets keep Persian largest, then English, then transliteration.
- Medium and Large add compact word chips (right-to-left order).

## License

Personal / learning project. Phrase translations are for everyday study, not certified localization.
