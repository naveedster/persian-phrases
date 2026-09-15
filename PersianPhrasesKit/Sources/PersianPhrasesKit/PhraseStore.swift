import Foundation

/// Loads the bundled catalog and picks a phrase that changes on a fixed clock.
///
/// WidgetKit (and iOS) decide when a timeline actually refreshes. Entries are
/// spaced ``refreshInterval`` apart so glancing at the Home Screen often shows
/// something new — not literally on every unlock.
public enum PhraseStore {
    public static let refreshInterval: TimeInterval = 5 * 60

    public static let languages: [LearningLanguage] = loadLanguages()

    public static var defaultLanguage: LearningLanguage {
        language(code: PhraseSettingsSnapshot.defaultLanguageCode) ?? languages.first { $0.code == "fa" } ?? languages[0]
    }

    public static func language(code: String) -> LearningLanguage? {
        languages.first { $0.code == code }
    }

    /// Concepts shared across every language (English gloss + category).
    public static let concepts: [Concept] = loadConcepts()

    public static var placeholder: Phrase {
        phrase(id: "hello", language: defaultLanguage)
            ?? phrase(for: Date(), settings: .init())
    }

    public static func phrases(matching settings: PhraseSettingsSnapshot) -> [Phrase] {
        let language = language(code: settings.languageCode) ?? defaultLanguage
        let all = translations(for: language)
        guard let categories = settings.enabledCategories else { return all }
        return all.filter { categories.contains($0.category) }
    }

    public static func phrases(in category: Phrase.Category?, matching settings: PhraseSettingsSnapshot) -> [Phrase] {
        let pool = phrases(matching: settings)
        guard let category else { return pool }
        return pool.filter { $0.category == category }
    }

    public static func phrase(id: String, language: LearningLanguage) -> Phrase? {
        translations(for: language).first { $0.id == id }
    }

    public static func phrase(id: String, matching settings: PhraseSettingsSnapshot) -> Phrase? {
        phrases(matching: settings).first { $0.id == id }
            ?? phrase(id: id, language: language(code: settings.languageCode) ?? defaultLanguage)
    }

    /// Deterministic rotation: the same date always maps to the same phrase.
    public static func phrase(for date: Date, settings: PhraseSettingsSnapshot, category: Phrase.Category? = nil) -> Phrase {
        var pool = phrases(in: category, matching: settings)
        if pool.isEmpty {
            pool = phrases(matching: settings)
        }
        guard !pool.isEmpty else {
            return translations(for: language(code: settings.languageCode) ?? defaultLanguage).first
                ?? fallbackHello
        }
        let slot = Int(date.timeIntervalSince1970 / refreshInterval)
        var mix = slot &* 1_000_003
        mix = mix &+ stableChecksum(settings.languageCode)
        if let category {
            mix = mix &+ stableChecksum(category.rawValue)
        } else if let enabled = settings.enabledCategories {
            mix = mix &+ stableChecksum(enabled.map(\.rawValue).sorted().joined(separator: ","))
        }
        let index = Int(mix.magnitude % UInt(pool.count))
        return pool[index]
    }

