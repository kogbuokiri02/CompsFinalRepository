import psycopg2

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

# Sample data for cuisines
cuisine_names = [
    "Italian", "Chinese", "Mexican", "Indian", "Japanese",
    "Mediterranean", "Thai", "French", "Greek", "Spanish",
    "Korean", "Vietnamese", "American", "Brazilian", "Russian",
    "Turkish", "Lebanese", "Egyptian", "African", "German"
]

try:
    # Inserting cuisine names into cuisine table
    for cuisine_name in cuisine_names:
        try:
            # Insert cuisine name into cuisine table
            cursor.execute(
                "INSERT INTO cuisine (cuisine_name) VALUES (%s) RETURNING id",
                (cuisine_name,)
            )
            cuisine_id = cursor.fetchone()[0]

            print(f"Inserted {cuisine_name} with ID {cuisine_id}")
        except psycopg2.Error as e:
            print(f"Error inserting {cuisine_name}: {e}")
            conn.rollback()

    # Commit changes to the database
    conn.commit()
    print("Cuisine data inserted successfully!")
except psycopg2.Error as e:
    print("Error inserting cuisine data:", e)
    conn.rollback()
finally:
    # Close cursor and connection
    cursor.close()
    conn.close()
