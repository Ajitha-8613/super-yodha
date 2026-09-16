from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

print("BREVO KEY LOADED:", bool(os.getenv("BREVO_API_KEY")))
print("BREVO SENDER:", os.getenv("BREVO_SENDER_EMAIL"))

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# DATABASE NAME
# ==========================================

DATABASE = "aura.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# CREATE DATABASE TABLE
# ==========================================

def init_database():

    connection = get_db_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            location TEXT NOT NULL,
            email TEXT NOT NULL,
            grievance TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
        """
    )

    connection.commit()

    connection.close()


# ==========================================
# SEND EMAIL
# ==========================================

def send_email(to_email, subject, body):
    try:
        api_key = os.getenv("BREVO_API_KEY")
        sender_email = os.getenv("BREVO_SENDER_EMAIL")
        print("Brevo API key loaded:", bool(api_key))
        print("Brevo API key length:", len(api_key) if api_key else 0)
        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        data = {
            "sender": {
                "name": "Super Yodha",
                "email": sender_email
            },
            "to": [
                {
                    "email": to_email
                }
            ],
            "subject": subject,
            "textContent": body
        }

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        if response.status_code == 201:
            print("Email sent successfully!")
            return True

        print("Email sending failed:", response.text)
        return False

    except Exception as e:
        print("Email sending failed:", e)
        return False

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# SUBMIT HELP REQUEST
# ==========================================

@app.route("/submit", methods=["POST"])
def submit_request():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No request data received."
        }), 400


    # ==========================================
    # GET INFORMATION FROM CHATBOT
    # ==========================================

    name = data.get("name", "").strip()
    age = data.get("age", "").strip()
    location = data.get("location", "").strip()
    email = data.get("email", "").strip()
    grievance = data.get("grievance", "").strip()


    # ==========================================
    # BASIC VALIDATION
    # ==========================================

    if not name:

        return jsonify({
            "success": False,
            "message": "Name is required."
        }), 400


    if not age:

        return jsonify({
            "success": False,
            "message": "Age is required."
        }), 400


    if not location:

        return jsonify({
            "success": False,
            "message": "Location is required."
        }), 400


    if not email:

        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400


    if not grievance:

        return jsonify({
            "success": False,
            "message": "Please describe your problem."
        }), 400


    # ==========================================
    # CURRENT DATE AND TIME
    # ==========================================

    submitted_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # ==========================================
    # SAVE REQUEST TO DATABASE
    # ==========================================

    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO requests
        (
            name,
            age,
            location,
            email,
            grievance,
            submitted_at,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            age,
            location,
            email,
            grievance,
            submitted_at,
            "Pending"
        )
    )

    connection.commit()

    request_id = cursor.lastrowid

    connection.close()


    # ==========================================
    # SEND EMAIL NOTIFICATION
    # ==========================================

    subject = (
        f"Super Yodha — Help Request Received #{request_id}"
    )


    body = f"""
Hello {name},

Your help request has been successfully received by Super Yodha.

Request ID: #{request_id}

Name: {name}
Age: {age}
Location: {location}
Email: {email}

Grievance:
{grievance}

Status: Pending
Submitted At: {submitted_at}

Your request has been recorded and will be reviewed.

