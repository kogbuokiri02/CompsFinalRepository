#Fake users
from faker import Faker
import psycopg2
from psycopg2 import sql

fake = Faker()

# PostgreSQL connection parameters
connection_params = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "root",
    "database": "food_preferences",
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**connection_params)
cursor = conn.cursor()

# Number of dummy users to insert
num_users = 1000

# Insert dummy users without the location attribute
for _ in range(num_users):
    insert_query = sql.SQL("""
        INSERT INTO users (email, username, password, role, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """)

    insert_data = (
        fake.email(),
        fake.user_name(),
        fake.password(),
        fake.random_element(["admin", "user"]),
    )

    try:
        cursor.execute(insert_query, insert_data)
    except psycopg2.Error as e:
        # Handle errors (e.g., log the error)
        print(f"Error: {e}")
        conn.rollback()

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
