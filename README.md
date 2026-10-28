# Bacly - Your Private Bac Tutor

Bacly is a mathematics tutoring platform for Algerian Baccalauréat students, following the Algerian national curriculum.

## Features

- **Ask Tutor** — Get step-by-step solutions to math exercises with LaTeX formatting
- **Practice** — Generate chapter-specific exercises with hints and automatic grading
- **Mock Exam** — Timed practice exams graded out of 20 (Bac scale)
- **Progress** — Track mastery by chapter with a 7-day study plan
- **History** — Review past tutor sessions and practice results
- **Teacher Dashboard** — Class overview and student roster management

## Run Locally

### Prerequisites
- Python 3.11+
- Django (see `requirements.txt`)

### Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Copy the example environment file and add your Gemini API key:
   ```
   cp .env.example .env
   ```
   Then edit `.env` and set `GEMINI_API_KEY`.

3. Apply migrations:
   ```
   python manage.py migrate
   ```

4. (Optional) Seed demo data:
   ```
   python manage.py seed_demo
   ```

5. Run the development server:
   ```
   python run_dev.py
   ```

The app will be available at http://127.0.0.1:3000

### Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Student | `demo_student` | `demo1234` |
| Teacher | `demo_teacher` | `demo1234` |

## Project Structure

- `bacly/` — Django project settings & AI services
- `accounts/` — User authentication & profiles
- `core/` — Dashboard, history, utilities
- `tutor/` — Ask Tutor feature
- `practice/` — Practice drills
- `exams/` — Mock exams
- `progress/` — Study plans & progress tracking
- `classes/` — Teacher class management
- `templates/` — HTML templates (HTMX + Alpine.js)

## Tech Stack

- Django 5.x (backend)
- SQLite (database)
- HTMX + Alpine.js (frontend interactivity)
- Tailwind CSS (styling)
- KaTeX (math rendering)
