import SwiftUI

struct ContentView: View {
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false

    var body: some View {
        if hasCompletedOnboarding {
            HomeView()
        } else {
            MacroOnboardingView()
        }
    }
}

struct MacroOnboardingView: View {
    @State private var calorieGoal: String = ""
    @State private var proteinGoal: String = ""
    @State private var carbGoal: String = ""
    @State private var fatGoal: String = ""
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
    @State private var navigateToHome = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("Set Your Nutrition Goals")
                    .font(.largeTitle)
                    .padding()
                
                nutritionInputView(title: "What is your daily caloric goal?", value: $calorieGoal, unit: "calories")
                nutritionInputView(title: "How many grams of protein?", value: $proteinGoal, unit: "g")
                nutritionInputView(title: "How many grams of carbs?", value: $carbGoal, unit: "g")
                nutritionInputView(title: "How many grams of fats?", value: $fatGoal, unit: "g")
                
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
                NavigationLink(destination: HomeView(), isActive: $navigateToHome) {
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
        // Save the user's preferences here
        // For example:
        // UserDefaults.standard.set(calorieGoal, forKey: "userCalorieGoal")
        // UserDefaults.standard.set(proteinGoal, forKey: "userProteinGoal")
        // UserDefaults.standard.set(carbGoal, forKey: "userCarbGoal")
        // UserDefaults.standard.set(fatGoal, forKey: "userFatGoal")
        
        // Mark onboarding as complete
        hasCompletedOnboarding = true
    }
}

struct HomeView: View {
    var body: some View {
        Text("Welcome to the Home View!")
            .font(.largeTitle)
            .navigationBarTitle("Home", displayMode: .inline)
            .navigationBarBackButtonHidden(true)
    }
}
