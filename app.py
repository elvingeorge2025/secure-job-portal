from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect, generate_csrf

from config import Config
from routes.auth_routes import auth_bp
from routes.job_routes import job_bp
from routes.applicant_routes import applicant_bp
from routes.admin_routes import admin_bp
from security.csrf_protection import init_csrf
from models.utils import init_db


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # Init DB (for MySQL this may just validate connection)
    init_db(app)

    # CSRF protection
    csrf = CSRFProtect()
    init_csrf(csrf, app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(applicant_bp)
    app.register_blueprint(admin_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    # CSRF token for templates
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
