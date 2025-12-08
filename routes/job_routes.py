from flask import Blueprint, render_template, request
from models.job_model import search_jobs, get_job_by_id

job_bp = Blueprint("job", __name__, url_prefix="/jobs")


@job_bp.route("/")
def jobs_list():
    q = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    category = request.args.get("category", "").strip()

    jobs = search_jobs(q=q, location=location, category=category)
    return render_template("jobs/jobs_list.html", jobs=jobs)


@job_bp.route("/<int:job_id>")
def job_detail(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return ("Job not found", 404)
    return render_template("jobs/job_detail.html", job=job)
