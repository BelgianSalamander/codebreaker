-- Create tables
CREATE TABLE IF NOT EXISTS users (
	username VARCHAR UNIQUE,
	password VARCHAR,
	admin BOOLEAN,
    visible BOOLEAN,
	PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS results (
	id INTEGER PRIMARY KEY,
	owner VARCHAR,
	score INT,
	status VARCHAR,
	proposed_input VARCHAR,
	broken_output VARCHAR,
	correct_output VARCHAR,
	problem VARCHAR,
	complete BOOLEAN,
	FOREIGN KEY (owner) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS settings (
	name VARCHAR UNIQUE,
	value INT
);

-- Do some initial setup
INSERT INTO settings(name, value) SELECT 'contestant_access', 0
    WHERE NOT EXISTS (SELECT * FROM settings WHERE name='contestant_access');
INSERT INTO settings(name, value) SELECT 'scoreboard_freeze_id', 100000000
    WHERE NOT EXISTS (SELECT * FROM settings WHERE name='scoreboard_freeze_id');