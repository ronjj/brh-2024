from datetime import datetime, timedelta
import math
import json
from itertools import combinations_with_replacement
from textwrap import indent
from itertools import combinations


# Load the JSON data from the file
with open('eateries_and_food.json', 'r') as file:
    eateries_data = json.load(file)

# Now you can access the eateries
eateries = eateries_data["eateries"]
food_dict = eateries_data["food_dict"]["food_dict"]


preferences = {
    "available_slots": [
        {
            "start": "10:00:00",
            "end": "10:30:00"
        },
        {
            "start": "12:30:00",
            "end": "20:00:00"
        }
    ],
    "nutrition_goals": {
        "calories": 3000,
        "protein": 250,
        "carbohydrates": 250,
        "fat": 100
    }
}


# Helper function to calculate time duration in hours between two time strings
def calculate_duration_in_hours(start_time_str, end_time_str):
    time_format = "%H:%M:%S"
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    # Calculate time difference in hours
    duration = (end_time - start_time).total_seconds() / 3600
    return duration

def calculate_valid_meal_slots(available_slots):
    total_meals = 0
    for slot in available_slots:
        duration = calculate_duration_in_hours(slot["start"], slot["end"])
        print(duration)

        if duration >= 1:
            # If duration is greater than or equal to 1 hour, it's a valid slot
            # Split the duration into 4-hour chunks if it's longer than 4 hours
            if (duration >= 3):
                total_meals += math.ceil(duration / 3)
            else:
                total_meals += 1

    # Ensure the number of meals is between 2 and 4
    total_meals = min(max(total_meals, 2), 4)

    return total_meals

def split_daily_goals(nutrition_goals, available_slots):
    # Calculate the number of valid meals based on slot duration and constraints
    num_meals = calculate_valid_meal_slots(available_slots)

    # Split the daily goals across the number of meals
    split_goals = {
        "calories": nutrition_goals["calories"] / num_meals,
        "protein": nutrition_goals["protein"] / num_meals,
        "carbohydrates": nutrition_goals["carbohydrates"] / num_meals,
        "fat": nutrition_goals["fat"] / num_meals
    }

    return split_goals, num_meals

# Example usage
split_goals, num_meals = split_daily_goals(preferences["nutrition_goals"], preferences["available_slots"])

print(f"Number of meals: {num_meals}")
print(f"Split nutrition goals per meal: {split_goals}")

def filter_events_by_time(eateries, available_slots):
    filtered_events = {}
    time_format_12_hour = "%I:%M%p"  # Format for 12-hour time (e.g., "11:00am")

    for eatery in eateries:
        for date_info in eatery["Dates"]:
            for event in date_info["Events"]:
                # Parse event times using the 12-hour format
                event_start = datetime.strptime(event["Start"], time_format_12_hour)
                event_end = datetime.strptime(event["End"], time_format_12_hour)

                for slot in available_slots:
                    # Use 24-hour format for available slots
                    slot_start = datetime.strptime(slot["start"], "%H:%M:%S")
                    slot_end = datetime.strptime(slot["end"], "%H:%M:%S")

                    # Check if the event fits within the user's available time slot
                    if event_start >= slot_start and event_end <= slot_end:
                        # Group events by date
                        event_date = date_info["Date"]
                        if event_date not in filtered_events:
                            filtered_events[event_date] = []
                        filtered_events[event_date].append({
                            "eatery": eatery["Name"],
                            "location": eatery["Location"],
                            "type": eatery["Type"],
                            "event": event
                        })

    return filtered_events

def get_available_foods(eatery_name, date, event):
    available_foods = []

    # Loop through each eatery
    for eatery in eateries:
        if eatery["Name"] == eatery_name:
            # Loop through the dates to find the specific date
            for date_info in eatery["Dates"]:
                if date_info["Date"] == date:
                    # Loop through events to find the corresponding event
                    for ev in date_info["Events"]:
                        if ev["Description"] == event["event"]["Description"]:
                            # Now we have the correct event, get its food items
                            for food_item in ev["Food"]:  # Get food items, default to empty list
                                #print(food_item)
                                # Fetch macros for the food item from food_dict
                                if food_item in food_dict:
                                    available_foods.append((food_item, food_dict[food_item]))
                            return available_foods  # Return once we find the matching event
    return available_foods  # Return empty if no foods found

