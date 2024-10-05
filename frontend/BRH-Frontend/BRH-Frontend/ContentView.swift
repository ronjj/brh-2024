//
//  ContentView.swift
//  BRH-Frontend
//
//  Created by Ronald Jabouin on 10/4/24.
//

import SwiftUI

struct OnboardingView: View {
    @State private var calorieGoal: String = ""
    @State private var proteinGoal: String = ""
    @State private var carbGoal: String = ""
    @State private var fatGoal: String = ""
    @State private var currentStep = 0
    
    let steps = ["Calorie", "Protein", "Carb", "Fat"]
    
    var body: some View {
        VStack {
            Text("Set Your Nutrition Goals")
                .font(.largeTitle)
                .padding()
            
            Spacer()
            
            switch currentStep {
            case 0:
                nutritionInputView(title: "What is your daily caloric goal?", value: $calorieGoal, unit: "calories")
            case 1:
                nutritionInputView(title: "How many grams of protein?", value: $proteinGoal, unit: "g")
            case 2:
                nutritionInputView(title: "How many grams of carbs?", value: $carbGoal, unit: "g")
            case 3:
                nutritionInputView(title: "How many grams of fats?", value: $fatGoal, unit: "g")
            default:
                Text("Setup Complete!")
            }
            
            Spacer()
            
            if currentStep < steps.count {
                Button(action: nextStep) {
                    Text("Next")
                        .frame(minWidth: 0, maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding()
            }
            
            ProgressView(value: Double(currentStep), total: Double(steps.count))
                .padding()
        }
    }
    
    func nutritionInputView(title: String, value: Binding<String>, unit: String) -> some View {
        VStack {
            Text(title)
                .font(.headline)
            
            HStack {
                TextField("Enter value", text: value)
                    .keyboardType(.numberPad)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Text(unit)
            }
            .padding()
        }
    }
    
    func nextStep() {
        if currentStep < steps.count {
            currentStep += 1
        }
    }
}

