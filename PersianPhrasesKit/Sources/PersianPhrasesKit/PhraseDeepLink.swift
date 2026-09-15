import Foundation

public enum PhraseDeepLink {
    public static let scheme = "persianphrases"

    public static func url(for phrase: Phrase) -> URL {
        URL(string: "\(scheme)://phrase/\(phrase.id)")!
    }

    public static func phraseID(from url: URL) -> String? {
        guard url.scheme == scheme else { return nil }
        if url.host == "phrase" {
            let id = url.pathComponents.last { $0 != "/" }
            return id?.isEmpty == false ? id : nil
        }
        return url.host
    }
}
