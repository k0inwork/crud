from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import db, Entry

# Define the blueprint to organize routes in a modular way.
# Avoids keeping all application logic in a single file.
main_bp = Blueprint('main', __name__)

# Route to display all entries in the diary.
# Supports GET to view the list.
@main_bp.route('/', methods=['GET'])
def index():
    try:
        # Retrieve all entries from the database, ordered by the most recent first.
        entries = Entry.query.order_by(Entry.created_at.desc()).all()

        # Check if the client requested JSON format via query parameter (?json).
        if 'json' in request.args:
            # Convert the list of objects into a list of dictionaries for JSON serialization.
            entries_list = [entry.to_dict() for entry in entries]
            return jsonify({'entries': entries_list, 'status': 'success'})

        # Otherwise, render the HTML template with the entries.
        # Pass the entries variable to the template context.
        return render_template('index.html', entries=entries)

    except Exception as e:
        # Catch unexpected errors (e.g., database connection issues).
        # Return a simple 500 error response.
        return jsonify({'error': str(e), 'message': 'An error occurred while fetching entries.'}), 500

# Route to handle creating a new diary entry.
# Supports both GET (to display form) and POST (to submit data).
@main_bp.route('/create', methods=['GET', 'POST'])
def create_entry():
    try:
        # If the request method is POST, attempt to process submitted data.
        if request.method == 'POST':
            # Handle JSON payload (e.g., from an API client or Postman).
            if request.is_json:
                data = request.get_json()
                # Extract title and content, default to empty string if missing.
                title = data.get('title', '')
                content = data.get('content', '')
            else:
                # Handle form URL-encoded payload (from an HTML form submission).
                title = request.form.get('title', '')
                content = request.form.get('content', '')

            # Basic validation: ensure the title is not empty.
            if not title:
                return jsonify({'error': 'Title cannot be empty.'}), 400

            # Instantiate the new entry object.
            new_entry = Entry(title=title, content=content)

            # Add the new object to the SQLAlchemy session.
            db.session.add(new_entry)

            # Commit the transaction to save the new entry to the database.
            db.session.commit()

            # Return JSON if requested by the client.
            if 'json' in request.args or request.is_json:
                return jsonify({'message': 'Entry created successfully.', 'entry': new_entry.to_dict()}), 201

            # Otherwise, redirect the user back to the main index page.
            return redirect(url_for('main.index'))

        # If the method is GET, render the HTML form template for creating an entry.
        return render_template('create.html')

    except Exception as e:
        # Generic exception block for unhandled errors.
        return jsonify({'error': str(e), 'message': 'Failed to create entry.'}), 500


# Route to fetch and display a single specific entry by its primary key ID.
# Uses <int:id> to ensure the ID parameter is cast as an integer.
@main_bp.route('/entry/<int:id>', methods=['GET'])
def get_entry(id):
    try:
        # Attempt to retrieve the entry; will automatically return a 404 response if not found.
        # This is a convenient SQLAlchemy feature for view functions.
        entry = Entry.query.get_or_404(id)

        # If JSON is requested via query string, serialize the object.
        if 'json' in request.args:
            return jsonify({'entry': entry.to_dict(), 'status': 'success'})

        # Default behavior: render the view HTML template with the single entry.
        return render_template('view.html', entry=entry)

    except Exception as e:
        # Fallback error handling.
        return jsonify({'error': str(e), 'message': 'Entry not found or database error.'}), 404


# Route to update an existing diary entry.
# Supports GET (to populate form) and POST (to submit changes).
@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    try:
        # Fetch the existing entry from the database.
        entry = Entry.query.get_or_404(id)

        # Handle form submission or JSON payload for the update action.
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                # Update attributes; retain old values if the new keys are missing.
                entry.title = data.get('title', entry.title)
                entry.content = data.get('content', entry.content)
                # Parse boolean state from JSON payload if present.
                if 'is_completed' in data:
                    entry.is_completed = bool(data.get('is_completed'))
            else:
                # Handle form data updates.
                entry.title = request.form.get('title', entry.title)
                entry.content = request.form.get('content', entry.content)
                # Form checkboxes only send 'on' when checked. Convert it to a boolean.
                entry.is_completed = request.form.get('is_completed') == 'on'

            # Commit the session to persist the changes in the database.
            db.session.commit()

            # Send JSON response if appropriate.
            if 'json' in request.args or request.is_json:
                return jsonify({'message': 'Entry updated successfully.', 'entry': entry.to_dict()})

            # Redirect to the home page upon successful edit.
            return redirect(url_for('main.index'))

        # Render the edit template, pre-filled with the current entry data.
        return render_template('edit.html', entry=entry)

    except Exception as e:
        # Generic error catching during the update process.
        return jsonify({'error': str(e), 'message': 'Failed to edit entry.'}), 500


# Route to handle deleting an entry.
# Although HTML forms don't support DELETE natively, allowing GET/POST makes HTML implementation easier.
# DELETE method is supported for API consumers.
@main_bp.route('/delete/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete_entry(id):
    try:
        # Look up the record by ID.
        entry = Entry.query.get_or_404(id)

        # Mark the object for deletion within the active database session.
        db.session.delete(entry)

        # Finalize the deletion by committing the transaction.
        db.session.commit()

        # Determine the appropriate response format (JSON vs Redirect).
        if 'json' in request.args or request.method == 'DELETE':
            return jsonify({'message': 'Entry deleted permanently.', 'deleted_id': id})

        # Send the user back to the index view after deleting via UI.
        return redirect(url_for('main.index'))

    except Exception as e:
        # Exception block for failed deletion attempts.
        return jsonify({'error': str(e), 'message': 'Failed to delete entry.'}), 500


# A helper route commonly implemented to quickly toggle the completion status of a task/entry.
# Switches the boolean flag on the fly without needing to go through the edit form.
@main_bp.route('/toggle/<int:id>', methods=['GET', 'POST'])
def toggle_completed(id):
    try:
        # Get the record.
        entry = Entry.query.get_or_404(id)

        # Invert the current boolean value for the completion status.
        entry.is_completed = not entry.is_completed

        # Commit the toggle change to the database.
        db.session.commit()

        # Respond according to the request format.
        if 'json' in request.args:
            return jsonify({'message': 'Status toggled successfully.', 'entry': entry.to_dict()})

        # Redirect back to the homepage.
        return redirect(url_for('main.index'))

    except Exception as e:
        # Fallback error catching.
        return jsonify({'error': str(e), 'message': 'Failed to toggle status.'}), 500
