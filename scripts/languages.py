"""Stable top-30 learning languages (BCP-47 speech codes for AVSpeechSynthesizer)."""

from __future__ import annotations

# code, bcp47/speech, English name, native name, rtl, transliteration
LANGUAGE_ROWS: list[tuple[str, str, str, str, bool, bool]] = [
    ("fa", "fa-IR", "Persian", "فارسی", True, True),
    ("ar", "ar-SA", "Arabic", "العربية", True, True),
    ("zh-Hans", "zh-CN", "Mandarin Chinese", "简体中文", False, True),
    ("es", "es-ES", "Spanish", "Español", False, False),
    ("fr", "fr-FR", "French", "Français", False, False),
    ("de", "de-DE", "German", "Deutsch", False, False),
    ("ja", "ja-JP", "Japanese", "日本語", False, True),
    ("ko", "ko-KR", "Korean", "한국어", False, True),
    ("hi", "hi-IN", "Hindi", "हिन्दी", False, True),
    ("pt", "pt-BR", "Portuguese", "Português", False, False),
    ("ru", "ru-RU", "Russian", "Русский", False, True),
    ("it", "it-IT", "Italian", "Italiano", False, False),
    ("tr", "tr-TR", "Turkish", "Türkçe", False, False),
    ("vi", "vi-VN", "Vietnamese", "Tiếng Việt", False, False),
    ("id", "id-ID", "Indonesian", "Bahasa Indonesia", False, False),
    ("th", "th-TH", "Thai", "ไทย", False, True),
    ("pl", "pl-PL", "Polish", "Polski", False, False),
    ("nl", "nl-NL", "Dutch", "Nederlands", False, False),
    ("sv", "sv-SE", "Swedish", "Svenska", False, False),
    ("el", "el-GR", "Greek", "Ελληνικά", False, True),
    ("he", "he-IL", "Hebrew", "עברית", True, True),
    ("uk", "uk-UA", "Ukrainian", "Українська", False, True),
    ("ro", "ro-RO", "Romanian", "Română", False, False),
    ("cs", "cs-CZ", "Czech", "Čeština", False, False),
    ("hu", "hu-HU", "Hungarian", "Magyar", False, False),
    ("ms", "ms-MY", "Malay", "Bahasa Melayu", False, False),
    ("fil", "fil-PH", "Filipino", "Filipino", False, False),
    ("sw", "sw-KE", "Swahili", "Kiswahili", False, False),
    ("ur", "ur-PK", "Urdu", "اردو", True, True),
    ("bn", "bn-BD", "Bengali", "বাংলা", False, True),
]

LANG_CODES = [row[0] for row in LANGUAGE_ROWS]
NON_LATIN = {code for code, _, _, _, _, uses_tr in LANGUAGE_ROWS if uses_tr}


def language_payload() -> list[dict]:
    rows = []
    for code, bcp47, english, native, rtl, uses_tr in LANGUAGE_ROWS:
        rows.append(
            {
                "code": code,
                "bcp47": bcp47,
                "englishName": english,
                "nativeName": native,
                "speechCode": bcp47,
                "isRightToLeft": rtl,
                "usesTransliteration": uses_tr,
                "coverage": "full",
            }
        )
    return rows
