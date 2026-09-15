# Daily Phrases

An iOS 17+ widget that shows a small everyday phrase whenever you glance at your phone — on the **Home Screen** or the **Lock Screen**. Pick one of **30 learning languages**, filter by topic, and tap play in the app for on-device pronunciation. English is the gloss. The companion **Daily Phrases** app browses the catalog, stores settings for the widget, and speaks the learning-language line.

This repository was authored on Linux. **Building, running, and adding the widget require Xcode on macOS.** The widget was not executed on a simulator in this environment.

The GitHub repo name remains `persian-phrases`. Bundle IDs stay `com.persianphrases.app` / `com.persianphrases.app.widget` so existing installs keep working.

## What you get

- **Home Screen widget** (Small, Medium, Large) via WidgetKit
- **Lock Screen widgets** (circular, rectangular, and inline)
- A **rotating phrase** queued every 5 minutes (`TimelineProvider`)
- **Settings**: learning language + multi-select topics, shared with the widget via App Group `group.com.persianphrases.app` (falls back to standard `UserDefaults` if the group is unavailable)
- Optional per-widget topic overlay (“Follow app settings” or one category)
- **~3,000 shared phrase concepts** with translations for **30 languages**
- **On-device audio** (`AVSpeechSynthesizer`) from the list, the detail screen, and widget taps (`dailyphrases://phrase/<id>?play=1` opens that phrase and plays it)
- Transliteration for non-Latin scripts; omitted for Latin-script languages
- Word-by-word chips where tokens exist (template frames keep two tokens; CJK/Thai degrade to phrase-sized chunks)

iOS decides when a widget actually refreshes. Timeline entries are spaced a few minutes apart so looking at the Home Screen often shows something new — not literally on every unlock.

**Physical iPhone, no Mac of your own:** see [DEVICE-INSTALL.md](DEVICE-INSTALL.md) (cloud Mac build + Sideloadly on Windows, free Apple ID). Download `PersianPhrases-ios.zip` from the repo root.

## Learning languages (BCP-47)

Default learning language is **Persian** (`fa` / `fa-IR`). English is always the translation.

| Code | Speech | Language |
| --- | --- | --- |
| `fa` | `fa-IR` | Persian |
| `ar` | `ar-SA` | Arabic |
| `zh-Hans` | `zh-CN` | Mandarin Chinese (Simplified) |
| `es` | `es-ES` | Spanish |
| `fr` | `fr-FR` | French |
| `de` | `de-DE` | German |
| `ja` | `ja-JP` | Japanese |
| `ko` | `ko-KR` | Korean |
| `hi` | `hi-IN` | Hindi |
| `pt` | `pt-BR` | Portuguese |
| `ru` | `ru-RU` | Russian |
| `it` | `it-IT` | Italian |
| `tr` | `tr-TR` | Turkish |
| `vi` | `vi-VN` | Vietnamese |
| `id` | `id-ID` | Indonesian |
| `th` | `th-TH` | Thai |
| `pl` | `pl-PL` | Polish |
| `nl` | `nl-NL` | Dutch |
| `sv` | `sv-SE` | Swedish |
| `el` | `el-GR` | Greek |
| `he` | `he-IL` | Hebrew |
| `uk` | `uk-UA` | Ukrainian |
| `ro` | `ro-RO` | Romanian |
| `cs` | `cs-CZ` | Czech |
| `hu` | `hu-HU` | Hungarian |
| `ms` | `ms-MY` | Malay |
| `fil` | `fil-PH` | Filipino |
| `sw` | `sw-KE` | Swahili |
| `ur` | `ur-PK` | Urdu |
| `bn` | `bn-BD` | Bengali |

Every language in the picker ships the **full catalog count**. Coverage is labeled “Full catalog” because files are complete, not because every generated sentence is native-quality (see below).

## Content coverage (honest)

The catalog is **concept-based**: one English idea + category, then a translation file per language.

- **Hand-written core (~45 phrases)** in all 30 languages: greetings, politeness, emergency, a few daily/food/travel lines (`hello`, `thank-you`, `help`, `where-is-the-bathroom`, …). These are the highest-quality strings. Persian is first-class here.
- **Generated remainder (~3,000 concepts)** from `scripts/lexicon.py` + sentence frames in `scripts/generate_catalog.py`. Same English concepts in every language so filters and widgets stay aligned.
- Template grammar is **learner-grade**, not a localization: articles, gender, word order, and particles are often simplified. Japanese/Korean/Chinese tokenization is coarse. Frames such as “I would like bread” are natural; some combinations are stiffer.
- Pronunciation quality depends on the **on-device iOS voice pack** for that `speechCode`. Install language voices in **Settings → Accessibility → Spoken Content → Voices** if a language sounds like English phonemes.

