import requests
import json
import time

# TMDB API key. 
API_KEY = "8341ad44a87f2c65829622f523b0e559"

# Base URL for the TMDB API
BASE_URL = "https://api.themoviedb.org/3/movie/top_rated"

# Total number of movies to retrieve (adjust based on API rate limits)
NUM_MOVIES = 40

# List to store movie data
movies = []

# Number of pages to fetch (calculate based on NUM_MOVIES and results per page)
RESULTS_PER_PAGE = 20
PAGES = NUM_MOVIES // RESULTS_PER_PAGE + 1

# Loop through pages, making API calls and collecting data
for page in range(1, PAGES + 1):
    params = {"api_key": API_KEY, "page": page}
    response = requests.get(BASE_URL, params=params)

    # Check for successful response
    if response.status_code == 200:
        data = json.loads(response.text)
        movies.extend(data["results"])

        # Implement rate limiting to avoid exceeding API limits
        time.sleep(2)  # Adjust sleep time as needed based on rate limits and API usage
    else:
        # Handle error cases (e.g., API key issues, rate limits exceeded)
        print(f"Error retrieving data for page {page}: {response.status_code}")
        break

# Format movie data for easy consumption and display
formatted_movies = []
for movie in movies:
    info = {
        "title": movie["title"],
        "release_date": movie["release_date"],
        "vote_average": movie["vote_average"],
        "overview": movie["overview"],
        "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else None
    }
    formatted_movies.append(info)

# Print or use the formatted movie data
print(formatted_movies)  # Or save to a file, display in a table, etc.
