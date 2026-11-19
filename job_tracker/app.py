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