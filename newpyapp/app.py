# =========================
# IMPORTS
# =========================
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================
load_dotenv()

app = Flask(__name__)

# =========================
# BASIC CONFIG
# =========================
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

# =========================
# DATABASE CONFIG
# =========================
DB_USER = os.getenv("DB_USER", "flaskuser")
DB_PASS = os.getenv("DB_PASSWORD", "flaskpass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "login_db")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# LOGIN MANAGER
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


# =========================
# USER MODEL
# =========================
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():

    stats = {
        "clients": 120,
        "projects": 45,
        "experience": 8,
    }

    projects = [
        {
            "image": "site1.jpeg",
            "title": "Residential Foundation",
            "desc": "Excavation planning and RCC footing execution with structural safety.",
        },
        {
            "image": "site2.jpeg",
            "title": "Column & Beam Work",
            "desc": "Alignment inspection and reinforcement verification.",
        },
        {
            "image": "site3.jpeg",
            "title": "Concrete Pouring",
            "desc": "Concrete ratio monitoring and vibration quality control.",
        },
        {
            "image": "site4.jpeg",
            "title": "Site Supervision",
            "desc": "Daily inspection ensuring safety and construction standards.",
        },
        {
            "image": "site5.jpeg",
            "title": "Finishing Work",
            "desc": "Final quality checks and structural compliance validation.",
        },
    ]

    return render_template("home.html", stats=stats, projects=projects)


# =========================
# ABOUT PAGE
# =========================
@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# CONTACT PAGE
# =========================
@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")

        # validation
        if not name or not email or not password:
            flash("Please fill required fields", "danger")
            return redirect(url_for("register"))

        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash("Email already registered", "warning")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            address=address,
            phone=phone,
            email=email,
            password=hashed_password,
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))


# =========================
# CREATE TABLES
# =========================
with app.app_context():
    db.create_all()


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
