-- Create tables with appropriate data types and constraints
CREATE TABLE top_movies (
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

CREATE TABLE genres (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE genres_movies (
  movie_id INTEGER REFERENCES top_movies(id) ON DELETE CASCADE,
  genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
  PRIMARY KEY (movie_id, genre_id)
);

COMMIT;
