import sys
import os

# Ensure project root is in sys.path so app and models can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app
from database import init_db

# Initialize database on cold start
try:
    with app.app_context():
        init_db()
except Exception as e:
    print(f"Vercel DB initialization notice: {e}")

# Vercel Serverless WSGI entrypoint
