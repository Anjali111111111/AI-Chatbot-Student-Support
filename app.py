"""
app.py
------
Main Flask application for the AI Chatbot for Student Support Services.
Contains all routes: login/logout, dashboard, chatbot, FAQ, courses,
notices, contact, and chat history.
"""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

from config import Config
from gemini_helper import get_chatbot_response

app = Flask(__name__)
app.config.from_object(Config)


# ----------------------------------------------------------------------
# Database helper
# ----------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-like access to rows
    return conn


# ----------------------------------------------------------------------
# Login-required decorator
# ----------------------------------------------------------------------
def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "student_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------

@app.route("/")
def index():
    if "student_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        student = conn.execute(
            "SELECT * FROM students WHERE email = ? AND password = ?",
            (email, password),
        ).fetchone()
        conn.close()

        if student:
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            session["roll_number"] = student["roll_number"]
            flash(f"Welcome back, {student['name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=session.get("student_name"))


@app.route("/chatbot")
@login_required
def chatbot_page():
    return render_template("chatbot.html")


@app.route("/chatbot/ask", methods=["POST"])
@login_required
def chatbot_ask():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message before sending."}), 400

    bot_reply = get_chatbot_response(user_message)

    # Save conversation to chat_history table
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO chat_history (student_id, user_message, bot_response) VALUES (?, ?, ?)",
        (session["student_id"], user_message, bot_reply),
    )
    conn.commit()
    conn.close()

    return jsonify({"reply": bot_reply})


@app.route("/faq")
@login_required
def faq():
    conn = get_db_connection()
    faqs = conn.execute("SELECT * FROM faqs").fetchall()
    conn.close()
    return render_template("faq.html", faqs=faqs)


@app.route("/courses")
@login_required
def courses():
    conn = get_db_connection()
    courses_list = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("courses.html", courses=courses_list)


@app.route("/notices")
@login_required
def notices():
    conn = get_db_connection()
    notices_list = conn.execute(
        "SELECT * FROM notices ORDER BY posted_on DESC"
    ).fetchall()
    conn.close()
    return render_template("notices.html", notices=notices_list)


@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html")


@app.route("/chat-history")
@login_required
def chat_history():
    conn = get_db_connection()
    history = conn.execute(
        "SELECT * FROM chat_history WHERE student_id = ? ORDER BY created_at DESC",
        (session["student_id"],),
    ).fetchall()
    conn.close()
    return render_template("chat_history.html", history=history)


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
