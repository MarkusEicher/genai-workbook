import os
import tempfile
import pytest
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from app import create_app
from lib.db import Db

@pytest.fixture
def app():
    # Create a temporary file to be used as our database
    db_fd, db_path = tempfile.mkstemp()
    
    # Create the app with test config
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })
    
    # Initialize the test database
    with app.app_context():
        cursor = app.db.cursor()
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_activities (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY,
                group_id INTEGER NOT NULL,
                study_activity_id INTEGER NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups(id),
                FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_review_items (
                id INTEGER PRIMARY KEY,
                word_id INTEGER NOT NULL,
                study_session_id INTEGER NOT NULL,
                correct BOOLEAN NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
            )
        ''')
        app.db.commit()

    yield app
    
    # Clean up the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()