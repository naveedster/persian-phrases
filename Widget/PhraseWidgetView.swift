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
            Text(phrase.lockScreenText)
                .font(.system(size: 13, weight: .semibold, design: .serif))
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .minimumScaleFactor(0.45)
                .environment(\.layoutDirection, phrase.language.isRightToLeft ? .rightToLeft : .leftToRight)
                .environment(\.locale, phrase.language.locale)
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
        VStack(alignment: phrase.language.isRightToLeft ? .trailing : .leading, spacing: 1) {
            Text(phrase.text)
                .font(.system(size: 15, weight: .semibold, design: .serif))
                .multilineTextAlignment(phrase.language.isRightToLeft ? .trailing : .leading)
                .lineLimit(1)
                .minimumScaleFactor(0.7)
                .frame(maxWidth: .infinity, alignment: phrase.language.isRightToLeft ? .trailing : .leading)
                .environment(\.layoutDirection, phrase.language.isRightToLeft ? .rightToLeft : .leftToRight)
                .environment(\.locale, phrase.language.locale)
            Text(phrase.compactEnglish)
                .font(.caption)
                .foregroundStyle(.secondary)
                .lineLimit(1)
                .minimumScaleFactor(0.8)
                .frame(maxWidth: .infinity, alignment: .leading)
            if phrase.showsTransliteration, let transliteration = phrase.transliteration {
                Text(transliteration)
                    .font(.caption2)
                    .foregroundStyle(.tertiary)
                    .lineLimit(1)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .widgetAccentable()
    }
}

private struct InlineLockWidget: View {
    let phrase: Phrase

    var body: some View {
        Text("\(phrase.lockScreenText)  \(phrase.compactEnglish)")
            .environment(\.locale, phrase.language.locale)
            .widgetAccentable()
    }
}

private struct SmallPhraseWidget: View {
    let entry: PhraseEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            WidgetEyebrow(phrase: entry.phrase, compact: true)
            Spacer(minLength: 0)
            LearningLine(phrase: entry.phrase, size: 22)
            Text(entry.phrase.english)
                .font(.caption)
                .foregroundStyle(PhrasePalette.ink)
                .lineLimit(2)
                .minimumScaleFactor(0.85)
            if entry.phrase.showsTransliteration, let transliteration = entry.phrase.transliteration {
                Text(transliteration)
                    .font(.caption2.italic())
                    .foregroundStyle(PhrasePalette.mutedInk)
                    .lineLimit(1)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
    }
}

private struct MediumPhraseWidget: View {
    let entry: PhraseEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            WidgetEyebrow(phrase: entry.phrase, compact: false)
            LearningLine(phrase: entry.phrase, size: 26)
            Text(entry.phrase.english)
                .font(.subheadline)
                .foregroundStyle(PhrasePalette.ink)
                .lineLimit(2)
            if entry.phrase.showsTransliteration, let transliteration = entry.phrase.transliteration {
                Text(transliteration)
                    .font(.caption.italic())
                    .foregroundStyle(PhrasePalette.mutedInk)
                    .lineLimit(1)
            }
            Spacer(minLength: 4)
            WordChipRow(phrase: entry.phrase, limit: 4)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
    }
}

private struct LargePhraseWidget: View {
    let entry: PhraseEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            WidgetEyebrow(phrase: entry.phrase, compact: false)
            LearningLine(phrase: entry.phrase, size: 32)
            Text(entry.phrase.english)
                .font(.body)
                .foregroundStyle(PhrasePalette.ink)
                .lineLimit(3)
            if entry.phrase.showsTransliteration, let transliteration = entry.phrase.transliteration {
                Text(entry.phrase.transliteration ?? transliteration)
                    .font(.subheadline.italic())
                    .foregroundStyle(PhrasePalette.mutedInk)
            }
            if let formality = entry.phrase.formality {
                Text(formality.englishLabel)
                    .font(.caption2.weight(.medium))
                    .foregroundStyle(PhrasePalette.sage)
            }
            Spacer(minLength: 6)
            Text("Word by word")
                .font(.caption.weight(.semibold))
                .foregroundStyle(PhrasePalette.mutedInk)
            WordChipRow(phrase: entry.phrase, limit: 8)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
    }
}

private struct WidgetEyebrow: View {
    let phrase: Phrase
    let compact: Bool

    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: phrase.category.symbolName)
                .font(.caption2.weight(.semibold))
            Text(compact ? phrase.category.englishTitle : "\(phrase.language.englishName) · \(phrase.category.englishTitle)")
                .font(.caption2.weight(.semibold))
                .lineLimit(1)
            Spacer(minLength: 0)
            Image(systemName: "speaker.wave.2")
                .font(.caption2)
                .opacity(0.7)
        }
        .foregroundStyle(PhrasePalette.sage)
    }
}

private struct LearningLine: View {
    let phrase: Phrase
    let size: CGFloat

    var body: some View {
        Text(phrase.text)
            .font(.system(size: size, weight: .semibold, design: .serif))
            .foregroundStyle(PhrasePalette.deepTerracotta)
            .multilineTextAlignment(phrase.language.isRightToLeft ? .trailing : .leading)
            .lineLimit(2)
            .minimumScaleFactor(0.7)
            .frame(maxWidth: .infinity, alignment: phrase.language.isRightToLeft ? .trailing : .leading)
            .environment(\.layoutDirection, phrase.language.isRightToLeft ? .rightToLeft : .leftToRight)
            .environment(\.locale, phrase.language.locale)
    }
}

private struct WordChipRow: View {
    let phrase: Phrase
    let limit: Int

    var body: some View {
        ViewThatFits(in: .horizontal) {
            chipStack(Array(phrase.words.prefix(limit)))
            chipStack(Array(phrase.words.prefix(max(2, limit - 2))))
            chipStack(Array(phrase.words.prefix(2)))
        }
    }

    private func chipStack(_ items: [Phrase.Word]) -> some View {
        let rtl = phrase.language.isRightToLeft
        return HStack(spacing: 6) {
            ForEach(rtl ? Array(items.reversed()) : items) { word in
                VStack(alignment: rtl ? .trailing : .leading, spacing: 1) {
                    Text(word.text)
                        .font(.system(.caption, design: .serif, weight: .semibold))
                        .foregroundStyle(PhrasePalette.deepTerracotta)
                        .environment(\.layoutDirection, rtl ? .rightToLeft : .leftToRight)
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
        .environment(\.layoutDirection, rtl ? .rightToLeft : .leftToRight)
        .frame(maxWidth: .infinity, alignment: rtl ? .trailing : .leading)
    }
}
