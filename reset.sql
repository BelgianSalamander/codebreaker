-- WARNING: THIS SCRIPT WILL DELETE ALL USER DATA! DO NOT RUN DURING A CODEBREAKER CONTEST
DELETE FROM users;
DELETE FROM results;

INSERT INTO users(username, password, visible, admin) VALUES ('tutors', 'simmeringaioli', FALSE, TRUE);

INSERT INTO users(username, password, visible, admin) VALUES ('testuser', 'testpass', TRUE, FALSE);
