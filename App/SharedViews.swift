import SwiftUI
import PersianPhrasesKit

struct PhraseRowView: View {
    let phrase: Phrase

    private var rtl: Bool { phrase.language.isRightToLeft }

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(alignment: .firstTextBaseline) {
                Text(phrase.category.englishTitle.uppercased())
                    .font(.caption2.weight(.semibold))
                    .tracking(0.6)
                    .foregroundStyle(PhrasePalette.sage)
                Spacer(minLength: 8)
                if let formality = phrase.formality {
                    FormalityBadge(formality: formality)
                }
            }

            Text(phrase.text)
                .font(.system(.title2, design: .serif, weight: .semibold))
                .foregroundStyle(PhrasePalette.deepTerracotta)
                .multilineTextAlignment(rtl ? .trailing : .leading)
                .frame(maxWidth: .infinity, alignment: rtl ? .trailing : .leading)
                .environment(\.layoutDirection, rtl ? .rightToLeft : .leftToRight)
                .environment(\.locale, phrase.language.locale)

            Text(phrase.english)
                .font(.body)
                .foregroundStyle(PhrasePalette.ink)
                .multilineTextAlignment(.leading)

            if phrase.showsTransliteration, let transliteration = phrase.transliteration {
                Text(transliteration)
                    .font(.subheadline.italic())
                    .foregroundStyle(PhrasePalette.mutedInk)
            }
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.white.opacity(0.72), in: RoundedRectangle(cornerRadius: 18, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .strokeBorder(PhrasePalette.chipStroke.opacity(0.7), lineWidth: 1)
        }
        .shadow(color: PhrasePalette.ink.opacity(0.05), radius: 8, y: 3)
    }
}

struct FormalityBadge: View {
    let formality: Phrase.Formality

    var body: some View {
        Text(formality.englishLabel)
            .font(.caption2.weight(.medium))
            .padding(.horizontal, 8)
            .padding(.vertical, 3)
            .foregroundStyle(PhrasePalette.deepTerracotta)
            .background(PhrasePalette.chipFill, in: Capsule())
    }
}

struct WordChip: View {
    let word: Phrase.Word
    var compact: Bool = false
    var rtl: Bool = true

    var body: some View {
        VStack(alignment: rtl ? .trailing : .leading, spacing: compact ? 1 : 3) {
            Text(word.text)
                .font(.system(compact ? .subheadline : .body, design: .serif, weight: .semibold))
                .foregroundStyle(PhrasePalette.deepTerracotta)
                .environment(\.layoutDirection, rtl ? .rightToLeft : .leftToRight)
            if !compact, let tr = word.transliteration, !tr.isEmpty {
                Text(tr)
                    .font(.caption2.italic())
                    .foregroundStyle(PhrasePalette.mutedInk)
            }
            Text(word.english)
                .font(.caption2)
                .foregroundStyle(PhrasePalette.ink)
                .multilineTextAlignment(rtl ? .trailing : .leading)
        }
        .padding(.horizontal, compact ? 8 : 10)
        .padding(.vertical, compact ? 6 : 8)
        .background(PhrasePalette.chipFill, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .strokeBorder(PhrasePalette.chipStroke, lineWidth: 1)
        }
    }
}
