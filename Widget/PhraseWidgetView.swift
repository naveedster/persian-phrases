import SwiftUI
import WidgetKit
import PersianPhrasesKit

struct PhraseWidgetView: View {
    @Environment(\.widgetFamily) private var family
    let entry: PhraseEntry

    var body: some View {
        Group {
            switch family {
            case .accessoryCircular:
                CircularLockWidget(phrase: entry.phrase)
            case .accessoryRectangular:
                RectangularLockWidget(phrase: entry.phrase)
            case .accessoryInline:
                InlineLockWidget(phrase: entry.phrase)
            case .systemSmall:
                SmallPhraseWidget(entry: entry)
            case .systemLarge:
                LargePhraseWidget(entry: entry)
            default:
                MediumPhraseWidget(entry: entry)
            }
        }
        .containerBackground(for: .widget) {
            if isAccessory {
                AccessoryWidgetBackground()
            } else {
                PhrasePalette.backgroundGradient
            }
        }
    }

    private var isAccessory: Bool {
        switch family {
        case .accessoryCircular, .accessoryRectangular, .accessoryInline:
            return true
        default:
            return false
        }
    }
}

private struct CircularLockWidget: View {
    let phrase: Phrase

    var body: some View {
        VStack(spacing: 1) {
            Text(phrase.lockScreenPersian)
                .font(.system(size: 13, weight: .semibold, design: .serif))
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .minimumScaleFactor(0.45)
                .environment(\.layoutDirection, .rightToLeft)
                .environment(\.locale, Locale(identifier: "fa"))
            Text(phrase.compactEnglish)
                .font(.system(size: 8, weight: .medium))
                .foregroundStyle(.secondary)
                .lineLimit(1)
                .minimumScaleFactor(0.6)
        }
        .padding(2)
        .widgetAccentable()
    }
}

private struct RectangularLockWidget: View {
    let phrase: Phrase

    var body: some View {
        VStack(alignment: .trailing, spacing: 1) {
            Text(phrase.persian)
                .font(.system(size: 15, weight: .semibold, design: .serif))
                .multilineTextAlignment(.trailing)
                .lineLimit(1)
                .minimumScaleFactor(0.7)
                .frame(maxWidth: .infinity, alignment: .trailing)
                .environment(\.layoutDirection, .rightToLeft)
                .environment(\.locale, Locale(identifier: "fa"))
            Text(phrase.compactEnglish)
                .font(.caption)
                .foregroundStyle(.secondary)
                .lineLimit(1)
                .minimumScaleFactor(0.8)
                .frame(maxWidth: .infinity, alignment: .leading)
            Text(phrase.transliteration)
                .font(.caption2)
                .foregroundStyle(.tertiary)
                .lineLimit(1)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
        .widgetAccentable()
    }
}

private struct InlineLockWidget: View {
    let phrase: Phrase

    var body: some View {
        Text("\(phrase.lockScreenPersian)  \(phrase.compactEnglish)")
            .environment(\.locale, Locale(identifier: "fa"))
            .widgetAccentable()
    }
}

private struct SmallPhraseWidget: View {
    let entry: PhraseEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            WidgetEyebrow(category: entry.phrase.category, compact: true)
            Spacer(minLength: 0)
            PersianLine(text: entry.phrase.persian, size: 22)
            Text(entry.phrase.english)
                .font(.caption)
                .foregroundStyle(PhrasePalette.ink)
                .lineLimit(2)
                .minimumScaleFactor(0.85)
            Text(entry.phrase.transliteration)
                .font(.caption2.italic())
                .foregroundStyle(PhrasePalette.mutedInk)
                .lineLimit(1)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
    }
}

private struct MediumPhraseWidget: View {
    let entry: PhraseEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            WidgetEyebrow(category: entry.phrase.category, compact: false)
            PersianLine(text: entry.phrase.persian, size: 26)
            Text(entry.phrase.english)
                .font(.subheadline)
                .foregroundStyle(PhrasePalette.ink)
                .lineLimit(2)
            Text(entry.phrase.transliteration)
                .font(.caption.italic())
                .foregroundStyle(PhrasePalette.mutedInk)
                .lineLimit(1)
            Spacer(minLength: 4)
            WordChipRow(words: entry.phrase.words, limit: 4)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
    }
}

private struct LargePhraseWidget: View {
    let entry: PhraseEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            WidgetEyebrow(category: entry.phrase.category, compact: false)
            PersianLine(text: entry.phrase.persian, size: 32)
            Text(entry.phrase.english)
                .font(.body)
                .foregroundStyle(PhrasePalette.ink)
                .lineLimit(3)
            Text(entry.phrase.transliteration)
                .font(.subheadline.italic())
                .foregroundStyle(PhrasePalette.mutedInk)
            if let formality = entry.phrase.formality {
                Text("\(formality.persianLabel) · \(formality.englishLabel)")
                    .font(.caption2.weight(.medium))
                    .foregroundStyle(PhrasePalette.sage)
            }
            Spacer(minLength: 6)
            Text("کلمه به کلمه")
                .font(.caption.weight(.semibold))
                .foregroundStyle(PhrasePalette.mutedInk)
                .frame(maxWidth: .infinity, alignment: .trailing)
                .environment(\.layoutDirection, .rightToLeft)
            WordChipRow(words: entry.phrase.words, limit: 8)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
    }
}

private struct WidgetEyebrow: View {
    let category: Phrase.Category
    let compact: Bool

    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: category.symbolName)
                .font(.caption2.weight(.semibold))
            Text(compact ? category.englishTitle : category.bilingualTitle)
                .font(.caption2.weight(.semibold))
                .lineLimit(1)
            Spacer(minLength: 0)
        }
        .foregroundStyle(PhrasePalette.sage)
    }
}

private struct PersianLine: View {
    let text: String
    let size: CGFloat

    var body: some View {
        Text(text)
            .font(.system(size: size, weight: .semibold, design: .serif))
            .foregroundStyle(PhrasePalette.deepTerracotta)
            .multilineTextAlignment(.trailing)
            .lineLimit(2)
            .minimumScaleFactor(0.7)
            .frame(maxWidth: .infinity, alignment: .trailing)
            .environment(\.layoutDirection, .rightToLeft)
            .environment(\.locale, Locale(identifier: "fa"))
    }
}

private struct WordChipRow: View {
    let words: [Phrase.Word]
    let limit: Int

    var body: some View {
        ViewThatFits(in: .horizontal) {
            chipStack(Array(words.prefix(limit)))
            chipStack(Array(words.prefix(max(2, limit - 2))))
            chipStack(Array(words.prefix(2)))
        }
    }

    private func chipStack(_ items: [Phrase.Word]) -> some View {
        HStack(spacing: 6) {
            ForEach(Array(items.reversed())) { word in
                VStack(alignment: .trailing, spacing: 1) {
                    Text(word.persian)
                        .font(.system(.caption, design: .serif, weight: .semibold))
                        .foregroundStyle(PhrasePalette.deepTerracotta)
                        .environment(\.layoutDirection, .rightToLeft)
                    Text(word.english)
                        .font(.system(size: 9))
                        .foregroundStyle(PhrasePalette.mutedInk)
                        .lineLimit(1)
                }
                .padding(.horizontal, 7)
                .padding(.vertical, 5)
                .background(PhrasePalette.chipFill, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
            }
        }
        .environment(\.layoutDirection, .rightToLeft)
        .frame(maxWidth: .infinity, alignment: .trailing)
    }
}
