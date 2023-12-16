from faker import Faker
import psycopg2
import random

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='',
    user='',
    password='',
    host='',
    port=''
)
cursor = conn.cursor()

# Faker instance
fake = Faker()

# Fetch business IDs and names from business_2 table
cursor.execute("SELECT id, business_name FROM business_2")
business_data = cursor.fetchall()

# Generate and insert fake reviews with business_id
for business_id, business_name in business_data:
    # Generate fake review rating (from 1.0 to 5.0)
    review_rating = round(random.uniform(1.0, 5.0), 1)

    # Generate fake review URL containing business_name
    review_url = f'https://www.example.com/{business_name.replace(" ", "-")}-reviews'

    # Insert fake review data into external_review table
    cursor.execute(
        """
        INSERT INTO external_review (review, review_url, business_id)
        VALUES (%s, %s, %s)
        """,
        (review_rating, review_url, business_id)
    )

conn.commit()

# Close cursor and connection
cursor.close()
conn.close()