Regards,
SUPER YODHA
Guardian of Earth
"""


    email_sent = send_email(
        email,
        subject,
        body
    )


    # ==========================================
    # RESPONSE TO FRONTEND
    # ==========================================

    if email_sent:

        return jsonify({
            "success": True,
            "message": (
                "Request recorded successfully. "
                "Email notification sent."
            ),
            "request_id": request_id,
            "email_sent": True
        })

    else:

        return jsonify({
            "success": True,
            "message": (
                "Request recorded successfully, "
                "but email notification failed."
            ),
            "request_id": request_id,
            "email_sent": False
        })


# ==========================================
# ADMIN PAGE
# ==========================================

@app.route("/admin")
def admin():

    return render_template("admin.html")


# ==========================================
# GET ALL REQUESTS
# ==========================================

@app.route("/admin/requests")
def get_requests():

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            name,
            age,
            location,
            email,
            grievance,
            submitted_at,
            status
        FROM requests
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()


    requests = []


    for row in rows:

        requests.append({

            "id": row["id"],

            "name": row["name"],

            "age": row["age"],

            "location": row["location"],

            "email": row["email"],

            "grievance": row["grievance"],

            "submitted_at": row["submitted_at"],

            "status": row["status"]

        })


    return jsonify({

        "success": True,

        "requests": requests

    })


# ==========================================
# UPDATE REQUEST STATUS
# ==========================================

@app.route("/update-status", methods=["POST"])
def update_status():

    data = request.get_json()


    if not data:

        return jsonify({
            "success": False,
            "message": "No update data received."
        }), 400


    request_id = data.get("id")

    new_status = data.get("status")


    # ==========================================
    # ALLOWED STATUSES
    # ==========================================

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]


    if new_status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid status."
        }), 400


    # ==========================================
    # FIND REQUEST
    # ==========================================

    connection = get_db_connection()


    existing_request = connection.execute(
        """
        SELECT *
        FROM requests
        WHERE id = ?
        """,
        (request_id,)
    ).fetchone()


    if existing_request is None:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Request not found."
        }), 404


    old_status = existing_request["status"]


    # ==========================================
    # DON'T UPDATE IF STATUS IS SAME
    # ==========================================

    if old_status == new_status:

        connection.close()

        return jsonify({
            "success": True,
            "message": "Status is already set to this value.",
            "status_changed": False,
            "email_sent": False
        })


    # ==========================================
    # UPDATE DATABASE
    # ==========================================

    connection.execute(
        """
        UPDATE requests
        SET status = ?
        WHERE id = ?
        """,
        (
            new_status,
            request_id
        )
    )


    connection.commit()

    connection.close()


    # ==========================================
    # USER INFORMATION
    # ==========================================

    user_email = existing_request["email"]

    user_name = existing_request["name"]

    grievance = existing_request["grievance"]


    # ==========================================
    # CREATE STATUS EMAIL
    # ==========================================

    if new_status == "In Progress":

        subject = (
            f"Super Yodha — Request #{request_id} Status Update"
        )


        body = f"""
Hello {user_name},

Your Super Yodha help request has been updated.

Request ID: #{request_id}

Previous Status: {old_status}
New Status: {new_status}

Your request is currently being reviewed by the Guardian Assistance System.

Grievance:
{grievance}

Regards,
SUPER YODHA
Guardian of Earth
"""


    elif new_status == "Resolved":

        subject = (
            f"Super Yodha — Request #{request_id} Resolved"
        )


        body = f"""
Hello {user_name},

Your Super Yodha help request has been resolved.

Request ID: #{request_id}

Previous Status: {old_status}
New Status: {new_status}

Grievance:
{grievance}

Thank you for contacting the Super Yodha Guardian Assistance System.

Regards,
SUPER YODHA
Guardian of Earth
"""


    else:

        subject = (
            f"Super Yodha — Request #{request_id} Status Update"
        )


        body = f"""
Hello {user_name},

Your Super Yodha help request status has been updated.

Request ID: #{request_id}

Previous Status: {old_status}
New Status: {new_status}

Regards,
SUPER YODHA
Guardian of Earth
"""


    # ==========================================
    # SEND STATUS EMAIL
    # ==========================================

    email_sent = send_email(
        user_email,
        subject,
        body
    )


    # ==========================================
    # RESPONSE
    # ==========================================

    return jsonify({

        "success": True,

        "message": "Request status updated successfully.",

        "status_changed": True,

        "old_status": old_status,

        "new_status": new_status,

        "email_sent": email_sent

    })


# ==========================================
# START APPLICATION
# ==========================================

init_database()

if __name__ == "__main__":
    app.run(debug=True)