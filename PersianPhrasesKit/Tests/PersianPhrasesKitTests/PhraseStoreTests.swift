import XCTest
@testable import PersianPhrasesKit

final class PhraseStoreTests: XCTestCase {
    func testCatalogHasAtLeastThreeThousandConcepts() {
        XCTAssertGreaterThanOrEqual(PhraseStore.concepts.count, 3000)
    }

    func testThirtyLearningLanguages() {
        XCTAssertEqual(PhraseStore.languages.count, 30)
        XCTAssertEqual(Set(PhraseStore.languages.map(\.code)).count, 30)
        XCTAssertNotNil(PhraseStore.language(code: "fa"))
        XCTAssertNotNil(PhraseStore.language(code: "zh-Hans"))
        XCTAssertNotNil(PhraseStore.language(code: "fil"))
    }

    func testPersianAndSpanishHaveFullCoverage() {
        let fa = PhraseStore.language(code: "fa")!
        let es = PhraseStore.language(code: "es")!
        XCTAssertGreaterThanOrEqual(PhraseStore.translations(for: fa).count, 3000)
        XCTAssertGreaterThanOrEqual(PhraseStore.translations(for: es).count, 3000)
        XCTAssertEqual(fa.coverage, .full)
        XCTAssertEqual(es.coverage, .full)
    }

    func testEveryPhraseHasRequiredFields() {
        let fa = PhraseStore.defaultLanguage
        for phrase in PhraseStore.translations(for: fa).prefix(200) {
            XCTAssertFalse(phrase.id.isEmpty)
            XCTAssertFalse(phrase.text.isEmpty, phrase.id)
            XCTAssertFalse(phrase.english.isEmpty, phrase.id)
            XCTAssertFalse(phrase.words.isEmpty, phrase.id)
        }
        let hello = PhraseStore.phrase(id: "hello", language: fa)
        XCTAssertEqual(hello?.text, "سلام")
        XCTAssertEqual(hello?.transliteration, "salām")
    }

    func testPhraseIdsAreUnique() {
        let ids = PhraseStore.concepts.map(\.id)
        XCTAssertEqual(ids.count, Set(ids).count)
    }

    func testEveryCategoryIsRepresented() {
        let settings = PhraseSettingsSnapshot()
        for category in Phrase.Category.allCases {
            XCTAssertFalse(
                PhraseStore.phrases(in: category, matching: settings).isEmpty,
                "Missing phrases for \(category.rawValue)"
            )
        }
    }

    func testSelectionIsDeterministicForADate() {
        let date = Date(timeIntervalSince1970: 1_720_000_000)
        let settings = PhraseSettingsSnapshot()
        let first = PhraseStore.phrase(for: date, settings: settings)
        let second = PhraseStore.phrase(for: date, settings: settings)
        XCTAssertEqual(first, second)
    }

    func testNearbySlotsCanRotate() {
        let start = Date(timeIntervalSince1970: 1_720_000_000)
        let settings = PhraseSettingsSnapshot()
        let phrases = (0..<12).map { offset in
            PhraseStore.phrase(for: start.addingTimeInterval(PhraseStore.refreshInterval * Double(offset)), settings: settings)
        }
        XCTAssertGreaterThan(Set(phrases.map(\.id)).count, 1)
    }

    func testSearchMatchesEnglishAndLearningLanguage() {
        let settings = PhraseSettingsSnapshot()
        XCTAssertFalse(PhraseStore.search("hello", matching: settings).isEmpty)
        XCTAssertFalse(PhraseStore.search("سلام", matching: settings).isEmpty)
        XCTAssertTrue(PhraseStore.search("zzzz-not-a-phrase", matching: settings).isEmpty)
    }

    func testCategoryFilterHonorsSettings() {
        var settings = PhraseSettingsSnapshot()
        settings.enabledCategoryRawValues = ["food"]
        let phrases = PhraseStore.phrases(matching: settings)
        XCTAssertFalse(phrases.isEmpty)
        XCTAssertTrue(phrases.allSatisfy { $0.category == .food })
    }

    func testWidgetCategoryFallsBackWhenDisabledInSettings() {
        var settings = PhraseSettingsSnapshot()
        settings.enabledCategoryRawValues = ["greetings"]
        let date = Date(timeIntervalSince1970: 1_720_000_000)
        let phrase = PhraseStore.phrase(for: date, settings: settings, category: .food)
        XCTAssertEqual(phrase.category, .greetings)
    }

    func testLanguageSwitchChangesText() {
        let fa = PhraseStore.language(code: "fa")!
        let es = PhraseStore.language(code: "es")!
        let faHello = PhraseStore.phrase(id: "hello", language: fa)
        let esHello = PhraseStore.phrase(id: "hello", language: es)
        XCTAssertEqual(faHello?.text, "سلام")
        XCTAssertEqual(esHello?.text, "Hola")
        XCTAssertNotEqual(faHello?.text, esHello?.text)
    }

    func testLatinLanguagesOmitTransliteration() {
        let es = PhraseStore.language(code: "es")!
        XCTAssertFalse(es.usesTransliteration)
        let hello = PhraseStore.phrase(id: "hello", language: es)
        XCTAssertFalse(hello?.showsTransliteration ?? true)
    }

    func testDeepLinkRoundTrip() {
        let phrase = PhraseStore.placeholder
        let url = PhraseDeepLink.url(for: phrase, autoPlay: true)
        XCTAssertEqual(PhraseDeepLink.phraseID(from: url), phrase.id)
        XCTAssertTrue(PhraseDeepLink.shouldAutoPlay(from: url))
        XCTAssertEqual(url.scheme, "dailyphrases")
    }

    func testLegacyDeepLinkStillParses() {
        let url = URL(string: "persianphrases://phrase/hello")!
        XCTAssertEqual(PhraseDeepLink.phraseID(from: url), "hello")
    }
}
