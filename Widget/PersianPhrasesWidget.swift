import WidgetKit
import SwiftUI
import AppIntents
import PersianPhrasesKit

struct PhraseEntry: TimelineEntry {
    let date: Date
    let phrase: Phrase
    let category: CategoryAppEnum
}

struct Provider: AppIntentTimelineProvider {
    func placeholder(in context: Context) -> PhraseEntry {
        PhraseEntry(date: Date(), phrase: PhraseStore.placeholder, category: .all)
    }

    func snapshot(for configuration: SelectCategoryIntent, in context: Context) async -> PhraseEntry {
        PhraseEntry(
            date: Date(),
            phrase: PhraseStore.phrase(for: Date(), category: configuration.resolvedCategory),
            category: configuration.category
        )
    }

    func timeline(for configuration: SelectCategoryIntent, in context: Context) async -> Timeline<PhraseEntry> {
        let now = Date()
        let interval = PhraseStore.refreshInterval
        let entries: [PhraseEntry] = (0..<36).map { index in
            let date = now.addingTimeInterval(interval * Double(index))
            return PhraseEntry(
                date: date,
                phrase: PhraseStore.phrase(for: date, category: configuration.resolvedCategory),
                category: configuration.category
            )
        }
        return Timeline(entries: entries, policy: .atEnd)
    }
}

struct PersianPhrasesWidget: Widget {
    let kind = "PersianPhraseWidget"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(
            kind: kind,
            intent: SelectCategoryIntent.self,
            provider: Provider()
        ) { entry in
            PhraseWidgetView(entry: entry)
                .widgetURL(PhraseDeepLink.url(for: entry.phrase))
        }
        .configurationDisplayName("Persian Phrase")
        .description("A rotating everyday Persian phrase on the Home Screen or Lock Screen.")
        .supportedFamilies([
            .systemSmall, .systemMedium, .systemLarge,
            .accessoryCircular, .accessoryRectangular, .accessoryInline
        ])
    }
}

enum CategoryAppEnum: String, AppEnum {
    case all
    case greetings
    case polite
    case food
    case travel
    case daily
    case shopping
    case emergency
    case time
    case weather
    case feelings
    case work
    case family
    case health

    static var typeDisplayRepresentation: TypeDisplayRepresentation {
        TypeDisplayRepresentation(name: "Category")
    }

    static var caseDisplayRepresentations: [CategoryAppEnum: DisplayRepresentation] {
        [
            .all: DisplayRepresentation(title: "All phrases", subtitle: "همه"),
            .greetings: DisplayRepresentation(title: "Greetings", subtitle: "سلام و احوالپرسی"),
            .polite: DisplayRepresentation(title: "Polite phrases", subtitle: "تعارفات"),
            .food: DisplayRepresentation(title: "Food & drink", subtitle: "غذا و نوشیدنی"),
            .travel: DisplayRepresentation(title: "Travel", subtitle: "سفر"),
            .daily: DisplayRepresentation(title: "Daily life", subtitle: "روزمره"),
            .shopping: DisplayRepresentation(title: "Shopping", subtitle: "خرید"),
            .emergency: DisplayRepresentation(title: "Emergency", subtitle: "اضطراری"),
            .time: DisplayRepresentation(title: "Time & numbers", subtitle: "زمان و اعداد"),
            .weather: DisplayRepresentation(title: "Weather", subtitle: "آب‌وهوا"),
            .feelings: DisplayRepresentation(title: "Feelings", subtitle: "احساسات"),
            .work: DisplayRepresentation(title: "Work & school", subtitle: "کار و درس"),
            .family: DisplayRepresentation(title: "Family", subtitle: "خانواده"),
            .health: DisplayRepresentation(title: "Health", subtitle: "سلامت")
        ]
    }

    var phraseCategory: Phrase.Category? {
        switch self {
        case .all: return nil
        case .greetings: return .greetings
        case .polite: return .polite
        case .food: return .food
        case .travel: return .travel
        case .daily: return .daily
        case .shopping: return .shopping
        case .emergency: return .emergency
        case .time: return .time
        case .weather: return .weather
        case .feelings: return .feelings
        case .work: return .work
        case .family: return .family
        case .health: return .health
        }
    }
}

struct SelectCategoryIntent: WidgetConfigurationIntent {
    static var title: LocalizedStringResource = "Phrase category"
    static var description = IntentDescription("Choose which kind of Persian phrases appear on your Home Screen or Lock Screen.")

    @Parameter(title: "Category")
    var category: CategoryAppEnum

    init() {
        self.category = .all
    }

    init(category: CategoryAppEnum) {
        self.category = category
    }

    var resolvedCategory: Phrase.Category? { category.phraseCategory }
}

#Preview(as: .systemSmall) {
    PersianPhrasesWidget()
} timeline: {
    PhraseEntry(date: .now, phrase: PhraseStore.placeholder, category: .all)
}

#Preview(as: .systemMedium) {
    PersianPhrasesWidget()
} timeline: {
    PhraseEntry(date: .now, phrase: PhraseStore.placeholder, category: .all)
}

#Preview(as: .systemLarge) {
    PersianPhrasesWidget()
} timeline: {
    PhraseEntry(date: .now, phrase: PhraseStore.placeholder, category: .all)
}

#Preview(as: .accessoryCircular) {
    PersianPhrasesWidget()
} timeline: {
    PhraseEntry(date: .now, phrase: PhraseStore.placeholder, category: .all)
}

#Preview(as: .accessoryRectangular) {
    PersianPhrasesWidget()
} timeline: {
    PhraseEntry(date: .now, phrase: PhraseStore.placeholder, category: .all)
}

#Preview(as: .accessoryInline) {
    PersianPhrasesWidget()
} timeline: {
    PhraseEntry(date: .now, phrase: PhraseStore.placeholder, category: .all)
}
