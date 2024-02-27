# Movie Database Scraper

This project is designed to scrape data from [The Movie Database (TMDb)](https://www.themoviedb.org/documentation/api) and inject it into a PostgreSQL database for further analysis and visualization.

## How to Run

To run the project, make sure you have Docker and Docker Compose installed on your system.

1. **Clone Repository**: Clone this repository to your local machine.

2. **Set Up Environment Variables**: Before proceeding, make sure you have your own TMDb API key. You can obtain one by [creating an account](https://www.themoviedb.org/signup) on TMDb and generating an API key from the [API settings page](https://www.themoviedb.org/settings/api). Once you have your API key, create a `.env` file in the root directory of the project and set the following environment variables:
    ```plaintext
    POSTGRES_DB=movie_db
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=password
    TMDB_API_KEY=your_tmdb_api_key
    ```

3. **Build and Start Docker Containers**: Run the following command in your terminal:
    ```bash
    ./run.sh
    ```
   This script will handle building the Docker images and starting the containers.

## Docker Setup

The project consists of two Docker services:

- **movies_db**: PostgreSQL database container.
- **movie_scraper**: Python container responsible for scraping movie data from TMDb and injecting it into the database.

## Directory Structure

- **data_manipulation**: Contains scripts for manipulating the retrieved data.
- **data_analysis**: Contains scripts for data analysis and visualization.
- **database**: Contains Dockerfile for the PostgreSQL database container.
- **requirements.txt**: Python dependencies required for the project.
- **run.sh**: Script to build and launch the Docker containers.

## Docker Configuration

### PostgreSQL Database Container (movies_db)
- **Image**: postgres:latest
- **Exposed Port**: 5432
- **Environment Variables**:
    - POSTGRES_DB: Name of the PostgreSQL database.
    - POSTGRES_USER: Username for PostgreSQL.
    - POSTGRES_PASSWORD: Password for PostgreSQL.
- **Volume**: Mounts `./pgdata` to `/var/lib/postgresql/data` for persistent data storage.

### Movie Scraper Container (movie_scraper)
- **Image**: Built from `./Dockerfile`.
- **Exposed Port**: 8050
- **Environment Variables**:
    - TMDB_API_KEY: API key for accessing TMDb API.
- **Dependencies**:
    - psycopg2==2.9.9
    - python-dotenv==1.0.1
    - requests==2.31.0
    - pandas==2.2.1
    - plotly==5.19.0
    - dash==2.15.0
    - dash-bootstrap-components==1.5.0
    - dash-core-components==2.0.0
    - dash-html-components==2.0.0
    - dash-table==5.0.0

## Notes
- Make sure to replace placeholders in the `.env` file with your actual database and API credentials.
- The scraper container depends on the database container, so ensure the database container is up and running before starting the scraper container.

Access the dashboard at [http://localhost:8050/](http://localhost:8050/).