"""
Scheme Sarthi - Flask Web Application with Per-User Email Storage & Authentication
Each user logs in with their Email & Password. Saved applications are strictly isolated per Email account.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import datetime
import random
import werkzeug.security as security
from gap_engine import analyze_user_gaps
from ml_engine import rf_engine, SCHEMES

app = Flask(__name__)
app.secret_key = "scheme_sarthi_auth_key_2026"

# In-memory storage for User Accounts & Per-Email Application Logs
# USERS_DB: { 'email': { 'name': '...', 'email': '...', 'password_hash': '...', 'state': '...', 'category': '...' } }
USERS_DB = {}

# SAVED_APPLICATIONS_DB: { 'app_id': { 'app_id': '...', 'user_email': 'email', 'scheme_name': '...', 'portal_name': '...', 'official_arn': '...', 'status': '...', 'notes': '...', 'created_at': '...' } }
SAVED_APPLICATIONS_DB = {}

STATES_LIST = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi (UT)", "Jammu & Kashmir (UT)"
]


@app.context_processor
def inject_user():
    user_email = session.get("user_email")
    user = USERS_DB.get(user_email) if user_email else None
    return dict(current_user=user)


@app.route("/")
def index():
    """Landing Page"""
    return render_template("index.html", total_schemes=len(SCHEMES))


# --- USER AUTHENTICATION ROUTES (REGISTER & LOGIN BY EMAIL) ---

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register Account by Email"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        state = request.form.get("state", "Karnataka")
        category = request.form.get("category", "General")

        if not email or not password or not name:
            flash("Please fill in your name, email, and password.", "danger")
            return render_template("register.html", states=STATES_LIST)

        if email in USERS_DB:
            flash(f"Account for '{email}' already exists. Please log in.", "warning")
            return redirect(url_for("login"))

        hashed_pw = security.generate_password_hash(password)
        USERS_DB[email] = {
            "name": name,
            "email": email,
            "password_hash": hashed_pw,
            "state": state,
            "category": category,
            "joined_date": datetime.date.today().strftime("%Y-%m-%d")
        }

        # Auto-login newly registered email session
        session["user_email"] = email
        flash(f"Welcome {name}! Your account ({email}) is created.", "success")
        return redirect(url_for("tracker"))

    return render_template("register.html", states=STATES_LIST)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in by Email and Password"""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = USERS_DB.get(email)
        if user and security.check_password_hash(user["password_hash"], password):
            session["user_email"] = email
            flash(f"Logged in successfully as {user['name']} ({email}).", "success")
            return redirect(url_for("tracker"))
        else:
            flash("Invalid email address or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout current user session"""
    email = session.pop("user_email", None)
    flash(f"Logged out from account ({email}).", "info")
    return redirect(url_for("login"))


# --- SCHEME ANALYZER & RESULTS ROUTES ---

@app.route("/analyzer", methods=["GET", "POST"])
def analyzer():
    """Form Input Page & Analysis Trigger"""
    if request.method == "POST":
        user_profile = {
            "age": request.form.get("age", 20, type=int),
            "income": request.form.get("income", 180000, type=float),
            "state": request.form.get("state", "Karnataka"),
            "district": request.form.get("district", "Bangalore Urban"),
            "category": request.form.get("category", "General"),
            "student_status": request.form.get("student_status", "Student"),
            "is_student": request.form.get("student_status") == "Student",
            "education": request.form.get("education", "12th Pass"),
            "is_disabled": request.form.get("is_disabled") == "yes",
            "disability_pct": request.form.get("disability_pct", 0, type=float),
            "gender": request.form.get("gender", "Male"),
            "occupation": request.form.get("occupation", "Student"),
            "area_type": request.form.get("area_type", "Urban"),
            "family_dependents": request.form.get("family_dependents", 4, type=int),
            "has_existing_benefits": request.form.get("has_existing_benefits") == "yes"
        }

        session["user_profile"] = user_profile
        return redirect(url_for("results"))

    user_email = session.get("user_email")
    default_state = "Karnataka"
    default_category = "OBC"
    if user_email and user_email in USERS_DB:
        default_state = USERS_DB[user_email]["state"]
        default_category = USERS_DB[user_email]["category"]

    return render_template("analyzer.html", states=STATES_LIST, default_state=default_state, default_category=default_category)


@app.route("/results")
def results():
    """Analysis Results & Action Planner Dashboard"""
    user_profile = session.get("user_profile")
    if not user_profile:
        user_profile = {
            "age": 20,
            "income": 180000,
            "state": "Karnataka",
            "district": "Bangalore Urban",
            "category": "OBC",
            "student_status": "Student",
            "is_student": True,
            "education": "12th Pass",
            "is_disabled": False,
            "disability_pct": 0,
            "gender": "Male",
            "occupation": "Student",
            "area_type": "Rural",
            "family_dependents": 4,
            "has_existing_benefits": False
        }

    analysis_data = analyze_user_gaps(user_profile)
    return render_template("results.html", data=analysis_data)


# --- PERSONAL APPLICATION LOG (PER-EMAIL ISOLATED STORAGE) ---

@app.route("/tracker")
def tracker():
    """Personal Saved Applications Dashboard per Email Account"""
    user_email = session.get("user_email")
    if not user_email or user_email not in USERS_DB:
        flash("Please log in with your email address to view your personal application log.", "warning")
        return redirect(url_for("login"))

    # Strictly filter saved applications for logged-in user's email
    user_apps = [
        app_item for app_item in SAVED_APPLICATIONS_DB.values()
        if app_item.get("user_email") == user_email
    ]

    user_apps.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return render_template("tracker.html", my_apps=user_apps, user_email=user_email)


@app.route("/api/save_application", methods=["POST"])
def save_application():
    """Saves a scheme to logged-in user's email account"""
    user_email = session.get("user_email")
    if not user_email or user_email not in USERS_DB:
        return jsonify({"success": False, "message": "Please log in with your email to save schemes to your account."}), 401

    data = request.json or {}
    scheme_name = data.get("scheme_name", "Government Scheme")
    portal_name = data.get("portal_name", "Official Portal")
    official_arn = data.get("official_arn", "").strip().upper()
    status = data.get("status", "In Preparation")
    notes = data.get("notes", "").strip()

    app_id = f"APP-LOG-{random.randint(10000, 99999)}"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")

    SAVED_APPLICATIONS_DB[app_id] = {
        "app_id": app_id,
        "user_email": user_email,
        "scheme_name": scheme_name,
        "portal_name": portal_name,
        "official_arn": official_arn if official_arn else "Not Entered",
        "status": status,
        "notes": notes if notes else "No personal notes added.",
        "created_at": now_str,
        "last_updated": now_str
    }

    return jsonify({"success": True, "app_id": app_id, "user_email": user_email, "message": f"Scheme saved to account ({user_email})!"})


@app.route("/api/delete_application/<app_id>", methods=["DELETE"])
def delete_application(app_id):
    """Deletes an entry from user's email account log"""
    user_email = session.get("user_email")
    if not user_email:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    if app_id in SAVED_APPLICATIONS_DB and SAVED_APPLICATIONS_DB[app_id]["user_email"] == user_email:
        del SAVED_APPLICATIONS_DB[app_id]
        return jsonify({"success": True, "message": "Entry removed from your account log."})

    return jsonify({"success": False, "message": "Item not found or unauthorized."}), 404


if __name__ == "__main__":
    print("Starting Scheme Sarthi Application on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
