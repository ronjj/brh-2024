from openai import OpenAI
from dotenv import load_dotenv
import os
from Food import Food

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

def fill_nutrition(food_dict):
    # Step 1: Gather all the keys (food names) from the dictionary
    food_names = list(food_dict.keys())
    chunk_size = 50

    # Split the food names into chunks of 30 items each
    for i in range(0, len(food_names), chunk_size):
        print("New Loop")
        food_chunk = food_names[i:i + chunk_size]

        # Step 2: Generate the prompt for the current chunk of food items
        prompt = "Provide a detailed nutritional breakdown for the following food items:\n\n"

        for food_name in food_chunk:
            prompt += f"Food: {food_name}\n"

        prompt += """
        For each food, return the values for calories, fat, carbs, and protein. Return the result for each item in this format:
        Example key: Grilled Huli Huli Chicken Breast
        Example response:
        Food: Grilled Huli Huli Chicken Breast
        Calories: 379
        Protein: 25
        Carbohydrates: 25
        Fat: 19
        
        Estimate a proportional serving size for this dish and give the values for calories, fat, carbs, and protein Return your result in this format: Calories: xxxx, Carbs = xxxx, Protein = xxxx, Fat = xxxx. 
        Please keep each of these metrics on separate lines.

        Please repeat this structure for each item in the list. DO NOT have any styling or bold words. Do not have any numbered lists. 
        For a new food simply start with Food: [Name of Food], then have a new line with Calories, Protien, Carbs, Fats, as shown in the example above. 
        """

        try:
            # Step 3: Call the API with the current chunk of food items
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            result = completion.choices[0].message.content

            # Step 4: Parse the result
            lines = result.split("\n")

            current_food = None

            # Step 5: Iterate through the response and update the food_dict
            for line in lines:
                line = line.strip()
                print(line)

                if line.startswith("Food: "):  # New food item starts
                    current_food = line.split(": ")[1].strip()

                elif "Calories" in line:
                    if current_food in food_dict:
                        if food_dict[current_food] is None:
                            # Create a new Food object if not already created
                            food_dict[current_food] = Food(current_food)
                            print("new food made")
                        food_dict[current_food].calories = float(line.split(":")[1].strip())

                elif "Carbohydrates" in line:
                    if current_food in food_dict and food_dict[current_food]:
                        food_dict[current_food].carbs = float(line.split(":")[1].strip())

                elif "Protein" in line:
                    if current_food in food_dict and food_dict[current_food]:
                        food_dict[current_food].protein = float(line.split(":")[1].strip())

                elif "Fat" in line:
                    if current_food in food_dict and food_dict[current_food]:
                        food_dict[current_food].fat = float(line.split(":")[1].strip())

        except Exception as e:
            print(f"Error during API call: {e}")

    print(food_dict)
