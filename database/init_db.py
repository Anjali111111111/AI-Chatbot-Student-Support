"""
init_db.py
----------
Run this script once to create the SQLite database file and populate it
with the schema and sample data.

Usage:
    python database/init_db.py
"""

import sqlite3
import os
import sys

# Make sure this script works whether run from project root or database/ folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DB_PATH = os.path.join(PROJECT_ROOT, "student_support.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
SAMPLE_DATA_PATH = os.path.join(BASE_DIR, "sample_data.sql")


def initialize_database():
    print(f"Creating database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    print("Schema created successfully.")

    with open(SAMPLE_DATA_PATH, "r") as f:
        conn.executescript(f.read())
    print("Sample data inserted successfully.")

    conn.commit()
    conn.close()
    print("Database initialization complete!")


if __name__ == "__main__":
    initialize_database()
