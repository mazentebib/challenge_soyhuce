import requests
import json
import time
import os
import os 
import sys

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
class_directory = os.path.join(parent_directory, 'challenge_soyhuce')
sys.path.append(class_directory)
from data_manipulation.const import *
from data_manipulation.sql_functions import sqlManager

# Replace with your actual TMDB API key
API_KEY = os.getenv("TMDB_API_KEY")

# Ensure API key is set
if not API_KEY:
    raise ValueError("Please set your TMDB API key as an environment variable or in the script.")

# Base URL for the TMDB API
BASE_URL_MOVIES = "https://api.themoviedb.org/3/movie/top_rated"
BASE_URL_GENRES = "https://api.themoviedb.org/3/genre/movie/list"

# Number of movies to retrieve (adjust based on API rate limits)
NUM_MOVIES = 500 

# Calculate pages based on results per page (20 in this case)
RESULTS_PER_PAGE = 20
PAGES = NUM_MOVIES // RESULTS_PER_PAGE + 1

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_all_movie_data():
    """Retrieves and returns all movie data from the API."""
    movies = []

    for page in range(1, PAGES + 1):
        params = {"api_key": API_KEY, "page": page}
        response = requests.get(BASE_URL_MOVIES, params=params)

        if response.status_code == 200:
            data = json.loads(response.text)
            movies.extend(data["results"])
            time.sleep(1)  # Implement respectful rate limiting
        else:
            print(f"Error retrieving data for page {page}: {response.status_code}")
            break

    return movies


def clean_data(data, desired_columns):
    """Cleans and extracts specific columns from movie data"""
    cleaned_data = []

    for movie in data:
        if not movie["adult"]:
            info = {key: movie[key] for key in desired_columns if key in movie}
            cleaned_data.append(info)

    return cleaned_data

def split_data_into_tables(cleaned_data):
    """Splits cleaned data into two tables: movies and movie_genres."""
    movies = []
    movie_genres = []

    for movie in cleaned_data:
        movie_id = movie.pop("id")  # Extract and remove "id" for genre table
        movies.append({
            "id": movie_id,
            "original_language": movie.get("original_language"),
            " kl": movie.get("original_title"),
            "overview": movie.get("overview"),
            "popularity": movie.get("popularity"),
            "release_date": movie.get("release_date"),
            "title": movie.get("title"),
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
        })

        for genre_id in movie.get("genre_ids", []):  # Handle potential missing "genre_ids"
            movie_genres.append({"movie_id": movie_id, "genre_id": genre_id})

    return movies, movie_genres


def get_all_genres():
    """Retrieves and returns genre data from the API."""
    response = requests.get(BASE_URL_GENRES, params={"api_key": API_KEY})

    if response.status_code == 200:
        data = json.loads(response.text)
        return data["genres"]
    else:
        print(f"Error retrieving genres: {response.status_code}")
        return []

if __name__ == "__main__":
    print("Fetching top rated movies from TMDB API...")
    movie_data = get_all_movie_data()
    print("Cleaning movie data...")
    cleaned_data = clean_data(movie_data, [
        "id","genre_ids", "original_language", "original_title", "overview",
        "popularity", "release_date", "title", "vote_average", "vote_count"
    ])
    print("Splitting data into tables...")
    movies, movie_genres = split_data_into_tables(cleaned_data)
    print("Fetching genre data from TMDB API...")
    all_genres = get_all_genres()

    db_manager = sqlManager()

    print("Creating tables in the database...")
    db_manager.create_table(TOP_MOVIES_TABLE_NAME, TOP_MOVIES_TABLE_DEFINITION)
    db_manager.create_table(GENRES_TABLE_NAME, GENRES_TABLE_DEFINITION)
    db_manager.create_table(GENRES_MOVIES_TABLE_NAME, GENRES_MOVIES_TABLE_DEFINITION)

    print("Inserting movie data into the database...")
    movies_values = [tuple(movie.values()) for movie in movies]
    db_manager.insert_data_to_table("top_movies", movies_values)

    print("Inserting genre data into the database...")
    genres_values = [(genre["id"], genre["name"]) for genre in all_genres]
    db_manager.insert_data_to_table("genres", genres_values)

    print("Inserting movie-genre mapping data into the database...")
    movie_genres_values = [tuple(entry.values()) for entry in movie_genres]
    db_manager.insert_data_to_table("genres_movies", movie_genres_values)

    print("Data saved to database successfully!")