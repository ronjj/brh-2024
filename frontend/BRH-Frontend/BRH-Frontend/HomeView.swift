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
            }
            .navigationTitle("Meal Plans")
            .onAppear(perform: loadData)
        }
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
        // For this example, we'll use mock data
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd"
        
        if let date1 = dateFormatter.date(from: "2024-10-05"),
           let date2 = dateFormatter.date(from: "2024-10-06") {
            mealPlans = [
                date1: DayPlan(meals: [
                    Meal(eatery: "Morrison Dining", time: "Late Lunch", details: MealDetails(start: "2:30pm", end: "4:00pm")),
                    Meal(eatery: "Keeton House Dining", time: "Dinner", details: MealDetails(start: "5:00pm", end: "8:00pm")),
                    Meal(eatery: "104West!", time: "Lunch", details: MealDetails(start: "12:30pm", end: "2:00pm"))
                ]),
                date2: DayPlan(meals: [
                    Meal(eatery: "Becker House Dining", time: "Dinner", details: MealDetails(start: "5:00pm", end: "8:00pm")),
                    Meal(eatery: "Morrison Dining", time: "Late Lunch", details: MealDetails(start: "2:00pm", end: "4:00pm"))
                ])
            ]
        }
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
                .foregroundColor(isChecked ? .accentColor : .gray)
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
