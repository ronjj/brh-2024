import SwiftUI

struct SplashScreenView: View {
    @State var isActive: Bool = false
    @State private var size = 0.8
    @State private var opacity = 0.5
    
    var body: some View {
        if isActive {
            NavigationStack {
                MacroOnboardingView()
            }
        } else {
            ZStack {
                LinearGradient(colors: [Color.darkGreen, Color.lightGreen],
                               startPoint: .bottomLeading,
                               endPoint: .topTrailing)
                VStack {
                    Text("WellBite")
                        .font(.system(size: 60, weight: .bold, design: .rounded))
                        .foregroundColor(.white)
                        .scaleEffect(size)
                        .opacity(opacity)
                        .onAppear {
                            withAnimation(.easeIn(duration: 1.75)) {
                                self.size = 0.9
                                self.opacity = 1.00
                            }
                        }
                }
            }
            .ignoresSafeArea(.all)
            .onAppear {
                DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                    withAnimation {
                        self.isActive = true
                    }
                }
            }
        }
    }
}

// Add these color extensions to your project
extension Color {
    static let darkGreen = Color(red: 0, green: 0.5, blue: 0)
    static let lightGreen = Color(red: 0.5, green: 1, blue: 0.5)
}
