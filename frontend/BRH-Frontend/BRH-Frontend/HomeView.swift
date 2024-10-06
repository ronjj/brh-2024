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
    let plans = [
        Plan(location: "Teagle Hall", time: "7:30AM", description: "Push"),
        Plan(location: "Morrison Dining", time: "8:30AM", description: "Breakfast"),
        Plan(location: "Rose Hall", time: "1:30PM", description: "Lunch")
    ]
    
    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 0) {
                    Section(header: sectionHeader) {
                        ForEach(plans) { plan in
                            PlanRowView(plan: plan)
                            if plan.id != plans.last?.id {
                                Divider()
                                    .padding(.leading, 50)
                            }
                        }
                    }
                }
                .background(Color(UIColor.systemGroupedBackground))
            }
            .navigationTitle("Plan")
            .navigationBarItems(trailing: Button(action: {
                // Add new item action
            }) {
                Image(systemName: "square.and.pencil")
            })
        }
    }
    
    private var sectionHeader: some View {
        Text("TODAY")
            .font(.caption)
            .foregroundColor(.purple)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal)
            .padding(.top, 20)
            .padding(.bottom, 5)
            .background(Color(UIColor.systemGroupedBackground))
    }
}

struct Plan: Identifiable {
    let id = UUID()
    let location: String
    let time: String
    let description: String
}

struct PlanRowView: View {
    let plan: Plan
    @State private var isChecked = true
    
    var body: some View {
        HStack {
            Image(systemName: isChecked ? "checkmark.circle.fill" : "circle")
                .foregroundColor(isChecked ? .blue : .gray)
                .onTapGesture {
                    isChecked.toggle()
                }
            VStack(alignment: .leading) {
                Text("\(plan.location) @ \(plan.time)")
                    .font(.headline)
                Text(plan.description)
                    .font(.subheadline)
                    .foregroundColor(.gray)
            }
            Spacer()
            NavigationLink(destination: PlanDetailView(plan: plan)) {
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

struct PlanDetailView: View {
    let plan: Plan
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text(plan.location)
                .font(.title)
            Text(plan.time)
                .font(.headline)
            Text(plan.description)
                .font(.body)
        }
        .padding()
        .navigationTitle("Plan Details")
    }
}

