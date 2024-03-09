-- Create Table users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR,
    username VARCHAR,
    password VARCHAR,
    role VARCHAR,
    created_at TIMESTAMP,
    users_locations_id INT REFERENCES users_locations(id)
);

-- Create Table dish_name
CREATE TABLE dishes (
    id SERIAL PRIMARY KEY,
    name VARCHAR
);

-- Create Table external_review
CREATE TABLE external_review (
    id SERIAL PRIMARY KEY,
    review INT,
    review_url VARCHAR,
    business_id INT REFERENCES Business(id)
);

-- Create Table users_partitioned
CREATE TABLE users_partitioned (
    CHECK (created_at >= '' AND created_at < '')
) INHERITS (users);

-- Create Table cuisine
CREATE TABLE cuisine (
    id SERIAL PRIMARY KEY,
    cuisine_name VARCHAR
);

-- Create Table user_review_tags
CREATE TABLE user_review_tags (
    id SERIAL PRIMARY KEY,
    user_review_id INT REFERENCES User_review(id),
    tags_id INT REFERENCES tags(id)
);

-- Create Table Business_2
CREATE TABLE Business (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    location POINT
);

-- Create Table Business_dishes
CREATE TABLE Business_dishes (
    id SERIAL PRIMARY KEY,
    dishes_id INT REFERENCES dishes(id),
    business_id INT REFERENCES Business(id)
);

-- Create Table users_locations
CREATE TABLE users_locations (
    id SERIAL PRIMARY KEY,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    geospatial_point POINT
);

-- Create Table open_hours
CREATE TABLE open_hours (
    id SERIAL PRIMARY KEY,
    day_of_week VARCHAR,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- Create Table likes
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    user_review_id INT REFERENCES User_review(id),
    created_at TIMESTAMP
);

-- Create Table tags
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    tag_name VARCHAR
);

-- Create Table Business_open_hours
CREATE TABLE Business_open_hours (
    id SERIAL PRIMARY KEY,
    business_id INT REFERENCES Business(id),
    open_hours_id INT REFERENCES open_hours(id)
);

-- Create Table Business_cuisine
CREATE TABLE Business_cuisine (
    business_id INT REFERENCES Business(id),
    cuisine_id INT REFERENCES cuisine(id)
);

-- Create Table Users_reviews
CREATE TABLE User_review (
    id SERIAL PRIMARY KEY,
    users_id INT REFERENCES users(id),
    business_dish_id INT REFERENCES Business_dishes(id),
    overall_reviews INT,
    taste_rating INT,
    preparation_time_rating INT,
    friendliness_to_restrictions INT,
    portion_rating INT,
    price INT,
    dish_reviews VARCHAR,
    created_at TIMESTAMP
);
---
Sign-in Page

User Profile Retrieval (GET Request):


SELECT username, email, role, created_at
FROM users
WHERE username = 'j';

CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_username_covering ON users(username) INCLUDE (email, role, created_at);


User Authentication (POST Request):

SELECT COUNT(*)
FROM users
WHERE username = '' AND password = '';


---
User Role Update (POST Request):

UPDATE users
SET role = 'new_role'
WHERE username = 'username';

---
User Engagement Analysis (Sample Query):

Analyze user engagement based on sign-up trends and adoption patterns.
-- Example: Partitioning by range
CREATE TABLE users_partitioned (
    CHECK (created_at >= '' AND created_at < '')
) INHERITS (users);

-- Create indexes on the partitioned table as needed
CREATE INDEX idx_created_at_partitioned ON users_partitioned(created_at);


---------
--- Example of indexing user_id column
CREATE INDEX idx_user_reviews_user_id ON user_review(user_id);
User Profile Page:

Posting Reviews:
SELECT  
    taste_rating, 
    preparation_time_rating, 
    portion_rating, 
    price, 
    dish_reviews
FROM 
    user_review
WHERE 
    user_id = 'user_id_her';

---
Like Count on Review: 
CREATE INDEX idx_likes_user_review_id ON likes(user_review_id);

SELECT 
    COUNT(*) AS like_count
FROM 
    likes
WHERE 
    review_id = 'review_id_here';

Reviews liked by a user:
CREATE INDEX idx_likes_user_id ON likes(user_id);
SELECT 
    ur.id AS review_id,
    ur.overall_rating,
    ur.taste_rating,
    ur.preparation_time_rating,
    ur.friendliness_to_restrictions,
    ur.portion_rating,
    ur.price,
    ur.dish_reviews,
    ur.created_at
FROM 
    user_review ur
JOIN 
    likes l ON ur.id = l.user_review_id
WHERE 
    l.user_id = 'user_id_here';



-------------------
Explore Page:

-- Index on business_2_dish_name table
CREATE INDEX idx_business_dish_name ON business_2_dish_name(business_2_id, dish_name_id);

-- Index on user_review table
CREATE INDEX idx_user_review_business_2_dish_name_id ON user_review(business_2_dish_name_id);

