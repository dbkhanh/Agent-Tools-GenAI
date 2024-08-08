from ..prompts.travel_agent import PROMPT_TRAVEL
from ..services.qdrant import qdrant
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_KEY)

#handle destinations collection review
def handle_travel_collection(message):
    similarity = qdrant.search_documents(
        query_text=message,
        collection_name="destination_collection",
        threshold=0.7
    )[0]
    
    prompt = PROMPT_TRAVEL.format(
        **{'dia_diem_lien_quan': similarity['payload']['document']}
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

travel_tool = {
    "name": "TravelHandler",
    "func": handle_travel_collection,
    "description": "Handles queries related to travel reviews."
}