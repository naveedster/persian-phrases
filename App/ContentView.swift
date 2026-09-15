import SwiftUI
import PersianPhrasesKit

struct ContentView: View {
    @EnvironmentObject private var settings: AppPhraseSettings
    @State private var path = NavigationPath()
    @State private var selectedCategory: Phrase.Category?
    @State private var query = ""
    @State private var autoPlayID: String?

    var body: some View {
        NavigationStack(path: $path) {
            PhraseListView(
                selectedCategory: $selectedCategory,
                query: $query
            )
            .navigationDestination(for: Phrase.self) { phrase in
                PhraseDetailView(phrase: phrase, autoPlay: autoPlayID == phrase.id)
                    .onAppear { autoPlayID = nil }
            }
        }
        .tint(PhrasePalette.terracotta)
        .onOpenURL { url in
            open(url)
        }
        .onAppear {
            if let pending = PhraseSettingsSnapshot.pendingPlayID() {
                PhraseSettingsSnapshot.setPendingPlayID(nil)
                openPhrase(id: pending, play: true)
            }
        }
    }

    private func open(_ url: URL) {
        guard let id = PhraseDeepLink.phraseID(from: url) else { return }
        openPhrase(id: id, play: PhraseDeepLink.shouldAutoPlay(from: url))
    }

    private func openPhrase(id: String, play: Bool) {
        guard let phrase = PhraseStore.phrase(id: id, matching: settings.snapshot)
            ?? PhraseStore.phrase(id: id, language: settings.language) else { return }
        autoPlayID = play ? phrase.id : nil
        var next = NavigationPath()
        next.append(phrase)
        path = next
    }
}

#Preview {
    ContentView()
        .environmentObject(AppPhraseSettings())
}
