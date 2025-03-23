

import streamlit as st
import os
import requests
from PIL import Image
import io
# Set up Nebius AI client with proper API key handling
from openai import OpenAI as NebiusClient  # ✅ FIXED IMPORT

# ...

client = NebiusClient(  # ✅ FIXED NAME
    base_url="https://api.studio.nebius.com/v1/",
    api_key=api_key
)

from dotenv import load_dotenv
# Set page config as the first command
st.set_page_config(page_title="🍽️ SmartMeal AI Planner", layout="wide")

# Load environment variables from .env file
load_dotenv()

# Set up Nebius AI client with proper API key handling
api_key = os.getenv("NEBIUS_API_KEY")  # Get the API key from the .env file
if not api_key:
    st.error("Please provide a valid Nebius API key in the .env file.")
    st.stop()

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=api_key
)

# Set up Spoonacular API key
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not SPOONACULAR_API_KEY:
    st.error("Please provide a valid Spoonacular API key in the .env file.")
    st.stop()

# Function to call Nebius AI
def call_nebius(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct",
            max_tokens=700,
            temperature=0.6,
            top_p=0.9,
            extra_body={"top_k": 50},
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Function to get meal image and recipe details using Spoonacular API
def get_meal_image_and_recipe(meal_name):
    try:
        url = f"https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "query": meal_name,
            "number": 1,
            "instructionsRequired": True,
            "addRecipeInformation": True
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                recipe = data["results"][0]
                image_url = recipe["image"]
                recipe_title = recipe["title"]
                recipe_instructions = recipe["analyzedInstructions"][0]["steps"] if recipe.get("analyzedInstructions") else []
                ingredients = recipe.get("extendedIngredients", [])
                nutrients = recipe.get("nutrition", {}).get("nutrients", [])
                return image_url, recipe_title, recipe_instructions, ingredients, nutrients
    except Exception as e:
        st.error(f"Error fetching data from Spoonacular: {str(e)}")
    return None, None, None, None, None

# Custom CSS for styling
# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(-45deg, #FFD700, #00008B, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] > div {
        padding: 1rem;
        background-color: transparent !important;
    }

    .app-name {
        font-family: 'Pacifico', cursive;
        font-size: 2rem;
        font-weight: bold;
        font-style: italic;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }

    .app-details {
        font-size: 1.2rem;
        color: white;
        margin-top: 10px;
    }
    .app-details-italic {
        font-size: 1rem;
        color: white;
        font-style: italic;
        margin-top: 5px;
    }

    .summary-title {
        font-size: 1rem;
        font-weight: bold;
        color: white;
        background: rgba(255, 255, 255, 0.2);
        padding: 5px 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .summary-value {
        font-size: 1rem;
        color: white;
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar for user input and app name
with st.sidebar:
    st.markdown('<div class="app-name">🍽️ SmartMeal AI</div>', unsafe_allow_html=True)

    st.header("👤 User Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", 10, 100)
    weight = st.number_input("Weight (kg)", 30, 200)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    country = st.text_input("Country")
    profession = st.selectbox("Profession", ["Doctor", "Student", "Engineer", "Lawyer", "Teacher" , "Shopkeeper" , "Housewife", "Office Worker", "Freelancer", "Businessman", "Coder", "Online Worker", "Other"])
    ingredients = st.text_area("Available Ingredients (comma-separated)")
    meal_time = st.selectbox("Meal Time", ["Breakfast", "Lunch", "Dinner", "Snack", "Drink"])
    meal_type = st.multiselect("Meal Type", ["Vegetarian", "Italian", "Thai", "Pakistani", "Chinese", "Indian", "Vegan", "Gluten-Free", "Keto", "Paleo"])
    health_goals = st.multiselect("Health Goal", [
        "Weight Loss", "Muscle Gain", "Fat Burn", "Improve Immunity", "Heart Health", 
        "Energy Boost", "Mental Clarity", "Balance Diet", "Detox", "Better Sleep", 
        "Improve Digestion", "Reduce Stress", "Boost Metabolism", "Improve Skin Health", 
        "Increase Stamina"
    ])
    generate = st.button("Generate Meal Plan")

st.title("🍽️SmartMeal AI - Personalized Nutrition App")

st.markdown(
    """
    <div class="app-details">
    Welcome to **SmartMeal AI**, your personalized nutrition assistant!
    </div>
    <div class="app-details-italic">
    This app helps you generate meal plans tailored to your preferences and health goals and give you complete nutrients according to your daily working routine.
    
    
    </div>


    """,
    unsafe_allow_html=True
)


if generate:
    with st.spinner("Generating personalized meal plan..."):

        user_info = {
            "Name": name,
            "Age": age,
            "Weight": f"{weight}kg",
            "Gender": gender,
            "Country": country,
            "Profession": profession,
            "Health Goals": ', '.join(health_goals),
            "Meal Type": ', '.join(meal_type),
            "Meal Time": meal_time,
            "Available Ingredients": ingredients
        }

        st.subheader("📋 User Info Summary")
        cols = st.columns(2)
        for i, (key, value) in enumerate(user_info.items()):
            with cols[i % 2]:
                st.markdown(f'<div class="summary-title"><i><b>{key}</b></i></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="summary-value">{value}</div>', unsafe_allow_html=True)

        ai_prompt = f"""
        Based on the following user profile, suggest 1 personalized meal with:
        - Meal name
        - Full recipe steps
        - Nutrient breakdown (carbs, protein, fat, fiber, vitamins)
        - Reason why this meal fits the user’s profession and health goals
        - Use the available ingredients if possible, but also suggest additional
        - Use the available ingredients if possible, but also suggest additional ingredients if necessary.
        - Consider country-specific and meal-type preferences.
        - Output should be well-formatted and easy to read.

        User Profile:
        Name: {name}
        Age: {age}
        Weight: {weight}kg
        Gender: {gender}
        Country: {country}
        Profession: {profession}
        Meal Time: {meal_time}
        Preferred Meal Types: {', '.join(meal_type)}
        Health Goals: {', '.join(health_goals)}
        Available Ingredients: {ingredients}
        """

        result = call_nebius(ai_prompt)

        if result:
            st.subheader("🍱 AI Suggested Meal Plan")

            # Extract meal name (assume it's the first line from AI)
            meal_name = result.splitlines()[0].strip()
            image_url, title, instructions, ing_list, nutrients = get_meal_image_and_recipe(meal_name)

            # 🖼️ Show meal image FIRST
            if image_url:
                st.image(image_url, caption=meal_name, use_column_width=True)

            # 💬 Show AI-generated meal details (with text)
            st.markdown(result)

            # 🍅 Ingredient breakdown section
            if ing_list:
                st.markdown("## 🧾 Ingredient Details")

                user_ingredients_set = set(i.strip().lower() for i in ingredients.split(",") if i.strip())
                used_from_user = []
                additional_needed = []

                for ing in ing_list:
                    ing_name = ing.get("name", "").lower()
                    original = ing.get("original", "")

                    if any(word in ing_name for word in user_ingredients_set):
                        used_from_user.append(original)
                    else:
                        additional_needed.append(original)

                if used_from_user:
                    st.markdown("✅ **Available Ingredients Used:**")
                    for ing in used_from_user:
                        st.markdown(f"- {ing}")

                if additional_needed:
                    st.markdown("➕ **Additional Ingredients Suggested:**")
                    for ing in additional_needed:
                        st.markdown(f"- **{ing}**")

            # 🥄 Recipe steps
            if instructions:
                st.markdown("### 🥣 Instructions")
                for step in instructions:
                    st.markdown(f"- {step['step']}")

            # 🧬 Nutrient info
            if nutrients:
                st.markdown("### 🧬 Nutritional Breakdown")
                for nut in nutrients:
                    st.markdown(f"- **{nut['name']}**: {nut['amount']} {nut['unit']}")

        else:
            st.error("Failed to generate a meal plan. Please try again.")
