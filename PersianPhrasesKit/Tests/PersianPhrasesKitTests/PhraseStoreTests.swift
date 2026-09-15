import XCTest
@testable import PersianPhrasesKit

final class PhraseStoreTests: XCTestCase {
    func testCatalogHasAtLeastOneThousandPhrases() {
        XCTAssertGreaterThanOrEqual(PhraseStore.all.count, 1000)
    }

    func testEveryPhraseHasRequiredFields() {
        for phrase in PhraseStore.all {
            XCTAssertFalse(phrase.id.isEmpty)
            XCTAssertFalse(phrase.persian.isEmpty, phrase.id)
            XCTAssertFalse(phrase.english.isEmpty, phrase.id)
            XCTAssertFalse(phrase.transliteration.isEmpty, phrase.id)
            XCTAssertFalse(phrase.words.isEmpty, phrase.id)
            for word in phrase.words {
                XCTAssertFalse(word.persian.isEmpty, phrase.id)
                XCTAssertFalse(word.english.isEmpty, phrase.id)
                XCTAssertFalse(word.transliteration.isEmpty, phrase.id)
            }
        }
    }

    func testPhraseIdsAreUnique() {
        let ids = PhraseStore.all.map(\.id)
        XCTAssertEqual(ids.count, Set(ids).count)
    }

    func testEveryCategoryIsRepresented() {
        for category in Phrase.Category.allCases {
            XCTAssertFalse(
                PhraseStore.phrases(in: category).isEmpty,
                "Missing phrases for \(category.rawValue)"
            )
        }
    }

    func testSelectionIsDeterministicForADate() {
        let date = Date(timeIntervalSince1970: 1_720_000_000)
        let first = PhraseStore.phrase(for: date)
        let second = PhraseStore.phrase(for: date)
        XCTAssertEqual(first, second)
    }

    func testNearbySlotsCanRotate() {
        let start = Date(timeIntervalSince1970: 1_720_000_000)
        let phrases = (0..<12).map { offset in
            PhraseStore.phrase(for: start.addingTimeInterval(PhraseStore.refreshInterval * Double(offset)))
        }
        XCTAssertGreaterThan(Set(phrases.map(\.id)).count, 1)
    }

    func testSearchMatchesEnglishAndPersian() {
        XCTAssertFalse(PhraseStore.search("hello").isEmpty)
        XCTAssertFalse(PhraseStore.search("سلام").isEmpty)
        XCTAssertTrue(PhraseStore.search("zzzz-not-a-phrase").isEmpty)
    }

    func testDeepLinkRoundTrip() {
        let phrase = PhraseStore.placeholder
        let url = PhraseDeepLink.url(for: phrase)
        XCTAssertEqual(PhraseDeepLink.phraseID(from: url), phrase.id)
    }
}
