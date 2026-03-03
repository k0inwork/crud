import os
from dotenv import load_dotenv

# Load environment variables from a .env file so secrets are not hardcoded
load_dotenv()

class Config:
    # Database connection string. Falls back to sqlite if DATABASE_URL is not set in the environment
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///diary.db'

    # Disable SQLAlchemy modification tracking to avoid warnings and save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key used for session management and CSRF protection in forms
    # Using a default fallback value if not provided in the environment (not recommended for production)
    SECRET_KEY = os.getenv('SECRET_KEY') or 'my-super-secret-key-for-my-diary'
