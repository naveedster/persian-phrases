import Foundation

public enum PhraseDeepLink {
    public static let scheme = "dailyphrases"
    public static let legacyScheme = "persianphrases"

    public static func url(for phrase: Phrase, autoPlay: Bool = true) -> URL {
        var components = URLComponents()
        components.scheme = scheme
        components.host = "phrase"
        components.path = "/\(phrase.id)"
        if autoPlay {
            components.queryItems = [URLQueryItem(name: "play", value: "1")]
        }
        return components.url ?? URL(string: "\(scheme)://phrase/\(phrase.id)")!
    }

    public static func phraseID(from url: URL) -> String? {
        guard url.scheme == scheme || url.scheme == legacyScheme else { return nil }
        if url.host == "phrase" {
            let id = url.pathComponents.last { $0 != "/" }
            return id?.isEmpty == false ? id : nil
        }
        return url.host
    }

    public static func shouldAutoPlay(from url: URL) -> Bool {
        guard let items = URLComponents(url: url, resolvingAgainstBaseURL: false)?.queryItems else {
            return url.scheme == scheme || url.scheme == legacyScheme
        }
        return items.contains { $0.name == "play" && ($0.value == nil || $0.value == "1" || $0.value?.lowercased() == "true") }
    }
}
