# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from firebaseConfig import db  # Import Firestore client from firebaseConfig.py
import firebase_admin
from firebase_admin import auth
from functools import wraps
import os
from firebase_admin import firestore

from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key")  # Use environment variable for secret key
CORS(app)  # Enable CORS

def verify_firebase_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            logger.warning("Missing Authorization Header")
            return jsonify({"status": "failed", "message": "Missing Authorization Header"}), 401

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise ValueError("Invalid token type")
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
            logger.info(f"Authenticated user UID: {request.user['uid']}")
        except Exception as e:
            logger.error(f"Invalid token: {e}")
            return jsonify({"status": "failed", "message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    return redirect(url_for('signup_page'))

@app.route("/signup", methods=["GET"])
def signup_page():
    logger.info("Rendering signup page.")
    return render_template("signup.html")

@app.route("/api/signup", methods=["POST"])
@verify_firebase_token
def signup_api():
    data = request.json
    logger.info(f"Received signup data: {data}")

    # Extract data from the request
    name = data.get("name")
    email = data.get("email")
    degreeID = data.get("degreeID")

    # Validate input
    if not all([name, email, degreeID]):
        logger.warning("Missing required fields in signup data.")
        return jsonify({"status": "failed", "message": "Missing required fields"}), 400

    try:
        # Check if the provided degreeID exists in the 'degrees' collection
        degree_ref = db.collection("degrees").document(str(degreeID))
        degree_doc = degree_ref.get()

        if not degree_doc.exists:
            logger.warning(f"Invalid degreeID: {degreeID}")
            return jsonify({"status": "failed", "message": "Invalid degreeID"}), 400

        # Get user UID from the token
        uid = request.user['uid']
        logger.info(f"Creating student record for UID: {uid}")

        # Prepare student data
        student_data = {
            "studentID": uid,
            "name": name,
            "email": email,
            "degreeID": int(degreeID),
            "enrollmentDate": firestore.SERVER_TIMESTAMP,
            "status": "pending"
        }

        # Add the student record to Firestore
        db.collection("students").document(uid).set(student_data)
        logger.info(f"Student record created for UID: {uid}")

        return jsonify({
            "status": "success",
            "message": "User created successfully",
            "studentID": uid
        }), 200

    except Exception as e:
        logger.error(f"Error during signup: {e}")
        return jsonify({"status": "failed", "message": "Internal server error"}), 500

@app.route("/login", methods=["GET"])
def login_page():
    logger.info("Rendering login page.")
    return render_template("login.html")

@app.route("/admin", methods=["GET"])
def admin_dashboard():
    # Serve the admin dashboard without authentication
    logger.info("Rendering admin dashboard.")
    return render_template("admin_dashboard.html")


@app.route("/get_students", methods=["GET"])
@verify_firebase_token
def get_students():
    user = request.user
    if not user.get('admin'):
        logger.warning(f"Unauthorized access attempt by UID: {user['uid']}")
        return jsonify({"status": "failed", "message": "Unauthorized access"}), 403

    try:
        students_ref = db.collection("students")
        students = students_ref.stream()

        students_list = []
        for student in students:
            student_data = student.to_dict()
            if student_data.get("enrollmentDate"):
                student_data["enrollmentDate"] = student_data["enrollmentDate"].timestamp()
            students_list.append(student_data)

        logger.info("Fetched students list successfully.")
        return jsonify({
            "status": "success",
            "students": students_list
        }), 200

    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        return jsonify({"status": "failed", "message": "Internal server error"}), 500

@app.route("/update_status/<student_id>", methods=["POST"])
@verify_firebase_token
def update_status(student_id):
    user = request.user
    if not user.get('admin'):
        logger.warning(f"Unauthorized status update attempt by UID: {user['uid']}")
        return jsonify({"status": "failed", "message": "Unauthorized access"}), 403

    data = request.json
    new_status = data.get("status")

    if new_status not in ['pending', 'approved', 'declined']:
        logger.warning(f"Invalid status value received: {new_status}")
        return jsonify({"status": "failed", "message": "Invalid status value"}), 400

    try:
        student_ref = db.collection("students").document(student_id)
        student_doc = student_ref.get()

        if not student_doc.exists:
            logger.warning(f"Student not found: {student_id}")
            return jsonify({"status": "failed", "message": "Student not found"}), 404

        student_ref.update({"status": new_status})
        logger.info(f"Updated status for student {student_id} to {new_status}")

        return jsonify({"status": "success", "message": "Status updated successfully"}), 200

    except Exception as e:
        logger.error(f"Error updating status for student {student_id}: {e}")
        return jsonify({"status": "failed", "message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
