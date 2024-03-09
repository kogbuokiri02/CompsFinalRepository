# Database Project - README

(All the results are in the TXT file) This project aims to create a database schema for a dish-review application, emphasizing user-centric design, efficient data organization, and optimized query performance.

## Dependencies

- Python 3.7 or higher
- PostgreSQL 16 or higher
- pgAdmin 4 (for database management)
- PostGIS extension for PostgreSQL
- Python Faker library (version 8.14.0 used)
- Google Maps Geocoding API (API Key required)

## Installation Steps

### PostgreSQL 16 Installation Steps:

1. Download PostgreSQL 16 from the official website: [PostgreSQL Downloads](https://www.postgresql.org/download/).
2. Follow the installation instructions based on your operating system.
3. During installation, ensure the inclusion of the PostGIS extension.
4. Set up a user and password for the PostgreSQL database.

### Dependencies:


Install the required Python libraries using pip:


pip install -r requirements.txt

## Google Maps Geocoding API Setup

To utilize the Google Maps Geocoding API for geographical data retrieval, follow these steps:

1. Obtain a Google Maps Geocoding API Key from the [Google Cloud Console](https://console.cloud.google.com/).

2. Set the API Key as an environment variable:

   ```bash
   export GOOGLE_MAPS_API_KEY='your-api-key'
## Database Schema and PostGIS

### Database Schema Design

The database schema is designed to handle various entities and their relationships. Refer to the provided [DBDiagram] for an overview of the database structure.

## PostGIS Installation and Configuration

1. Install PostgreSQL 16 (or compatible version) if not already installed. You can download it from the [official PostgreSQL website](https://www.postgresql.org/download/).

2. Install the PostGIS extension for PostgreSQL to enable geospatial capabilities:

   ```bash
   sudo apt-get update
   sudo apt-get install postgis
3. Enable PostGIS on your database by running the following command in the PostgreSQL shell:

	```bash
	CREATE EXTENSION postgis;

4. Verify that PostGIS is installed and functioning correctly:
	```bash
	SELECT PostGIS_Version();

### pgAdmin Setup

1. **Download and Install pgAdmin:**

   Download pgAdmin from the [official website](https://www.pgadmin.org/download/) and follow the installation instructions for your operating system.

2. **Connect to PostgreSQL Database:**

   - Open pgAdmin and click on the "Add New Server" button.
   - Enter the required details:
     - Host: [Your PostgreSQL host]
     - Port: [Port number]
     - Username: [Your username]
     - Password: [Your password]
   - Click "Save" to connect to your PostgreSQL database.
## ER DIAGRAM
Table users {
  id int [pk]
  email varchar
  username varchar
  password varchar
  role varchar
  created_at datetime
  users_locations_id int [ref: > users_locations.id] 
}

Table dishes {
  id int [pk]
  name varchar
}

Table external_review {
  id int [pk]
  review int
  review_url varchar
  business_id int [ref: > Business.id]
}

Table users_partitioned {
  id int [pk]
  //inherits users based on time slot
}

Table cuisine {
  id int [pk]
  cuisine_name varchar
}

Table user_review_tags {
  id int [pk]
  user_review_id int [ref: > User_review.id]
  tags_id int [ref: > tags.id]
}

Table Business {
  id int [pk]
  business_name varchar
  address varchar
  city varchar
  state varchar
  country varchar
  location point
}

Table Business_dishes {
  id int [pk]
  dishes_id int [ref: >dishes.id]
  business_id int [ref: > Business.id]
}

Table users_locations {
  id int [pk]
  address varchar
  city varchar
  state varchar
  country varchar
  geospatial_point point
}

Table open_hours {
  id int [pk]
  day_of_week varchar
  start_time datetime
  end_time datetime
}

Table likes {
  id int [pk]
  user_id int [ref: > users.id]
  user_review_id int [ref: >User_review.id]
  created_at datetime
}

Table tags {
  id int [pk]
  tag_name varchar
}

Table Business_open_hours {
  id int [pk]
  business_id int [ref: > Business.id]
  open_hours_id int [ref: > open_hours.id]
}

Table Business_cuisine {
  business_id int [ref: > Business.id]
  cuisine_id int [ref: > cuisine.id]
}

Table User_review {
  id int [pk]
  users_id int [ref: > users.id]
  business_dish_id int [ref: > Business_dishes.id]
  overall_review int
  taste_rating int
  preparation_time_rating int
  friendliness_to_restrictions int
  portion_rating int
  price_rating int
  dish_reviews varchar
  created_at timestamp
}


