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
    @State private var mealPlans: [Date: DayPlan] = [:]
       @State private var showingCalendarAlert = false
       
       var body: some View {
           NavigationView {
               ScrollView {
                   LazyVStack(spacing: 0) {
                       ForEach(Array(mealPlans.keys.sorted()), id: \.self) { date in
                           Section(header: sectionHeader(for: date)) {
                               ForEach(mealPlans[date]?.meals ?? [], id: \.eatery) { meal in
                                   PlanRowView(meal: meal)
                                   if meal.eatery != mealPlans[date]?.meals.last?.eatery {
                                       Divider()
                                           .padding(.leading, 50)
                                   }
                               }
                               if let macros = mealPlans[date]?.macros {
                                   Divider()
                                       .padding(.leading, 50)
                                   MacroTotalsRowView(macros: macros)
                               }
                           }
                       }
                   }
                   .background(Color(UIColor.systemGroupedBackground))
               }
               .navigationTitle("Meal Plans")
               .navigationBarItems(
                   trailing: Button(action: addToCalendar) {
                       Text("Add Meals to Calendar")
                   }
               )
               .onAppear(perform: loadData)
               .alert(isPresented: $showingCalendarAlert) {
                   Alert(
                       title: Text("Success"),
                       message: Text("Meals have been successfully added to your calendar."),
                       dismissButton: .default(Text("OK"))
                   )
               }
           }
       }
    
    private func addToCalendar() {
            // Here you would typically add the actual logic to add meals to the calendar
            // For now, we'll just show the success alert
            showingCalendarAlert = true
        }
    
    private func sectionHeader(for date: Date) -> some View {
        Text(formatDate(date))
            .font(.headline)
            .foregroundColor(.accentColor)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal)
            .padding(.top, 20)
            .padding(.bottom, 5)
            .background(Color(UIColor.systemGroupedBackground))
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "EEEE, MMMM d"
        let formatted = formatter.string(from: date)
        return formatted + daySuffix(from: date)
    }
    
    private func daySuffix(from date: Date) -> String {
        let calendar = Calendar.current
        let dayOfMonth = calendar.component(.day, from: date)
        switch dayOfMonth {
        case 1, 21, 31: return "st"
        case 2, 22: return "nd"
        case 3, 23: return "rd"
        default: return "th"
        }
    }

    private func loadData() {
            // In a real app, you'd parse the JSON here and convert string dates to Date objects
            // For this example, we'll use mock data that includes the macros
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "yyyy-MM-dd"
            
            if let date1 = dateFormatter.date(from: "2024-10-05"),
               let date2 = dateFormatter.date(from: "2024-10-06") {
                mealPlans = [
                    date1: DayPlan(
                        meals: [
                            Meal(eatery: "Morrison Dining", time: "Late Lunch", details: MealDetails(start: "2:30pm", end: "4:00pm", bestCombination: [
                                Food(name: "Vegan Cheese Pizza", serving: 1, calories: 300, protein: 12, carbs: 38, fats: 15),
                                Food(name: "Pepperoni Pizza", serving: 1, calories: 350, protein: 15, carbs: 35, fats: 18)
                            ])),
                            Meal(eatery: "Keeton House Dining", time: "Dinner", details: MealDetails(start: "5:00pm", end: "8:00pm", bestCombination: [
                                Food(name: "Taco Mania", serving: 1, calories: 400, protein: 20, carbs: 40, fats: 20),
                                Food(name: "Queso Blanco Sauce", serving: 1, calories: 210, protein: 7, carbs: 6, fats: 18)
                            ]))
                        ],
                        macros: Macros(calories: 1760, protein: 84, carbs: 159, fats: 96)
                    ),
                    date2: DayPlan(
                        meals: [
                            Meal(eatery: "Becker House Dining", time: "Dinner", details: MealDetails(start: "5:00pm", end: "8:00pm", bestCombination: [
                                Food(name: "Broccoli, Spinach & Chickpea Pasta", serving: 1, calories: 300, protein: 15, carbs: 40, fats: 10),
                                Food(name: "Ancho Chili Spice Chicken Thigh", serving: 1, calories: 320, protein: 25, carbs: 0, fats: 20),
                                Food(name: "Waffle Bar", serving: 1, calories: 350, protein: 6, carbs: 40, fats: 18)
                            ]))
                        ],
                        macros: Macros(calories: 1620, protein: 73, carbs: 153, fats: 81)
                    )
                ]
            }
        }
    }


