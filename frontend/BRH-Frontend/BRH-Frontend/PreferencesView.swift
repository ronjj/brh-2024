//
//  PreferencesView.swift
//  BRH-Frontend
//
//  Created by Ronald Jabouin on 10/5/24.
//

import SwiftUI

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
