from ..prompts.food_agent import PROMPT_FOOD
from openai import OpenAI
from ..services.qdrant import qdrant
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_KEY)

#handle food collection reviews
def handle_food_collection(message):
    similarity = qdrant.search_documents(
        query_text=message,
        collection_name="demo_collection",
        threshold=0.7
    )[0]
    
    prompt = PROMPT_FOOD.format(
        **{'mon_an_lien_quan': similarity['payload']['document']}
    )
    
    chat_history = [
        {"role": "system", "content": prompt}
    ]
    chat_history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=chat_history
    )
    result = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": result})
    return result

food_tool = {
    "name": "FoodHandler",
    "func": handle_food_collection,
    "description": "Handles queries related to food reviews."
}