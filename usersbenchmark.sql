BEGIN;

-- Simulate a SELECT operation on the users table
SELECT * FROM users WHERE id = floor(random() * 1000000 + 1)::int;

-- Simulate an INSERT operation on the users table with unique email addresses
INSERT INTO users (email, username, password, role, created_at)
VALUES ('user' || floor(random() * 1000 + 1)::int || '@example.com', 'testuser', 'testpassword', 'user', NOW());

-- Simulate an UPDATE operation on the users table
UPDATE users SET email = 'newuser' || floor(random() * 1000 + 1)::int || '@example.com' WHERE id = floor(random() * 1000000 + 1)::int;

-- Simulate a DELETE operation on the users table
DELETE FROM users WHERE id = floor(random() * 1000000 + 1)::int;

COMMIT;
