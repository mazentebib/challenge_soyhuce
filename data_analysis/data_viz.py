import dash
from dash import Output, Input,dcc,html
import plotly.express as px
import pandas as pd
from data_manipulation.sql_functions import sqlManager

""" try:
        df['popularity'] = pd.to_numeric(df['popularity'])
    except ValueError:
        print("Error: Unable to convert 'popularity' column to numeric.")
"""

def process_data(df, min_year, max_year, selected_genres=None):
    try:
        df['popularity'] = pd.to_numeric(df['popularity'])
    except ValueError:
        print("Error: Unable to convert 'popularity' column to numeric.")
    
    if selected_genres:
        if not isinstance(selected_genres, list):
            selected_genres = [selected_genres]
        df = df[df['genre_name'].isin(selected_genres)]

    genre_counts = (
        df.loc[(df['release_year'] >= min_year) & (df['release_year'] <= max_year)]['genre_name']
        .value_counts()  # Count occurrences of each genre for specified years
        .sort_values(ascending=False)  # Sort by descending count
        .head(10)  # Keep the top 10 most popular genres
    )
    return genre_counts

def top_movies(df, min_year, max_year, selected_genres=None):
    # Count the number of entries for each movie ID
    movie_entry_counts = df['movie_id'].value_counts()
    
    # Update popularity by dividing it by the number of entries for each movie
    df['popularity'] = df['popularity'] / df['movie_id'].map(movie_entry_counts)
    
    try:
        df['popularity'] = pd.to_numeric(df['popularity'])
    except ValueError:
        print("Error: Unable to convert 'popularity' column to numeric.")
    
    filtered_df = df[(df['release_year'] >= min_year) & (df['release_year'] <= max_year)]
    
    if selected_genres:
        if not isinstance(selected_genres, list):
            selected_genres = [selected_genres]
        filtered_df = filtered_df[filtered_df['genre_name'].isin(selected_genres)]

    # Sort the DataFrame by popularity in descending order
    filtered_df = filtered_df.sort_values(by='popularity', ascending=False)

    # Select the top 10 movies by popularity
    top_movies = filtered_df.head(10)[['title', 'popularity']]
    return top_movies


manager = sqlManager()

# Create the view if it doesn't exist
manager.create_view()
movies = manager.get_data_from_table("movie_genres_view")

df = pd.DataFrame(movies, columns=["movie_id", "title", "original_title", "vote_average", "popularity", "genre_name", "release_year"])

min_year = df['release_year'].min()
max_year = df['release_year'].max()

genre_counts = process_data(df.copy(), min_year, max_year)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dcc.RangeSlider(
        id="year-range",
        min=min_year,
        max=max_year,
        value=[min_year, max_year],
        marks={str(min_year): str(min_year), str(max_year): str(max_year)}
    ),
dcc.Dropdown(
    id='genre-dropdown',
    options=[{'label': genre, 'value': genre} for genre in df['genre_name'].unique()],
    value="Drama",  # Set the default selected genre to "Drama"
    multi=True,
    placeholder="Select Genres"
)
,
    dcc.Graph(
        id="pie-chart"
    ),
    dcc.Graph(
        id="bar-chart"
    ),
    # Update total movie count based on selected years and genres
    html.Div(
        id="total-movies",
        children=[f"Total number of Movies: {df['movie_id'].nunique()}"],
        style={"fontSize": 12, "marginTop": 20}
    )
])


@app.callback(
    [Output("pie-chart", "figure"), Output("bar-chart", "figure"), Output("total-movies", "children")],
    [Input("year-range", "value"), Input("genre-dropdown", "value")]
)
def update_chart_and_total(year_range, selected_genres):
    min_year, max_year = year_range
    genre_counts = process_data(df.copy(), min_year, max_year, selected_genres)

    # Update total movies for the selected range and genres
    filtered_df = df[(df['release_year'] >= min_year) & (df['release_year'] <= max_year)]
    if selected_genres:
        if not isinstance(selected_genres, list):
            selected_genres = [selected_genres]
        filtered_df = filtered_df[filtered_df['genre_name'].isin(selected_genres)]
    total_movies = filtered_df['movie_id'].nunique()

    # Calculate total movies for the entire range if no genres are selected
    if not selected_genres:
        total_movies = df[(df['release_year'] >= min_year) & (df['release_year'] <= max_year)]['movie_id'].nunique()

    # Create pie chart
    pie_chart_data = {
        "data": [
            {
                "values": genre_counts.values,
                "labels": genre_counts.index.to_list(),
                "type": "pie",
                "textinfo": "percent",
                "textposition": "outside",
                "startangle": 140,
            }
        ],
        "layout": {
            "title": f"Most Popular Genres ({min_year} - {max_year})" if not selected_genres else f"Most Popular Genres ({min_year} - {max_year}) for {', '.join(selected_genres)}",
            "showlegend": True,
            "legend": {"title": "Genre", "x": 1.1, "y": 1}
        }
    }

    # Create bar chart
    top_movies_data = top_movies(df.copy(), min_year, max_year, selected_genres)

    bar_chart_data = {
        "data": [
            {
                "x": top_movies_data['popularity'],
                "y": top_movies_data['title'],
                "type": "bar",
                "orientation": "h",
                "hoverinfo": "none"  

            }
        ],
        "layout": {
            "title": f"Most Popular Movies ({min_year} - {max_year})" if not selected_genres else f"Most Popular Movies ({min_year} - {max_year}) for {', '.join(selected_genres)}",
            "xaxis": {"title": "Popularity"},
            "yaxis": {"title": ""},
            "margin": {"l": 150},
            "barmode": "stack"  # Ensure all bars are displayed without overlap

        }
    }

    # Return empty string if no genres selected
    total_movies_info = f"Total number of Movies: {total_movies}"

    return pie_chart_data, bar_chart_data, total_movies_info




if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)
    print("Visualization complete!")