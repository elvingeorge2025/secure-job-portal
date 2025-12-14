USE secure_job_portal;

-- Default admin (password will be set via the app; placeholder hash)
INSERT INTO users (name, email, password_hash, role)
VALUES ('Admin User', 'admin@example.com', '$2b$12$changemechangemechangemech', 'admin')
ON DUPLICATE KEY UPDATE email=email;

INSERT INTO jobs (title, description, requirements, salary, location, category, status)
VALUES
