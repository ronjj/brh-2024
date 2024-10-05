//
//  HomeView.swift
//  BRH-Frontend
//
//  Created by Ronald Jabouin on 10/4/24.
//

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
                
                // Add more content for the Home tab here
            }
            .navigationBarTitle("Home", displayMode: .inline)
        }
    }
}

struct PreferencesTabView: View {
    var body: some View {
        NavigationView {
            VStack {
                Text("Preferences")
                    .font(.title)
                    .padding()
                
                // Add preferences settings here
            }
            .navigationBarTitle("Preferences", displayMode: .inline)
        }
    }
}
