import os
from dotenv import load_dotenv

# Load variables from a .env file if present
load_dotenv()


class Config:
    # Application branding (used in page titles, navbar, README, etc.)
    APP_NAME = "AI Chatbot for Student Support"

    # Secret key used to sign session cookies (FastAPI/Starlette SessionMiddleware)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key_change_this")

    # SQLite database file path
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "student_support.db")

    # Google Gemini API key
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

    # Gemini model used for LLM-powered response generation
    GEMINI_MODEL = "gemini-3.5-flash"

    # Minimum TF-IDF cosine similarity for an FAQ match to be considered
    # confident enough to use as retrieval context / direct answer.
    FAQ_SIMILARITY_THRESHOLD = 0.35
