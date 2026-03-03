import os
from app import create_app

# Instantiate the Flask application via the factory pattern function.
# This makes the application ready to be served or run in development mode.
app = create_app()

# This conditional ensures that the server runs only if this script is executed directly
# (e.g., python run.py) and not when imported elsewhere.
if __name__ == '__main__':
    # Start the local development server.
    # host='0.0.0.0' exposes the server to all network interfaces.
    # debug=True provides tracebacks in the browser for easier development.
    # The port is dynamically loaded from the environment, defaulting to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
