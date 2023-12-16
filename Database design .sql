CREATE TABLE "users" (
  "id" int PRIMARY KEY,
  "email" varchar,
  "username" varchar,
  "password" varchar,
  "role" varchar,
  "created_at" datetime,
  "location_id" point
);

CREATE TABLE "dishes" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "preference_id" int
);

CREATE TABLE "user_review" (
  "dishes_id" int,
  "user_id" int,
  "preferences_id" int,
  "date_posted" datetime
);

CREATE TABLE "external_review" (
  "id" int PRIMARY KEY,
  "review" varchar,
  "review_url" varchar,
  "business_id" int
);

CREATE TABLE "delivery_options" (
  "id" int PRIMARY KEY,
  "app_name" varchar,
  "allows_delivery" bool,
  "delivery_address_form" varchar,
  "delivery_fee" int
);

CREATE TABLE "cuisine" (
  "id" int PRIMARY KEY,
  "cuisine_name" varchar
);

CREATE TABLE "Business_2" (
  "id" int PRIMARY KEY,
  "business_name" varchar,
  "address" varchar,
  "city" varchar,
  "state" varchar,
  "country" varchar,
  "location" point,
  "cuisine" varchar
);

CREATE TABLE "cuisine_dish" (
  "id" int PRIMARY KEY,
  "cuisine_id" int,
  "dish_id" int
);

CREATE TABLE "users_locations" (
  "address" varchar,
  "city" varchar,
  "state" varchar,
  "country" varchar,
  "geospatial_point" point
);

CREATE TABLE "preferences" (
  "id" int PRIMARY KEY,
  "preference_name" varchar
);

CREATE TABLE "open_hours" (
  "id" int PRIMARY KEY,
  "day_of_week" varchar,
  "start_time" datetime,
  "end_time" datetime
);

CREATE TABLE "Business_open_hours" (
  "id" int PRIMARY KEY,
  "business_id" int,
  "open_hours_id" int
);

CREATE TABLE "Business_cuisine" (
  "business_id" int,
  "cuisine_id" int
);

CREATE TABLE "User_review" (
  "id" int PRIMARY KEY,
  "user_id" int,
  "dish_id" int,
  "taste_rating" int,
  "preparation_time_rating" int,
  "friendliness_to_restrictions" int,
  "portion_rating" int,
  "dish_reviews" varchar,
  "price" float
);

ALTER TABLE "dishes" ADD FOREIGN KEY ("preference_id") REFERENCES "preferences" ("id");

ALTER TABLE "user_review" ADD FOREIGN KEY ("dishes_id") REFERENCES "dishes" ("id");

ALTER TABLE "user_review" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_review" ADD FOREIGN KEY ("preferences_id") REFERENCES "preferences" ("id");

ALTER TABLE "external_review" ADD FOREIGN KEY ("business_id") REFERENCES "Business_2" ("id");

ALTER TABLE "cuisine_dish" ADD FOREIGN KEY ("cuisine_id") REFERENCES "cuisine" ("id");

ALTER TABLE "cuisine_dish" ADD FOREIGN KEY ("dish_id") REFERENCES "dishes" ("id");

ALTER TABLE "Business_open_hours" ADD FOREIGN KEY ("business_id") REFERENCES "Business_2" ("id");

ALTER TABLE "Business_open_hours" ADD FOREIGN KEY ("open_hours_id") REFERENCES "open_hours" ("id");

ALTER TABLE "Business_cuisine" ADD FOREIGN KEY ("business_id") REFERENCES "Business_2" ("id");

ALTER TABLE "Business_cuisine" ADD FOREIGN KEY ("cuisine_id") REFERENCES "cuisine" ("id");

ALTER TABLE "User_review" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "User_review" ADD FOREIGN KEY ("dish_id") REFERENCES "dishes" ("id");