Identify Relevant Dish-Business Pairs: 
SELECT
    bdjn.business_id,
    bdjn.dish_id
FROM
    user_review ur
JOIN
    business_2_dish_name bdjn ON ur.business_2_dish_name_id = bdjn.id
JOIN
    likes l ON ur.id = l.user_review_id
GROUP BY
    bdjn.business_id, bdjn.dish_id
ORDER BY
    AVG(ur.overall_rating) DESC, COUNT(l.id) DESC
LIMIT 10;




Retrieve Most Liked Review for a Specific Dish-Business Pair:

SELECT 
    user_review.id AS review_id,
    user_review.overall_review AS overall_rating,
    user_review.taste_rating,
    user_review.preparation_time_rating,
    user_review.friendliness_to_restrictions AS friendliness_rating,
    user_review.portion_rating,
    user_review.price AS price_rating,
    user_review.dish_reviews,
    user_review.created_at,
    COUNT(likes.id) AS likes_count
FROM 
    user_review
JOIN 
    business_2_dish_name ON user_review.business_2_dish_name_id = business_2_dish_name.id
LEFT JOIN 
    likes ON user_review.id = likes.user_review_id
WHERE 
    business_2_dish_name.business_2_id = '230'
    AND business_2_dish_name.dish_name_id = '27'
GROUP BY 
    user_review.id
ORDER BY 
    user_review.created_at DESC, likes_count DESC
LIMIT 1;


Most Recent Reviews Section: 

Explain Analyze
SELECT 
    user_review.id,
    user_review.overall_review,
    user_review.taste_rating,
    user_review.preparation_time_rating,
    user_review.friendliness_to_restrictions,
    user_review.portion_rating,
    user_review.price,
    user_review.dish_reviews,
    user_review.created_at,
    COUNT(likes.id) AS likes_count
FROM 
    user_review
LEFT JOIN 
    likes ON user_review.id = likes.user_review_id
GROUP BY 
    user_review.id
ORDER BY 
    user_review.created_at DESC, likes_count DESC
LIMIT 10;
---
Filtering on Explore Page:

Cuisine-Based Filtering
CREATE INDEX idx_cuisine_cuisine_name ON cuisine (cuisine_name);
CREATE INDEX idx_business_dish_name_business_id ON business_2_dish_name (business_2_id);
CREATE INDEX idx_business_dish_name_dish_name_id ON business_2_dish_name (dish_name_id);
-- Step 1: Get business_id based on desired cuisine
WITH desired_businesses AS (
    SELECT 
        business_2.id
    FROM 
        business_2
    JOIN 
        business_cuisine ON business_2.id = business_cuisine.business_id
    JOIN 
        cuisine ON business_cuisine.cuisine_id = cuisine.id
    WHERE 
        cuisine.cuisine_name = 'Italian'
)
-- Step 2: Get dishes associated with the business from the junction table
, business_dishes AS (
    SELECT 
        bdjn.business_2_id,
        bdjn.dish_name_id
    FROM 
        business_2_dish_name bdjn
    JOIN 
        desired_businesses ON bdjn.business_2_id = desired_businesses.id
)
-- Step 3: Get reviews from the user_review table based on dishes
SELECT 
    ur.id AS review_id,
    ur.overall_review,
    ur.taste_rating,
    ur.preparation_time_rating,
    ur.friendliness_to_restrictions,
    ur.portion_rating,
    ur.price,
    ur.dish_reviews,
    ur.created_at
FROM 
    user_review ur
JOIN 
    business_dishes ON ur.business_2_dish_name_id = business_dishes.dish_name_id
ORDER BY 
    ur.created_at DESC
LIMIT 10;
Results:


Operating Hours Filtering:
CREATE INDEX idx_business_open_hours_business_id ON business_open_hours (business_id);
CREATE INDEX idx_day_day_name ON day (day_name);
CREATE INDEX idx_business_open_hours_business_day ON business_open_hours (business_id, day_id);
-- Step 1: Get business_id based on desired operating hours
WITH desired_businesses AS (
    SELECT 
        b2.id
    FROM 
        business_2 b2
    JOIN 
        business_open_hours boh ON b2.id = boh.business_id
    JOIN 
        day d ON boh.day_id = d.id
    WHERE 
        d.day_name = 'Monday'  -- Adjust based on the desired day
        AND boh.opening_time <= '08:00:00'  -- Adjust based on the desired opening time
        AND boh.closing_time >= '12:00:00'  -- Adjust based on the desired closing time
)
-- Step 2: Get dishes associated with the business from the junction table
, business_dishes AS (
    SELECT 
        bdjn.business_id,
        bdjn.dish_name_id
    FROM 
        business_2_dish_name bdjn
    JOIN 
        desired_businesses ON bdjn.business_id = desired_businesses.id
)
-- Step 3: Get reviews from the user_review table based on dishes
SELECT 
    ur.id AS review_id,
    ur.overall_review,
    ur.taste_rating,
    ur.preparation_time_rating,
    ur.friendliness_to_restrictions,
    ur.portion_rating,
    ur.price,
    ur.dish_reviews,
    ur.created_at
