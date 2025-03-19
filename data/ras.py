version: "3.1"

intents:
  - greet
  - goodbye
  - recipe_search

entities:
  - recipe_query

slots:
  recipe_query:
    type: text
    influence_conversation: true

responses:
  utter_greet:
    - text: "Hello! I'm your AI Recipe Generator. What recipe are you looking for today?"

  utter_goodbye:
    - text: "Goodbye! Enjoy your cooking!"

  utter_ask_recipe_query:
    - text: "Please tell me the ingredients or dish name you're searching for."

actions:
  - action_search_recipe

---
nlu:
- intent: greet
  examples: |
    - Hi
    - Hello
    - Hey there

- intent: goodbye
  examples: |
    - Bye
    - Goodbye
    - See you later

- intent: recipe_search
  examples: |
    - I want a recipe with chicken
    - Show me a pasta recipe
    - Find recipes using potatoes

---
stories:
- story: greet and ask recipe
  steps:
  - intent: greet
  - action: utter_greet
  - intent: recipe_search
  - action: action_search_recipe

- story: say goodbye
  steps:
  - intent: goodbye
  - action: utter_goodbye

---
endpoints:
  action_endpoint:
    url: "http://localhost:5055/webhook"
  

import streamlit as st
import requests

# Rasa endpoint URL
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

def chat_with_rasa(message):
    response = requests.post(RASA_API_URL, json={"sender": "user", "message": message})
    if response.status_code == 200:
        return response.json()
    return [{"text": "Sorry, something went wrong."}]

# Streamlit UI
st.title("AI Recipe Generator with Rasa and SpaCy")
st.write("Chat with me to get recipe recommendations!")

# Chat interface
user_query = st.text_input("Ask me for a recipe suggestion or ingredient details:")

if user_query:
    responses = chat_with_rasa(user_query)
    for res in responses:
        st.write(res.get("text", ""))