Do not treat generated lines as certified translations. Expand `core_phrases()` in `generate_catalog.py` when you want native review for a language.

## Open in Xcode

1. On a Mac, install **Xcode 15 or later** (iOS 17 SDK).
2. Open `PersianPhrases.xcodeproj`.
3. Select the **PersianPhrases** scheme and an iPhone simulator or a signed device.
4. In the PersianPhrases and PersianPhrasesWidget targets, set **Signing & Capabilities → Team** to your Apple Developer team (or your Personal Team). Confirm the App Group `group.com.persianphrases.app` is available to both targets (required for widget filters; the app still runs without it).
5. Press **Run** (⌘R). The host app launches; the widget extension is embedded automatically.

If you change bundle IDs, keep the widget ID as `your.app.id.widget` and update the App Group string in both `.entitlements` files and `PhraseSettingsSnapshot.appGroupID`.

## Add the widget to the Home Screen

On a simulator or device where the app is installed:

1. Long-press an empty area of the Home Screen until the icons jiggle.
2. Tap **+** in the corner.
3. Search for **Daily Phrases**.
4. Choose **Small**, **Medium**, or **Large**, then **Add Widget**.
5. Optional: long-press the widget → **Edit Widget** to pin one topic, or leave **Follow app settings**.

On the Simulator you may need **Device → Trigger Screenshot** / go Home (**⌘⇧H**) to see the Home Screen.

Tapping the widget opens that phrase in the app and plays audio (`dailyphrases://phrase/<id>?play=1`). The legacy `persianphrases://` scheme still works.

## Add a Lock Screen widget

1. Wake the iPhone and **long-press the Lock Screen**.
2. Tap **Customize**, then **Lock Screen**.
3. Tap a widget well above or below the clock (or the inline area around the date).
4. Search for **Daily Phrases** and add **circular**, **rectangular**, or **inline**.
5. Tap **Done**. You can still **Edit Widget** to pick a category.

StandBy uses the Home Screen small widget; Lock Screen uses the accessory families.

## Project layout

```
PersianPhrases.xcodeproj     Xcode project (app + widget)
App/                         SwiftUI host app (settings, speech, browse)
Widget/                      WidgetKit extension
PersianPhrasesKit/           Shared Swift package (model, catalog, colors)
  Sources/.../Resources/
    concepts.json            Shared English concepts + categories
    languages.json           Top-30 language metadata
    translations/{code}.json Per-language strings (`zh-Hans` → zh_Hans.json)
scripts/                     Catalog generator, validator, Sideloadly helpers
```

The app and widget both depend on **PersianPhrasesKit**. Settings live in App Group UserDefaults so the timeline only rotates phrases that match the current language and topics.

## Settings and widgets

- **Learning language**: one active language (widget-friendly). Default `fa`.
- **Topics**: multi-select; at least one stays on. Empty stored list means “all topics.”
- Widget timeline reads `PhraseSettingsSnapshot.load()` and intersects with the optional widget category intent.
- If a widget is pinned to a topic you turned off in Settings, it falls back to the remaining enabled topics instead of going blank.

## Audio

`SpeechPlayer` uses `AVSpeechSynthesizer` with `.playback` / `.spokenAudio` so a **user-initiated** play button still speaks when the Ring/Silent switch is on. WidgetKit cannot reliably play audio in the widget itself; the speaker icon is a hint that a tap opens the phrase with auto-play.

## Regenerate the catalog

```bash
python3 scripts/generate_catalog.py
# or the older alias:
python3 scripts/generate_phrases.py

python3 scripts/test_catalog.py
```

Edit `scripts/languages.py` for the 30-language list, `scripts/lexicon.py` for nouns, and `core_phrases()` / `FRAMES` in `scripts/generate_catalog.py` for sentences. After changing JSON, rebuild in Xcode.

```bash
# On a Mac with Swift installed:
cd PersianPhrasesKit && swift test
```

Linux can only run the Python validator (`scripts/test_catalog.py`).

## How rotation works

`PhraseStore.phrase(for:settings:category:)` maps `floor(date / 5 minutes)` plus language and enabled topics to a stable index. The widget timeline emits about three hours of entries (`policy: .atEnd`). WidgetKit may coalesce refreshes when the device is idle; that is expected.

## Design notes

- RTL languages (`fa`, `ar`, `he`, `ur`) use `layoutDirection` + the language locale; English and Latin transliteration stay LTR.
- Small widgets keep the learning-language line largest, then English, then transliteration when present.
- Medium and Large add compact word chips.

## License

Personal / learning project. Phrase translations are for everyday study, not certified localization.
