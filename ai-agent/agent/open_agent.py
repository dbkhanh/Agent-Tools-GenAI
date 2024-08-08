from openai import OpenAI
from agent.tools.food_agent import food_tool
from agent.tools.travel_agent import travel_tool
from agent.tools.react_agent import ReActAgent
from agent.tools.wiki_agent import wiki_tool
from dotenv import load_dotenv
import wikipedia
import os

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_KEY)

FOOD_KEYWORDS = ["food", "dish", "cuisine", "recipe", "ingredient", "eat", "candy", "coffee"]
TRAVEL_KEYWORDS = ["destination", "place", "travel", "visit", "tourist", "where", "cave", "Bali"]

def determine_collection(message):
    message_lower = message.lower()
    if any(keyword in message_lower for keyword in FOOD_KEYWORDS):
        return "demo_collection"
    elif any(keyword in message_lower for keyword in TRAVEL_KEYWORDS):
        return "destination_collection"
    else:
        return "Not found!" 


def search_wikipedia(query):
    try:
        wikipedia.set_lang("en")  # Set Wikipedia language to English
        search_results = wikipedia.search(query)
        if search_results:
            page = wikipedia.page(search_results[0])
            return page.content
        else:
            return "No relevant Wikipedia article found."
    except wikipedia.exceptions.WikipediaException as e:
        return f"Error: {str(e)}"

# Initialize the react agent
agent = ReActAgent(tools=[food_tool, travel_tool, wiki_tool])

def get_response(message):
    collection_name = determine_collection(message)
    
    if collection_name == "demo_collection":
        result = agent.run("FoodHandler", message)
    elif collection_name == "destination_collection":
        result = agent.run("TravelHandler", message)
    else:
        result = agent.run("WikiHandler", message)

    return result
