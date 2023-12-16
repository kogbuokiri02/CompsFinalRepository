import requests
import psycopg2

api_key = '5mw9gEjtvBlF_nGoargmqpTdplTnEIaHmwlT2rE0tYFDfxRLy38JDTzlBj8wgUi4U-A9oJ65IEehW8k8RRKydsrolQ-4PKHltSEQGxXiUukfwrVfaZ9SjwUAOpt7ZXYx'
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

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='food_preferences',
    user='postgres',
    password='root',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

while True:
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        restaurant_data = response.json().get('businesses', [])

        for restaurant in restaurant_data:
            business_name = restaurant.get('name')

            cursor.execute("SELECT id FROM business_2 WHERE business_name = %s", (business_name,))
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
                    INSERT INTO business_2 (business_name, address, city, state, country, location)
                    VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                    RETURNING id
                    """,
                    (business_name, address, city, state, country, longitude, latitude)
                )
                business_id = cursor.fetchone()[0]

            cuisines = [category.get('title') for category in restaurant.get('categories', [])]
            
            for cuisine_str in cuisines:
                individual_cuisines = [c.strip() for c in cuisine_str.split(',')]  # Split cuisines by comma

                for cuisine in individual_cuisines:
                    cursor.execute("SELECT id FROM cuisine WHERE cuisine_name = %s", (cuisine,))
                    cuisine_id = cursor.fetchone()

                    if cuisine_id is None:
                        cursor.execute("INSERT INTO cuisine (cuisine_name) VALUES (%s) RETURNING id", (cuisine,))
                        cuisine_id = cursor.fetchone()[0]
                    else:
                        cuisine_id = cuisine_id[0]

                    cursor.execute(
                        "SELECT 1 FROM business_cuisine WHERE business_id = %s AND cuisine_id = %s",
                        (business_id, cuisine_id)
                    )
                    existing_relationship = cursor.fetchone()

                    if not existing_relationship:
                        cursor.execute(
                            "INSERT INTO business_cuisine (business_id, cuisine_id) VALUES (%s, %s)",
                            (business_id, cuisine_id)
                        )

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

cursor.close()
conn.close()

