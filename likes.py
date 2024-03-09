import psycopg2
import random
from datetime import datetime, timedelta

# Connection to PostgreSQL database
try:
    conn = psycopg2.connect(
	dbname='food_preferences',
        user='postgres',
        password='root',
        host='localhost',
        port='5432'
    )
    print("Connected to the database!")
except Exception as e:
    print("Unable to connect to the database:", e)
    exit()

# Create a cursor to perform database operations
cursor = conn.cursor()

# Get the existing user_ids from the users table
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

# Insert entries into the likes table
for user_review_id in range(1, 701):  # Assuming user_review_ids range from 1 to 700
    user_id = random.choice(user_ids)
    created_at = datetime.now() - timedelta(days=random.randint(1, 365))

    cursor.execute(
        "INSERT INTO likes (user_id, user_review_id, created_at) VALUES (%s, %s, %s) RETURNING id",
        (user_id, user_review_id, created_at)
    )
    inserted_id = cursor.fetchone()[0]

# Commit changes to the database
conn.commit()

# Close cursor and connection
cursor.close()
conn.close()
