import Foundation

public struct Phrase: Identifiable, Codable, Hashable, Sendable {
    public let id: String
    public let persian: String
    public let english: String
    public let transliteration: String
    public let category: Category
    public let formality: Formality?
    public let words: [Word]

    public init(
        id: String,
        persian: String,
        english: String,
        transliteration: String,
        category: Category,
        formality: Formality? = nil,
        words: [Word]
    ) {
        self.id = id
        self.persian = persian
        self.english = english
        self.transliteration = transliteration
        self.category = category
        self.formality = formality
        self.words = words
    }

    /// Short Persian for circular Lock Screen widgets.
    public var lockScreenPersian: String {
        let compact = persian
            .replacingOccurrences(of: "؟", with: "")
            .replacingOccurrences(of: "!", with: "")
            .trimmingCharacters(in: .whitespacesAndNewlines)
        if compact.count <= 12 {
            return persian
        }
        return words.first?.persian ?? persian
    }

    /// English without a trailing formality note, for tiny accessory layouts.
    public var compactEnglish: String {
        guard let idx = english.firstIndex(of: "(") else {
            return english
        }
        let head = english[..<idx].trimmingCharacters(in: .whitespaces)
        return head.isEmpty ? english : String(head)
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

        public var persianTitle: String {
            switch self {
            case .greetings: return "سلام و احوالپرسی"
            case .polite: return "تعارفات"
            case .food: return "غذا و نوشیدنی"
            case .travel: return "سفر"
            case .daily: return "روزمره"
            case .shopping: return "خرید"
            case .emergency: return "اضطراری"
            case .time: return "زمان و اعداد"
            case .weather: return "آب‌وهوا"
            case .feelings: return "احساسات"
            case .work: return "کار و درس"
            case .family: return "خانواده"
            case .health: return "سلامت"
            }
        }

        public var bilingualTitle: String {
            "\(persianTitle) · \(englishTitle)"
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

        public var persianLabel: String {
            switch self {
            case .formal: return "رسمی"
            case .informal: return "غیررسمی"
            }
        }
    }

    struct Word: Codable, Hashable, Sendable, Identifiable {
        public let persian: String
        public let transliteration: String
        public let english: String

        public var id: String { "\(persian)|\(transliteration)|\(english)" }

        public init(persian: String, transliteration: String, english: String) {
            self.persian = persian
            self.transliteration = transliteration
            self.english = english
        }
    }
}
