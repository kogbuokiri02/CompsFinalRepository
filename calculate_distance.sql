-- Create function to calculate distance
CREATE OR REPLACE FUNCTION calculate_distance(
    IN user_latitude DOUBLE PRECISION,
    IN user_longitude DOUBLE PRECISION,
    IN business_latitude DOUBLE PRECISION,
    IN business_longitude DOUBLE PRECISION
)
RETURNS DOUBLE PRECISION AS $$
BEGIN
    RETURN 6371 * ACOS(
        SIN(RADIANS(user_latitude)) * SIN(RADIANS(business_latitude)) +
        COS(RADIANS(user_latitude)) * COS(RADIANS(business_latitude)) *
        COS(RADIANS(business_longitude) - RADIANS(user_longitude))
    );
END;
$$ LANGUAGE plpgsql;

BEGIN;

-- Simulate distance calculation between a user and a business
-- Replace :user_id1 and :business_id1 with actual user and business IDs
SELECT
    :user_id1 AS user_id,
    :business_id1 AS business_id,
    calculate_distance(
        (SELECT user_latitude FROM users_locations WHERE location_id = :user_id1),
        (SELECT user_longitude FROM users_locations WHERE location_id = :user_id1),
        (SELECT business_latitude FROM business_2 WHERE id = :business_id1),
        (SELECT business_longitude FROM business_2 WHERE id = :business_id1)
    ) AS distance_km;

COMMIT;
