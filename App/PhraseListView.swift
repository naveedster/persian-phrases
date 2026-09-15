import SwiftUI
import PersianPhrasesKit

struct PhraseListView: View {
    @EnvironmentObject private var settings: AppPhraseSettings
    @Binding var selectedCategory: Phrase.Category?
    @Binding var query: String

    private var phrases: [Phrase] {
        let effective: Phrase.Category? = {
            guard let selectedCategory else { return nil }
            return settings.isEnabled(selectedCategory) ? selectedCategory : nil
        }()
        return PhraseStore.search(query, category: effective, matching: settings.snapshot)
    }

    private var enabledCategories: [Phrase.Category] {
        Phrase.Category.allCases.filter { settings.isEnabled($0) }
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                AddWidgetGuide()
                categoryBar
                resultsHeader
                phraseCards
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 32)
        }
        .background(PhrasePalette.backgroundGradient.ignoresSafeArea())
        .navigationTitle("Daily Phrases")
        .navigationBarTitleDisplayMode(.large)
        .toolbarBackground(PhrasePalette.cream, for: .navigationBar)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                NavigationLink {
                    SettingsView(settings: settings)
                } label: {
                    Image(systemName: "gearshape.fill")
                        .foregroundStyle(PhrasePalette.terracotta)
                }
                .accessibilityLabel("Settings")
            }
        }
        .searchable(
            text: $query,
            placement: .navigationBarDrawer(displayMode: .always),
            prompt: "Search phrases"
        )
        .onChange(of: settings.languageCode) { _, _ in
            if let selectedCategory, !settings.isEnabled(selectedCategory) {
                self.selectedCategory = nil
            }
        }
        .onChange(of: settings.enabledCategories) { _, _ in
            if let selectedCategory, !settings.isEnabled(selectedCategory) {
                self.selectedCategory = nil
            }
        }
    }

    private var categoryBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                CategoryChip(
                    title: "All",
                    symbol: "square.grid.2x2",
                    selected: selectedCategory == nil
                ) {
                    selectedCategory = nil
                }
                ForEach(enabledCategories) { category in
                    CategoryChip(
                        title: category.englishTitle,
                        symbol: category.symbolName,
                        selected: selectedCategory == category
                    ) {
                        selectedCategory = category
                    }
                }
            }
            .padding(.vertical, 2)
        }
    }

    private var resultsHeader: some View {
        HStack(alignment: .firstTextBaseline) {
            VStack(alignment: .leading, spacing: 4) {
                Text(settings.language.bilingualName)
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(PhrasePalette.ink)
                Text(selectedCategory?.englishTitle ?? "\(phrases.count) everyday phrases")
                    .font(.subheadline)
                    .foregroundStyle(PhrasePalette.mutedInk)
            }
            Spacer()
            Text("\(phrases.count)")
                .font(.caption.weight(.semibold))
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(PhrasePalette.chipFill, in: Capsule())
                .foregroundStyle(PhrasePalette.deepTerracotta)
        }
    }

    @ViewBuilder
    private var phraseCards: some View {
        if PhraseStore.concepts.isEmpty {
            EmptyCatalogView()
        } else if phrases.isEmpty {
            if query.isEmpty {
                ContentUnavailableView(
                    "No phrases in these topics",
                    systemImage: "line.3.horizontal.decrease.circle",
                    description: Text("Turn on more topics in Settings, or choose All.")
                )
                .frame(maxWidth: .infinity)
                .padding(.vertical, 24)
            } else {
                EmptySearchView(query: query)
            }
        } else {
            LazyVStack(spacing: 12) {
                ForEach(phrases) { phrase in
                    HStack(alignment: .top, spacing: 8) {
                        NavigationLink(value: phrase) {
                            PhraseRowView(phrase: phrase)
                        }
                        .buttonStyle(.plain)
                        SpeakButton(phrase: phrase, compact: true)
                            .padding(.top, 12)
                    }
                }
            }
        }
    }
}

private struct CategoryChip: View {
    let title: String
    let symbol: String
    let selected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Label(title, systemImage: symbol)
                .font(.caption.weight(.semibold))
                .lineLimit(1)
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .foregroundStyle(selected ? Color.white : PhrasePalette.ink)
                .background(selected ? PhrasePalette.terracotta : PhrasePalette.chipFill, in: Capsule())
                .overlay {
                    Capsule()
                        .strokeBorder(selected ? Color.clear : PhrasePalette.chipStroke, lineWidth: 1)
                }
        }
        .buttonStyle(.plain)
        .accessibilityAddTraits(selected ? .isSelected : [])
    }
}

private struct EmptyCatalogView: View {
    var body: some View {
        ContentUnavailableView(
            "No phrases loaded",
            systemImage: "text.book.closed",
            description: Text("The bundled catalog could not be read. Rebuild from the PersianPhrasesKit package.")
        )
        .foregroundStyle(PhrasePalette.mutedInk)
        .frame(maxWidth: .infinity)
        .padding(.vertical, 40)
    }
}

private struct EmptySearchView: View {
    let query: String

    var body: some View {
        ContentUnavailableView.search(text: query)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 24)
    }
}
