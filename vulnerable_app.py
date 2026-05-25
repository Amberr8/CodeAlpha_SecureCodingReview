import sqlite3 # Built-in database module
import hashlib # For hashing passwords (but MD5 is weak)
import subprocess # For running system commands (but can be dangerous)
import pickle # For serialization (but can be dangerous)

# VULNERABILITY 1: Hardcoded credentials
SECRET_KEY = "admin123" #hardcoded secret key 
DB_PASSWORD = "root1234"

def get_db_connection(): # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("users.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY,
                     username TEXT,
                     password TEXT)""")
    return conn
# VULNERABILITY 2: SQL Injection
def login(username, password): # User input is directly concatenated into the SQL query
    conn = get_db_connection()
    cursor = conn.cursor()
    # Directly inserting user input into SQL query 
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

# VULNERABILITY 3: Weak password hashing (MD5)
def register(username, password):
    conn = get_db_connection()
    # MD5 is broken and easily cracked
    hashed = hashlib.md5(password.encode()).hexdigest()
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                 (username, hashed))
    conn.commit()
    conn.close()
    print(f"User {username} registered.")
# VULNERABILITY 4: Command Injection
def ping_host(hostname):
    # User input passed directly to shell 
    output = subprocess.call("ping " + hostname, shell=True)
    return output

# VULNERABILITY 5: Insecure Deserialization
def load_session(data):
    # pickle.loads on untrusted data allows remote code execution
    session = pickle.loads(data)
    return session

# Main
if __name__ == "__main__":
    register("admin", "password123")
    user = login("admin", "password123")
    print("Login result:", user)
    ping_host("google.com")