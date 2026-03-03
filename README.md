# Diary Backend Application

A functional backend application for a daily planner (diary) developed using Python and the Flask framework. The application handles CRUD (Create, Read, Update, Delete) operations, supports both HTML-rendered templates via Jinja2, and exposes a JSON API using query parameters.

This project is structured using Flask application factories and Blueprints for modularity, and utilizes SQLAlchemy for database interaction. It is designed to work with a PostgreSQL database, but includes an automatic fallback to a local SQLite database for simplified testing environments.

## Features

- **Create Entry:** Allows users to add a new diary entry with a title and content.
- **Read Entries:** View a list of all entries sorted by creation date, or view a specific entry in detail.
- **Update Entry:** Edit the title, content, or completion status of an existing entry.
- **Delete Entry:** Permanently remove an entry from the database.
- **Toggle Status:** Quickly mark a diary entry task as completed or incomplete.
- **Dual Output:** Every relevant endpoint supports rendering a standard HTML page or returning JSON payload when the `?json=1` query parameter is provided or when submitting `application/json` payload.

## Technology Stack

- **Python 3+**
- **Flask:** Core web framework.
- **Flask-SQLAlchemy:** Database ORM extension.
- **PostgreSQL / psycopg2-binary:** Primary database engine and adapter.
- **python-dotenv:** Environment variable management.
- **Jinja2:** HTML templating engine.

## Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # venv\Scripts\activate   # On Windows
   ```

3. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy the provided `.env.example` file to `.env` in the root directory.
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and populate it with your PostgreSQL connection string and a secret key:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database_name
   SECRET_KEY=your_secure_secret_key
   ```
   *Note: If `DATABASE_URL` is omitted, the application will automatically initialize a local `diary.db` SQLite database.*

5. **Run the Application Server:**
   ```bash
   python run.py
   ```
   The application will be accessible via browser or API client at: `http://127.0.0.1:5000`

## API Endpoints Overview

The application functions as a standard web application. However, appending `?json` to the URL triggers the JSON API response.

- **`GET /`**
  - Description: Fetches all entries.
  - Returns: HTML template or JSON array of entries.
- **`GET /entry/<id>`**
  - Description: Fetches a specific entry by its primary key ID.
  - Returns: HTML template or JSON object representing the entry.
- **`POST /create`**
  - Description: Creates a new entry. Accepts Form Data or JSON (`{"title": "...", "content": "..."}`).
  - Returns: HTML redirect or JSON object containing the newly created entry.
- **`POST /edit/<id>`**
  - Description: Updates an existing entry by ID. Accepts Form Data or JSON.
  - Returns: HTML redirect or JSON confirmation.
- **`POST /delete/<id>` or `DELETE /delete/<id>`**
  - Description: Deletes an entry by ID.
  - Returns: HTML redirect or JSON confirmation.
- **`GET` or `POST /toggle/<id>`**
  - Description: Reverses the `is_completed` boolean status of a specific entry.
  - Returns: HTML redirect or JSON confirmation.
