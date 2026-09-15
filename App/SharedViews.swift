import SwiftUI
import PersianPhrasesKit

struct PhraseRowView: View {
    let phrase: Phrase

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

            Text(phrase.persian)
                .font(.system(.title2, design: .serif, weight: .semibold))
                .foregroundStyle(PhrasePalette.deepTerracotta)
                .multilineTextAlignment(.trailing)
                .frame(maxWidth: .infinity, alignment: .trailing)
                .environment(\.layoutDirection, .rightToLeft)
                .environment(\.locale, Locale(identifier: "fa"))

            Text(phrase.english)
                .font(.body)
                .foregroundStyle(PhrasePalette.ink)
                .multilineTextAlignment(.leading)

            Text(phrase.transliteration)
                .font(.subheadline.italic())
                .foregroundStyle(PhrasePalette.mutedInk)
        }
        .padding(16)
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
        Text("\(formality.persianLabel) · \(formality.englishLabel)")
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

    var body: some View {
        VStack(alignment: .trailing, spacing: compact ? 1 : 3) {
            Text(word.persian)
                .font(.system(compact ? .subheadline : .body, design: .serif, weight: .semibold))
                .foregroundStyle(PhrasePalette.deepTerracotta)
                .environment(\.layoutDirection, .rightToLeft)
            if !compact {
                Text(word.transliteration)
                    .font(.caption2.italic())
                    .foregroundStyle(PhrasePalette.mutedInk)
            }
            Text(word.english)
                .font(.caption2)
                .foregroundStyle(PhrasePalette.ink)
                .multilineTextAlignment(.trailing)
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
