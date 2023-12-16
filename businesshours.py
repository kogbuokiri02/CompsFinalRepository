from faker import Faker
import psycopg2
import random

fake = Faker()

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='',
    user='',
    password='',
    host='',
    port=''
)
cursor = conn.cursor()

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Fetch existing businesses
cursor.execute("SELECT id FROM business_2")
businesses = cursor.fetchall()

for business_id in businesses:
    for day_idx, day in enumerate(days_of_week, start=1):
        start_time = fake.time(pattern='%H:%M:%S', end_datetime=None)
        end_time = fake.time(pattern='%H:%M:%S', end_datetime=None)

        # Check if the generated open hours match any existing entry in open_hours
        cursor.execute(
            "SELECT id FROM open_hours WHERE day_of_week = %s AND start_time = %s AND end_time = %s",
            (day_idx, start_time, end_time)
        )
        existing_open_hours = cursor.fetchone()

        if existing_open_hours:
            # Link existing open_hours entry to the business
            cursor.execute(
                "INSERT INTO business_open_hours (business_id, open_hours_id) VALUES (%s, %s)",
                (business_id, existing_open_hours[0])
            )
        else:
            # Add new open_hours entry to open_hours table and link it to the business
            cursor.execute(
                "INSERT INTO open_hours (day_of_week, start_time, end_time) VALUES (%s, %s, %s) RETURNING id",
                (day_idx, start_time, end_time)
            )
            new_open_hours_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO business_open_hours (business_id, open_hours_id) VALUES (%s, %s)",
                (business_id, new_open_hours_id)
            )

conn.commit()

# Close cursor and connection
cursor.close()
conn.close()
