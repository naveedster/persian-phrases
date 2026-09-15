import PersianPhrasesKit
import SwiftUI

struct SettingsView: View {
    @ObservedObject var settings: AppPhraseSettings

    var body: some View {
        List {
            languageSection
            topicSection
            aboutSection
        }
        .scrollContentBackground(.hidden)
        .background(PhrasePalette.backgroundGradient.ignoresSafeArea())
        .navigationTitle("Settings")
        .navigationBarTitleDisplayMode(.inline)
    }

    private var languageSection: some View {
        Section {
            ForEach(PhraseStore.languages) { language in
                Button {
                    settings.languageCode = language.code
                } label: {
                    HStack(spacing: 12) {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(language.nativeName)
                                .font(.body.weight(.semibold))
                                .foregroundStyle(PhrasePalette.ink)
                                .environment(\.layoutDirection, language.isRightToLeft ? .rightToLeft : .leftToRight)
                            Text(language.englishName)
                                .font(.caption)
                                .foregroundStyle(PhrasePalette.mutedInk)
                        }
                        Spacer()
                        Text(language.coverageLabel)
                            .font(.caption2.weight(.medium))
                            .foregroundStyle(PhrasePalette.sage)
                        if settings.languageCode == language.code {
                            Image(systemName: "checkmark.circle.fill")
                                .foregroundStyle(PhrasePalette.terracotta)
                        }
                    }
                }
                .accessibilityAddTraits(settings.languageCode == language.code ? .isSelected : [])
            }
        } header: {
            Text("Learning language")
        } footer: {
            Text("Widgets use this language. English stays the gloss. Every listed language ships the full \(PhraseStore.concepts.count) phrase catalog. Greetings, politeness, and emergency lines are hand-written; the rest are generated from shared templates (see README).")
        }
    }

    private var topicSection: some View {
        Section {
            Button("Select all topics") {
                settings.selectAllCategories()
            }
            .foregroundStyle(PhrasePalette.terracotta)

            ForEach(Phrase.Category.allCases) { category in
                Button {
                    settings.toggle(category)
                } label: {
                    HStack {
                        Label(category.englishTitle, systemImage: category.symbolName)
                            .foregroundStyle(PhrasePalette.ink)
                        Spacer()
                        if settings.isEnabled(category) {
                            Image(systemName: "checkmark.circle.fill")
                                .foregroundStyle(PhrasePalette.terracotta)
                        } else {
                            Image(systemName: "circle")
                                .foregroundStyle(PhrasePalette.chipStroke)
                        }
                    }
                }
                .accessibilityAddTraits(settings.isEnabled(category) ? .isSelected : [])
            }
        } header: {
            Text("Topics")
        } footer: {
            Text("Home Screen and Lock Screen widgets only rotate phrases in the topics you keep on. At least one topic stays selected.")
        }
    }

    private var aboutSection: some View {
        Section {
            LabeledContent("Catalog", value: "\(PhraseStore.concepts.count) phrases")
            LabeledContent("Languages", value: "\(PhraseStore.languages.count)")
            LabeledContent("Active", value: settings.language.bilingualName)
        } header: {
            Text("Catalog")
        } footer: {
            Text("Pronunciation uses on-device speech (AVSpeechSynthesizer). Quality varies by language and iOS voice pack.")
        }
    }
}

#Preview {
    NavigationStack {
        SettingsView(settings: AppPhraseSettings())
    }
}
