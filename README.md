# Cloud-Based Code Compilation and Execution Platform

Flask web app where users write code in Python, JavaScript, C or C++ and run it in the browser.

## Run locally
    pip install -r requirements.txt
    python app.py        # http://localhost:5000

## Environment variables
- `SECRET_KEY` - random secret for sessions
- `ADMIN_PASSWORD` - password for the seeded `admin` user
- `DATABASE_URL` - optional (Postgres/MySQL); defaults to local SQLite