FROM 
    user_review ur
JOIN 
    business_dishes ON ur.business_2_dish_name_id = business_dishes.dish_name_id
ORDER BY 
    ur.created_at DESC
LIMIT 10;



Tag-based Filtering
SELECT 
    user_reviews.review_id,
    user_reviews.overall_rating,
    user_reviews.taste_rating,
    user_reviews.preparation_time_rating,
    user_reviews.friendliness_rating,
    user_reviews.portion_rating,
    user_reviews.price_rating,
    user_reviews.dish_reviews,
    user_reviews.created_at
FROM 
    user_reviews
JOIN 
    tags ON user_reviews.tag_id = tags.tag_id
WHERE 
    tags.tag_name = 'desired_tag';


Proximity-based Searching (both map and filtering):

CREATE INDEX idx_business_location ON business_2 USING GIST(location);
CREATE INDEX idx_users_location ON users_locations USING GIST(geographical_point);

-Get businesses on the map close to user:
SELECT 
    business_2.id,
    business_2.business_name,
    business_2.address,
    ST_Distance(business_2.location, users_locations.geographical_point) AS distance
FROM 
    business_2
JOIN
    users_locations ON ST_DWithin(business_2.location, users_locations.geographical_point, 500);




-Get Reviews based on user proximity:
-- Step 1: Get business_id based on proximity
WITH nearby_businesses AS (
    SELECT 
        business_2.id
    FROM 
        business_2
    JOIN
        users_locations ON ST_DWithin(business_2.location, users_locations.geographical_point, 500)
)
-- Step 2: Get reviews from the user_review table based on proximity
SELECT 
    ur.id AS review_id,
    ur.overall_review,
    ur.taste_rating,
    ur.preparation_time_rating,
    ur.friendliness_to_restrictions,
    ur.portion_rating,
    ur.price,
    ur.dish_reviews,
    ur.created_at
FROM 
    user_review ur
JOIN 
    business_2 ON ur.business_2_dish_name_id = business_2.id
JOIN 
    nearby_businesses ON ur.business_2_dish_name_id = nearby_businesses.id
ORDER BY 
    ur.created_at DESC
LIMIT 10;
-- Step 1: Get business_id based on proximity
WITH nearby_businesses AS (
    SELECT 
        business_2.id
    FROM 
        business_2
    JOIN
        users_locations ON ST_DWithin(business_2.location, users_locations.geographical_point, 500)
)
-- Step 2: Get reviews from the user_review table based on proximity
SELECT 
    ur.id AS review_id,
    ur.overall_review,
    ur.taste_rating,
    ur.preparation_time_rating,
    ur.friendliness_to_restrictions,
    ur.portion_rating,
    ur.price,
    ur.dish_reviews,
    ur.created_at
FROM 
    user_review ur
JOIN 
    business_2 ON ur.business_2_dish_name_id = business_2.id
JOIN 
    nearby_businesses ON ur.business_2_dish_name_id = nearby_businesses.id
ORDER BY 
    ur.created_at DESC
LIMIT 10;


Rating-Based Filtering: 

SELECT 
    user_review.id,
    user_review.overall_review,
    user_review.taste_rating,
    user_review.preparation_time_rating,
    user_review.friendliness_to_restrictions,
    user_review.portion_rating,
    user_review.price,
    user_review.dish_reviews,
    user_review.created_at
FROM 
    user_reviews
WHERE 
    user_reviews.overall_rating >= 'desired_minimum_rating';

---
User Review Card
SELECT 
    user_review.id,
    user_review.overall_rating,
    user_review.taste_rating,
    user_review.preparation_time_rating,
    user_review.friendliness_to_restrictions,
    user_review.portion_rating,
    user_review.price,
    user_review.dish_reviews,
    user_review.created_at,
    users.username
FROM 
    user_reviews
JOIN 
    users ON user_reviews.user_id = users.id
WHERE 
    user_reviews.id = 'desired_review_id';
---
Business Page: 

Most Like User Review for Menu Item:
SELECT 
    ur.user_id,
    ur.overall_review,
    ur.taste_rating,
    ur.preparation_time_rating,
    ur.friendliness_to_restrictions,
    ur.portion_rating,
    ur.price,
    ur.dish_reviews,
    ur.created_at,
    u.username
FROM 
    user_review ur
JOIN 
    business_2_dish_name bdjn ON ur.business_2_dish_name_id = bdjn.id
JOIN 
    users u ON ur.user_id = u.id
LEFT JOIN
    likes l ON ur.id = l.user_review_id
WHERE 
    bdjn.business_2_id = 'desired_business_id'
ORDER BY 
    COUNT(l.id) DESC
LIMIT 
    6;


External Review:
SELECT 
    external_reviews.external_review_id,
    external_reviews.overall_rating,
    external_reviews.review_link
FROM 
    external_reviews
WHERE 
    external_reviews.business_id = 'desired_business_id';

