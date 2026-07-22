"""
app.py
------
Main FastAPI application for the AI Chatbot for Student Support.

This file wires together:
- Session-based student login (Starlette SessionMiddleware + a custom
  FastAPI dependency/exception-handler pair that redirects unauthenticated
  users, similar in spirit to Flask's @login_required decorator)
- Server-rendered pages (Jinja2Templates) for Dashboard, FAQ, Courses,
  Notice Board, Contact, and Chat History -- the original HTML/CSS/JS is
  reused unchanged
- A small REST API layer under /api/... that exposes the AI chatbot
  pipeline (TF-IDF FAQ retrieval + Gemini LLM + rule-based fallback)
  defined in gemini_helper.py / nlp_engine.py

Route paths and Jinja endpoint *names* are kept identical to the original
Flask version (e.g. "dashboard", "chatbot_page", "chat_history") so the
existing templates -- which call url_for(...) and session.get(...) --
continue to work with no redesign.
"""

import sqlite3

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel

from config import Config
from gemini_helper import get_chatbot_response

app = FastAPI(title=Config.APP_NAME)
app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ----------------------------------------------------------------------
# Database helper
# ----------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------------------------------------------------
# Template rendering helper
# Re-creates the small pieces of Flask/Jinja "magic" (url_for, flash
# messages, session) that the existing templates rely on, so the HTML
# files did not need to be rewritten for FastAPI.
# ----------------------------------------------------------------------
def render(request: Request, template_name: str, status_code: int = 200, **context):
    def _url_for(name: str, **path_params):
        # Flask templates call url_for('static', filename=...); FastAPI's
        # StaticFiles route expects a 'path' param instead of 'filename'.
        if name == "static" and "filename" in path_params:
            path_params = dict(path_params)
            path_params["path"] = path_params.pop("filename")
        return str(request.url_for(name, **path_params))

    def _get_flashed_messages(with_categories: bool = False):
        flashes = request.session.pop("_flashes", [])
        if with_categories:
            return flashes
        return [message for _category, message in flashes]

    ctx = {
        "request": request,
        "session": request.session,
        "url_for": _url_for,
        "get_flashed_messages": _get_flashed_messages,
        "app_name": Config.APP_NAME,
    }
    ctx.update(context)
    return templates.TemplateResponse(template_name, ctx, status_code=status_code)


def flash(request: Request, message: str, category: str = "info"):
    flashes = request.session.get("_flashes", [])
    flashes.append([category, message])
    request.session["_flashes"] = flashes


# ----------------------------------------------------------------------
# Login-required dependency (FastAPI's equivalent of a route decorator)
# ----------------------------------------------------------------------
class LoginRequiredError(Exception):
    """Raised by the login_required dependency; handled below to redirect."""


@app.exception_handler(LoginRequiredError)
async def login_required_handler(request: Request, exc: LoginRequiredError):
    flash(request, "Please log in to continue.", "warning")
    return RedirectResponse(url="/login", status_code=303)


def login_required(request: Request):
    if "student_id" not in request.session:
        raise LoginRequiredError()
    return request.session


# ----------------------------------------------------------------------
# Page routes (server-rendered, same paths as the original Flask app)
# ----------------------------------------------------------------------

@app.get("/", name="index")
def index(request: Request):
    if "student_id" in request.session:
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", name="login")
def login_get(request: Request):
    if "student_id" in request.session:
        return RedirectResponse(url="/dashboard", status_code=303)
    return render(request, "login.html")


@app.post("/login", name="login")
async def login_post(request: Request):
    form = await request.form()
    email = str(form.get("email", "")).strip()
    password = str(form.get("password", "")).strip()

    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE email = ? AND password = ?",
        (email, password),
    ).fetchone()
    conn.close()

    if student:
        request.session["student_id"] = student["id"]
        request.session["student_name"] = student["name"]
        request.session["roll_number"] = student["roll_number"]
        flash(request, f"Welcome back, {student['name']}!", "success")
        return RedirectResponse(url="/dashboard", status_code=303)

    flash(request, "Invalid email or password. Please try again.", "danger")
    return RedirectResponse(url="/login", status_code=303)


