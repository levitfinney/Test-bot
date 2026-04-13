from flask import Flask, request, jsonify, render_template, session
import sqlite3, requests

app = Flask(__name__)
app.secret_key = "change_this_key"

# =========================
# DATABASE
# =========================
def db():
    return sqlite3.connect("data.db")

def init():
    c = db().cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        q TEXT,
        r TEXT
    )
    """)

    db().commit()
    db().close()

init()

# =========================
# SAFETY
# =========================
def safe(text):
    blocked = ["hack", "bypass", "exploit"]
    return not any(b in text.lower() for b in blocked)

# =========================
# AI (HuggingFace)
# =========================
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY"}

def ai(prompt):
    try:
        r = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        return r.json()[0]["generated_text"]
    except:
        return "AI offline."

# =========================
# SAVE HISTORY
# =========================
def save(uid, q, r):
    c = db().cursor()
    c.execute("INSERT INTO history (user_id, q, r) VALUES (?,?,?)", (uid, q, r))
    db().commit()
    db().close()

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json["q"]

    if not safe(q):
        return jsonify({"r": "⚠️ Not allowed."})

    response = ai("Teach step by step: " + q)

    uid = session.get("uid", 1)
    save(uid, q, response)

    return jsonify({"r": response})

if __name__ == "__main__":
    app.run(debug=True)
