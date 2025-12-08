from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

from security.access_control import login_required, role_required
from models.user_model import get_user_by_id, update_user_profile
from models.job_model import get_job_by_id
from models.application_model import create_application, get_applications_for_user
from models.utils import log_action, get_upload_folder
from security.validators import allowed_file

applicant_bp = Blueprint("applicant", __name__, url_prefix="/applicant")


@applicant_bp.route("/dashboard")
@login_required
@role_required("applicant")
def dashboard():
    user = get_user_by_id(session["user_id"])
    return render_template("applicant/dashboard.html", user=user)


@applicant_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("applicant")
def edit_profile():
    user = get_user_by_id(session["user_id"])
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        bio = request.form.get("bio", "").strip()

        update_user_profile(user["id"], name=name, phone=phone, bio=bio)
        log_action(user["id"], "update_profile", "Profile updated", request.remote_addr)
        flash("Profile updated successfully", "success")
        return redirect(url_for("applicant.edit_profile"))

    return render_template("applicant/edit_profile.html", user=user)


@applicant_bp.route("/apply/<int:job_id>", methods=["GET", "POST"])
@login_required
@role_required("applicant")
def apply_job(job_id):
    job = get_job_by_id(job_id)
    if not job or job["status"] != "active":
        flash("Job is not available", "danger")
        return redirect(url_for("job.jobs_list"))

    if request.method == "POST":
        if "cv" not in request.files:
            flash("CV is required", "danger")
            return render_template("applicant/apply_job.html", job=job)

        file = request.files["cv"]
        if file.filename == "":
            flash("No file selected", "danger")
            return render_template("applicant/apply_job.html", job=job)

        if not allowed_file(file.filename):
            flash("Invalid file type. Only PDF allowed.", "danger")
            return render_template("applicant/apply_job.html", job=job)

        filename = secure_filename(file.filename)
        # Add user id to prevent collisions
        filename = f"{session['user_id']}_{job_id}_{filename}"
        upload_folder = get_upload_folder()

        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        cover_letter = request.form.get("cover_letter", "").strip()

        create_application(
            user_id=session["user_id"],
            job_id=job_id,
            cv_filename=filename,
            cover_letter=cover_letter,
        )

        log_action(session["user_id"], "apply_job", f"Applied for job {job_id}", request.remote_addr)
        flash("Application submitted successfully", "success")
        return redirect(url_for("applicant.my_applications"))

    return render_template("applicant/apply_job.html", job=job)


@applicant_bp.route("/applications")
@login_required
@role_required("applicant")
def my_applications():
    apps = get_applications_for_user(session["user_id"])
    return render_template("applicant/my_applications.html", applications=apps)
