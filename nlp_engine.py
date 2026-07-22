"""
nlp_engine.py
-------------
Lightweight NLP / Machine Learning layer for the AI Chatbot for Student
Support.

This module intentionally avoids heavy deep-learning frameworks
(no TensorFlow / PyTorch, no custom model training) and instead uses
classic, interpretable NLP + ML techniques from scikit-learn -- ideal
for a final-year engineering project that should be easy to explain
in a viva:

1. Basic text preprocessing (normalisation)
2. TF-IDF based FAQ retrieval (semantic-ish similarity search) using
   scikit-learn's TfidfVectorizer + cosine similarity
3. Simple keyword-based intent classification
4. Rule-based fallback responses used when the Gemini LLM is
   unavailable (no API key / network error / quota exceeded)

These pieces are combined in gemini_helper.py into a small
"LLM + Retrieval" pipeline: the FAQ retriever first looks for a close
match in the knowledge base; that match (if any) is passed to Gemini
as extra context, and if Gemini itself is unreachable, the retrieved
FAQ or a rule-based response is returned instead so the chatbot never
goes silent.
"""

import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Minimum cosine similarity score (0-1) for a retrieved FAQ to be trusted.
SIMILARITY_THRESHOLD = 0.35

# Very small keyword map used for lightweight intent classification.
# Not a trained classifier -- just a transparent, explainable rule set
# that is easy to extend with more keywords/intents.
INTENT_KEYWORDS = {
    "exam": ["exam", "test", "marks", "grade", "result", "assessment", "hall ticket", "timetable"],
    "fees": ["fee", "fees", "payment", "scholarship", "tuition", "dues"],
    "placement": ["placement", "job", "internship", "recruiter", "career", "interview", "drive"],
    "hostel": ["hostel", "accommodation", "room", "warden"],
    "course": ["course", "subject", "syllabus", "curriculum", "credits", "branch"],
    "login": ["login", "password", "account", "portal", "otp", "sign in"],
    "notice": ["notice", "announcement", "circular", "holiday", "calendar"],
    "greeting": ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"],
}

# Rule-based fallback responses, keyed by intent. Used only when the LLM
# cannot be reached, so the chatbot still gives a useful, on-topic reply.
FALLBACK_RESPONSES = {
    "exam": "For exam-related queries, please check the Notice Board for the latest schedule or contact the examination cell.",
    "fees": "For fee payment or scholarship queries, please check the Notice Board for deadlines or visit the accounts office.",
    "placement": "For placement drives and internship opportunities, please check the Notice Board and the placement cell circulars.",
    "hostel": "For hostel-related concerns, please contact the hostel warden's office.",
    "course": "You can find detailed course information on the Course Information page.",
    "login": "If you're facing login issues, please verify your credentials or contact the IT support desk via the Contact page.",
    "notice": "The latest announcements are always available on the Notice Board.",
    "greeting": "Hello! I'm your AI assistant for student support. Ask me about courses, exams, fees, placements, or notices.",
    "general": "I couldn't reach the AI service just now, but based on your question here's the closest guidance I have. "
               "For anything else, please reach out through the Contact page.",
}


def preprocess_text(text: str) -> str:
    """
    Basic text preprocessing / normalisation:
    - lowercasing
    - punctuation removal
    - whitespace collapsing
    This keeps the TF-IDF vocabulary clean and consistent.
    """
    text = (text or "").lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def classify_intent(text: str) -> str:
    """Lightweight keyword-based intent classification."""
    cleaned = preprocess_text(text)
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in cleaned:
                return intent
    return "general"


def rule_based_fallback(text: str) -> str:
    """Returns a canned, intent-aware response when the LLM is unavailable."""
    intent = classify_intent(text)
    return FALLBACK_RESPONSES.get(intent, FALLBACK_RESPONSES["general"])


class FAQRetriever:
    """
    TF-IDF based FAQ retrieval engine.

    Fits a TF-IDF vectorizer over the FAQ questions stored in the database
    and, given a student's query, finds the closest FAQ using cosine
    similarity. This is a classic Information Retrieval / lightweight ML
    technique -- no training data or model weights are needed, the
    vectorizer is fit on the fly against the (small) FAQ dataset, which is
    fast enough to run per-request and easy to explain in a viva.
    """

    def __init__(self, faqs):
        # faqs: list of dict-like objects with 'question' and 'answer' keys
        self.faqs = list(faqs)
        self.questions = [preprocess_text(f["question"]) for f in self.faqs]
        self.vectorizer = None
        self.tfidf_matrix = None

        if self.questions:
            self.vectorizer = TfidfVectorizer(stop_words="english")
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def best_match(self, query: str):
        """
        Returns (faq_dict, similarity_score) for the closest FAQ.
        If no FAQ is confidently close enough, returns (None, best_score).
        """
        if not self.questions or self.vectorizer is None:
            return None, 0.0

        query_vector = self.vectorizer.transform([preprocess_text(query)])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        best_index = int(similarities.argmax())
        best_score = float(similarities[best_index])

        if best_score >= SIMILARITY_THRESHOLD:
            return self.faqs[best_index], best_score
        return None, best_score

    def top_matches(self, query: str, top_n: int = 3):
        """
        Returns the top-N FAQs ranked by similarity to the query.
        Useful for AI-powered "related questions" style recommendations.
        """
        if not self.questions or self.vectorizer is None:
            return []

        query_vector = self.vectorizer.transform([preprocess_text(query)])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        ranked_indices = similarities.argsort()[::-1][:top_n]

        results = []
        for idx in ranked_indices:
            score = float(similarities[idx])
            if score > 0:
                results.append({**dict(self.faqs[idx]), "similarity": round(score, 2)})
        return results
