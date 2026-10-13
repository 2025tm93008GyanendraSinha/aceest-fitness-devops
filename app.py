import sqlite3
from flask import Flask, render_template, request, jsonify, session

DB_NAME = "aceest_fitness.db"
app = Flask(__name__)
app.secret_key = "aceest_devops_secret"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        age INTEGER,
        height REAL,
        weight REAL,
        program TEXT,
        calories INTEGER,
        target_weight REAL,
        target_adherence INTEGER,
        membership_status TEXT,
        membership_end TEXT
    )
    """)
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES ('admin','admin','Admin')")
    conn.commit()
    conn.close()

@app.route("/")
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return render_template("index.html", user=None)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    row = cur.fetchone()
    conn.close()
    
    if row:
        session["user"] = {"username": username, "role": row[0]}
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"status": "success"}), 200

@app.route("/api/clients", methods=["GET", "POST"])
def manage_clients():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        if not name:
            return jsonify({"error": "Name required"}), 400
        try:
            cur.execute("INSERT OR IGNORE INTO clients (name, membership_status) VALUES (?, ?)", (name, "Active"))
            conn.commit()
            conn.close()
            return jsonify({"message": f"Client {name} saved"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    cur.execute("SELECT id, name, program, membership_status FROM clients")
    clients = [{"id": row[0], "name": row[1], "program": row[2], "status": row[3]} for row in cur.fetchall()]
    conn.close()
    return jsonify({"clients": clients}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
    