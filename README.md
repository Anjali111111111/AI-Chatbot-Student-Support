# AI Chatbot for Student Support

An AI-powered web application that provides students with intelligent,
always-available support for common academic and campus queries. It combines
a **FastAPI** backend, a lightweight **NLP/ML retrieval layer**, and the
**Google Gemini LLM** to answer student questions accurately — with FAQs,
course information, a notice board, and personal chat history built around a
simple student login.

## Project Overview

Students frequently have repetitive questions about exams, fees, courses,
placements, and campus notices. This project addresses that with a single
chat-first support portal that:

- Understands a student's question using **NLP text preprocessing** and a
  **TF-IDF similarity search** over the college's FAQ knowledge base.
- Uses the matched FAQ as **retrieval context** for the **Gemini LLM**, which
  generates a natural, conversational answer grounded in real institutional
  data (a lightweight Retrieval-Augmented Generation pipeline).
- Falls back to the retrieved FAQ answer — or a **rule-based, intent-aware
  response** — if the LLM is temporarily unavailable, so the chatbot never
  goes silent.
- Wraps all of this in a clean, session-authenticated FastAPI application
  with server-rendered pages and a small JSON REST API.

The result is a compact but complete demonstration of applied AI: NLP,
lightweight ML (no deep learning, no model training), and LLM integration,
built on a modern async Python web framework.

## Features

1. **Student Login** — Session-based authentication backed by SQLite.
2. **AI Chatbot** — Conversational assistant combining TF-IDF retrieval and
   the Gemini LLM.
3. **FAQ Page** — Browsable FAQ knowledge base, also used as the chatbot's
   retrieval source.
4. **Course Information** — List of available courses with codes, duration,
   and descriptions.
5. **Notice Board** — Up-to-date academic notices (exam schedules, placement
   drives, internships, workshops, scholarships, deadlines, holidays).
6. **Contact Information** — Support office email, phone, address, and hours.
7. **Chat History** — Each student can review their own past chatbot
   conversations.

## AI Features

| Feature | Technique | Where it lives |
|---|---|---|
| Text preprocessing | Lowercasing, punctuation stripping, whitespace normalisation | `nlp_engine.py` |
| FAQ semantic search | TF-IDF vectorization + cosine similarity (scikit-learn) | `nlp_engine.py` → `FAQRetriever` |
| Intent classification | Lightweight keyword-based classifier (exam, fees, placement, hostel, course, login, notice, greeting) | `nlp_engine.py` → `classify_intent()` |
| Rule-based fallback | Intent-aware canned responses used when the LLM is unreachable | `nlp_engine.py` → `rule_based_fallback()` |
| LLM response generation | Google Gemini API (`gemini-1.5-flash`) | `gemini_helper.py` |
| Retrieval-Augmented Generation | Best-matching FAQ is injected into the Gemini prompt as context | `gemini_helper.py` → `get_chatbot_response()` |
| AI-powered recommendations | Top-N related FAQ ranking by TF-IDF similarity | `nlp_engine.py` → `FAQRetriever.top_matches()` |

No deep learning frameworks (TensorFlow/PyTorch) and no custom model
training are used — every technique above is classic, interpretable NLP/ML
that is easy to explain end-to-end in an academic evaluation or viva.

## Technology Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn (ASGI server)
- **Templating:** Jinja2 (server-rendered HTML)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API), Bootstrap 5
- **Database:** SQLite
- **AI / NLP / ML:** scikit-learn (TF-IDF + cosine similarity), custom
  intent classifier, Google Gemini API (LLM)
- **Session management:** Starlette `SessionMiddleware`

## System Architecture

```
                         ┌───────────────────────┐
                         │   Browser (Bootstrap   │
                         │   UI + Fetch API JS)   │
                         └───────────┬───────────┘
                                     │ HTTP / JSON
                                     ▼
                         ┌───────────────────────┐
                         │   FastAPI app (app.py) │
                         │  - Session auth        │
                         │  - Page routes (Jinja2)│
                         │  - REST API (/api/...) │
                         └───────────┬───────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 ▼                   ▼                   ▼
        ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐
        │  SQLite DB      │  │ nlp_engine.py  │  │ gemini_helper.py │
        │  (students,     │  │ - preprocess   │  │ - Gemini LLM call│
        │   faqs, courses,│  │ - TF-IDF       │  │ - RAG prompt     │
        │   notices,      │  │   retrieval    │  │ - fallback logic │
        │   chat_history) │  │ - intent + rules│ │                  │
        └────────────────┘  └────────────────┘  └──────────────────┘
                                     ▲                    │
                                     └────────────────────┘
                              FAQ context feeds into the
                              LLM prompt (retrieval-augmented)
```