def find_best_food_combination(available_foods, remaining_goals):
    best_combination = {}
    closest_difference = float('inf')

    # Generate combinations of foods (up to 3 servings per item)
    for combo in combinations_with_replacement(available_foods, 3):  # Choose up to 3 items
        total_calories = total_protein = total_carbs = total_fat = 0

        # Calculate total macros for the combination
        for food_item, macros in combo:
            if macros != None:
                servings = 1  # You can modify this to try different servings per item
                total_calories += macros['calories'] * servings
                total_protein += macros['protein'] * servings
                total_carbs += macros['carbohydrates'] * servings
                total_fat += macros['fat'] * servings

        # Calculate differences from goals
        calorie_diff = abs(total_calories - remaining_goals['calories'])
        protein_diff = abs(total_protein - remaining_goals['protein'])
        carb_diff = abs(total_carbs - remaining_goals['carbohydrates'])
        fat_diff = abs(total_fat - remaining_goals['fat'])

        total_diff = calorie_diff + protein_diff + carb_diff + fat_diff

        # Check if this is the best combination so far
        if total_diff < closest_difference:
            closest_difference = total_diff
            best_combination = {}

            # Create a structured combination with details
            for food_item, macros in combo:
                if macros != None:
                    servings = 1  # You can adjust this to reflect different serving sizes
                    best_combination[food_item] = [
                        servings,
                        macros['calories'] * servings,
                        macros['protein'] * servings,
                        macros['carbohydrates'] * servings,
                        macros['fat'] * servings
                    ]

    return best_combination, closest_difference



# Modified part to return a structured dictionary instead of printing
def find_best_combinations_for_events(eateries, preferences, split_goals):
    # Filter events based on available slots
    filtered_events = filter_events_by_time(eateries, preferences["available_slots"])
    #print(filtered_events)

    result = {}  # This will store the final structured output

    # Loop through each date and the corresponding events
    for date, events in filtered_events.items():
        result[date] = []  # Initialize a list for each date

        # Loop through events on that date
        for event in events:
            # Get available foods for the current event
            available_foods = get_available_foods(event["eatery"], date, event)

            # Calculate best combination for the current event
            best_combination, difference = find_best_food_combination(available_foods, split_goals)

            # Add the event details and best combination to the result for that date
            result[date].append({
                "eatery": event["eatery"],
                "time": event["event"]["Description"],
                "Start": event["event"]["Start"],
                "End": event["event"]["End"],
                "Best combination": best_combination,
                "difference": difference
            })

    return result

# Example usage
best_combinations = find_best_combinations_for_events(eateries, preferences, split_goals)
#print(json.dumps(best_combinations, indent=4))

# def select_meals_per_day(best_combinations, num_meals):
#     final_output = {}
#
#     # Time ranges for breakfast, lunch, afternoon snack, and dinner (approximate)
#     breakfast_range = ("06:00:00", "10:30:00")
#     lunch_range = ("11:00:00", "14:30:00")
#     afternoon_snack_range = ("15:00:00", "17:30:00")
#     dinner_range = ("18:00:00", "22:00:00")
#
#     # Helper function to check if a time falls within a given range
#     def is_in_time_range(time_str, time_range):
#         time_format_12_hour = "%I:%M%p"  # Format for 12-hour time (e.g., "11:00am")
#         time_format_24_hour = "%H:%M:%S"  # Format for 24-hour time (e.g., "14:30:00")
#
#         # Convert the event time from 12-hour format to 24-hour format
#         event_time = datetime.strptime(time_str, time_format_12_hour)
#
#         # Convert the slot times from 24-hour format to datetime objects
#         start_time = datetime.strptime(time_range[0], time_format_24_hour)
#         end_time = datetime.strptime(time_range[1], time_format_24_hour)
#
#         return start_time <= event_time <= end_time
#
#     # Loop through each day in the best_combinations dictionary
#     for date, events in best_combinations.items():
#         final_output[date] = []
#         selected_meals = []
#
#         # Separate events based on time into categories
#         breakfast_events = []
#         lunch_events = []
#         afternoon_snack_events = []
#         dinner_events = []
#
#         for event in events:
#             event_time_str = event["Start"]
#
#             if is_in_time_range(event_time_str, breakfast_range):
#                 breakfast_events.append(event)
#             elif is_in_time_range(event_time_str, lunch_range):
#                 lunch_events.append(event)
#             elif is_in_time_range(event_time_str, afternoon_snack_range):
#                 afternoon_snack_events.append(event)
#             elif is_in_time_range(event_time_str, dinner_range):
#                 dinner_events.append(event)
#
#         # Select meals based on the number of meals desired
#         meal_categories = [breakfast_events, lunch_events, afternoon_snack_events, dinner_events]
#         meal_names = ["breakfast", "lunch", "afternoon snack", "dinner"]
#
#         # Ensure you are selecting the desired number of meals
#         for category, name in zip(meal_categories, meal_names):
#             if len(selected_meals) >= num_meals:
#                 break
#             if category:  # Check if any events exist in this category
#                 selected_meals.append(category[0])  # You can modify this logic to choose more meals
#
#         # If fewer meals are selected than num_meals, keep selecting until the limit is reached
#         if len(selected_meals) < num_meals:
#             for category in meal_categories:
#                 for meal in category:
#                     if len(selected_meals) >= num_meals:
#                         break
#                     if meal not in selected_meals:
#                         selected_meals.append(meal)
#
#         # Calculate total macro breakdown and structure the final output for the day
#         total_macros = {
#             "calories": 0,
#             "protein": 0,
#             "carbohydrates": 0,
#             "fat": 0
#         }
#         for meal in selected_meals:
#             best_combination = meal["Best combination"]
#             for food_item, macros in best_combination.items():
#                 total_macros["calories"] += macros[1]
#                 total_macros["protein"] += macros[2]
#                 total_macros["carbohydrates"] += macros[3]
#                 total_macros["fat"] += macros[4]
#
#             # Append the selected meal details
#             final_output[date].append({
#                 "eatery": meal["eatery"],
#                 "meal_time": meal["Start"] + " - " + meal["End"],  # Assuming start/end time
#                 "best_combination": best_combination,
#                 "total_macros": total_macros
#             })
#
#     return final_output

