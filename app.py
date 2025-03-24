import streamlit as st
import requests
import pandas as pd
import spacy
import os
import subprocess
import platform
from pathlib import Path

# Load SpaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
if platform.system() == "Windows":
    BASE_DIR = Path("M:/sem8/owais_project")
else:
    BASE_DIR = Path("/mount/src/owais_project2")


# Load dataset
df = pd.read_csv(os.path.join(BASE_DIR, "food_data.csv"), encoding='utf-8').drop(['Unnamed: 0'], axis=1)

# Rasa API endpoint
RASA_API_URL =  "http://127.0.0.1:4040"  

def chat_with_rasa(message):
    response = requests.post(RASA_API_URL, json={"sender": "user", "message": message})
    print("API Response:", response.json())
    if response.status_code == 200:
        return response.json()
    return [{"text": "Sorry, something went wrong."}]

def search_recipe(query):
    query = query.lower().strip()
    doc = nlp(query)

    # Identify keywords from the query
    keywords = [token.lemma_ for token in doc if token.is_alpha]
    
    # Search for matching recipes
    matches = df[
        df['Title'].str.contains('|'.join(keywords), case=False, na=False) |
        df['Ingredients'].str.contains('|'.join(keywords), case=False, na=False)
    ]
    return matches[['Title', 'Ingredients', 'Instructions', 'Image_Name']].head(3)

# Streamlit UI
st.title("AI Recipe Generator")
st.write("Search for delicious recipes by typing ingredients or dish names!")

# User input for search or chat with Rasa bot
user_query = st.text_input("Enter your query (e.g., 'chicken', 'pasta', 'potatoes'):")

if user_query:
    # Check for recipe search first
    results = search_recipe(user_query)

    if isinstance(results, pd.DataFrame) and not results.empty:
        for idx, row in results.iterrows():
            st.subheader(row['Title'].title())
            st.write(f"**Ingredients:** {row['Ingredients']}")
            st.write(f"**Instructions:** {row['Instructions']}")
            
            # Display Image if Available
            image_path = os.path.join(BASE_DIR, "FoodImages/Food Images", row['Image_Name'] + ".jpg")

            if os.path.exists(image_path):
                st.image(image_path, caption=row['Title'].title(), width=500)
            else:
                st.write("Image not available")
    else:
        # Fall back to chatbot response
        responses = chat_with_rasa(user_query)
        for res in responses:
            st.write(f"Bot: {res.get('text', '')}")