**Chatbot request flow:**
1. Student sends a message → `POST /chatbot/ask`.
2. `nlp_engine.FAQRetriever` preprocesses the text and finds the closest FAQ
   via TF-IDF cosine similarity.
3. If Gemini is configured, `gemini_helper.get_chatbot_response()` sends the
   message (plus the matched FAQ as context, if any) to Gemini and returns
   its answer.
4. If Gemini is unavailable, the matched FAQ answer — or a rule-based,
   intent-aware fallback — is returned instead.
5. The conversation is stored in `chat_history` and shown to the student.

## Folder Structure

```
ai_chatbot_student_support/
│
├── app.py                 # FastAPI application: routes, auth, REST API
├── config.py               # Configuration (app name, secret key, DB path, Gemini key)
├── gemini_helper.py        # LLM + Retrieval pipeline (Gemini API orchestration)
├── nlp_engine.py            # NLP/ML layer: preprocessing, TF-IDF retrieval, intent, fallback
├── requirements.txt
├── README.md
│
├── database/
│   ├── schema.sql          # Table definitions
│   ├── sample_data.sql     # Sample/test data (students, FAQs, courses, notices)
│   └── init_db.py          # Script to create & seed the SQLite database
│
├── templates/               # Jinja2 HTML templates (unchanged UI, reused as-is)
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── chatbot.html
│   ├── faq.html
│   ├── courses.html
│   ├── notices.html
│   ├── contact.html
│   └── chat_history.html
│
└── static/
    ├── css/style.css
    └── js/script.js
```

## Installation Guide

### 1. Get the project
Place the `ai_chatbot_student_support` folder anywhere on your system.

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root (see [Environment Variables](#environment-variables) below).

### 5. Initialize the database
```bash
python database/init_db.py
```
This creates `student_support.db` with schema + sample data, including test
student logins.

### 6. Run the application
```bash
uvicorn app:app --reload
```
or simply:
```bash
python app.py
```
Open your browser at **http://127.0.0.1:8000**
Interactive API docs (Swagger UI) are available at **http://127.0.0.1:8000/docs**.

### Sample Test Login

| Field    | Value              |
|----------|--------------------|
| Email    | john@student.com   |
| Password | student123         |

(See `database/sample_data.sql` for more sample students.)

## Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_google_gemini_api_key_here
SECRET_KEY=any_random_secret_string
```

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Recommended | Enables live LLM responses from Google Gemini. Get a free key at https://aistudio.google.com/app/apikey |
| `SECRET_KEY` | Recommended | Signs session cookies. Use any random string in production. |

> If `GEMINI_API_KEY` is not set, the chatbot automatically runs in
> **retrieval + rule-based fallback mode** — it will still answer using
> TF-IDF FAQ matching and intent-aware canned responses, so the app never
> crashes during a demo or offline evaluation.

## API Endpoints

### Page routes (server-rendered)

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/` | Redirects to dashboard or login | — |
| GET/POST | `/login` | Login page / login form submission | — |
| GET | `/logout` | Clears session and logs out | — |
| GET | `/dashboard` | Student dashboard | Required |
| GET | `/chatbot` | Chatbot UI page | Required |
| GET | `/faq` | FAQ page | Required |
| GET | `/courses` | Course information page | Required |
| GET | `/notices` | Notice board page | Required |
| GET | `/contact` | Contact information page | Required |
| GET | `/chat-history` | Student's personal chat history | Required |

### REST / JSON API

| Method | Path | Description | Auth |
|---|---|---|---|
| POST | `/chatbot/ask` | Send a message to the AI chatbot; returns `{reply, source, intent, similarity}` | Required |
| GET | `/api/health` | Health check; reports whether the Gemini API key is configured | — |
| GET | `/api/faqs` | Returns all FAQs as JSON | Required |
| GET | `/api/faq/search?q=...` | TF-IDF powered FAQ search; returns top matching FAQs with similarity scores | Required |

Example chatbot request:
```bash
curl -X POST http://127.0.0.1:8000/chatbot/ask \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<your-session-cookie>" \
  -d '{"message": "When are the semester exams?"}'
```

Example response:
```json
{
  "reply": "The end semester examination timetable has been published on the academic portal...",
  "source": "faq_retrieval",
  "intent": "exam",
  "similarity": 0.81
}
```

## Future Improvements

- Hash student passwords (e.g. with `passlib`/`bcrypt`) instead of storing
  them in plain text.
- Add a student self-registration flow with email verification.
- Add an admin panel for managing FAQs, courses, and notices without editing
  SQL directly.
- Upgrade TF-IDF retrieval to sentence-embedding based semantic search
  (e.g. `sentence-transformers`) for better paraphrase handling.
- Add conversation memory so the chatbot can handle multi-turn context.
- Add analytics on the most common student intents to guide FAQ updates.
- Containerize with Docker and add CI/CD for deployment.
