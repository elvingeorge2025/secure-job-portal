import re
from email_validator import validate_email as ev_validate, EmailNotValidError
from config import Config


def sanitize_email(email: str) -> str:
    return email.strip().lower()


def validate_registration(data):
    errors = []

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")

    if not name:
        errors.append("Name is required.")
    if not email:
        errors.append("Email is required.")
    else:
        try:
            ev_validate(email)
        except EmailNotValidError:
            errors.append("Invalid email address.")

    if len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain an uppercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain a number.")
    if password != confirm_password:
        errors.append("Passwords do not match.")

    return errors


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS
