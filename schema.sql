CREATE TABLE IF NOT EXISTS animals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('Dog', 'Cat', 'Horse', 'Hamster', 'Donkey') NOT NULL,
    name VARCHAR(255),
    birth_date DATE,
    commands JSON
);
cv