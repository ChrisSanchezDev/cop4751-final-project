# cop4751-final-project
Chris Sanchez's Final Project for COP4751: Adv DB Management.

## Job Tracker

This Flask application manages companies, job postings, applications, and professional contacts
using MySQL. The job matcher ranks saved postings against a comma-separated list of user skills.

### Running locally

1. Create the `job_tracker` MySQL database by running [`schema.sql`](schema.sql).
2. Set the MySQL connection values in [`database.py`](database.py).
3. Install dependencies with `pip install -r requirements.txt`.
4. Start the application with `python app.py`.
