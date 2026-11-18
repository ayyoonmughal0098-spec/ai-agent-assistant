import requests
from langchain_community.tools import DuckDuckGoSearchResults

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url, timeout=10).json()
        current = data['current_condition'][0]
        return f"{city} me abhi {current['temp_C']}°C hai, {current['weatherDesc'][0]['value']}. Hawa {current['windspeedKmph']} km/h chal rahi hai."
    except Exception as e:
        return f"Weather nahi mila: {e}"

search_tool = DuckDuckGoSearchResults(num_results=3)