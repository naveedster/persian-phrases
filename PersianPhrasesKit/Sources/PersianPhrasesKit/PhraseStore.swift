import Foundation

/// Loads the bundled catalog and picks a phrase that changes on a fixed clock.
///
/// WidgetKit (and iOS) decide when a timeline actually refreshes. Entries are
/// spaced ``refreshInterval`` apart so glancing at the Home Screen often shows
/// something new — not literally on every unlock.
public enum PhraseStore {
    public static let refreshInterval: TimeInterval = 5 * 60

    public static let all: [Phrase] = load()

    public static var placeholder: Phrase {
        all.first { $0.id == "salam" } ?? all.first ?? fallbackHello
    }

    private static let fallbackHello = Phrase(
        id: "salam",
        persian: "سلام",
        english: "Hello (informal / everyday)",
        transliteration: "salām",
        category: .greetings,
        formality: .informal,
        words: [
            Phrase.Word(persian: "سلام", transliteration: "salām", english: "hello / peace")
        ]
    )

    public static func phrases(in category: Phrase.Category?) -> [Phrase] {
        guard let category else { return all }
        return all.filter { $0.category == category }
    }

    /// Deterministic rotation: the same date always maps to the same phrase.
    /// Uses a stable mix of the time slot (not Swift's randomized `Hasher`).
    public static func phrase(for date: Date, category: Phrase.Category? = nil) -> Phrase {
        let pool = phrases(in: category)
        guard !pool.isEmpty else { return placeholder }
        let slot = Int(date.timeIntervalSince1970 / refreshInterval)
        var mix = slot &* 1_000_003
        if let category {
            mix = mix &+ stableChecksum(category.rawValue)
        }
        let index = Int(mix.magnitude % UInt(pool.count))
        return pool[index]
    }

    public static func search(_ query: String, in category: Phrase.Category? = nil) -> [Phrase] {
        let pool = phrases(in: category)
        let trimmed = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return pool }
        return pool.filter { phrase in
            phrase.persian.localizedCaseInsensitiveContains(trimmed)
                || phrase.english.localizedCaseInsensitiveContains(trimmed)
                || phrase.transliteration.localizedCaseInsensitiveContains(trimmed)
                || phrase.words.contains {
                    $0.persian.localizedCaseInsensitiveContains(trimmed)
                        || $0.english.localizedCaseInsensitiveContains(trimmed)
                        || $0.transliteration.localizedCaseInsensitiveContains(trimmed)
                }
        }
    }

    private static func stableChecksum(_ value: String) -> Int {
        value.utf8.reduce(0) { $0 &* 31 &+ Int($1) }
    }

    private static func load() -> [Phrase] {
        let candidates = [
            Bundle.module.url(forResource: "phrases", withExtension: "json"),
            Bundle.module.url(forResource: "phrases", withExtension: "json", subdirectory: "Resources")
        ]
        guard let url = candidates.compactMap({ $0 }).first else {
            assertionFailure("phrases.json is missing from PersianPhrasesKit")
            return []
        }
        do {
            let data = try Data(contentsOf: url)
            let decoded = try JSONDecoder().decode([Phrase].self, from: data)
            return decoded
        } catch {
            assertionFailure("Failed to decode phrases.json: \(error)")
            return []
        }
    }
}
