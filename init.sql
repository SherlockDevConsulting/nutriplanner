-- Création de la table foods
CREATE TABLE IF NOT EXISTS foods (
    id SERIAL PRIMARY KEY,
    code VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    brands VARCHAR(255),
    serving_quantity INT,
    unit VARCHAR(50),
    raw BOOLEAN,
    energy_serving INT,
    energy_100g INT,
    fiber_serving FLOAT,
    fiber_100g FLOAT,
    salt_serving FLOAT,
    salt_100g FLOAT,
    carbohydrates_100g FLOAT,
    carbohydrates_serving FLOAT,
    fat_100g FLOAT,
    fat_serving FLOAT,
    proteins_100g FLOAT,
    proteins_serving FLOAT
);

-- Création de la table meal_items
CREATE TABLE IF NOT EXISTS meal_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    quantity FLOAT NOT NULL,
    unit VARCHAR(50),
    note VARCHAR(255),
    food_id INT,
    FOREIGN KEY (food_id) REFERENCES foods(id)
);

-- Création de la table meals
CREATE TABLE IF NOT EXISTS meals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Table de relation entre meals et meal_items
CREATE TABLE IF NOT EXISTS meal_item_meal_association (
    meal_id INT,
    meal_item_id INT,
    PRIMARY KEY (meal_id, meal_item_id),
    FOREIGN KEY (meal_id) REFERENCES meals(id),
    FOREIGN KEY (meal_item_id) REFERENCES meal_items(id)
);
