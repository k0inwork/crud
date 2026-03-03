from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy object (will be linked to the app in __init__.py)
db = SQLAlchemy()

# Model for daily diary entries (maps to a database table)
class Entry(db.Model):
    # Specify the table name explicitly
    __tablename__ = 'entries'

    # Unique identifier for the entry (Primary Key)
    id = db.Column(db.Integer, primary_key=True)

    # Title of the diary entry. Maximum length 200, cannot be empty (nullable=False)
    title = db.Column(db.String(200), nullable=False)

    # Main content of the entry. Text type allows for long text blocks
    content = db.Column(db.Text, nullable=False)

    # Status indicating whether the task/entry is completed. Defaults to False.
    is_completed = db.Column(db.Boolean, default=False)

    # Auto-populated creation timestamp for when the entry is added to the database
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # String representation of the object for easier debugging and logging
    def __repr__(self):
        return f'<Entry {self.id} - {self.title}>'

    # Helper method to convert the SQLAlchemy model instance into a dictionary
    # Useful for returning JSON responses in the API
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'is_completed': self.is_completed,
            # Format datetime as string to ensure JSON serialization works correctly
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