def select_best_meals(meals_dict, num_meals):
    selected_meals = {}

    for date, meals in meals_dict.items():
        # Sort meals by 'difference' in descending order to prioritize better meals
        meals.sort(key=lambda x: x['difference'], reverse=True)

        # Track used times to avoid selecting meals at the same time
        used_times = set()
        selected_for_date = []

        for meal in meals:
            # Check if the meal's time slot is already used
            if meal['time'] not in used_times:
                selected_for_date.append(meal)
                used_times.add(meal['time'])

            # Stop if we have selected the desired number of meals
            if len(selected_for_date) == num_meals:
                break

        # Store selected meals for the date
        selected_meals[date] = selected_for_date

    return selected_meals

# Example usage
#final_meal_plan = select_meals_per_day(best_combinations, num_meals)

# Output the final meal plan (this can be further formatted or returned as needed)
#print(json.dumps(final_meal_plan, indent=4))

best_meals = select_best_meals(best_combinations, num_meals)
data_to_save = {}

for date, meals in best_meals.items():
    print(f"Meals for {date}:")

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0

    meal_details = []

    for meal in meals:
        print(f"- {meal['eatery']} ({meal['time']})")
        print(meal)

        # Replace Infinity with 0 for the difference
        difference = meal.get("difference", None)
        if difference == float('inf'):
            difference = 0

        # Add meal details to the list
        meal_details.append({
            "eatery": meal['eatery'],
            "time": meal['time'],
            "details": {
                **meal,  # Include all other meal details
                "difference": difference  # Replace Infinity with 0
            }
        })

        # Check if the 'Best combination' is empty
        if meal['Best combination']:
            # Extract the macros and calories from the 'Best combination'
            for food, values in meal['Best combination'].items():
                total_calories += values[1]  # Calories
                total_protein += values[2]  # Protein
                total_carbs += values[3]  # Carbs
                total_fats += values[4]  # Fats
        else:
            # If 'Best combination' is empty, assign None to totals
            total_calories += 0
            total_protein += 0
            total_carbs += 0
            total_fats += 0

    # Prepare the macros dictionary
    macros = {
        "calories": total_calories if total_calories is not None else None,
        "protein": total_protein if total_protein is not None else None,
        "carbs": total_carbs if total_carbs is not None else None,
        "fats": total_fats if total_fats is not None else None
    }

    # Store data in the main dictionary
    data_to_save[date] = {
        "meals": meal_details,
        "macros": macros
    }

    # Print the totals for the day
    print(f"\nTotal for {date}:")
    print(f"Calories: {total_calories}, Protein: {total_protein}g, Carbs: {total_carbs}g, Fats: {total_fats}g")
    print("\n" * 3)

# Save to JSON file
with open('meals_data.json', 'w') as json_file:
    json.dump(data_to_save, json_file, indent=4)