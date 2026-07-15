import SwiftUI

struct KeyframeAnimationsDemo: View {
    @State private var errorTrigger = false
    @State private var bounceTrigger = false
    
    var body: some View {
        VStack(spacing: 30) {
            Image(systemName: "bell.fill")
                .font(.largeTitle)
                .phaseAnimator([1.0, 1.25, 0.9, 1.0], trigger: bounceTrigger) { content, phase in
                    content
                        .scaleEffect(phase)
                } animation: { phase in
                    switch phase {
                    case 1.25: .snappy(duration: 0.15)
                    case 0.9: .bouncy(duration: 0.2)
                    default: .smooth
                    }
                }
                .onTapGesture { bounceTrigger.toggle() }
            
            Button("Trigger Error Shake") {
                errorTrigger.toggle()
            }
            .keyframeAnimator(
                initialValue: ShakeEffectValue(),
                trigger: errorTrigger
            ) { content, value in
                content
                    .offset(x: value.xOffset)
                    .scaleEffect(value.scale)
            } keyframes: { _ in
                KeyframeTrack(\.xOffset) {
                    CubicKeyframe(-15, duration: 0.05)
                    SpringKeyframe(15, duration: 0.1, spring: .bouncy)
                    SpringKeyframe(-10, duration: 0.1, spring: .snappy)
                    SpringKeyframe(0, duration: 0.1, spring: .smooth)
                }
                KeyframeTrack(\.scale) {
                    CubicKeyframe(0.95, duration: 0.05)
                    CubicKeyframe(1.05, duration: 0.1)
                    CubicKeyframe(1.0, duration: 0.2)
                }
            }
        }
    }
}

struct ShakeEffectValue {
    var xOffset: CGFloat = 0.0
    var scale: CGFloat = 1.0
}
