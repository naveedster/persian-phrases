import SwiftUI
import PersianPhrasesKit

struct PhraseDetailView: View {
    let phrase: Phrase
    var autoPlay: Bool = false

    private var rtl: Bool { phrase.language.isRightToLeft }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                header
                translationCard
                if !phrase.words.isEmpty {
                    wordSection
                }
            }
            .padding(20)
        }
        .background(PhrasePalette.backgroundGradient.ignoresSafeArea())
        .navigationTitle(phrase.category.englishTitle)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                SpeakButton(phrase: phrase)
            }
        }
        .onAppear {
            if autoPlay {
                SpeechPlayer.shared.play(phrase)
            }
        }
    }

    private var header: some View {
        VStack(alignment: rtl ? .trailing : .leading, spacing: 12) {
            HStack {
                Label(phrase.category.englishTitle, systemImage: phrase.category.symbolName)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(PhrasePalette.sage)
                Spacer()
                if let formality = phrase.formality {
                    FormalityBadge(formality: formality)
                }
            }

            Text(phrase.text)
                .font(.system(size: 36, weight: .semibold, design: .serif))
                .foregroundStyle(PhrasePalette.deepTerracotta)
                .multilineTextAlignment(rtl ? .trailing : .leading)
                .frame(maxWidth: .infinity, alignment: rtl ? .trailing : .leading)
                .environment(\.layoutDirection, rtl ? .rightToLeft : .leftToRight)
                .environment(\.locale, phrase.language.locale)
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
            labeledBlock(title: "English", value: phrase.english)
            if phrase.showsTransliteration, let transliteration = phrase.transliteration {
                Divider().overlay(PhrasePalette.chipStroke)
                labeledBlock(title: "Transliteration", value: transliteration, italic: true)
            }
        }
        .padding(18)
        .background(Color.white.opacity(0.72), in: RoundedRectangle(cornerRadius: 20, style: .continuous))
    }

    private var wordSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Word by word")
                .font(.headline)
                .foregroundStyle(PhrasePalette.ink)

            Text(rtl
                 ? "Read right to left, the way this script is written."
                 : "Tap play to hear the full line. Tokens are a learning aid, not a linguistic parse.")
                .font(.footnote)
                .foregroundStyle(PhrasePalette.mutedInk)

            WordBreakdownView(words: phrase.words, language: phrase.language)
        }
    }

    private func labeledBlock(title: String, value: String, italic: Bool = false) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title)
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
    var language: LearningLanguage = PhraseStore.defaultLanguage

    var body: some View {
        VStack(spacing: 10) {
            ForEach(Array(words.enumerated()), id: \.element.id) { index, word in
                HStack(alignment: .top, spacing: 12) {
                    Text("\(index + 1)")
                        .font(.caption.weight(.bold))
                        .foregroundStyle(PhrasePalette.gold)
                        .frame(width: 18)

                    VStack(alignment: language.isRightToLeft ? .trailing : .leading, spacing: 4) {
                        Text(word.text)
                            .font(.system(.title3, design: .serif, weight: .semibold))
                            .foregroundStyle(PhrasePalette.deepTerracotta)
                            .frame(maxWidth: .infinity, alignment: language.isRightToLeft ? .trailing : .leading)
                            .environment(\.layoutDirection, language.isRightToLeft ? .rightToLeft : .leftToRight)
                        if language.usesTransliteration, let tr = word.transliteration, !tr.isEmpty {
                            Text(tr)
                                .font(.subheadline.italic())
                                .foregroundStyle(PhrasePalette.mutedInk)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
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
