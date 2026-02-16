from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            address TEXT,
            mobile TEXT,
            disease TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO patients VALUES (1, 'Rahul Kumar', 25, 'Delhi', '9876543210', 'Fever')")
        cursor.execute("INSERT INTO patients VALUES (2, 'Anita Sharma', 30, 'Mumbai', '9123456780', 'Diabetes')")
        cursor.execute("INSERT INTO patients VALUES (3, 'Arjun Singh', 40, 'Chennai', '9988776655', 'Asthma')")

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    patient = None

    if request.method == "POST":
        patient_id = request.form["patient_id"]

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()

    return render_template("index.html", patient=patient)

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("SELECT disease, COUNT(*) FROM patients GROUP BY disease")
    data = cursor.fetchall()

    conn.close()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("dashboard.html", labels=labels, values=values)


if __name__ == "__main__":
    app.run(debug=True)
