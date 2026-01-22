import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load env once
load_dotenv(dotenv_path="backend/.env")


# 🔹 OpenAI (AI Answer)
def ask_openai(question: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a health assistant. "
                    "Give safe, general medical information and advise consulting a doctor."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response.choices[0].message.content


# 🔹 Tavily (Web / Real-time Summary)
def tavily_search(question: str):
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Tavily API key not configured"

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": question,
        "search_depth": "basic",
        "include_answer": True,
        "max_results": 3
    }

    res = requests.post(url, json=payload, timeout=20)
    res.raise_for_status()
    data = res.json()

    return data.get("answer", "No web summary found")
