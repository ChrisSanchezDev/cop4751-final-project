# AI Usage Documentation

## Tools Used

- Copilot SDK in VS Code for application design, Flask routes, MySQL queries,
  Jinja templates, CSS, documentation, and debugging.

## Key Prompts

1. "Teach me how to add Flask routes in app.py that connect the existing Python database helpers
   to the companies, jobs, applications, and contacts tables."
2. "How do I build the Applications page with forms for application status, resume
   version, cover letters, and interview information."
3. "Guide me for implementing a Job Match page that compares user skills with JSON job
   requirements and displays matched and missing skills."
4. "Help create the HTML and CSS for the pages, though please consider I already have a good amount of backend knowledge in Python and C#, if you can integrate that in my assistance please."
5. "Can you please help me create a README.md based on the information of this project?"

## What Worked Well

- AI helped me connect Flask route logic in app.py with parameterized SQL queries
  and the existing database.py helper functions.
- AI-suggested SQL joins and Flask route patterns combined with my own additions provided a useful starting
  point for the CRUD pages, especially Applications and Job Match.
- AI helped create Bootstrap HTML and custom CSS for pages that required more
  frontend work than I normally do as a backend-focused developer.
- It caught template and route issues before changes were staged.
- It quickly helped me create a good README.md that was well formatted.

## What I Modified

- Adapted generated app.py routes and queries to the project's exact table and
  column names.
- Kept the four-table MySQL schema required by the specification.
- Added validation for required fields, salary ranges, JSON-backed data, and
  interview ratings.
- Changed job requirements to use comma-separated user input while continuing
  to store a JSON array.
- Replaced raw interview JSON entry with structured fields that Flask converts
  into a JSON object.
- Added representative sample URLs, phone numbers, and contact notes.
- Adjusted the HTML and CSS to match the application's data and improve
  usability.
- Reviewed and staged changes incrementally rather than accepting a complete
  generated section or file all at once.

## Lessons Learned

- AI-generated code still needs to be tested against the actual schema and
  templates.
- Python route code and SQL queries must be checked together because a correct
  query still needs to match the data passed into the template.
- JSON columns can preserve flexible data while structured forms make the
  application easier to use.
- Small, focused commits make it easier to review changes and identify
  regressions.
- Clear prompts that include the existing file structure produce more useful
  implementation results, especially when asking for frontend help.
