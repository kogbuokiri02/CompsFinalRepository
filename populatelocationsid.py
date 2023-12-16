#populate user_location
import psycopg2
import random

# Establish a database connection
conn = psycopg2.connect(dbname='', user='', password='', host='', port='')
cursor = conn.cursor()

try:
    # Fetch all ids from users table
    cursor.execute("SELECT id FROM users")
    ids = cursor.fetchall()

    for user_id in ids:
        # Fetch a random location_id from users_locations
        cursor.execute("""
            SELECT location_id 
            FROM users_locations 
            ORDER BY RANDOM() 
            LIMIT 1;
        """)
        random_location_id = cursor.fetchone()[0]  # Fetch the first row of the result

        # Update the user with the random location_id
        cursor.execute(f"""
            UPDATE users 
            SET location_id = '{random_location_id}' 
            WHERE id = '{user_id[0]}';
        """)

    # Commit the changes to the database
    conn.commit()
    print("Random location IDs inserted successfully into users table.")

except psycopg2.Error as e:
    conn.rollback()
    print(f"Error: {e}")

finally:
    cursor.close()
    conn.close()
