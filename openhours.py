#Due to my qps to yelp I was not able to do this all the way
import requests
import psycopg2

api_key = ''  # Add your Yelp API key here

headers = {
    'Authorization': f'Bearer {api_key}'
}
url = 'https://api.yelp.com/v3/businesses/search'

params = {
    'location': 'Glendale, California',
    'categories': 'restaurants',
    'limit': 50,  # Fetch 50 results per request
    'offset': 0   # Start with the first set of results
}

def insert_business_data(cursor, restaurant, params):
    business_name = restaurant.get('name')
    cursor.execute("SELECT id FROM Business_3 WHERE business_name = %s", (business_name,))
    business_id = cursor.fetchone()

    if business_id is None:
        address = ', '.join(restaurant.get('location', {}).get('display_address', []))
        city = restaurant.get('location', {}).get('city')
        state = restaurant.get('location', {}).get('state')
        country = restaurant.get('location', {}).get('country')
        latitude = restaurant.get('coordinates', {}).get('latitude')
        longitude = restaurant.get('coordinates', {}).get('longitude')

        cursor.execute(
            """
            INSERT INTO Business_3 (business_name, address, city, state, country, location)
            VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
            RETURNING id
            """,
            (business_name, address, city, state, country, longitude, latitude)
        )
        business_id = cursor.fetchone()[0]

    return business_id

#insert cuisine_information
def insert_cuisine_data(cursor, restaurant, business_id, params):
    cuisines = [category.get('title') for category in restaurant.get('categories', [])]

    for cuisine_str in cuisines:
        individual_cuisines = [c.strip() for c in cuisine_str.split(',')]

        for cuisine in individual_cuisines:
            cursor.execute("SELECT id FROM Cuisine_3 WHERE cuisine_name = %s", (cuisine,))
            cuisine_id = cursor.fetchone()

            if cuisine_id is None:
                cursor.execute("INSERT INTO Cuisine_3 (cuisine_name) VALUES (%s) RETURNING id", (cuisine,))
                cuisine_id = cursor.fetchone()[0]
            else:
                cuisine_id = cuisine_id[0]

            cursor.execute(
                "SELECT 1 FROM Business_Cuisine_3 WHERE business_id = %s AND cuisine_id = %s",
                (business_id, cuisine_id)
            )
            existing_relationship = cursor.fetchone()

            if not existing_relationship:
                cursor.execute(
                    "INSERT INTO Business_Cuisine_3 (business_id, cuisine_id) VALUES (%s, %s)",
                    (business_id, cuisine_id)
                )
#insert openhours
def insert_open_hours_data(cursor, restaurant, business_id, params):
    open_hours_data = restaurant.get('hours', [])

    for day_schedule in open_hours_data:
        day_of_week = day_schedule.get('day')
        start_time = day_schedule.get('start')
        end_time = day_schedule.get('end')

        cursor.execute(
            """
            INSERT INTO Open_Hours_3 (day_of_week, start_time, end_time)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (day_of_week, start_time, end_time)
        )
        open_hours_id = cursor.fetchone()[0]

        # Establish relationship in Business_Open_Hours_3 table
        cursor.execute(
            """
            INSERT INTO Business_Open_Hours_3 (business_id, open_hours_id)
            VALUES (%s, %s)
            """,
            (business_id, open_hours_id)
        )

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='',
    user='',
    password='',
    host='',
    port=''
)
cursor = conn.cursor()

try:
    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            restaurant_data = response.json().get('businesses', [])

            for restaurant in restaurant_data:
                business_id = insert_business_data(cursor, restaurant, params)
                insert_cuisine_data(cursor, restaurant, business_id, params)
                insert_open_hours_data(cursor, restaurant, business_id, params)

            conn.commit()

            # Increment offset for the next page
            params['offset'] += params['limit']

            if len(restaurant_data) < params['limit']:
                # If fewer restaurants were fetched than the limit, it means we've reached the end
                break
        else:
            print('Failed to fetch data from Yelp API. Status code:', response.status_code)
            print('Error message:', response.json())
            break

except Exception as e:
    print("An error occurred:", e)

finally:
    cursor.close()
    conn.close()
