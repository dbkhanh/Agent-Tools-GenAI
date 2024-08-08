from openai import OpenAI
import wikipedia
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_KEY)

# Function to search Wikipedia for related information
def search_wikipedia(query, max_words=100):
    try:
        wikipedia.set_lang("en") 
        search_results = wikipedia.search(query)
        if search_results:
            page = wikipedia.page(search_results[0])
            content = page.content
            words = content.split()[:50]
            truncated_content = ' '.join(words)
            return truncated_content
        else:
            return "No relevant Wikipedia article found."
    except wikipedia.exceptions.WikipediaException as e:
        return f"Error: {str(e)}"



def handle_wikipedia(message):
    wikipedia_content = search_wikipedia(message)
    chat_history = [
        {"role": "system", "content": wikipedia_content},
        {"role": "user", "content": message}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=chat_history
    )
    result = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": result})
    
    return result

wiki_tool = {
    "name": "WikiHandler",
    "func": handle_wikipedia,
    "description": "Handles queries related to travel reviews."
}