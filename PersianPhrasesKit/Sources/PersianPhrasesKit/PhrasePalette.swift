import SwiftUI

public enum PhrasePalette {
    public static let cream = Color(red: 0.984, green: 0.961, blue: 0.925)
    public static let parchment = Color(red: 0.965, green: 0.933, blue: 0.878)
    public static let terracotta = Color(red: 0.722, green: 0.333, blue: 0.184)
    public static let deepTerracotta = Color(red: 0.545, green: 0.227, blue: 0.133)
    public static let ink = Color(red: 0.173, green: 0.141, blue: 0.110)
    public static let mutedInk = Color(red: 0.392, green: 0.337, blue: 0.275)
    public static let sage = Color(red: 0.357, green: 0.478, blue: 0.431)
    public static let gold = Color(red: 0.737, green: 0.580, blue: 0.275)
    public static let chipFill = Color(red: 0.953, green: 0.910, blue: 0.835)
    public static let chipStroke = Color(red: 0.855, green: 0.776, blue: 0.655)

    public static var backgroundGradient: LinearGradient {
        LinearGradient(
            colors: [cream, parchment],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
    }
}
