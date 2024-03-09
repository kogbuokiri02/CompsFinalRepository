# Database Project - README

This project aims to create a database schema for a dish-review application, emphasizing user-centric design, efficient data organization, and optimized query performance.

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

