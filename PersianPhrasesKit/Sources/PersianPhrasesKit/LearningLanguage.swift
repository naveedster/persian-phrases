import Foundation

/// A learnable target language in the shared catalog.
public struct LearningLanguage: Identifiable, Codable, Hashable, Sendable {
    public let code: String
    public let bcp47: String
    public let englishName: String
    public let nativeName: String
    public let speechCode: String
    public let isRightToLeft: Bool
    public let usesTransliteration: Bool
    public let coverage: Coverage

    public var id: String { code }

    public var locale: Locale { Locale(identifier: bcp47) }

    /// Display name used in pickers: native first, then English.
    public var bilingualName: String {
        if nativeName.caseInsensitiveCompare(englishName) == .orderedSame {
            return englishName
        }
        return "\(nativeName) · \(englishName)"
    }

    public var coverageLabel: String {
        switch coverage {
        case .full: return "Full catalog"
        case .core: return "Core phrases"
        case .partial: return "Partial"
        }
    }

    public enum Coverage: String, Codable, Sendable {
        case full
        case core
        case partial
    }
}
