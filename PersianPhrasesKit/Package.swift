// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "PersianPhrasesKit",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(name: "PersianPhrasesKit", targets: ["PersianPhrasesKit"])
    ],
    targets: [
        .target(
            name: "PersianPhrasesKit",
            resources: [
                .process("Resources")
            ]
        ),
        .testTarget(
            name: "PersianPhrasesKitTests",
            dependencies: ["PersianPhrasesKit"]
        )
    ]
)
