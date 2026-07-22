"""
gemini_helper.py
-----------------
LLM-powered response generation for the AI Chatbot for Student Support.

This module implements a small "LLM + Retrieval" pipeline:

    1. The student's message is run through the TF-IDF FAQRetriever
       (nlp_engine.py) to find the closest matching FAQ, if any.
    2. If a confident FAQ match is found, it is passed to Gemini as
       extra context (retrieval-augmented generation), so the LLM can
       ground its answer in the college's actual FAQ knowledge base.
    3. If the Gemini API key is missing or the API call fails for any
       reason (offline demo, quota, network issue), the pipeline falls
       back to the retrieved FAQ answer or, if no FAQ matched, a
       rule-based response from nlp_engine.py -- so the chatbot always
       responds with something useful instead of crashing or going silent.

Keeping this orchestration logic in one place makes the AI pipeline easy
to explain end-to-end during a viva.
"""

from google import genai

from config import Config
from nlp_engine import FAQRetriever, classify_intent, rule_based_fallback

client = None

if Config.GEMINI_API_KEY:
    client = genai.Client(api_key=Config.GEMINI_API_KEY)

# System instructions that shape the chatbot's behaviour and personality
SYSTEM_PROMPT = (
    "You are 'Campus Assist', the AI chatbot for the AI Chatbot for Student "
    "Support platform. You help students with questions about courses, "
    "exams, fees, placements, hostel life, and campus notices. "
    "Keep your answers short, clear, and student-friendly. "
    "If a 'Relevant FAQ' is provided in the prompt, use it as ground-truth "
    "context and prefer it over guessing. "
    "If you don't know something specific to the college, politely suggest "
    "the student check the Notice Board or contact the support office via "
    "the Contact page."
)


def get_chatbot_response(user_message: str, faqs=None) -> dict:
    """
    Runs the full LLM + Retrieval pipeline for a single student message.

    Args:
        user_message: the raw text typed by the student.
        faqs: list of FAQ rows (dict-like, with 'question'/'answer') used
              to build the TF-IDF retriever for this request.

    Returns:
        A dict with:
            reply       - the text to show the student
            source      - which part of the pipeline produced the reply
                          ("llm_with_retrieval", "llm", "faq_retrieval",
                          "faq_retrieval_fallback", "rule_based_fallback")
            intent      - the lightweight keyword-classified intent
            similarity  - the TF-IDF cosine similarity of the best FAQ match
    """
    user_message = (user_message or "").strip()
    if not user_message:
        return {
            "reply": "Please type a question so I can help you.",
            "source": "validation",
            "intent": "general",
            "similarity": 0.0,
        }

    intent = classify_intent(user_message)
    retriever = FAQRetriever(faqs or [])
    matched_faq, similarity = retriever.best_match(user_message)

    # ---- No Gemini API key configured: retrieval + rule-based demo mode ----
    if not Config.GEMINI_API_KEY:
        if matched_faq:
            return {
                "reply": matched_faq["answer"],
                "source": "faq_retrieval",
                "intent": intent,
                "similarity": round(similarity, 2),
            }
        return {
            "reply": rule_based_fallback(user_message),
            "source": "rule_based_fallback",
            "intent": intent,
            "similarity": round(similarity, 2),
        }

    # ---- Build the (optional) retrieval-augmented prompt for Gemini ----
    prompt = user_message
    if matched_faq:
        prompt = (
            f"Relevant FAQ:\nQ: {matched_faq['question']}\nA: {matched_faq['answer']}\n\n"
            f"Student question: {user_message}\n\n"
            "Using the FAQ context above if it is relevant, answer the "
            "student's question naturally and concisely."
        )

    try:
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
        )

        reply_text = response.text.strip()

        if not reply_text:
            raise ValueError("Empty response from Gemini")

        return {
            "reply": reply_text,
            "source": "llm_with_retrieval" if matched_faq else "llm",
            "intent": intent,
            "similarity": round(similarity, 2),
        }

    except Exception as e:
        print("\n========== GEMINI ERROR ==========")
        print(repr(e))
        print("==================================\n")

        # Gemini unavailable -- gracefully fall back to retrieval / rules
        if matched_faq:
          return {
            "reply": matched_faq["answer"],
            "source": "faq_retrieval_fallback",
            "intent": intent,
            "similarity": round(similarity, 2),
     }

        return {
            "reply": rule_based_fallback(user_message),
            "source": "rule_based_fallback",
            "intent": intent,
            "similarity": round(similarity, 2),
    }
