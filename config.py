import os
from dotenv import load_dotenv

# Load variables from a .env file if present
load_dotenv()

class Config:
    # Flask secret key (used for session management)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key_change_this")

    # SQLite database file path
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "student_support.db")

    # Google Gemini API key
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

    # Gemini model to use
    GEMINI_MODEL = "gemini-3-flash-preview"
