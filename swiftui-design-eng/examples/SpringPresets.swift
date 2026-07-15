import SwiftUI

struct SpringPresetsDemo: View {
    @State private var isBouncy = false
    @State private var isSnappy = false
    @State private var isSmooth = false
    
    var body: some View {
        VStack(spacing: 20) {
            Button("Bouncy") {
                withAnimation(.bouncy) {
                    isBouncy.toggle()
                }
            }
            .scaleEffect(isBouncy ? 1.2 : 1.0)
            
            Button("Snappy") {
                withAnimation(.snappy) {
                    isSnappy.toggle()
                }
            }
            .scaleEffect(isSnappy ? 1.2 : 1.0)
            
            Button("Smooth") {
                withAnimation(.smooth) {
                    isSmooth.toggle()
                }
            }
            .scaleEffect(isSmooth ? 1.2 : 1.0)
        }
    }
}
