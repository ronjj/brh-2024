from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

class Food:
    # Name of Food
    title = ""

    # Macros
    calories = 0.0
    carbs = 0.0
    protein = 0.0
    fat = 0.0

    # Category - Soup, BagelBar, etc.
    category = ""

    # Ingredient List
    ingredients = []

    def __init__(self, title, category):
        self.title = title
        self.category = category

        #MAKE MORE EFFICIENT:
        #self.setup_food()

    # Make API Calls etc
    def setup_food(self):
        prompt = f"""
            Provide a detailed nutritional breakdown for the food item "{self.title}", which is served at Cornell University dining halls. 
            The category is "{self.category}". Estimate a proportional serving size for this dish and give the values for calories, fat, carbs, and protein Return your result in this format: Calories: xxxx, Carbs = xxxx, Protein = xxxx, Fat = xxxx. 
            Please keep each of these metrics on separate lines.
            Do not bold anything or include any text styling. Keep lines simple and short.

            Example request: Grilled Huli Huli Chicken Breast
            Example response for above request:
            Calories: 379
            Protein: 25
            Carbohydrates: 25
            Fat: 19
            """

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = completion.choices[0].message.content

            lines = result.split('\n')

            # Go through each line to find the relevant metrics
            for line in lines:
                if "Calories" in line:
                    self.calories = float(line.split(":")[1].strip())
                elif "Carbs" in line:
                    self.carbs = float(line.split(":")[1].strip())
                elif "Protein" in line:
                    self.protein = float(line.split(":")[1].strip())
                elif "Fat" in line:
                    self.fat = float(line.split(":")[1].strip())


        except Exception as e:
            print(f"Error retrieving nutritional data: {e}")
            # Handle errors or default values if API call fails
            self.calories = 0
            self.fat = 0
            self.carbs = 0
            self.protein = 0

    def toString(self):
        print(f"Food: {self.title}\n"
              f"Calories: {self.calories}\n"
              f"Carbohydrates: {self.carbs}\n"
              f"Protein: {self.protein}\n"
              f"Fat: {self.fat}\n")
