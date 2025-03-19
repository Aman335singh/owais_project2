from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import pandas as pd
import spacy
import os

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_md")

# Load cleaned dataset
df = pd.read_csv("M:/sem8/owais_project/food_data.csv").drop(['Unnamed: 0'], axis=1)

class ActionSearchRecipe(Action):

    def name(self) -> str:
        return "action_search_recipe"

    def run(self, dispatcher, tracker, domain) -> list:
        query = tracker.get_slot("recipe_query")
        if not query:
            dispatcher.utter_message("Please specify what recipe you're looking for.")
            return []

        doc = nlp(query)
        keywords = [token.lemma_ for token in doc if token.is_alpha]
        matches = df[
            df['Title'].str.contains('|'.join(keywords), case=False, na=False) |
            df['Ingredients'].str.contains('|'.join(keywords), case=False, na=False)
        ]

        if not matches.empty:
            response = "Here are some delicious recipes for you:\n"
            for idx, row in matches.head(3).iterrows():
                response += f"\n**{row['Title']}**\n- Ingredients: {row['Ingredients']}\n- Instructions: {row['Instructions']}\n"
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("Sorry, I couldn't find any recipes for your query.")

        return [SlotSet("recipe_query", None)]