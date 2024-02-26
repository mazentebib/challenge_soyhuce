"""
CONSTANTS PROJECT
"""

TOP_MOVIES_TABLE_NAME = "top_movies"
TOP_MOVIES_TABLE_DEFINITION = """
top_movies (
    id SERIAL PRIMARY KEY,
    original_language VARCHAR(255),
    original_title VARCHAR(255),
    overview TEXT,
    popularity NUMERIC,
    release_date DATE,
    title VARCHAR(255),
    vote_average NUMERIC,
    vote_count INTEGER
);
"""
TOP_MOVIES_TABLE_COLUMNS = (
    "id",  # SERIAL PRIMARY KEY (automatically generated)
    "original_language",
    "original_title",
    "overview",
    "popularity",
    "release_date",
    "title",
    "vote_average",
    "vote_count",
)


GENRES_TABLE_NAME = "genres"
GENRES_TABLE_DEFINITION = """
genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
"""
GENRES_TABLE_COLUMNS = (
    "id",  # SERIAL PRIMARY KEY (automatically generated)
    "name",
)
GENRES_MOVIES_TABLE_COLUMNS = (
    "movie_id",
    "genre_id",
)
GENRES_MOVIES_TABLE_NAME = "genres_movies"
GENRES_MOVIES_TABLE_DEFINITION = """
genres_movies (
    movie_id INTEGER REFERENCES top_movies(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);
"""