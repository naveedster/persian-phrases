import SwiftUI
import PersianPhrasesKit

struct AddWidgetGuide: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(alignment: .top, spacing: 12) {
                Image(systemName: "square.stack.3d.up.fill")
                    .font(.title2)
                    .foregroundStyle(PhrasePalette.terracotta)
                    .frame(width: 36, height: 36)
                    .background(PhrasePalette.chipFill, in: RoundedRectangle(cornerRadius: 10, style: .continuous))

                VStack(alignment: .leading, spacing: 4) {
                    Text("Add a widget")
                        .font(.system(.headline, design: .serif))
                        .foregroundStyle(PhrasePalette.deepTerracotta)
                    Text("A new phrase each time you glance at your phone")
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(PhrasePalette.ink)
                }
            }

            Text("The widget is the main way to learn — a small line in your learning language on the Home Screen or Lock Screen. iOS decides the exact refresh time; phrases are queued every few minutes so you often see something new. Tap a widget to open that phrase and hear it spoken.")
                .font(.footnote)
                .foregroundStyle(PhrasePalette.mutedInk)
                .fixedSize(horizontal: false, vertical: true)

            VStack(alignment: .leading, spacing: 10) {
                step(number: 1, text: "Long-press an empty area on the Home Screen until the icons jiggle.")
                step(number: 2, text: "Tap the + button in the corner.")
                step(number: 3, text: "Search for “Daily Phrases”, choose Small, Medium, or Large, then tap Add Widget.")
            }
        }
        .padding(18)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 22, style: .continuous)
                .fill(Color.white.opacity(0.78))
        )
        .overlay {
            RoundedRectangle(cornerRadius: 22, style: .continuous)
                .strokeBorder(PhrasePalette.gold.opacity(0.45), lineWidth: 1)
        }
    }

    private func step(number: Int, text: String) -> some View {
        HStack(alignment: .top, spacing: 12) {
            Text("\(number)")
                .font(.caption.weight(.bold))
                .foregroundStyle(.white)
                .frame(width: 22, height: 22)
                .background(PhrasePalette.terracotta, in: Circle())

            Text(text)
                .font(.footnote)
                .foregroundStyle(PhrasePalette.mutedInk)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}
