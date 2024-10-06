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
    @State private var isAddingToCalendar = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 0) {
                    ForEach(Array(mealPlans.keys.sorted()), id: \.self) { date in
                        Section(header: sectionHeader(for: date)) {
                            ForEach(sortedMeals(for: date), id: \.id) { meal in
                                PlanRowView(meal: meal)
                                if meal.id != sortedMeals(for: date).last?.id {
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
                trailing: 
                    HStack {
                    Button(action: addToCalendar) {
                        if isAddingToCalendar {
                            ProgressView()
                        } else {
                            Text("Add Meals to Calendar")
                        }
                    }
                    .disabled(isAddingToCalendar)
                    
                    if !isAddingToCalendar {
                        Image(systemName: "calendar")
                            .foregroundStyle(Color.accentColor)
                    }
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
      
      // ... (keep the existing formatDate, daySuffix, and sectionHeader functions) ...
      
    private func sortedMeals(for date: Date) -> [Meal] {
        let meals = mealPlans[date]?.meals ?? []
        return meals.sorted {
            let time1 = parseTime($0.details.start)
            let time2 = parseTime($1.details.start)
            return time1 < time2
        }
    }
    
    private func parseTime(_ timeString: String) -> Date {
        let formatter = DateFormatter()
        formatter.dateFormat = "h:mma"
        return formatter.date(from: timeString) ?? Date.distantPast
    }
    
    // ... (keep the existing formatDate, daySuffix, sectionHeader functions) ...
    
    private func loadData() {
        guard let url = Bundle.main.url(forResource: "meals_data", withExtension: "json"),
              let data = try? Data(contentsOf: url) else {
            print("Error: Couldn't find or load meal_data.json")
            return
        }
        
        do {
            let json = try JSONDecoder().decode([String: DayPlanData].self, from: data)
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "yyyy-MM-dd"
            
            for (dateString, dayPlanData) in json {
                if let date = dateFormatter.date(from: dateString) {
                    let meals = dayPlanData.meals.map { mealData in
                        Meal(id: "\(dateString)-\(mealData.eatery)-\(mealData.time)",
                             eatery: mealData.eatery,
                             time: mealData.time,
                             details: MealDetails(start: mealData.details.Start,
                                                  end: mealData.details.End,
                                                  bestCombination: mealData.details.bestCombination.map { (name, values) in
                                                      Food(name: name,
                                                           serving: Int(values[0]),
                                                           calories: Int(values[1]),
                                                           protein: Int(values[2]),
                                                           carbs: Int(values[3]),
                                                           fats: Int(values[4]))
                                                  }))
                    }
                    let macros = Macros(calories: dayPlanData.macros.calories,
                                        protein: dayPlanData.macros.protein,
                                        carbs: dayPlanData.macros.carbs,
                                        fats: dayPlanData.macros.fats)
                    mealPlans[date] = DayPlan(meals: meals, macros: macros)
                }
            }
        } catch {
            print("Error decoding JSON: \(error)")
        }
    }
    
    private func addToCalendar() {
        isAddingToCalendar = true
        
        // Simulate adding to calendar with a 2.5 second delay
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.5) {
            isAddingToCalendar = false
            showingCalendarAlert = true
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
    
    
    struct DayPlanData: Codable {
        let meals: [MealData]
        let macros: MacrosData
    }

    struct MealData: Codable {
        let eatery: String
        let time: String
        let details: MealDetailsData
    }

    struct MealDetailsData: Codable {
        let Start: String
        let End: String
        let bestCombination: [String: [Double]]
        
        enum CodingKeys: String, CodingKey {
            case Start
            case End
            case bestCombination = "Best combination"
        }
    }
    
    struct MacrosData: Codable {
        let calories: Int
        let protein: Int
        let carbs: Int
        let fats: Int
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
        let id: String
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
                    .foregroundColor(.accentColor)
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
}

