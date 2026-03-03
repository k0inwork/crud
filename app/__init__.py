from flask import Flask
from config import Config
from .models import db
from .routes import main_bp

# Application Factory function to create and configure the Flask application instance.
# Recommended approach for maintainability and testing instead of global app instances.
def create_app():
    # Instantiate the Flask application
    app = Flask(__name__)

    # Load configuration settings from the Config object (defined in config.py)
    app.config.from_object(Config)

    # Initialize the SQLAlchemy extension with the application instance
    db.init_app(app)

    # Register the main blueprint to attach all routes to the application
    app.register_blueprint(main_bp)

    # Use the application context to perform setup tasks like creating database tables
    # if they do not exist already (useful for development and local testing).
    with app.app_context():
        # Creates all tables mapped by SQLAlchemy models (e.g., 'entries')
        db.create_all()

    # Return the configured application instance
    return app
