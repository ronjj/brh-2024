import SwiftUI

struct MacroOnboardingView: View {
    @AppStorage("userCalorieGoal") private var userCalorieGoal = ""
    @AppStorage("userProteinGoal") private var userProteinGoal = ""
    @AppStorage("userCarbGoal") private var userCarbGoal = ""
    @AppStorage("userFatGoal") private var userFatGoal = ""
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
    @State private var currentStep = 0
    @State private var navigateToHome = false
    
    var body: some View {
        NavigationView {
            VStack {
                if currentStep == 0 {
                    MacroInputView(currentStep: $currentStep)
                } else {
                    GoogleLoginView(onLoginSuccess: {
                        completeOnboarding()
                        navigateToHome = true
                    })
                }
            }
            .navigationBarHidden(true)
            .background(
                NavigationLink(destination: HomeView().navigationBarBackButtonHidden(true), isActive: $navigateToHome) {
                    EmptyView()
                }
            )
        }
    }
    
    func completeOnboarding() {
        hasCompletedOnboarding = true
    }
}

struct MacroInputView: View {
    @AppStorage("userCalorieGoal") private var userCalorieGoal = ""
    @AppStorage("userProteinGoal") private var userProteinGoal = ""
    @AppStorage("userCarbGoal") private var userCarbGoal = ""
    @AppStorage("userFatGoal") private var userFatGoal = ""
    @Binding var currentStep: Int
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Set Your Nutrition Goals")
                .font(.largeTitle)
                .padding()
            
            nutritionInputView(title: "What is your daily caloric goal?", value: $userCalorieGoal, unit: "calories")
            nutritionInputView(title: "How many grams of protein?", value: $userProteinGoal, unit: "g")
            nutritionInputView(title: "How many grams of carbs?", value: $userCarbGoal, unit: "g")
            nutritionInputView(title: "How many grams of fats?", value: $userFatGoal, unit: "g")
            
            Spacer()
            
            Button {
                currentStep += 1
            } label: {
                Text("Next")
                    .frame(minWidth: 0, maxWidth: .infinity)
                    .padding()
                    .background(Color.accentColor)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            .padding()
        }
        .padding()
    }
    
    func nutritionInputView(title: String, value: Binding<String>, unit: String) -> some View {
        VStack(alignment: .leading) {
            Text(title)
                .font(.headline)
            
            HStack {
                TextField("Enter value", text: value)
                    .keyboardType(.numberPad)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Text(unit)
            }
        }
    }
}

struct GoogleLoginView: View {
    var onLoginSuccess: () -> Void
    
    var body: some View {
        VStack {
            Text("Connect Your Calendar")
                .font(.largeTitle)
                .padding()
            
            Text("Login with Google to add your calendar")
                .font(.subheadline)
                .padding()
            
            Button("Login with Google") {
                // Implement Google login logic here
                // After successful login:
                onLoginSuccess()
            }
            .padding()
            .background(Color.accentColor)
            .foregroundColor(.white)
            .cornerRadius(10)
        }
    }
}
