import Combine
import PersianPhrasesKit
import SwiftUI
import WidgetKit

@MainActor
final class AppPhraseSettings: ObservableObject {
    @Published var languageCode: String {
        didSet { persist() }
    }

    @Published var enabledCategories: Set<Phrase.Category> {
        didSet { persist() }
    }

    init(snapshot: PhraseSettingsSnapshot = .load()) {
        languageCode = snapshot.languageCode
        if let enabled = snapshot.enabledCategories {
            enabledCategories = enabled
        } else {
            enabledCategories = Set(Phrase.Category.allCases)
        }
    }

    var snapshot: PhraseSettingsSnapshot {
        let raw: Set<String>
        if enabledCategories.count == Phrase.Category.allCases.count {
            raw = []
        } else {
            raw = Set(enabledCategories.map(\.rawValue))
        }
        return PhraseSettingsSnapshot(languageCode: languageCode, enabledCategoryRawValues: raw)
    }

    var language: LearningLanguage {
        PhraseStore.language(code: languageCode) ?? PhraseStore.defaultLanguage
    }

    func isEnabled(_ category: Phrase.Category) -> Bool {
        enabledCategories.contains(category)
    }

    func toggle(_ category: Phrase.Category) {
        if enabledCategories.contains(category) {
            if enabledCategories.count == 1 { return }
            enabledCategories.remove(category)
        } else {
            enabledCategories.insert(category)
        }
    }

    func selectAllCategories() {
        enabledCategories = Set(Phrase.Category.allCases)
    }

    private func persist() {
        snapshot.save()
        WidgetCenter.shared.reloadAllTimelines()
    }
}
