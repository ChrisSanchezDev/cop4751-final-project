from flask import Flask, render_template, request, redirect, url_for, flash
from database import query_all, query_one, execute_write

app = Flask(__name__)
app.secret_key = 'cop4751_job_tracker_secret_key'

@app.route('/')
def dashboard():
    company_count = query_one('SELECT COUNT(*) AS count FROM companies')['count']
    job_count = query_one('SELECT COUNT(*) AS count FROM jobs')['count']
    app_count = query_one('SELECT COUNT(*) AS count FROM applications')['count']
    contact_count = query_one('SELECT COUNT(*) AS count FROM contacts')['count']

    status_breakdown = query_all('''
        SELECT status, COUNT(*) AS count
        FROM applications
        GROUP BY status
        ORDER BY count DESC
    ''')

    recent_applications = query_all('''
        SELECT a.application_id, c.company_name, j.job_title, a.application_date, a.status
        FROM applications a
        INNER JOIN jobs j ON a.job_id = j.job_id
        INNER JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
        LIMIT 5
    ''')

    return render_template(
        'dashboard.html',
        company_count=company_count,
        job_count=job_count,
        app_count=app_count,
        contact_count=contact_count,
        status_breakdown=status_breakdown,
        recent_applications=recent_applications
    )

@app.route('/companies')
def companies():
    return 'Companies page coming next!'

@app.route('/jobs')
def jobs():
    return 'Jobs page coming next!'

@app.route('/applications')
def applications():
    return 'Applications page coming next!'

@app.route('/contacts')
def contacts():
    return 'Contacts page coming next!'

@app.route('/job-match')
def job_match():
    return 'Job Match page coming next!'

if __name__ == '__main__':
    app.run(debug=True)