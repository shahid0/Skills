import SwiftUI

struct ScopedAnimationsDemo: View {
    @State private var isSelected = false
    
    var body: some View {
        VStack {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 80))
                .animation(.snappy) { content in
                    content
                        .scaleEffect(isSelected ? 1.25 : 1.0)
                }
                .animation(.smooth) { content in
                    content
                        .shadow(radius: isSelected ? 16 : 4)
                }
                .onTapGesture {
                    isSelected.toggle()
                }
            
            Text("User Profile")
                .font(.headline)
                .padding(.top, 8)
        }
    }
}
