# AI Chatbot for Student Support Services

An IBM PBEL GenAI Virtual Internship project. A Flask web application that provides
students with an AI-powered chatbot (Google Gemini API), FAQs, course information,
a notice board, contact details, and personal chat history — all behind a simple
student login system.

## Features

1. **Student Login** — Simple session-based authentication using SQLite.
2. **AI Chatbot** — Powered by the Google Gemini API, answers student queries.
3. **FAQ Page** — Commonly asked questions and answers.
4. **Course Information** — List of available courses with details.
5. **Notice Board** — Latest college/institute notices.
6. **Contact Information** — Contact details of the institute/support desk.
7. **Chat History** — Each student can view their own past chatbot conversations.

## Tech Stack

- Python 3.10+
- Flask (backend/web framework)
- HTML, CSS, JavaScript, Bootstrap 5 (frontend)
- SQLite (database)
- Google Gemini API (AI chatbot)

## Folder Structure

```
ai_chatbot_student_support/
│
├── app.py                 # Main Flask application (routes/controllers)
├── config.py               # Configuration (secret key, Gemini API key, DB path)
├── gemini_helper.py        # Handles communication with Gemini API
├── requirements.txt
├── README.md
│
├── database/
│   ├── schema.sql          # Table definitions
│   ├── sample_data.sql     # Sample/test data
│   └── init_db.py          # Script to create & seed the SQLite database
│
├── templates/               # Jinja2 HTML templates
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

## Installation & Setup

### 1. Clone / copy the project folder
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

### 4. Set your Gemini API key
Create a file named `.env` in the project root (same folder as `app.py`) with:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
SECRET_KEY=any_random_secret_string
```
You can get a free Gemini API key from https://aistudio.google.com/app/apikey

> If no key is set, the chatbot will still run using a safe fallback response,
> so the app never crashes during a demo.

### 5. Initialize the database
```bash
python database/init_db.py
```
This creates `student_support.db` with tables and sample data (including a
test student login).

### 6. Run the application
```bash
python app.py
```
Open your browser at: **http://127.0.0.1:5000**

## Sample Test Login

| Field    | Value            |
|----------|-------------------|
| Email    | john@student.com |
| Password | student123        |

(See `database/sample_data.sql` for more sample students.)

## How It Works

1. Student logs in using email & password (checked against SQLite `students` table).
2. On successful login, a Flask **session** is created.
3. From the Dashboard, the student can access the Chatbot, FAQs, Courses,
   Notice Board, Contact page, and their Chat History.
4. The Chatbot page sends the student's message via JavaScript (Fetch API) to
   the `/chatbot` Flask route, which calls `gemini_helper.py` to get an AI
   response from Google Gemini, stores the conversation in the `chat_history`
   table, and returns the reply to be displayed in the chat window.

## Notes for Submission

- This project is intentionally kept simple and readable for academic evaluation.
- All passwords in `sample_data.sql` are plain text ONLY for demo/internship
  purposes. In a real production app, passwords must be hashed
  (the login code already uses `werkzeug.security` hashing for any new
  signups if extended).
