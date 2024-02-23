import requests
import json
import time
import os

# Replace with your actual TMDB API key
API_KEY = "8341ad44a87f2c65829622f523b0e559"

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

# Target directory and filename
OUTPUT_DIR = "./data/"
OUTPUT_FILE_MOVIES = "top_movies.json"
OUTPUT_FILE_GENRES = "genres.json"
OUTPUT_FILE_MG = "mg.json"
def save_data_to_json(data, output_dir, output_file):
    """Saves formatted movie data to a JSON file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, output_file), "w") as f:
        json.dump(data, f, indent=4)

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
    """Cleans and extracts specific columns from movie data."""
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
            "original_title": movie.get("original_title"),
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

def save_genres_to_json(genres):
    """Saves genre data to a JSON file."""
    with open("genres.json", "w") as f:
        json.dump(genres, f, indent=4)

if __name__ == "__main__":
    movie_data = get_all_movie_data()
    cleaned_data = clean_data(movie_data, [
    "id","genre_ids", "original_language", "original_title", "overview",
    "popularity", "release_date", "title", "vote_average", "vote_count"
    ])
    movies, movie_genres= split_data_into_tables(cleaned_data)
    save_data_to_json(movies, OUTPUT_DIR, OUTPUT_FILE_MOVIES)
    save_data_to_json(movie_genres, OUTPUT_DIR, OUTPUT_FILE_MG)
    print(f"Successfully saved top {NUM_MOVIES} movies to {os.path.join(OUTPUT_DIR, OUTPUT_FILE_MOVIES)}")

    all_genres = get_all_genres()
    save_data_to_json(all_genres, OUTPUT_DIR, OUTPUT_FILE_GENRES)
    print(f"Successfully saved genres to {os.path.join(OUTPUT_DIR, OUTPUT_FILE_GENRES)}")
