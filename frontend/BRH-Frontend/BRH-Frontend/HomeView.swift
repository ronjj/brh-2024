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
    @State private var mealPlans: [String: DayPlan] = [:]
    
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
                        }
                    }
                }
                .background(Color(UIColor.systemGroupedBackground))
            }
            .navigationTitle("Meal Plans")
            .onAppear(perform: loadData)
        }
    }
    
    private func sectionHeader(for date: String) -> some View {
        Text(date)
            .font(.caption)
            .foregroundColor(.purple)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal)
            .padding(.top, 20)
            .padding(.bottom, 5)
            .background(Color(UIColor.systemGroupedBackground))
    }
    
    private func loadData() {
        // In a real app, you'd parse the JSON here
        // For this example, we'll use a mock data structure
        mealPlans = [
            "2024-10-05": DayPlan(meals: [
                Meal(eatery: "Morrison Dining", time: "Late Lunch", details: MealDetails(start: "2:30pm", end: "4:00pm")),
                Meal(eatery: "Keeton House Dining", time: "Dinner", details: MealDetails(start: "5:00pm", end: "8:00pm")),
                Meal(eatery: "104West!", time: "Lunch", details: MealDetails(start: "12:30pm", end: "2:00pm"))
            ]),
            "2024-10-06": DayPlan(meals: [
                Meal(eatery: "Becker House Dining", time: "Dinner", details: MealDetails(start: "5:00pm", end: "8:00pm")),
                Meal(eatery: "Morrison Dining", time: "Late Lunch", details: MealDetails(start: "2:00pm", end: "4:00pm"))
            ])
        ]
    }
}

struct DayPlan {
    let meals: [Meal]
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
        VStack(alignment: .leading, spacing: 20) {
            Text(meal.eatery)
                .font(.title)
            Text(meal.time)
                .font(.headline)
            Text("\(meal.details.start) - \(meal.details.end)")
                .font(.body)
        }
        .padding()
        .navigationTitle("Meal Details")
    }
}
