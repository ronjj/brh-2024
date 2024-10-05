import requests
from Food import Food
from NutritionCaller import fill_nutrition

food_dict = {}

url = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    places = data["data"]["eateries"]

    #Contains all information about all eateries on campus
    # Eateries Structure:
    # Eateries:
    # - Name
    # - About
    # - Latitude
    # - Longitude
    # - Location
    # - Type
    # - Dates: (Array)
    #   - Date (date)
    #   - Events: (Array)
    #     - Description (descr)
    #     - Start (start)
    #     - End (end)
    #     - Food: (Array)
    #       - FoodItem (item)
    #       - Category (category)

    eateries = []

    for eatery in places:
        #Basic Information
        name = eatery["nameshort"]
        about = eatery["aboutshort"]
        latitude = eatery["latitude"]

        longitude = eatery["longitude"]

        location = eatery["location"]

        eateryType = eatery["eateryTypes"][0]["descr"] #'Dining Room' or 'Cafe'


        #Food Information based on Date
        dates = []

        #Looking at each day in specific dining hall
        for day in eatery["operatingHours"]:
            date = day["date"]
            #Contains all the events for the day (Breakfast, lunch, dinner, late dinner, etc.)
            events = []

            #Looking at each service in a day
            for event in day["events"]:
                descr = event["descr"]
                start = event["start"]
                end = event["end"]

                #Contains all food for the event
                food = []

                #Looking at each category in a service
                for catType in event["menu"]:
                    category = catType["category"]

                    #Looking at each food item in category
                    for item in catType["items"]:
                        name = item["item"]
                        food.append(name)

                        if name not in food_dict:
                            food_dict[name] = None

                new_event = {
                    "Description" : descr,
                    "Start" : start,
                    "End" : end,
                    "Food" : food
                }

                events.append(new_event)

            new_date = {
                "Date" : date,
                "Events" : events
            }

            dates.append(new_date)

        new_eatery = {
            "Name": name,
            "About": about,
            "Latitude": latitude,
            "Longitude": longitude,
            "Location": location,
            "Type" : eateryType,
            "Dates": dates
        }

        eateries.append(new_eatery)

    print(len(food_dict.keys()))
    fill_nutrition(food_dict)

else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")


