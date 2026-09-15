import SwiftUI
import PersianPhrasesKit

@main
struct PersianPhrasesApp: App {
    @StateObject private var settings = AppPhraseSettings()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(settings)
                .preferredColorScheme(.light)
        }
    }
}
