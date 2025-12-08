from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import get_user_by_email, create_user
from security.password_utils import verify_password
from security.validators import validate_registration, sanitize_email
from models.utils import log_action

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = sanitize_email(request.form.get("email", ""))
        password = request.form.get("password", "")

        user = get_user_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            flash("Invalid email or password", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["role"] = user["role"]

        log_action(user["id"], "login", "User logged in", request.remote_addr)
        flash("Logged in successfully", "success")

        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("applicant.dashboard"))

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "email": sanitize_email(request.form.get("email", "")),
            "phone": request.form.get("phone", "").strip(),
            "password": request.form.get("password", ""),
            "confirm_password": request.form.get("confirm_password", ""),
        }

        errors = validate_registration(data)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("register.html")

        user_id = create_user(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            password=data["password"],
            role="applicant",
        )
        log_action(user_id, "register", "New account created", request.remote_addr)
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    user_id = session.get("user_id")
    session.clear()
    if user_id:
        log_action(user_id, "logout", "User logged out", request.remote_addr)
    flash("Logged out successfully", "info")
    return redirect(url_for("home"))
