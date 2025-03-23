# 📘 SmartMeal AI Planner - Technical Documentation

## Overview
**SmartMeal AI** is a personalized meal planning app that leverages AI and real-world food data to generate meal recommendations tailored to user profiles. It uses Streamlit for the interface, Nebius Studio's LLM for meal intelligence, and Spoonacular API for recipes and nutrition.

---

## 🧱 Project Structure
```
smartmeal-ai-planner/
├── app.py                  # Main Streamlit application
├── .env                   # API keys (not included in repo)
├── requirements.txt       # Python dependencies
├── README.md              # Project description
└── docs/                  # Documentation folder (optional)
```

---

## 🔐 API Keys Setup
Create a `.env` file in the project root with the following keys:
```env
NEBIUS_API_KEY=your_nebius_api_key
SPOONACULAR_API_KEY=your_spoonacular_api_key
```
These are securely loaded using `python-dotenv`.

---

## 🧠 Core Technologies

| Tech            | Description |
|----------------|-------------|
| **Streamlit**  | UI framework for fast, interactive Python web apps |
| **Nebius AI**  | Hosts Meta LLaMA 3.1 70B model for meal generation |
| **Spoonacular API** | Provides real-world recipe, ingredient, and nutrition data |
| **Python**     | Main programming language |
| **HTTPX / Requests** | Handle API communication |
| **Pillow (PIL)** | Display meal images |
| **dotenv**     | Load API keys from .env |

---

## 🧩 Functionality Breakdown

### 1. **User Input Form (Sidebar)**
- Name
- Age
- Weight
- Gender
- Country
- Profession
- Meal Time (e.g., Breakfast, Lunch)
- Meal Types (Vegan, Keto, etc.)
- Health Goals
- Available Ingredients

### 2. **AI Prompt Construction**
- Compiles user input into a detailed prompt
- Sends to Nebius LLM for intelligent meal suggestion

### 3. **Nebius LLM Output**
- Meal Name
- Full Recipe
- Nutritional Breakdown (Carbs, Proteins, Fats, Vitamins)
- Reasoning tailored to user profile

### 4. **Spoonacular API Integration**
- Search by meal name
- Retrieve:
  - Recipe instructions
  - Image
  - Ingredients
  - Nutrition info

### 5. **Ingredient Matching**
- Compare Spoonacular ingredients with user input
- Display used vs. needed ingredients

### 6. **Dynamic UI Rendering**
- Responsive layout with gradient CSS background
- Shows:
  - User summary
  - Meal image
  - AI results
  - Recipe steps
  - Ingredients
  - Nutritional chart

---

## 📜 API Details

### Nebius LLM Endpoint
```
POST https://api.studio.nebius.com/v1/chat/completions
```
Payload:
```json
{
  "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
  "messages": [{"role": "user", "content": "your prompt"}],
  "max_tokens": 700,
  "temperature": 0.6,
  "top_p": 0.9,
  "extra_body": {"top_k": 50}
}
```

### Spoonacular API Endpoint
```
GET https://api.spoonacular.com/recipes/complexSearch
```
Params:
```python
{
  "apiKey": SPOONACULAR_API_KEY,
  "query": meal_name,
  "number": 1,
  "instructionsRequired": True,
  "addRecipeInformation": True
}
```

---

## 🧪 Testing
- Ensure `.env` is correctly loaded
- Validate API responses
- Test prompt with different user profiles
- Check ingredient parsing logic

---

## 📈 Future Enhancements
- 🔒 Authentication & login system
- 🛒 Smart grocery list generation
- 📱 Mobile-optimized UI
- 📆 Weekly plan export (PDF)
- 🧬 Track daily macros
- 🧠 More detailed health analytics

---

## 🤖 AI Prompt Logic Example
```
Based on the following user profile, suggest 1 personalized meal with:
- Meal name
- Full recipe steps
- Nutrient breakdown (carbs, protein, fat, fiber, vitamins)
- Reason why this meal fits the user’s profession and health goals
- Use the available ingredients if possible, but also suggest additional
- Consider country-specific and meal-type preferences
```

---

## ✅ Dependencies
Install via:
```bash
pip install -r requirements.txt
```
Contents:
```
streamlit
requests
httpx
Pillow
openai
python-dotenv
```

---

## 🧑‍💻 Author
Built with by NOOR UL NISA

---

## 📄 License
[MIT](LICENSE) – Free to use, modify, and distribute.

