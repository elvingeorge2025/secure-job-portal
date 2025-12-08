
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date

from security.access_control import login_required, role_required
from models.job_model import (
    create_job,
    get_job_by_id,
    update_job,
    delete_job,
    get_jobs_with_counts,
)
from models.application_model import (
    get_applications_for_job,
    get_application_with_user_and_job,
    get_stats,
)
from models.utils import log_action

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    stats = get_stats()
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route("/jobs/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_job():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        requirements = request.form.get("requirements", "").strip()
        salary = request.form.get("salary", "").strip()
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "").strip()

        if not title or not description:
            flash("Title and description are required", "danger")
            return render_template("admin/create_job.html")

        create_job(
            title=title,
            description=description,
            requirements=requirements,
            salary=salary,
            location=location,
            category=category,
            created_by=session["user_id"],
        )

        log_action(session["user_id"], "create_job", f"Job created: {title}", request.remote_addr)
        flash("Job created successfully", "success")
        return redirect(url_for("admin.manage_jobs"))

    return render_template("admin/create_job.html")


@admin_bp.route("/jobs")
@login_required
@role_required("admin")
def manage_jobs():
    jobs = get_jobs_with_counts()
    return render_template("admin/manage_jobs.html", jobs=jobs)


@admin_bp.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_job(job_id):
    job = get_job_by_id(job_id)
    if not job:
        flash("Job not found", "danger")
        return redirect(url_for("admin.manage_jobs"))

    if request.method == "POST":
        data = {
            "title": request.form.get("title", "").strip(),
            "description": request.form.get("description", "").strip(),
            "requirements": request.form.get("requirements", "").strip(),
            "salary": request.form.get("salary", "").strip(),
            "location": request.form.get("location", "").strip(),
            "category": request.form.get("category", "").strip(),
            "status": request.form.get("status", "active"),
        }

        update_job(job_id, **data)
        log_action(session["user_id"], "edit_job", f"Job updated: {job_id}", request.remote_addr)
        flash("Job updated successfully", "success")
        return redirect(url_for("admin.manage_jobs"))

    return render_template("admin/edit_job.html", job=job)


@admin_bp.route("/jobs/<int:job_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_job(job_id):
    delete_job(job_id)
    log_action(session["user_id"], "delete_job", f"Job deleted: {job_id}", request.remote_addr)
    flash("Job deleted", "info")
    return redirect(url_for("admin.manage_jobs"))


@admin_bp.route("/jobs/<int:job_id>/applicants")
@login_required
@role_required("admin")
def view_applicants(job_id):
    applications = get_applications_for_job(job_id)
    job = get_job_by_id(job_id)
    if not job:
        flash("Job not found", "danger")
        return redirect(url_for("admin.manage_jobs"))
    return render_template("admin/view_applicants.html", job=job, applications=applications)


@admin_bp.route("/applications/<int:application_id>")
@login_required
@role_required("admin")
def applicant_details(application_id):
    app = get_application_with_user_and_job(application_id)
    if not app:
        flash("Application not found", "danger")
        return redirect(url_for("admin.manage_jobs"))
    return render_template("admin/applicant_details.html", application=app)
