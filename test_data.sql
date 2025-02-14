-- Create groups table
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create study activities table
CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create study sessions table (since we'll be inserting into this)
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    study_activity_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
);

-- Insert test groups
INSERT INTO groups (id, name) VALUES 
  (1, 'Beginner Japanese'),
  (2, 'Intermediate Kanji'),
  (3, 'JLPT N5 Study Group');

-- Insert test study activities
INSERT INTO study_activities (id, name) VALUES
  (1, 'Vocabulary Review'),
  (2, 'Kanji Practice'),
  (3, 'Reading Comprehension'); 