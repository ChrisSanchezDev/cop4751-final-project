import json
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

@app.route('/companies', methods=['GET', 'POST'])
def companies():
    if request.method == 'POST':
        company_id = request.form.get('company_id')
        company_name = request.form.get('company_name', '').strip()
        industry = request.form.get('industry', '').strip() or None
        website = request.form.get('website', '').strip() or None
        city = request.form.get('city', '').strip() or None
        state = request.form.get('state', '').strip() or None
        notes = request.form.get('notes', '').strip() or None

        if not company_name:
            flash('Company name is required.', 'danger')
            return redirect(url_for('companies'))

        if company_id:
            execute_write('''
                UPDATE companies
                SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s
                WHERE company_id = %s
            ''', (company_name, industry, website, city, state, notes, company_id))
            flash('Company updated successfully.', 'success')
        else:
            execute_write('''
                INSERT INTO companies (company_name, industry, website, city, state, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (company_name, industry, website, city, state, notes))
            flash('Company added successfully.', 'success')

        return redirect(url_for('companies'))

    edit_id = request.args.get('edit_id')
    edit_company = None
    if edit_id:
        edit_company = query_one('SELECT * FROM companies WHERE company_id = %s', (edit_id,))

    all_companies = query_all('SELECT * FROM companies ORDER BY company_name')
    return render_template('companies.html', companies=all_companies, edit_company=edit_company)

@app.route('/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    execute_write('DELETE FROM companies WHERE company_id = %s', (company_id,))
    flash('Company deleted.', 'info')
    return redirect(url_for('companies'))

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        job_id = request.form.get('job_id')
        company_id = request.form.get('company_id')
        job_title = request.form.get('job_title', '').strip()
        job_type = request.form.get('job_type') or None
        salary_min_raw = request.form.get('salary_min', '').strip()
        salary_max_raw = request.form.get('salary_max', '').strip()
        job_url = request.form.get('job_url', '').strip() or None
        date_posted = request.form.get('date_posted', '').strip() or None
        req_input = request.form.get('requirements', '').strip()

        if not company_id or not job_title:
            flash('Company and Job Title are required.', 'danger')
            return redirect(url_for('jobs'))

        salary_min = int(salary_min_raw) if salary_min_raw.isdigit() else None
        salary_max = int(salary_max_raw) if salary_max_raw.isdigit() else None

        if salary_min is not None and salary_max is not None and salary_min > salary_max:
            flash('Minimum salary cannot be greater than maximum salary.', 'danger')
            return redirect(url_for('jobs'))

        requirements_json = None
        if req_input:
            if req_input.startswith('['):
                try:
                    parsed = json.loads(req_input)
                    if not isinstance(parsed, list):
                        flash('Requirements JSON must be an array of skills.', 'danger')
                        return redirect(url_for('jobs'))
                    requirements_json = json.dumps(parsed)
                except ValueError:
                    flash('Invalid JSON format in requirements.', 'danger')
                    return redirect(url_for('jobs'))
            else:
                skill_list = [skill.strip() for skill in req_input.split(',') if skill.strip()]
                requirements_json = json.dumps(skill_list)

        if job_id:
            execute_write('''
                UPDATE jobs
                SET company_id = %s, job_title = %s, job_type = %s, salary_min = %s,
                    salary_max = %s, job_url = %s, date_posted = %s, requirements = %s
                WHERE job_id = %s
            ''', (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements_json, job_id))
            flash('Job updated successfully.', 'success')
        else:
            execute_write('''
                INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements_json))
            flash('Job added successfully.', 'success')

        return redirect(url_for('jobs'))

    edit_id = request.args.get('edit_id')
    edit_job = None
    if edit_id:
        edit_job = query_one('SELECT * FROM jobs WHERE job_id = %s', (edit_id,))

    all_jobs = query_all('''
        SELECT j.*, c.company_name
        FROM jobs j
        INNER JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.date_posted DESC, j.job_id DESC
    ''')
    all_companies = query_all('SELECT company_id, company_name FROM companies ORDER BY company_name')
    return render_template('jobs.html', jobs=all_jobs, companies=all_companies, edit_job=edit_job)

@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    execute_write('DELETE FROM jobs WHERE job_id = %s', (job_id,))
    flash('Job deleted.', 'info')
    return redirect(url_for('jobs'))

