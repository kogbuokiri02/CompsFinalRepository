#userlocation table
import psycopg2
import requests
import googlemaps

# Function to fetch user IDs from the users table
def fetch_user_ids_from_users_table():
    try:
        conn = psycopg2.connect(
            dbname='',
            user='',
            password='',
            host='',
            port=''
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        return user_ids
    except psycopg2.Error as e:
        print(f"Error fetching user IDs: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()

# Function to fetch data from the API
def fetch_data_from_api():
    try:
        response = requests.get('https://data.lacity.org/resource/6rrh-rzua.json')
        if response.status_code == 200:
            api_data = response.json()
            return api_data
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return []

# Function to get geographical point from address using Google Maps API
def get_geographical_point(address):
    try:
        gmaps = googlemaps.Client(key='')
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return f"POINT ({location['lng']} {location['lat']})"
        else:
            return None
    except Exception as e:
        print(f"Geocoding failed for {address}: {e}")
        return None

# Function to fetch existing addresses from the users_locations table
def fetch_existing_addresses():
    try:
        conn = psycopg2.connect(
            dbname='',
            user='',
            password='',
            host='',
            port=''
        )
        cursor = conn.cursor()

        cursor.execute("SELECT address FROM users_locations")
        existing_addresses = [row[0] for row in cursor.fetchall()]

        return existing_addresses
    except psycopg2.Error as e:
        print(f"Error fetching existing addresses: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()

# Function to insert unique data into users_locations
def insert_unique_data_into_users_locations(api_data, user_ids, existing_addresses, num_records):
    try:
        conn = psycopg2.connect(
            dbname='',
            user='',
            password='',
            host='',
            port=''
        )
        cursor = conn.cursor()

        for record in api_data[:num_records]:
            user_id = user_ids.pop(0) if user_ids else None

            address = record.get('street_address')
            city = record.get('city')

            print(f"Fetched address: {address}, City: {city}")

            if address not in existing_addresses:
                geographical_point = get_geographical_point(f"{address}, {city}")

                if geographical_point:
                    cursor.execute(
                        "INSERT INTO users_locations (user_id, address, city, geographical_point) VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326))",
                        (user_id, address, city, geographical_point)
                    )
                    print("Data inserted successfully!")
                else:
                    print(f"Geographical point not found for {address}, {city}")
            else:
                print(f"Address already exists: {address}")

            conn.commit()  # Commit changes

    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Fetch user IDs, API data, and existing addresses
user_ids_from_users_table = fetch_user_ids_from_users_table()
api_data = fetch_data_from_api()
existing_addresses = fetch_existing_addresses()
num_unique_records = 100  # Number of unique records to insert

# Insert unique data into users_locations
if user_ids_from_users_table and api_data and existing_addresses:
    insert_unique_data_into_users_locations(api_data, user_ids_from_users_table, existing_addresses, num_unique_records)

