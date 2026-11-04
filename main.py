"""Alternate entry point for running the Flask application locally."""

from app import app


if __name__ == "__main__":
    app.run(debug=False)
