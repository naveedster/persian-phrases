#!/usr/bin/env python3
"""Validate the generated multilingual catalog without Xcode."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "PersianPhrasesKit" / "Sources" / "PersianPhrasesKit" / "Resources"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from languages import LANG_CODES  # noqa: E402

CATEGORIES = {
    "greetings",
    "polite",
    "food",
    "travel",
    "daily",
    "shopping",
    "emergency",
    "time",
    "weather",
    "feelings",
    "work",
    "family",
    "health",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    languages = load(RES / "languages.json")
    concepts = load(RES / "concepts.json")
    codes = [row["code"] for row in languages]

    assert len(languages) == 30, f"expected 30 languages, got {len(languages)}"
    assert codes == LANG_CODES, "languages.json order/codes drifted from scripts/languages.py"
    assert len({row["code"] for row in languages}) == 30
    assert any(row["code"] == "fa" for row in languages)
    assert any(row["code"] == "zh-Hans" for row in languages)
    assert len(concepts) >= 3000, f"need >= 3000 concepts, got {len(concepts)}"
    ids = [c["id"] for c in concepts]
    assert len(ids) == len(set(ids)), "duplicate concept ids"
    present_cats = {c["category"] for c in concepts}
    missing_cats = CATEGORIES - present_cats
    assert not missing_cats, f"missing categories: {missing_cats}"

    curated = [c for c in concepts if c.get("source") == "curated"]
    assert len(curated) >= 40, f"expected a hand-written core, got {len(curated)}"

    for lang in languages:
        fname = lang["code"].replace("-", "_") + ".json"
        path = RES / "translations" / fname
        assert path.exists(), f"missing {path.name}"
        data = load(path)
        missing = [cid for cid in ids if cid not in data]
        assert not missing, f"{lang['code']} missing {len(missing)} ids, e.g. {missing[:5]}"
        hello = data["hello"]
        assert hello["text"].strip(), f"{lang['code']} hello is empty"
        if lang["usesTransliteration"]:
            assert hello.get("transliteration"), f"{lang['code']} hello needs transliteration"
        else:
            assert not hello.get("transliteration"), f"{lang['code']} should omit transliteration"

    fa = load(RES / "translations" / "fa.json")
    es = load(RES / "translations" / "es.json")
    assert fa["hello"]["text"] == "سلام"
    assert fa["hello"]["transliteration"] == "salām"
    assert es["hello"]["text"] == "Hola"
    assert "transliteration" not in es["hello"]

    print(f"OK: {len(concepts)} concepts × {len(languages)} languages")
    print(f"curated core: {len(curated)}; generated: {len(concepts) - len(curated)}")


if __name__ == "__main__":
    main()
