import pandas as pd
import matplotlib.pyplot as plt
from sql_functions import sqlManager

""" try:
        df['popularity'] = pd.to_numeric(df['popularity'])
    except ValueError:
        print("Error: Unable to convert 'popularity' column to numeric.")
"""

def create_pie_chart(df, min_year, max_year):
    """
    Creates a pie chart showing the most popular genres among the top 10 movies
    within the specified year range.

    Args:
        df (pd.DataFrame): The DataFrame containing movie data.
        min_year (int): The minimum year to consider.
        max_year (int): The maximum year to consider.

    Returns:
        None
    """
    try:
        df['popularity'] = pd.to_numeric(df['popularity'])
    except ValueError:
        print("Error: Unable to convert 'popularity' column to numeric.")
    genre_counts = (
        df['genre_name']
        .value_counts()  # Count occurrences of each genre
        .sort_values(ascending=False)  # Sort by descending count
        .head(10)  # Keep the top 10 most popular genres
    )


    # Total number of unique movies
    num_unique_movies = df['movie_id'].nunique()

    # Create the pie chart
    fig, ax1 = plt.subplots(figsize=(8, 8))

    # Pie chart for genres
    wedges, texts, autotexts = ax1.pie(genre_counts, autopct='%1.1f%%', startangle=140)  # Customize appearance
    ax1.legend(wedges, genre_counts.index.to_list(), title="Genre", loc="upper left", bbox_to_anchor=(1.15, 1))
    print (f"count of genres : {genre_counts}")

    ax1.set_title("Most Popular Genres")
    ax1.axis('equal')

    # Text for total number of movies (adjust position as needed)
    ax2 = fig.add_subplot(111, frameon=False)  # Invisible axes for text placement
    print (f"Total number of Movies: {num_unique_movies}")
    ax2.text(0.95, 0.15, f"Total number of Movies: {num_unique_movies}", ha='left', va='top', fontsize=12)
    ax2.axis("off")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":

    manager = sqlManager()

    # Create the view if it doesn't exist
    manager.create_view()
    movies = manager.get_data("movie_genres_view")

    df = pd.DataFrame(movies, columns=["movie_id", "title", "original_title", "vote_average", "popularity", "genre_name", "release_year"])
    """
    while True:
        try:
            min_year = int(input("Enter the minimum year: "))
            max_year = int(input("Enter the maximum year: "))
            if min_year > max_year:
                print("Invalid input: min year must be less than or equal to max year.")
            else:
                break
        except ValueError:
            print("Invalid input: please enter valid integers.")"""
    create_pie_chart(df, 1960, 2005)

    print("Visualization complete!")

