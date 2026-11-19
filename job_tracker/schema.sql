DROP DATABASE IF EXISTS job_tracker;
CREATE DATABASE job_tracker;
USE job_tracker;

DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS companies;

CREATE TABLE companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    notes TEXT
);

CREATE TABLE jobs (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    job_type ENUM('Full-time', 'Part-time', 'Contract', 'Internship'),
    salary_min INT,
    salary_max INT,
    job_url VARCHAR(300),
    date_posted DATE,
    requirements JSON,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    job_id INT NOT NULL,
    application_date DATE NOT NULL,
    status ENUM('Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn') DEFAULT 'Applied',
    resume_version VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data JSON,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

CREATE TABLE contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE INDEX idx_job_title ON jobs(job_title);
CREATE INDEX idx_app_status ON applications(status);
CREATE INDEX idx_company_industry ON companies(industry);

INSERT INTO companies (company_name, industry, website, city, state) VALUES
('Tech Solutions Inc', 'Technology', 'www.techsolutions.com', 'Miami', 'Florida'),
('Data Analytics Corp', 'Data Science', 'www.dataanalytics.com', 'Austin', 'Texas'),
('Cloud Systems LLC', 'Cloud Computing', 'www.cloudsystems.com', 'Seattle', 'Washington'),
('Digital Innovations', 'Software', 'www.digitalinnovations.com', 'San Francisco', 'California'),
('Smart Tech Group', 'AI/ML', 'www.smarttech.com', 'Boston', 'Massachusetts');

INSERT INTO jobs (company_id, job_title, salary_min, salary_max, job_type, date_posted, requirements) VALUES
(1, 'Software Developer', 70000, 90000, 'Full-time', '2025-01-15', '["Python", "SQL", "Git"]'),
(1, 'Database Administrator', 75000, 95000, 'Full-time', '2025-01-10', NULL),
(2, 'Data Analyst', 65000, 85000, 'Full-time', '2025-01-12', '["SQL", "Excel", "Tableau"]'),
(3, 'Cloud Engineer', 80000, 100000, 'Full-time', '2025-01-08', NULL),
(4, 'Junior Developer', 55000, 70000, 'Full-time', '2025-01-14', NULL),
(4, 'Senior Developer', 95000, 120000, 'Full-time', '2025-01-14', NULL),
(5, 'ML Engineer', 90000, 115000, 'Full-time', '2025-01-11', NULL);

INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data) VALUES
(1, '2025-01-16', 'Applied', 'v2.1', TRUE, NULL),
(3, '2025-01-13', 'Interview', 'v2.1', TRUE, '{"interview_rounds": 2, "interviewers": ["Sarah Johnson", "Mike Chen"], "technical_questions": ["SQL joins", "Python basics", "API design"], "feedback": "Strong technical skills, good communication", "next_steps": "Final round scheduled"}'),
(4, '2025-01-09', 'Rejected', 'v2.0', FALSE, NULL),
(5, '2025-01-15', 'Applied', 'v2.1', TRUE, NULL),
(7, '2025-01-12', 'Screening', 'v2.1', TRUE, '{"interview_rounds": 1, "interviewers": ["Emily Williams"], "technical_questions": ["Database normalization", "Transaction isolation"], "feedback": "Needs more experience with cloud platforms", "rating": 3}');

INSERT INTO contacts (company_id, contact_name, email, title) VALUES
(1, 'Sarah Johnson', 'sjohnson@techsolutions.com', 'HR Manager'),
(2, 'Michael Chen', 'mchen@dataanalytics.com', 'Technical Recruiter'),
(3, 'Emily Williams', 'ewilliams@cloudsystems.com', 'Hiring Manager'),
(4, 'David Brown', NULL, 'Senior Developer'),
(5, 'Lisa Garcia', 'lgarcia@smarttech.com', 'Talent Acquisition');