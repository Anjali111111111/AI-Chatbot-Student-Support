"""
gemini_helper.py
-----------------
Handles all communication with the Google Gemini API for the chatbot feature.
Keeping this logic in a separate file keeps app.py clean and easy to read.
"""

import google.generativeai as genai
from config import Config

# Configure the Gemini client only if an API key is available
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)

# System instructions that shape the chatbot's behaviour and personality
SYSTEM_PROMPT = (
    "You are 'Campus Assist', a friendly and helpful AI chatbot for a college's "
    "Student Support Services portal. You help students with questions about "
    "courses, exams, fees, campus facilities, notices, and general student life. "
    "Keep your answers short, clear, and student-friendly. "
    "If you don't know something specific to the college, politely suggest the "
    "student contact the support office via the Contact page."
)


def get_chatbot_response(user_message: str) -> str:
    """
    Sends the student's message to Gemini and returns the AI's reply as text.
    If the API key is missing or a request fails, a safe fallback message
    is returned instead of crashing the app (useful for offline demos).
    """
    if not user_message or not user_message.strip():
        return "Please type a question so I can help you."

    if not Config.GEMINI_API_KEY:
        return (
            "AI service is not configured yet. Please add your GEMINI_API_KEY "
            "in the .env file to enable live AI responses. "
            "(This is a fallback demo response.)"
        )

    try:
        model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )
        response = model.generate_content(user_message)
        return response.text.strip() if response and response.text else \
            "Sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        # Any API error (bad key, network issue, quota, etc.) is handled gracefully
        return f"Sorry, the AI service is currently unavailable. ({str(e)})"
