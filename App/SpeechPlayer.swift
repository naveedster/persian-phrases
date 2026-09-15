import AVFoundation
import Combine
import PersianPhrasesKit
import SwiftUI

@MainActor
final class SpeechPlayer: NSObject, ObservableObject, AVSpeechSynthesizerDelegate {
    static let shared = SpeechPlayer()

    @Published private(set) var speakingID: String?

    private let synthesizer = AVSpeechSynthesizer()

    override init() {
        super.init()
        synthesizer.delegate = self
    }

    func toggle(_ phrase: Phrase) {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
            if speakingID == phrase.id {
                speakingID = nil
                return
            }
        }
        play(phrase)
    }

    func play(_ phrase: Phrase) {
        synthesizer.stopSpeaking(at: .immediate)
        activateSession()
        let utterance = AVSpeechUtterance(string: phrase.text)
        let voice = AVSpeechSynthesisVoice(language: phrase.language.speechCode)
            ?? AVSpeechSynthesisVoice(language: phrase.language.code)
            ?? AVSpeechSynthesisVoice(language: phrase.language.bcp47)
        utterance.voice = voice
        utterance.rate = AVSpeechUtteranceDefaultSpeechRate * 0.9
        utterance.pitchMultiplier = 1.0
        speakingID = phrase.id
        synthesizer.speak(utterance)
    }

    func stop() {
        synthesizer.stopSpeaking(at: .immediate)
        speakingID = nil
    }

    func isSpeaking(_ phrase: Phrase) -> Bool {
        speakingID == phrase.id && synthesizer.isSpeaking
    }

    private func activateSession() {
        let session = AVAudioSession.sharedInstance()
        // User-initiated play: speak even if the Ring/Silent switch is on.
        try? session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
        try? session.setActive(true)
    }

    nonisolated func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        Task { @MainActor in
            speakingID = nil
        }
    }

    nonisolated func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        Task { @MainActor in
            if !self.synthesizer.isSpeaking {
                speakingID = nil
            }
        }
    }
}

struct SpeakButton: View {
    let phrase: Phrase
    var compact: Bool = false
    @ObservedObject private var player = SpeechPlayer.shared

    var body: some View {
        Button {
            player.toggle(phrase)
        } label: {
            Image(systemName: player.isSpeaking(phrase) ? "stop.fill" : "speaker.wave.2.fill")
                .font(compact ? .body.weight(.semibold) : .title3.weight(.semibold))
                .foregroundStyle(PhrasePalette.terracotta)
                .frame(width: compact ? 32 : 40, height: compact ? 32 : 40)
                .background(PhrasePalette.chipFill, in: Circle())
        }
        .buttonStyle(.plain)
        .accessibilityLabel(player.isSpeaking(phrase) ? "Stop pronunciation" : "Play pronunciation")
        .accessibilityHint("Speaks the phrase in \(phrase.language.englishName)")
    }
}