    public static func search(_ query: String, category: Phrase.Category? = nil, matching settings: PhraseSettingsSnapshot) -> [Phrase] {
        let pool = phrases(in: category, matching: settings)
        let trimmed = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return pool }
        return pool.filter { phrase in
            phrase.text.localizedCaseInsensitiveContains(trimmed)
                || phrase.english.localizedCaseInsensitiveContains(trimmed)
                || (phrase.transliteration?.localizedCaseInsensitiveContains(trimmed) ?? false)
                || phrase.words.contains {
                    $0.text.localizedCaseInsensitiveContains(trimmed)
                        || $0.english.localizedCaseInsensitiveContains(trimmed)
                        || ($0.transliteration?.localizedCaseInsensitiveContains(trimmed) ?? false)
                }
        }
    }

    public static func coverageCount(for language: LearningLanguage) -> Int {
        translations(for: language).count
    }

    // MARK: - Internals

    public struct Concept: Codable, Sendable, Hashable, Identifiable {
        public let id: String
        public let category: Phrase.Category
        public let formality: Phrase.Formality?
        public let english: String
        public let source: Phrase.Source
    }

    private struct TranslationFile: Codable {
        let text: String
        let transliteration: String?
        let words: [WordDTO]
    }

    private struct WordDTO: Codable {
        let text: String
        let transliteration: String?
        let english: String
    }

    private static let cacheLock = NSLock()
    private static var translationCache: [String: [Phrase]] = [:]

    private static let fallbackLanguage = LearningLanguage(
        code: "fa",
        bcp47: "fa-IR",
        englishName: "Persian",
        nativeName: "فارسی",
        speechCode: "fa-IR",
        isRightToLeft: true,
        usesTransliteration: true,
        coverage: .full
    )

    private static var fallbackHello: Phrase {
        Phrase(
            id: "hello",
            english: "Hello",
            text: "سلام",
            transliteration: "salām",
            category: .greetings,
            formality: .informal,
            words: [Phrase.Word(text: "سلام", transliteration: "salām", english: "hello")],
            language: fallbackLanguage,
            source: .curated
        )
    }

    public static func translations(for language: LearningLanguage) -> [Phrase] {
        cacheLock.lock()
        defer { cacheLock.unlock() }
        if let cached = translationCache[language.code] {
            return cached
        }
        let loaded = loadTranslations(for: language)
        translationCache[language.code] = loaded
        return loaded
    }

    private static func stableChecksum(_ value: String) -> Int {
        value.utf8.reduce(0) { $0 &* 31 &+ Int($1) }
    }

    private static func resourceURL(name: String, ext: String, subdirectory: String? = nil) -> URL? {
        let candidates = [
            Bundle.module.url(forResource: name, withExtension: ext, subdirectory: subdirectory),
            Bundle.module.url(forResource: name, withExtension: ext),
            Bundle.module.url(forResource: name, withExtension: ext, subdirectory: "Resources")
        ]
        return candidates.compactMap { $0 }.first
    }

    private static func loadLanguages() -> [LearningLanguage] {
        guard let url = resourceURL(name: "languages", ext: "json") else {
            assertionFailure("languages.json is missing")
            return [fallbackLanguage]
        }
        do {
            let data = try Data(contentsOf: url)
            return try JSONDecoder().decode([LearningLanguage].self, from: data)
        } catch {
            assertionFailure("Failed to decode languages.json: \(error)")
            return [fallbackLanguage]
        }
    }

    private static func loadConcepts() -> [Concept] {
        guard let url = resourceURL(name: "concepts", ext: "json") else {
            assertionFailure("concepts.json is missing")
            return []
        }
        do {
            let data = try Data(contentsOf: url)
            return try JSONDecoder().decode([Concept].self, from: data)
        } catch {
            assertionFailure("Failed to decode concepts.json: \(error)")
            return []
        }
    }

    private static func loadTranslations(for language: LearningLanguage) -> [Phrase] {
        let fileName = language.code.replacingOccurrences(of: "-", with: "_")
        guard let url = resourceURL(name: fileName, ext: "json", subdirectory: "translations")
            ?? resourceURL(name: fileName, ext: "json") else {
            assertionFailure("Missing translation file for \(language.code)")
            return []
        }
        do {
            let data = try Data(contentsOf: url)
            let decoded = try JSONDecoder().decode([String: TranslationFile].self, from: data)
            let conceptByID = Dictionary(uniqueKeysWithValues: concepts.map { ($0.id, $0) })
            var phrases: [Phrase] = []
            phrases.reserveCapacity(decoded.count)
            for concept in concepts {
                guard let tr = decoded[concept.id] else { continue }
                let words = tr.words.map {
                    Phrase.Word(text: $0.text, transliteration: $0.transliteration, english: $0.english)
                }
                phrases.append(
                    Phrase(
                        id: concept.id,
                        english: concept.english,
                        text: tr.text,
                        transliteration: tr.transliteration,
                        category: concept.category,
                        formality: concept.formality,
                        words: words,
                        language: language,
                        source: concept.source
                    )
                )
            }
            // Keep any extra translated IDs that are not in concepts.json (shouldn't happen).
            if phrases.count != decoded.count {
                for (id, tr) in decoded where conceptByID[id] == nil {
                    phrases.append(
                        Phrase(
                            id: id,
                            english: tr.words.map(\.english).joined(separator: " "),
                            text: tr.text,
                            transliteration: tr.transliteration,
                            category: .daily,
                            words: tr.words.map {
                                Phrase.Word(text: $0.text, transliteration: $0.transliteration, english: $0.english)
                            },
                            language: language,
                            source: .generated
                        )
                    )
                }
            }
            return phrases
        } catch {
            assertionFailure("Failed to decode \(language.code) translations: \(error)")
            return []
        }
    }
}
