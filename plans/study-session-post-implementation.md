# Plan to Implement /study_sessions POST Route

This document outlines the steps to implement the `/study_sessions` POST route, including testing considerations.

## I. Endpoint Design

*   [x] **1. Define Request Body:**  The request body should contain the necessary information to create a new study session.  This will likely include:
    *   `group_id`: The ID of the group the session belongs to.
    *   `study_activity_id`: The ID of the study activity performed.

*   [x] **2. Define Response:** The response should return the newly created study session object, including its ID, or an appropriate error message if creation fails.  A successful creation should return a 201 status code (Created).

## II. Implementation Steps

*   [x] **3. Create Route Handler:** Add the `@app.route('/api/study-sessions', methods=['POST'])` and `@cross_origin()` decorators to the `load(app)` function. Create the `create_study_session()` function.

*   [x] **4. Parse Request Body:** Inside the `create_study_session()` function, parse the JSON request body using `request.get_json()`. Handle potential JSON decoding errors.

*   [x] **5. Validate Input:** Check if `group_id` and `study_activity_id` are present in the request body.  Also, validate that these IDs exist in the database (e.g., check if a group and study activity with those IDs exist). Return a 400 Bad Request if the input is invalid.

*   [x] **6. Insert into Database:** Use a parameterized SQL query to insert a new record into the `study_sessions` table. The `created_at` timestamp should be generated on the server.

*   [x] **7. Retrieve Created Session:** After the insert, retrieve the newly created study session from the database using the `lastrowid` or a similar method to get the ID.

*   [x] **8. Format Response:**  Format the retrieved study session data into a JSON response, including the `id`, `group_id`, `group_name`, `activity_id`, `activity_name`, `start_time` (which is the created_at time), `end_time` (can be the same as start time initially), and `review_items_count` (initially 0).

*   [x] **9. Error Handling:** Implement proper error handling using `try...except` blocks to catch database errors or other exceptions. Return appropriate HTTP status codes (e.g., 500 Internal Server Error) and error messages in the JSON response.

## III. Testing

*   [x] **10. Unit Tests:** Create unit tests to cover the following scenarios:
    *   Successful creation of a study session.
    *   Invalid request body (missing fields).
    *   Non-existent `group_id` or `study_activity_id`.
    *   Database errors during insertion.
    *   JSON decoding errors.

*   [x] **11. Test Data:** Create test data (groups and study activities) in your database before running the tests.

*   [x] **12. Test Framework:** Use a testing framework like `pytest` to write and run the tests.

*   [x] **13. Assertions:** Use assertions in our tests to verify the response status codes, response body content, and the data in the database after the POST request.

## IV. Example Code Snippet (Illustrative)

```python
@app.route('/api/study-sessions', methods=['POST'])
@cross_origin()
def create_study_session():
    try:
        data = request.get_json()
        if not data or 'group_id' not in data or 'study_activity_id' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        group_id = data['group_id']
        study_activity_id = data['study_activity_id']

        # ... (Database validation for group_id and study_activity_id) ...

        cursor = app.db.cursor()
        cursor.execute('''
            INSERT INTO study_sessions (group_id, study_activity_id, created_at)
            VALUES (?, ?, datetime('now'))
        ''', (group_id, study_activity_id))
        app.db.commit()

        session_id = cursor.lastrowid  # Or a database-specific way to get the ID

        # ... (Retrieve the session data and format the JSON response) ...

        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500