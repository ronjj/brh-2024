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
            List {
                Section(header: Text("TODAY").font(.caption).foregroundColor(.purple)) {
                    PlanRowView(location: "Teagle Hall", time: "7:30AM", description: "Push")
                    PlanRowView(location: "Morrison Dining", time: "8:30AM", description: "Breakfast")
                    PlanRowView(location: "Rose Hall", time: "1:30PM", description: "Lunch")
                }
            }
            .listStyle(InsetGroupedListStyle())
            .navigationTitle("Plan")
            .navigationBarItems(trailing: Button(action: {
                // Add new item action
            }) {
                Image(systemName: "square.and.pencil")
            })
        }
    }
}

struct PlanRowView: View {
    let location: String
    let time: String
    let description: String
    @State private var isChecked = true
    
    var body: some View {
        HStack {
            Image(systemName: isChecked ? "checkmark.circle.fill" : "circle")
                .foregroundColor(isChecked ? .blue : .gray)
                .onTapGesture {
                    isChecked.toggle()
                }
            VStack(alignment: .leading) {
                Text("\(location) @ \(time)")
                    .font(.headline)
                Text(description)
                    .font(.subheadline)
                    .foregroundColor(.gray)
            }
            Spacer()
            Text("Detail")
                .foregroundColor(.blue)
            Image(systemName: "chevron.right")
                .foregroundColor(.gray)
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
