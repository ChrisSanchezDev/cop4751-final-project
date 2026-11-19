# Job Application Tracker - COP4751 Course Project

A full-stack database application for tracking job applications, companies, job
postings, professional contacts, and skill-based job matching.

This project uses **Python 3 with Flask**, **MySQL**, **HTML/CSS**, and
**Bootstrap 5**. It was created for COP4751 Advanced Database Management and
demonstrates CRUD operations, relational joins, MySQL JSON columns, validation,
and Git-based incremental development.

## Features

- **Dashboard**: View company, job, application, and contact counts, application
  status totals, and recent applications.
- **Companies**: Add, list, edit, and delete companies.
- **Jobs**: Add, list, edit, and delete job postings linked to companies.
  Supports salary ranges, optional job URLs, dates, and JSON skill requirements.
- **Applications**: Track application dates, statuses, resume versions, cover
  letters, and structured interview information stored as JSON.
- **Contacts**: Manage recruiters and other company contacts.
- **Job Match**: Enter comma-separated skills and rank jobs by skill match
  percentage, including matched and missing skills.

## Project Structure

```text
job_tracker/
├── app.py                 # Flask application and route handlers
├── database.py            # MySQL connection and query helper functions
├── schema.sql             # Database creation, indexes, and sample data
├── requirements.txt       # Python dependencies
├── AI_USAGE.md            # GenAI usage documentation
├── README.md              # Project overview and setup instructions
├── static/
│   └── style.css          # Custom styling
└── templates/
    ├── base.html          # Shared navigation and page layout
    ├── dashboard.html     # Dashboard overview
    ├── companies.html     # Company CRUD page
    ├── jobs.html          # Job posting CRUD page
    ├── applications.html  # Application CRUD page
    ├── contacts.html      # Contact CRUD page
    └── job_match.html     # Job skill matching page
```

## Setup and Installation

### 1. Create the database

Open MySQL Workbench or a MySQL client and run [`schema.sql`](schema.sql).
The script creates the `job_tracker` database, tables, indexes, and sample
records.

### 2. Configure MySQL

Open [`database.py`](database.py) and update the `DB_CONFIG` values for the
local MySQL installation:

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',
    'database': 'job_tracker'
}
```

### 3. Install dependencies

From the project directory, run:

```bash
pip install -r requirements.txt
```

### 4. Run the application

Start the Flask development server:

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

## Database Design

The application uses four related tables:

- `companies`
- `jobs`
- `applications`
- `contacts`

Foreign keys connect jobs to companies, applications to jobs, and contacts to
companies. The `jobs.requirements` and `applications.interview_data` columns
use MySQL JSON to store flexible, semi-structured information.