@app.get("/logout", name="logout")
def logout(request: Request):
    request.session.clear()
    flash(request, "You have been logged out successfully.", "info")
    return RedirectResponse(url="/login", status_code=303)


@app.get("/dashboard", name="dashboard")
def dashboard(request: Request, _student=Depends(login_required)):
    return render(request, "dashboard.html", name=request.session.get("student_name"))


@app.get("/chatbot", name="chatbot_page")
def chatbot_page(request: Request, _student=Depends(login_required)):
    return render(request, "chatbot.html")


@app.get("/faq", name="faq")
def faq(request: Request, _student=Depends(login_required)):
    conn = get_db_connection()
    faqs = conn.execute("SELECT * FROM faqs").fetchall()
    conn.close()
    return render(request, "faq.html", faqs=faqs)


@app.get("/courses", name="courses")
def courses(request: Request, _student=Depends(login_required)):
    conn = get_db_connection()
    courses_list = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render(request, "courses.html", courses=courses_list)


@app.get("/notices", name="notices")
def notices(request: Request, _student=Depends(login_required)):
    conn = get_db_connection()
    notices_list = conn.execute(
        "SELECT * FROM notices ORDER BY posted_on DESC"
    ).fetchall()
    conn.close()
    return render(request, "notices.html", notices=notices_list)


@app.get("/contact", name="contact")
def contact(request: Request, _student=Depends(login_required)):
    return render(request, "contact.html")


@app.get("/chat-history", name="chat_history")
def chat_history(request: Request, _student=Depends(login_required)):
    conn = get_db_connection()
    history = conn.execute(
        "SELECT * FROM chat_history WHERE student_id = ? ORDER BY created_at DESC",
        (request.session["student_id"],),
    ).fetchall()
    conn.close()
    return render(request, "chat_history.html", history=history)


# ----------------------------------------------------------------------
# AI Chatbot REST API
# (used by static/js/script.js via fetch(); also directly testable as a
# standalone JSON API / documented automatically at /docs)
# ----------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str


@app.post("/chatbot/ask", name="chatbot_ask")
def chatbot_ask(request: Request, payload: ChatRequest, _student=Depends(login_required)):
    user_message = payload.message.strip()
    if not user_message:
        return JSONResponse({"reply": "Please type a message before sending."}, status_code=400)

    conn = get_db_connection()
    faq_rows = conn.execute("SELECT question, answer FROM faqs").fetchall()
    faqs = [dict(row) for row in faq_rows]

    result = get_chatbot_response(user_message, faqs=faqs)

    conn.execute(
        "INSERT INTO chat_history (student_id, user_message, bot_response) VALUES (?, ?, ?)",
        (request.session["student_id"], user_message, result["reply"]),
    )
    conn.commit()
    conn.close()

    return JSONResponse(
        {
            "reply": result["reply"],
            "source": result.get("source"),
            "intent": result.get("intent"),
            "similarity": result.get("similarity"),
        }
    )


# ----------------------------------------------------------------------
# Small supporting AI/REST endpoints (used for the FAQ smart-search demo
# and to make the AI pipeline independently testable via /docs)
# ----------------------------------------------------------------------

@app.get("/api/health", name="api_health")
def api_health():
    return {
        "status": "ok",
        "app": Config.APP_NAME,
        "llm_configured": bool(Config.GEMINI_API_KEY),
    }


@app.get("/api/faqs", name="api_faqs")
def api_faqs(_student=Depends(login_required)):
    conn = get_db_connection()
    faq_rows = conn.execute("SELECT id, question, answer FROM faqs").fetchall()
    conn.close()
    return [dict(row) for row in faq_rows]


@app.get("/api/faq/search", name="api_faq_search")
def api_faq_search(q: str, _student=Depends(login_required)):
    """TF-IDF powered FAQ search -- returns the top matching FAQs for a query."""
    from nlp_engine import FAQRetriever

    conn = get_db_connection()
    faq_rows = conn.execute("SELECT id, question, answer FROM faqs").fetchall()
    conn.close()

    retriever = FAQRetriever([dict(row) for row in faq_rows])
    return {"query": q, "results": retriever.top_matches(q, top_n=3)}


# ----------------------------------------------------------------------
# Entry point (for `python app.py`; `uvicorn app:app --reload` also works)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
