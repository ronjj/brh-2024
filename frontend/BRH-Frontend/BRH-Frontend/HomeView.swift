import SwiftUI

struct HomeView: View {
    var body: some View {
        TabView {
            HomeTabView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
            
            PreferencesTabView()
                .tabItem {
                    Label("Preferences", systemImage: "gear")
                }
        }
    }
}

struct HomeTabView: View {
    var body: some View {
        NavigationView {
            VStack {
                Text("Welcome to the Home Tab!")
                    .font(.title)
                    .padding()
            }
            .navigationBarTitle("Home", displayMode: .inline)
        }
    }
}

struct PreferencesTabView: View {
    @AppStorage("userCalorieGoal") private var userCalorieGoal = ""
    @AppStorage("userProteinGoal") private var userProteinGoal = ""
    @AppStorage("userCarbGoal") private var userCarbGoal = ""
    @AppStorage("userFatGoal") private var userFatGoal = ""
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Nutrition Goals")) {
                    nutritionGoalRow(title: "Daily Calorie Goal", value: $userCalorieGoal, unit: "calories")
                    nutritionGoalRow(title: "Protein Goal", value: $userProteinGoal, unit: "g")
                    nutritionGoalRow(title: "Carb Goal", value: $userCarbGoal, unit: "g")
                    nutritionGoalRow(title: "Fat Goal", value: $userFatGoal, unit: "g")
                }
            }
            .navigationBarTitle("Preferences", displayMode: .inline)
        }
    }
    
    private func nutritionGoalRow(title: String, value: Binding<String>, unit: String) -> some View {
        HStack {
            Text(title)
            Spacer()
            TextField("Enter goal", text: value)
                .keyboardType(.numberPad)
                .multilineTextAlignment(.trailing)
            Text(unit)
        }
    }
}
