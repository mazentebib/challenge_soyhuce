CREATE DATABASE IF NOT EXISTS '${POSTGRES_DB}' OWNER '${POSTGRES_USER}';

CREATE USER IF NOT EXISTS movies_user WITH PASSWORD '${DATABASE_PASSWORD}';

GRANT ALL PRIVILEGES ON DATABASE movies TO movies_user;

CREATE TABLE IF NOT EXISTS top_movies (
  id SERIAL PRIMARY KEY,
  original_language VARCHAR(255),
  original_title VARCHAR(255),
  overview TEXT,
  popularity NUMERIC,
  release_date DATE,
  title VARCHAR(255),
  video BOOLEAN,
  vote_average NUMERIC,
  vote_count INTEGER
);

CREATE TABLE IF NOT EXISTS genres (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS genres_movies (
  movie_id INTEGER REFERENCES top_movies(id) ON DELETE CASCADE,
  genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
  PRIMARY KEY (movie_id, genre_id)
);

COMMIT;
