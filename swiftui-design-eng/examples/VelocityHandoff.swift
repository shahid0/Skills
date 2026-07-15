import SwiftUI

struct VelocityHandoffDemo: View {
    @GestureState private var dragOffset = CGSize.zero
    @State private var position = CGSize.zero
    
    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(.blue.gradient)
            .frame(width: 150, height: 150)
            .offset(x: position.width + dragOffset.width, y: position.height + dragOffset.height)
            .gesture(
                DragGesture()
                    .updating($dragOffset) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { value in
                        withAnimation(.spring(duration: 0.35, bounce: 0.15)) {
                            position.width += value.translation.width
                            position.height += value.translation.height
                        }
                    }
            )
    }
}

struct ManualVelocityHandoffDemo: View {
    @GestureState private var dragOffset = CGSize.zero
    @State private var position = CGSize.zero
    
    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(.purple.gradient)
            .frame(width: 150, height: 150)
            .offset(x: position.width + dragOffset.width, y: position.height + dragOffset.height)
            .gesture(
                DragGesture()
                    .updating($dragOffset) { value, state, _ in
                        state = value.translation
                    }
                    .onEnded { value in
                        let velocity = value.velocity
                        let distance = CGSize(
                            width: -value.translation.width,
                            height: -value.translation.height
                        )
                        
                        let initialVelocityY = velocity.height / (distance.height == 0 ? 1 : distance.height)
                        
                        withAnimation(
                            .interpolatingSpring(
                                mass: 1.0,
                                stiffness: 150,
                                damping: 18,
                                initialVelocity: initialVelocityY
                            )
                        ) {
                            position = .zero
                        }
                    }
            )
    }
}
