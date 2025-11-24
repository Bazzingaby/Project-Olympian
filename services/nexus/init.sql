CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    team_id INT,
    jersey_number INT
);

CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    home_team VARCHAR(255),
    away_team VARCHAR(255),
    date DATE
);

CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES matches(match_id),
    type VARCHAR(50),
    timestamp FLOAT,
    details JSONB
);
