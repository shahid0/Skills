import SwiftUI

struct TransitionDemo: View {
    @State private var showCard = false
    @Namespace private var animationNamespace
    
    var body: some View {
        VStack {
            Button("Toggle") {
                withAnimation(.snappy) {
                    showCard.toggle()
                }
            }
            
            if showCard {
                RoundedRectangle(cornerRadius: 16)
                    .fill(.red.gradient)
                    .matchedGeometryEffect(id: "box", in: animationNamespace)
                    .frame(width: 200, height: 200)
                    .transition(ScaleAndRotateTransition())
            } else {
                Circle()
                    .fill(.red.gradient)
                    .matchedGeometryEffect(id: "box", in: animationNamespace)
                    .frame(width: 80, height: 80)
            }
        }
    }
}

struct ScaleAndRotateTransition: Transition {
    func body(content: Content, phase: TransitionPhase) -> some View {
        content
            .rotationEffect(.degrees(phase.isIdentity ? 0 : 45))
            .scaleEffect(phase.isIdentity ? 1.0 : 0.7)
            .opacity(phase.isIdentity ? 1.0 : 0.0)
    }
}
