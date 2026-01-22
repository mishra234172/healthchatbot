from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.services import ask_openai, tavily_search

# Load env
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

app = FastAPI()

# CORS (frontend ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg": "HealthBot running with OpenAI + Tavily 🚀"}

@app.post("/ask")
def ask(data: dict):
    question = data.get("question")

    if not question:
        return {
            "ai": "No question provided",
            "summary": "Please ask a health-related question"
        }

    ai_answer = "AI service unavailable"
    web_summary = "Web service unavailable"

    # 🔹 OpenAI
    try:
        if OPENAI_KEY:
            ai_answer = ask_openai(question)
    except Exception as e:
        ai_answer = f"AI error: {str(e)}"

    # 🔹 Tavily
    try:
        if TAVILY_KEY:
            web_summary = tavily_search(question)
    except Exception as e:
        web_summary = f"Web error: {str(e)}"

    return {
        "ai": ai_answer,
        "summary": web_summary
    }
