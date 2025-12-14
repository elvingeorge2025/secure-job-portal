USE secure_job_portal;

-- Default admin (password will be set via the app; placeholder hash)
INSERT INTO users (name, email, password_hash, role)
VALUES ('Admin User', 'admin@example.com', '$2b$12$changemechangemechangemech', 'admin')
ON DUPLICATE KEY UPDATE email=email;

INSERT INTO jobs (title, description, requirements, salary, location, category, status)
VALUES
('Junior Security Analyst', 'Assist in security monitoring and incident handling.', 'Basic networking, Linux, interest in security.', '€35,000', 'Dublin', 'Security', 'active'),
('Full Stack Developer', 'Develop and maintain web applications.', 'Python, Flask, MySQL, HTML/CSS/JS.', '€45,000', 'Remote', 'Software Development', 'active'),
('Cybersecurity Intern', 'Assist senior analysts with threat detection and basic investigations.', 'Knowledge of networking basics, willingness to learn, Python basics.', '€28,000', 'Cork', 'Security', 'active'),
('Backend Python Developer', 'Build and maintain backend services and APIs.', 'Python, Flask/Django, SQL, REST APIs.', '€55,000', 'Dublin', 'Software Development', 'active'),
('Front-End Developer', 'Create responsive UI components and improve UX.', 'HTML, CSS, JavaScript, React preferred.', '€42,000', 'Galway', 'Web Development', 'active'),
('DevOps Engineer', 'Manage CI/CD pipelines and cloud infrastructure.', 'Docker, Kubernetes, AWS/GCP, Linux.', '€65,000', 'Remote', 'DevOps', 'active'),
('IT Support Specialist', 'Provide hardware and software support for employees.', 'Troubleshooting, Windows/Linux, communication skills.', '€32,000', 'Limerick', 'IT Support', 'active'),
('Data Analyst', 'Analyze datasets to generate insights and dashboards.', 'SQL, Excel, Python, Power BI/Tableau.', '€50,000', 'Dublin', 'Data', 'active'),
('QA Automation Engineer', 'Write automated test scripts and improve testing frameworks.', 'Selenium, Python/Java, attention to detail.', '€48,000', 'Remote', 'Quality Assurance', 'active'),
('Cloud Solutions Architect', 'Design scalable cloud-based systems for clients.', 'AWS/Azure, networking, architecture experience.', '€80,000', 'Dublin', 'Cloud', 'active'),
('Network Administrator', 'Manage corporate network, firewalls, and VPN.', 'Cisco, TCP/IP, Routing and Switching.', '€46,000', 'Cork', 'Networking', 'active'),
('Machine Learning Engineer', 'Build and deploy ML models for production use.', 'Python, ML frameworks, data preprocessing.', '€70,000', 'Remote', 'AI/ML', 'active');
