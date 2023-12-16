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

# Sample data for cuisines and dishes
cuisines_and_dishes = {
    "Salvadoran": [("Pupusas", "Pancake"), ("Yuca Fries", "Fries")],
    "Caribbean": [("Jerk Chicken", "Chicken Dish"), ("Ackee and Saltfish", "Saltfish Dish")]
    # ... (other cuisine and dish data)
}



try:
    # Inserting dish names into dish_name table
    for cuisine, dishes in cuisines_and_dishes.items():
        for dish, preference in dishes:
            try:
                # Check if the preference exists and get its ID
                cursor.execute("SELECT id FROM preferences WHERE preference_name = %s", (preference,))
                preference_id = cursor.fetchone()

                if preference_id:
                    preference_id = preference_id[0]

                    # Insert dish name into dish_name table
                    cursor.execute(
                        "INSERT INTO dish_name (name, preference_id) VALUES (%s, %s) RETURNING id",
                        (dish, preference_id)
                    )
                    dish_id = cursor.fetchone()[0]

                    # Get cuisine ID
                    cursor.execute("SELECT id FROM cuisine WHERE cuisine_name = %s", (cuisine,))
                    cuisine_id = cursor.fetchone()[0]

                    # Establish many-to-many relationship between cuisine and dish_name
                    cursor.execute(
                        "INSERT INTO cuisine_dish (cuisine_id, dish_id) VALUES (%s, %s)",
                        (cuisine_id, dish_id)
                    )
            except psycopg2.Error as e:
                print(f"Error inserting {dish} from {cuisine}: {e}")
                conn.rollback()

    # Commit changes to the database
    conn.commit()
    print("Data inserted successfully!")
except psycopg2.Error as e:
    print("Error inserting data:", e)
    conn.rollback()
finally:
    # Close cursor and connection
    cursor.close()
    conn.close()
