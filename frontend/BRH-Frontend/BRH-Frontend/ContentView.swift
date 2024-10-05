import SwiftUI

struct MacroOnboardingView: View {
    @AppStorage("userCalorieGoal") private var userCalorieGoal = ""
    @AppStorage("userProteinGoal") private var userProteinGoal = ""
    @AppStorage("userCarbGoal") private var userCarbGoal = ""
    @AppStorage("userFatGoal") private var userFatGoal = ""
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
    @State private var navigateToHome = false
    
    var body: some View {
        NavigationView {
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
                    completeOnboarding()
                    navigateToHome = true
                } label: {
                    Text("Complete Setup")
                        .frame(minWidth: 0, maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding()
            }
            .padding()
            .navigationBarHidden(true)
            .background(
                NavigationLink(destination: HomeView().navigationBarBackButtonHidden(true), isActive: $navigateToHome) {
                    EmptyView()
                }
            )
        }
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
    
    func completeOnboarding() {
        // The user's preferences are already saved in AppStorage
        // Just mark onboarding as complete
        hasCompletedOnboarding = true
    }
}

