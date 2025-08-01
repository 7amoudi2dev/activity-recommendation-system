CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(100),
    birth_date DATE,
    machine_name VARCHAR(100),
    username VARCHAR(100),
    temperature FLOAT,
    activity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
