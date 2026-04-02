"""WSGI entry point for production (gunicorn)."""
from rinq.app import app

if __name__ == '__main__':
    app.run()
