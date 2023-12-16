#business Location
import requests
import psycopg2

api_key = 'RImUHTz6PWCoLQpvud-oxzHvz0obOD22hZwQtDMRmq9RdckRYyTbXGK8OaPn4t4kRMLIbWxLy0ia0-uGElGQIbct4wljiz6Q_FeBirxsutuILvlasQFSlON2_jp2ZXYx'
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
    dbname='',
    user='',
    password='',
    host='',
    port='5432'
)
cursor = conn.cursor()

while True:
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        restaurant_data = response.json().get('businesses', [])

        for restaurant in restaurant_data:
            business_name = restaurant.get('name')

            # Check if the business name already exists in the database
            cursor.execute("SELECT COUNT(*) FROM business WHERE business_name = %s", (business_name,))
            count = cursor.fetchone()[0]

            if count == 0:
                address = ', '.join(restaurant.get('location', {}).get('display_address', []))
                city = restaurant.get('location', {}).get('city')
                state = restaurant.get('location', {}).get('state')
                country = restaurant.get('location', {}).get('country')
                latitude = restaurant.get('coordinates', {}).get('latitude')
                longitude = restaurant.get('coordinates', {}).get('longitude')

                # Insert data into the business table with geography type casting
                cursor.execute(
                    """
                    INSERT INTO business (business_name, address, city, state, country, location)
                    VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                    """,
                    (business_name, address, city, state, country, longitude, latitude)
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
