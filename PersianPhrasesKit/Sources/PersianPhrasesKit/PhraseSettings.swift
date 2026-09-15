import Foundation

/// Shared app + widget preferences stored in the App Group suite when available.
public struct PhraseSettingsSnapshot: Equatable, Sendable {
    public var languageCode: String
    public var enabledCategoryRawValues: Set<String>

    public static let defaultLanguageCode = "fa"
    public static let appGroupID = "group.com.persianphrases.app"

    private static let languageKey = "learningLanguageCode"
    private static let categoriesKey = "enabledCategories"
    public static let pendingPlayIDKey = "pendingAutoPlayPhraseID"

    public init(languageCode: String = defaultLanguageCode, enabledCategoryRawValues: Set<String> = []) {
        self.languageCode = languageCode
        self.enabledCategoryRawValues = enabledCategoryRawValues
    }

    public var enabledCategories: Set<Phrase.Category>? {
        let values = enabledCategoryRawValues.compactMap(Phrase.Category.init(rawValue:))
        if values.isEmpty || values.count == Phrase.Category.allCases.count {
            return nil
        }
        return Set(values)
    }

    public static func load(from defaults: UserDefaults = .phraseShared) -> PhraseSettingsSnapshot {
        let code = defaults.string(forKey: languageKey) ?? defaultLanguageCode
        let raw = defaults.stringArray(forKey: categoriesKey) ?? []
        return PhraseSettingsSnapshot(
            languageCode: code,
            enabledCategoryRawValues: Set(raw)
        )
    }

    public func save(to defaults: UserDefaults = .phraseShared) {
        defaults.set(languageCode, forKey: Self.languageKey)
        defaults.set(Array(enabledCategoryRawValues).sorted(), forKey: Self.categoriesKey)
    }

    public static func pendingPlayID(from defaults: UserDefaults = .phraseShared) -> String? {
        defaults.string(forKey: pendingPlayIDKey)
    }

    public static func setPendingPlayID(_ id: String?, defaults: UserDefaults = .phraseShared) {
        if let id, !id.isEmpty {
            defaults.set(id, forKey: pendingPlayIDKey)
        } else {
            defaults.removeObject(forKey: pendingPlayIDKey)
        }
    }
}

public extension UserDefaults {
    /// App Group suite, falling back to standard defaults when the group is unavailable
    /// (common with free Apple ID / Sideloadly signing).
    static var phraseShared: UserDefaults {
        UserDefaults(suiteName: PhraseSettingsSnapshot.appGroupID) ?? .standard
    }
}
