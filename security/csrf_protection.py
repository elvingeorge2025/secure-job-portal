def init_csrf(csrf, app):
    """
    Initialize Flask-WTF CSRF protection.
    All POST, PUT, DELETE will require valid CSRF token.
    """
    csrf.init_app(app)
