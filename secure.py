import sqlite3
import hashlib
import subprocess
import os
import bcrypt # For secure password hashing

# FIX 1: No hardcoded credentials  load from environment variables
SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")

def get_db_connection(): # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("users_secure.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY,
                     username TEXT,
                     password TEXT)""")
    return conn

# FIX 2: Parameterized queries  prevents SQL injection
def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Using ? placeholders — safe from SQL injection
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        stored_hash = result[2].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            return result
    return None

# FIX 3: Strong password hashing with bcrypt
def register(username, password):
    conn = get_db_connection()
    # bcrypt automatically adds salt and uses strong hashing
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                 (username, hashed.decode()))
    conn.commit()
    conn.close()
    print(f"User {username} registered securely.")

# FIX 4: No shell=True  prevents command injection
def ping_host(hostname):
    # Validate input and pass as list —never use shell=True
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789.-")
    if not all(c in allowed for c in hostname.lower()):
        print("Invalid hostname.")
        return
    output = subprocess.call(["ping", "-n", "1", hostname], shell=False)
    return output

# FIX 5: No pickle  use JSON for safe deserialization
import json
def load_session(data):
    # JSON cannot execute code safe to deserialize
    session = json.loads(data)
    return session

# Main
if __name__ == "__main__":
    register("admin", "StrongPass@2024")
    user = login("admin", "StrongPass@2024")
    print("Login result:", "Success" if user else "Failed")
    ping_host("google.com")
