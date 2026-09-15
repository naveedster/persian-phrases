import SwiftUI
import PersianPhrasesKit

struct PhraseDetailView: View {
    let phrase: Phrase

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                header
                translationCard
                wordSection
            }
            .padding(20)
        }
        .background(PhrasePalette.backgroundGradient.ignoresSafeArea())
        .navigationTitle(phrase.category.englishTitle)
        .navigationBarTitleDisplayMode(.inline)
    }

    private var header: some View {
        VStack(alignment: .trailing, spacing: 12) {
            HStack {
                Label(phrase.category.bilingualTitle, systemImage: phrase.category.symbolName)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(PhrasePalette.sage)
                Spacer()
                if let formality = phrase.formality {
                    FormalityBadge(formality: formality)
                }
            }

            Text(phrase.persian)
                .font(.system(size: 36, weight: .semibold, design: .serif))
                .foregroundStyle(PhrasePalette.deepTerracotta)
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
                .environment(\.layoutDirection, .rightToLeft)
                .environment(\.locale, Locale(identifier: "fa"))
                .minimumScaleFactor(0.7)
        }
        .padding(20)
        .frame(maxWidth: .infinity)
        .background(Color.white.opacity(0.75), in: RoundedRectangle(cornerRadius: 24, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .strokeBorder(PhrasePalette.chipStroke.opacity(0.8), lineWidth: 1)
        }
    }

    private var translationCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            labeledBlock(persian: "معنی", english: "English", value: phrase.english)
            Divider().overlay(PhrasePalette.chipStroke)
            labeledBlock(persian: "آوانگاری", english: "Transliteration", value: phrase.transliteration, italic: true)
        }
        .padding(18)
        .background(Color.white.opacity(0.72), in: RoundedRectangle(cornerRadius: 20, style: .continuous))
    }

    private var wordSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("کلمه به کلمه · Word by word")
                .font(.headline)
                .foregroundStyle(PhrasePalette.ink)

            Text("Read right to left, the way the Persian line is written.")
                .font(.footnote)
                .foregroundStyle(PhrasePalette.mutedInk)

            WordBreakdownView(words: phrase.words)
        }
    }

    private func labeledBlock(persian: String, english: String, value: String, italic: Bool = false) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("\(persian) · \(english)")
                .font(.caption.weight(.semibold))
                .foregroundStyle(PhrasePalette.sage)
            Text(value)
                .font(italic ? .title3.italic() : .title3)
                .foregroundStyle(PhrasePalette.ink)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}

struct WordBreakdownView: View {
    let words: [Phrase.Word]

    var body: some View {
        VStack(spacing: 10) {
            ForEach(Array(words.enumerated()), id: \.element.id) { index, word in
                HStack(alignment: .top, spacing: 12) {
                    Text("\(index + 1)")
                        .font(.caption.weight(.bold))
                        .foregroundStyle(PhrasePalette.gold)
                        .frame(width: 18)

                    VStack(alignment: .trailing, spacing: 4) {
                        Text(word.persian)
                            .font(.system(.title3, design: .serif, weight: .semibold))
                            .foregroundStyle(PhrasePalette.deepTerracotta)
                            .frame(maxWidth: .infinity, alignment: .trailing)
                            .environment(\.layoutDirection, .rightToLeft)
                        Text(word.transliteration)
                            .font(.subheadline.italic())
                            .foregroundStyle(PhrasePalette.mutedInk)
                            .frame(maxWidth: .infinity, alignment: .leading)
                        Text(word.english)
                            .font(.body)
                            .foregroundStyle(PhrasePalette.ink)
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
                .padding(14)
                .background(Color.white.opacity(0.72), in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 16, style: .continuous)
                        .strokeBorder(PhrasePalette.chipStroke.opacity(0.8), lineWidth: 1)
                }
            }
        }
    }
}

#Preview {
    NavigationStack {
        PhraseDetailView(phrase: PhraseStore.placeholder)
    }
}