struct DayPlan {
    let meals: [Meal]
    let macros: Macros
}

struct Macros {
    let calories: Int
    let protein: Int
    let carbs: Int
    let fats: Int
}

struct Meal: Identifiable {
    let id = UUID()
    let eatery: String
    let time: String
    let details: MealDetails
}

struct MealDetails {
    let start: String
    let end: String
    let bestCombination: [Food]
}

struct Food: Identifiable {
    let id = UUID()
    let name: String
    let serving: Int
    let calories: Int
    let protein: Int
    let carbs: Int
    let fats: Int
}

struct PlanRowView: View {
    let meal: Meal
    @State private var isChecked = false
    
    var body: some View {
        HStack {
            Image(systemName: isChecked ? "checkmark.circle.fill" : "circle")
                .foregroundColor(isChecked ? .blue : .gray)
                .onTapGesture {
                    isChecked.toggle()
                }
            VStack(alignment: .leading) {
                Text("\(meal.eatery) @ \(meal.time)")
                    .font(.headline)
                Text("\(meal.details.start) - \(meal.details.end)")
                    .font(.subheadline)
                    .foregroundColor(.gray)
            }
            Spacer()
            NavigationLink(destination: MealDetailView(meal: meal)) {
                HStack {
                    Text("Detail")
                        .foregroundColor(.gray)
                    Image(systemName: "chevron.right")
                        .foregroundColor(.gray)
                }
            }
        }
        .padding()
        .background(Color(UIColor.secondarySystemGroupedBackground))
    }
}

struct MealDetailView: View {
    let meal: Meal
    
    var body: some View {
        List {
            Section(header: Text("Meal Information")) {
                Text(meal.eatery)
                    .font(.headline)
                Text(meal.time)
                Text("\(meal.details.start) - \(meal.details.end)")
            }
            
            Section(header: Text("Best Combination")) {
                ForEach(meal.details.bestCombination) { food in
                    FoodRowView(food: food)
                }
            }
        }
        .listStyle(InsetGroupedListStyle())
        .navigationTitle("Meal Details")
    }
}

struct MacroTotalsRowView: View {
    let macros: Macros
    
    var body: some View {
        HStack {
            Image(systemName: "sum")
                .foregroundColor(.purple)
            VStack(alignment: .leading) {
                Text("Daily Totals")
                    .font(.headline)
                Text("Cal: \(macros.calories) | P: \(macros.protein)g | C: \(macros.carbs)g | F: \(macros.fats)g")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            Spacer()
        }
        .padding()
        .background(Color(UIColor.secondarySystemGroupedBackground))
    }
}

struct FoodRowView: View {
    let food: Food
    
    var body: some View {
        VStack(alignment: .leading, spacing: 5) {
            Text(food.name)
                .font(.headline)
            HStack {
                Text("Serving: \(food.serving)")
                Spacer()
                Text("Calories: \(food.calories)")
            }
            .font(.subheadline)
            .foregroundColor(.secondary)
            HStack {
                Text("Protein: \(food.protein)g")
                Spacer()
                Text("Carbs: \(food.carbs)g")
                Spacer()
                Text("Fats: \(food.fats)g")
            }
            .font(.subheadline)
            .foregroundColor(.secondary)
        }
        .padding(.vertical, 5)
    }
}
