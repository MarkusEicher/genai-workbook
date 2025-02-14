import json
import pytest
from datetime import datetime

def test_create_study_session_success(client, app):
    # Setup test data
    with app.app_context():
        cursor = app.db.cursor()
        cursor.execute("INSERT INTO groups (id, name) VALUES (1, 'Test Group')")
        cursor.execute("INSERT INTO study_activities (id, name) VALUES (1, 'Test Activity')")
        app.db.commit()

        # Make request
        response = client.post('/api/study-sessions',
            json={'group_id': 1, 'study_activity_id': 1})
        
        # Assert response
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['group_id'] == 1
        assert data['group_name'] == 'Test Group'
        assert data['activity_id'] == 1
        assert data['activity_name'] == 'Test Activity'
        assert data['review_items_count'] == 0
        assert 'id' in data
        assert 'start_time' in data
        assert 'end_time' in data

        # Verify database state
        cursor.execute('''
            SELECT 
                ss.id,
                ss.group_id,
                g.name as group_name,
                sa.id as activity_id,
                sa.name as activity_name,
                ss.created_at,
                COUNT(wri.id) as review_items_count
            FROM study_sessions ss
            JOIN groups g ON g.id = ss.group_id
            JOIN study_activities sa ON sa.id = ss.study_activity_id
            LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
            WHERE ss.id = ?
            GROUP BY ss.id
        ''', (data['id'],))
        
        db_session = cursor.fetchone()
        assert db_session is not None
        assert db_session['group_id'] == data['group_id']
        assert db_session['group_name'] == data['group_name']
        assert db_session['activity_id'] == data['activity_id']
        assert db_session['activity_name'] == data['activity_name']
        assert db_session['review_items_count'] == 0
        assert db_session['created_at'] == data['start_time']

def test_create_study_session_missing_fields(client):
    # Test missing group_id
    response = client.post('/api/study-sessions', 
        json={'study_activity_id': 1})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Missing required fields'
    assert 'group_id' in data['missing_fields']

    # Test missing study_activity_id
    response = client.post('/api/study-sessions', 
        json={'group_id': 1})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'study_activity_id' in data['missing_fields']

    # Test empty request
    response = client.post('/api/study-sessions', json={})
    assert response.status_code == 400

def test_create_study_session_invalid_ids(client, app):
    # Setup test data
    with app.app_context():
        cursor = app.db.cursor()
        cursor.execute("INSERT INTO groups (id, name) VALUES (1, 'Test Group')")
        app.db.commit()

        # Test non-existent study_activity_id
        response = client.post('/api/study-sessions', 
            json={'group_id': 1, 'study_activity_id': 999})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Study activity not found'
        assert data['study_activity_id'] == 999

        # Test non-existent group_id
        response = client.post('/api/study-sessions', 
            json={'group_id': 999, 'study_activity_id': 1})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Group not found'
        assert data['group_id'] == 999

def test_create_study_session_invalid_json(client):
    response = client.post('/api/study-sessions', 
        data='invalid json',
        content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Invalid JSON in request body'