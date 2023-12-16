import psycopg2

# Connection to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname='',
        user='',
        password='',
        host='',
        port=''
    )
    print("Connected to the database!")
except Exception as e:
    print("Unable to connect to the database:", e)
    exit()

# Create a cursor to perform database operations
cursor = conn.cursor()

# Sample data for a user review
user_id = 1  # Replace with an existing user ID
taste_rating = 4.5
preparation_time_rating = 3.5
friendliness_to_restrictions = 5.0
portion_rating = 4.0
dish_reviews = "Delicious dish, loved the flavors!"
price = 4.5

try:
    # Insert a review into user_review table with only user_id
    cursor.execute(
        "INSERT INTO user_review (user_id, taste_rating, preparation_time_rating, "
        "friendliness_to_restrictions, portion_rating, dish_reviews, price) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (user_id, taste_rating, preparation_time_rating,
         friendliness_to_restrictions, portion_rating, dish_reviews, price)
    )

    # Commit changes to the database
    conn.commit()
    print("Review inserted successfully!")
except psycopg2.Error as e:
    print("Error inserting review:", e)
    conn.rollback()
finally:
    # Close cursor and connection
    cursor.close()
    conn.close()
