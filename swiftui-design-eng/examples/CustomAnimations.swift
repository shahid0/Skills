import SwiftUI

struct CustomAnimationsDemo: View {
    @State private var position: CGFloat = 0.0
    
    var body: some View {
        VStack {
            Circle()
                .fill(.orange.gradient)
                .frame(width: 50, height: 50)
                .offset(y: position)
            
            Button("Animate Gravity") {
                withAnimation(Animation(GravityBounceAnimation(duration: 1.5))) {
                    position = position == 0.0 ? 300.0 : 0.0
                }
            }
        }
    }
}

struct GravityBounceAnimation: CustomAnimation {
    let duration: TimeInterval
    
    func animate<V: VectorArithmetic>(
        value: V, 
        time: TimeInterval, 
        context: inout AnimationContext<V>
    ) -> V? {
        if time > duration { return nil }
        
        let progress = time / duration
        let yProgress = progress * progress
        return value.scaled(by: yProgress)
    }
}
