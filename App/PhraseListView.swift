import SwiftUI
import PersianPhrasesKit

struct PhraseListView: View {
    @Binding var selectedCategory: Phrase.Category?
    @Binding var query: String

    private var phrases: [Phrase] {
        PhraseStore.search(query, in: selectedCategory)
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
        .navigationTitle("عبارات · Phrases")
        .navigationBarTitleDisplayMode(.large)
        .toolbarBackground(PhrasePalette.cream, for: .navigationBar)
        .searchable(
            text: $query,
            placement: .navigationBarDrawer(displayMode: .always),
            prompt: "جستجو · Search phrases"
        )
    }

    private var categoryBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                CategoryChip(
                    title: "همه · All",
                    symbol: "square.grid.2x2",
                    selected: selectedCategory == nil
                ) {
                    selectedCategory = nil
                }
                ForEach(Phrase.Category.allCases) { category in
                    CategoryChip(
                        title: "\(category.persianTitle) · \(category.englishTitle)",
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
                Text("Phrase book")
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(PhrasePalette.ink)
                Text(selectedCategory?.bilingualTitle ?? "\(PhraseStore.all.count) everyday phrases")
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
        if PhraseStore.all.isEmpty {
            EmptyCatalogView()
        } else if phrases.isEmpty {
            EmptySearchView(query: query)
        } else {
            LazyVStack(spacing: 12) {
                ForEach(phrases) { phrase in
                    NavigationLink(value: phrase) {
                        PhraseRowView(phrase: phrase)
                    }
                    .buttonStyle(.plain)
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
            description: Text("The bundled catalog could not be read. Rebuild the app from the PersianPhrasesKit package.")
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
