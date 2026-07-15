import SwiftUI

struct MetalShadersDemo: View {
    @State private var start = Date()
    
    var body: some View {
        TimelineView(.animation) { timeline in
            let timeValue = timeline.date.timeIntervalSince(start)
            
            Image("sea-background")
                .resizable()
                .aspectRatio(contentMode: .fill)
                .frame(width: 300, height: 300)
                .clipShape(Rectangle())
                .colorEffect(ShaderLibrary.waveColor(.float(timeValue)))
        }
    }
}
