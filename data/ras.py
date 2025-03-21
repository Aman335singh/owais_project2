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
    mappings:
      - type: from_entity
        entity: recipe_query

responses:
  utter_greet:
    - text: "Hello! I'm your AI Recipe Generator. What recipe are you looking for today?"
    - text: "Hey there! What delicious dish are you craving today?"

  utter_goodbye:
    - text: "Goodbye! Enjoy your cooking!"

  utter_ask_recipe_query:
    - text: "Please tell me the ingredients or dish name you're searching for."

  utter_fallback:
    - text: "I'm not sure how to help with that. Could you ask about a recipe or ingredients?"

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
    - What can I make with tomatoes and cheese?
    - Suggest a vegetarian dish

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

- story: fallback response
  steps:
  - intent: recipe_search
  - action: utter_fallback

---
endpoints:
  action_endpoint:
    url: "http://localhost:5055/webhook"

---
import streamlit as st
import requests

# Rasa endpoint URL
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

def chat_with_rasa(message):
    try:
        response = requests.post(RASA_API_URL, json={"sender": "user", "message": message}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return [{"text": "Sorry, I couldn't connect to the server. Please try again."}]

# Streamlit UI
st.title("AI Recipe Generator with Rasa and SpaCy")
st.write("Chat with me to get recipe recommendations!")

# Conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Chat interface
user_query = st.text_input("Ask me for a recipe suggestion or ingredient details:")

if user_query:
    st.session_state.conversation.append(f"**You:** {user_query}")
    responses = chat_with_rasa(user_query)
    for res in responses:
        st.session_state.conversation.append(f"**Bot:** {res.get('text', '')}")

# Display conversation history
for message in st.session_state.conversation:
    st.write(message)