@app.route('/applications', methods=['GET', 'POST'])
def applications():
    if request.method == 'POST':
        application_id = request.form.get('application_id')
        job_id = request.form.get('job_id')
        application_date = request.form.get('application_date', '').strip()
        status = request.form.get('status', 'Applied')
        resume_version = request.form.get('resume_version', '').strip() or None
        cover_letter_sent = request.form.get('cover_letter_sent') == 'on'
        interview_input = request.form.get('interview_data', '').strip()

        if not job_id or not application_date:
            flash('Job and Application Date are required.', 'danger')
            return redirect(url_for('applications'))

        interview_json = None
        if interview_input:
            try:
                parsed = json.loads(interview_input)
                interview_json = json.dumps(parsed)
            except ValueError:
                flash('Interview data must be valid JSON.', 'danger')
                return redirect(url_for('applications'))

        if application_id:
            execute_write('''
                UPDATE applications
                SET job_id = %s, application_date = %s, status = %s, resume_version = %s,
                    cover_letter_sent = %s, interview_data = %s
                WHERE application_id = %s
            ''', (job_id, application_date, status, resume_version, cover_letter_sent, interview_json, application_id))
            flash('Application updated successfully.', 'success')
        else:
            execute_write('''
                INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (job_id, application_date, status, resume_version, cover_letter_sent, interview_json))
            flash('Application added successfully.', 'success')

        return redirect(url_for('applications'))

    edit_id = request.args.get('edit_id')
    edit_app = None
    if edit_id:
        edit_app = query_one('SELECT * FROM applications WHERE application_id = %s', (edit_id,))

    all_applications = query_all('''
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        INNER JOIN jobs j ON a.job_id = j.job_id
        INNER JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC, a.application_id DESC
    ''')
    all_jobs = query_all('''
        SELECT j.job_id, j.job_title, c.company_name
        FROM jobs j
        INNER JOIN companies c ON j.company_id = c.company_id
        ORDER BY c.company_name, j.job_title
    ''')
    return render_template('applications.html', applications=all_applications, jobs=all_jobs, edit_app=edit_app)

@app.route('/applications/delete/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    execute_write('DELETE FROM applications WHERE application_id = %s', (application_id,))
    flash('Application deleted.', 'info')
    return redirect(url_for('applications'))

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        contact_id = request.form.get('contact_id')
        company_id = request.form.get('company_id')
        contact_name = request.form.get('contact_name', '').strip()
        title = request.form.get('title', '').strip() or None
        email = request.form.get('email', '').strip() or None
        phone = request.form.get('phone', '').strip() or None
        linkedin_url = request.form.get('linkedin_url', '').strip() or None
        notes = request.form.get('notes', '').strip() or None

        if not company_id or not contact_name:
            flash('Company and Contact Name are required.', 'danger')
            return redirect(url_for('contacts'))

        if contact_id:
            execute_write('''
                UPDATE contacts
                SET company_id = %s, contact_name = %s, title = %s, email = %s,
                    phone = %s, linkedin_url = %s, notes = %s
                WHERE contact_id = %s
            ''', (company_id, contact_name, title, email, phone, linkedin_url, notes, contact_id))
            flash('Contact updated successfully.', 'success')
        else:
            execute_write('''
                INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (company_id, contact_name, title, email, phone, linkedin_url, notes))
            flash('Contact added successfully.', 'success')

        return redirect(url_for('contacts'))

    edit_id = request.args.get('edit_id')
    edit_contact = None
    if edit_id:
        edit_contact = query_one('SELECT * FROM contacts WHERE contact_id = %s', (edit_id,))

    all_contacts = query_all('''
        SELECT ct.*, c.company_name
        FROM contacts ct
        INNER JOIN companies c ON ct.company_id = c.company_id
        ORDER BY ct.contact_name
    ''')
    all_companies = query_all('SELECT company_id, company_name FROM companies ORDER BY company_name')
    return render_template('contacts.html', contacts=all_contacts, companies=all_companies, edit_contact=edit_contact)

@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    execute_write('DELETE FROM contacts WHERE contact_id = %s', (contact_id,))
    flash('Contact deleted.', 'info')
    return redirect(url_for('contacts'))

@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    skills_input = ''
    results = []

    if request.method == 'POST':
        skills_input = request.form.get('skills', '').strip()
        user_skills = {skill.strip().lower() for skill in skills_input.split(',') if skill.strip()}

        if user_skills:
            jobs_with_reqs = query_all('''
                SELECT j.job_id, j.job_title, j.job_type, j.salary_min, j.salary_max,
                       j.requirements, c.company_name
                FROM jobs j
                INNER JOIN companies c ON j.company_id = c.company_id
                WHERE j.requirements IS NOT NULL
            ''')

            for job in jobs_with_reqs:
                try:
                    raw_requirements = json.loads(job['requirements'])
                except (TypeError, ValueError):
                    continue

                if isinstance(raw_requirements, dict):
                    job_skills = raw_requirements.get('required_skills', [])
                elif isinstance(raw_requirements, list):
                    job_skills = raw_requirements
                else:
                    job_skills = []

                job_skills = [skill for skill in job_skills if isinstance(skill, str)]
                if not job_skills:
                    continue

                matched = [skill for skill in job_skills if skill.lower() in user_skills]
                missing = [skill for skill in job_skills if skill.lower() not in user_skills]
                match_pct = round((len(matched) / len(job_skills)) * 100)

                results.append({
                    'job_title': job['job_title'],
                    'company_name': job['company_name'],
                    'job_type': job['job_type'],
                    'match_pct': match_pct,
                    'matched_count': len(matched),
                    'total_skills': len(job_skills),
                    'matched_skills': matched,
                    'missing_skills': missing
                })

            results.sort(key=lambda result: result['match_pct'], reverse=True)

    return render_template('job_match.html', skills_input=skills_input, results=results)

if __name__ == '__main__':
    app.run(debug=True)