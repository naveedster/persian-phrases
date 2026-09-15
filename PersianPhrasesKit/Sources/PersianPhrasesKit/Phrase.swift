import Foundation

public struct Phrase: Identifiable, Hashable, Sendable {
    public let id: String
    public let english: String
    public let text: String
    public let transliteration: String?
    public let category: Category
    public let formality: Formality?
    public let words: [Word]
    public let language: LearningLanguage
    public let source: Source

    public init(
        id: String,
        english: String,
        text: String,
        transliteration: String?,
        category: Category,
        formality: Formality? = nil,
        words: [Word],
        language: LearningLanguage,
        source: Source = .generated
    ) {
        self.id = id
        self.english = english
        self.text = text
        self.transliteration = transliteration
        self.category = category
        self.formality = formality
        self.words = words
        self.language = language
        self.source = source
    }

    public var showsTransliteration: Bool {
        language.usesTransliteration && !(transliteration?.isEmpty ?? true)
    }

    /// Short learning-language text for circular Lock Screen widgets.
    public var lockScreenText: String {
        let compact = text
            .replacingOccurrences(of: "؟", with: "")
            .replacingOccurrences(of: "?", with: "")
            .replacingOccurrences(of: "!", with: "")
            .trimmingCharacters(in: .whitespacesAndNewlines)
        if compact.count <= 12 {
            return text
        }
        return words.first?.text ?? text
    }

    /// English without a trailing formality note, for tiny accessory layouts.
    public var compactEnglish: String {
        guard let idx = english.firstIndex(of: "(") else {
            return english
        }
        let head = english[..<idx].trimmingCharacters(in: .whitespaces)
        return head.isEmpty ? english : String(head)
    }

    public enum Source: String, Codable, Sendable {
        case curated
        case generated
    }
}

public extension Phrase {
    enum Category: String, Codable, CaseIterable, Identifiable, Sendable {
        case greetings
        case polite
        case food
        case travel
        case daily
        case shopping
        case emergency
        case time
        case weather
        case feelings
        case work
        case family
        case health

        public var id: String { rawValue }

        public var englishTitle: String {
            switch self {
            case .greetings: return "Greetings"
            case .polite: return "Polite"
            case .food: return "Food"
            case .travel: return "Travel"
            case .daily: return "Daily life"
            case .shopping: return "Shopping"
            case .emergency: return "Emergency"
            case .time: return "Time"
            case .weather: return "Weather"
            case .feelings: return "Feelings"
            case .work: return "Work & school"
            case .family: return "Family"
            case .health: return "Health"
            }
        }

        public var symbolName: String {
            switch self {
            case .greetings: return "hand.wave"
            case .polite: return "heart"
            case .food: return "fork.knife"
            case .travel: return "airplane"
            case .daily: return "sun.max"
            case .shopping: return "bag"
            case .emergency: return "exclamationmark.triangle"
            case .time: return "clock"
            case .weather: return "cloud.sun"
            case .feelings: return "face.smiling"
            case .work: return "briefcase"
            case .family: return "house"
            case .health: return "cross.case"
            }
        }
    }

    enum Formality: String, Codable, Sendable {
        case formal
        case informal

        public var englishLabel: String {
            switch self {
            case .formal: return "Formal"
            case .informal: return "Informal"
            }
        }
    }

    struct Word: Hashable, Sendable, Identifiable {
        public let text: String
        public let transliteration: String?
        public let english: String

        public var id: String { "\(text)|\(transliteration ?? "")|\(english)" }

        public init(text: String, transliteration: String? = nil, english: String) {
            self.text = text
            self.transliteration = transliteration
            self.english = english
        }
    }
}
