# Expense Tracker

A Django web application for tracking personal expenses, managing budgets, and organizing shared spending in one place.

## Features

- User registration and login
- Add and manage expenses
- Budget tracking
- Dashboard views for spending insights
- Shared expense support

## Tech Stack

- Python
- Django
- HTML / CSS
- PostgreSQL-ready via `psycopg2-binary`

## Getting Started

1. Create a virtual environment.
2. Activate the virtual environment.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Move into the Django project folder:
   `cd expense_tracker`
5. Apply migrations:
   `python manage.py migrate`
6. Start the development server:
   `python manage.py runserver`

Open `http://127.0.0.1:8000/` in your browser after the server starts.

## Project Structure

- `expense_tracker/manage.py` Django management entry point
- `expense_tracker/expense_tracker/` project configuration
- `expense_tracker/core/` application logic, views, models, and templates
- `requirements.txt` Python dependencies

## Future Improvements

- Charts and analytics for spending trends
- Category-based filtering
- Export reports
- Better mobile responsiveness
