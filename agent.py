import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import Tool
from tools import get_weather, search_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    model_kwargs={"thinking_config": {"thinking_budget": 0, "include_thoughts": False}}
)

tools = [
    Tool(
        name="get_weather",
        func=get_weather,
        description="Kisi bhi sheher ka live mausam batane ke liye. Input me sirf sheher ka naam do, jaise 'Peshawar'"
    ),
    search_tool
]

agent = create_agent(
    llm,
    tools,
    system_prompt="""You are Ayyoon AI Assistant. You are a multilingual assistant.

RULE: Always reply in the SAME language the user used.
- If user writes in English -> reply in English
- If user writes in Roman Urdu -> reply in Roman Urdu
- If user writes in Urdu (Urdu script) -> reply in Urdu script
- If user writes in Pashto -> reply in Pashto
- If user writes in Punjabi, Sindhi, Arabic, Hindi, etc. -> reply in that same language

Never force Urdu or English. Auto-detect the user's language from their message and match it.

FORMAT RULE: Always give clean formatted answer.
Use heading, bullet points and emojis.
For weather: 🌤️ Weather, 🌡️ Temperature, 💨 Wind, 💧 Humidity.
Keep answer short and clear.""")

def ask_agent(question):
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    last_msg = result["messages"][-1]
    content = last_msg.content

    # Agar jawab list me aaye to sirf text nikaalo, signature ko chor do
    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                texts.append(part.get("text", ""))
            elif isinstance(part, str):
                texts.append(part)
        return "".join(texts)
    return content