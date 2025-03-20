from app import flask_app
import app.main  # Ensure Flask routes are loaded

if __name__ == '__main__':
    flask_app.run(debug=True, port=5001)
