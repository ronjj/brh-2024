import requests
from typing import List, Dict, Any

async def get_eateries() -> List[Dict[str, Any]]:
    url = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data from Cornell Dining API")

    data = response.json()
    places = data["data"]["eateries"]
    eateries = []

    for eatery in places:
        name = eatery["nameshort"]
        about = eatery["aboutshort"]
        latitude = eatery["latitude"]
        longitude = eatery["longitude"]
        location = eatery["location"]
        eateryType = eatery["eateryTypes"][0]["descr"]

        dates = []
        for day in eatery["operatingHours"]:
            date = day["date"]
            events = []

            for event in day["events"]:
                descr = event["descr"]
                start = event["start"]
                end = event["end"]
                food = []

                for catType in event["menu"]:
                    # category = catType["category"]
                    for item in catType["items"]:
                        food.append(item["item"])

                events.append({
                    "Description": descr,
                    "Start": start,
                    "End": end,
                    "Food": food
                })

            dates.append({
                "Date": date,
                "Events": events
            })

        eateries.append({
            "Name": name,
            "About": about,
            "Latitude": latitude,
            "Longitude": longitude,
            "Location": location,
            "Type": eateryType,
            "Dates": dates
        })

    return eateries