import SwiftUI
import PersianPhrasesKit

struct ContentView: View {
    @State private var path = NavigationPath()
    @State private var selectedCategory: Phrase.Category?
    @State private var query = ""

    var body: some View {
        NavigationStack(path: $path) {
            PhraseListView(
                selectedCategory: $selectedCategory,
                query: $query
            )
            .navigationDestination(for: Phrase.self) { phrase in
                PhraseDetailView(phrase: phrase)
            }
        }
        .tint(PhrasePalette.terracotta)
        .onOpenURL { url in
            guard let id = PhraseDeepLink.phraseID(from: url),
                  let phrase = PhraseStore.all.first(where: { $0.id == id }) else { return }
            path.append(phrase)
        }
    }
}

#Preview {
    ContentView()
}
