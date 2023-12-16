import requests
import psycopg2

# Replace with your actual API key and PostgreSQL connection details
google_maps_api_key = "AIzaSyAzt2tKlXilJwGMg8b4iRw0g4Wa-LHRY-Q"
db_connection_string = "dbname=food_preferences user=postgres password=root host=localhost"

# Connect to PostgreSQL
conn = psycopg2.connect(db_connection_string)
cursor = conn.cursor()

# Glendale area bounding box (adjust as needed)
glendale_bbox = "34.1814,-118.2962|34.1788,-118.2916"

# Example method to fetch addresses from a data source (replace with your logic)
def fetch_addresses():
    return [
        "3934 Community Ave, Glendale, CA",
	"1500 CEDAR HILL RD, Glendale, CA",
	"601 CONCORD ST, GLENDALE, CA",
	"700 S CENTRAL AVE, GLENDALE, CA",
	"216 W WINDSOR RD, GLENDALE, CA",
	"6444 SAN FERNANDO RD UNIT 5354, GLENDALE, CA",
	"1136 THOMPSON AVE, GLENDALE, CA",
	"1135 THOMPSON AVE APT A, GLENDALE, CA",
	"1049 WINCHESTER AVE APT 201, GLENDALE, CA",
	"369 MILFORD ST, GLENDALE, CA",
	"2055 ELEANORE DR, GLENDALE, CA", 
	"1530 E CHEVY CHASE DR STE 207, GLENDALE, CA", 
	"200 W WILSON AVE UNIT 2317, GLENDALE, CA", 
	"410 MILFORD ST APT 205, GLENDALE, CA",
	"1500 S CENTRAL AVE STE 117, GLENDALE, CA",
	"417 E PALMER AVE, GLENDALE, CA",
	"2001 PARCHER DR, GLENDALE, CA",
	"1040 LINDEN AVE APT A, GLENDALE, CA",
	"4529 SAN FERNANDO RD STE I, GLENDALE, CA", 
	"1147 STANLEY AVE APT 5, GLENDALE, CA",
	"2701 SLEEPY HOLLOW PL, GLENDALE, CA", 
	"860 CAVANAGH RD, GLENDALE, CA",
	"2616 CANADA BLVD APT 303, GLENDALE, CA",
	"505 N BRAND BLVD STE 1525, GLENDALE, CA",
	"601 E GLENOAKS BLVD STE 103, GLENDALE, CA",
	"1808 VERDUGO BLVD STE 404, GLENDALE, CA",
	"1169 RAYMOND AVE, GLENDALE, CA", 
	"338 SALEM ST APT 201, GLENDALE, CA",
	"458 W WILSON AVE, GLENDALE, CA",
	"325 W WINDSOR RD APT B, GLENDALE, CA", 
	"1340 ORANGE GROVE AVE, GLENDALE, CA", 
	"2201 HOLLISTER TER, GLENDALE, CA",
	"961 CALLE LA PRIMAVERA, GLENDALE, CA", 
	"1242 MARIPOSA ST APT 1, GLENDALE, CA", 
	"143 N VERDUGO RD APT 5, GLENDALE, CA",
	"400 NESMUTH RD, GLENDALE, CA", 
	"101 N ORANGE ST, GLENDALE, CA",
	"634 RALEIGH ST APT A, GLENDALE, CA", 
	"101 E MOUNTAIN ST, GLENDALE, CA", 
	"1135 THOMPSON AVE, GLENDALE, CA", 
	"1039 IRVING AVE APT A, GLENDALE, CA", 
	"1150 CONCORD ST, GLENDALE, CA", 
	"710 SALEM ST, GLENDALE, CA",
	"1307 E WILSON AVE, GLENDALE, CA",
	"600 W BROADWAY, GLENDALE, CA",
	"1001 ORANGE GROVE AVE, GLENDALE, CA",
	"1545 N VERDUGO RD STE 203, GLENDALE, CA", 
	"1545 N VERDUGO RD STE 230, GLENDALE, CA",
	"1718 LAKE ST, GLENDALE, CA",
	"343 CONCORD ST GLENDALE CA",
	"200 W MILFORD ST APT 604, GLENDALE, CA", 
	"200 E BROADWAY APT 310, GLENDALE, CA", 
	"1200 IRVING AVE, GLENDALE, CA", 
	"1025 RAYMOND AVE, GLENDALE, CA",
	"1201 N PACIFIC AVE STE 104, GLENDALE, CA",
	"130 N BRAND BLVD STE 200, GLENDALE, CA",
	"320 E STOCKER ST APT 101, GLENDALE, CA",
	"505 N BRAND BLVD STE 230, GLENDALE, CA",
	"328 W LOMITA AVE APT 106, GLENDALE, CA", 
	"117 S CEDAR ST, GLENDALE, CA",
	"1439 E MOUNTAIN ST, GLENDALE, CA",
	"1031 THOMPSON AVE APT A, GLENDALE, CA", 
	"1157 WESTERN AVE APT B, GLENDALE, CA",
	"250 W STOCKER ST APT 201, GLENDALE, CA",
	"351 SALEM ST APT 1, GLENDALE, CA", 
	"2801 E CHEVY CHASE DR, GLENDALE, CA",
	"3701 LA CRESCENTA AVE, GLENDALE, CA",
	"101 N VERDUGO RD UNIT 11052, GLENDALE, CA", 
	"611 N BRAND BLVD STE 240, GLENDALE, CA", 
	"249 N GLENDALE AVE, GLENDALE, CA",
	"1160 JUSTIN AVE APT 1, GLENDALE, CA", 
	"5838 SAN FERNANDO RD STE A, GLENDALE, CA",
	"200 S CHEVY CHASE DR, GLENDALE, CA", 
	"1521 E WINDSOR RD APT 12, GLENDALE, CA",
	"3301 CASTERA AVE, GLENDALE, CA", 
	"622 W CALIFORNIA AVE, GLENDALE, CA",
	"118 E PALMER AVE APT 1, GLENDALE, CA", 
	"530 N KENWOOD ST APT 1, GLENDALE, CA", 
	"1500 CAPISTRANO AVE, GLENDALE, CA", 
	"1029 ALLEN AVE APT A, GLENDALE, CA", 
	"1801 CLEVELAND RD, GLENDALE, CA", 
	"1621 S CENTRAL AVE, GLENDALE, CA", 
	"401 E HARVARD ST, GLENDALE, CA", 
	"100 W BROADWAY STE 1050, GLENDALE, CA",
	"412 W BROADWAY FL 3, GLENDALE, CA", 
	"1801 TOPOCK ST, GLENDALE, CA"
	



    ]

# Fetch and geocode addresses
for address in fetch_addresses():
    # Construct the Geocoding API request URL
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}"

    # Make the API request
    response = requests.get(url)
    data = response.json()

    # Parse the response and extract latitude and longitude
    location = data["results"][0]["geometry"]["location"]
    latitude = location["lat"]
    longitude = location["lng"]

    # Check if the address already exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE address = %s", (address,))
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert data into the "users" table
        cursor.execute(
            "INSERT INTO users (address, location) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography)",
            (address, longitude, latitude)
        )
    else:
        # Update the location for an existing address
        cursor.execute(
            "UPDATE users SET location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography WHERE address = %s",
            (longitude, latitude, address)
        )

# Commit changes and close connections
conn.commit()
cursor.close()
conn.close()

