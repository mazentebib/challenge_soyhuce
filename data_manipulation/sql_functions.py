#!/usr/bin/python3
import os
import dotenv
from psycopg2 import connect, Error
from data_manipulation.const import *


# Load environment variables from `.env` file (if applicable)
dotenv.load_dotenv()

# Function to execute SQL queries with error handling
class sqlManager:
    """
    SQL Manager class 
    """
    def __init__(self):
        dotenv.load_dotenv()
        # Database connection details 
        self.DB_HOST = os.getenv("POSTGRES_HOST")
        self.DB_NAME = os.getenv("POSTGRES_DB")
        self.DB_USER = os.getenv("POSTGRES_USER")
        self.DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.DB_PORT = os.getenv("POSTGRES_PORT")

        self.create_table(TOP_MOVIES_TABLE_NAME, TOP_MOVIES_TABLE_DEFINITION)
        self.create_table(GENRES_TABLE_NAME, GENRES_TABLE_DEFINITION)
        self.create_table(GENRES_MOVIES_TABLE_NAME, GENRES_MOVIES_TABLE_DEFINITION)

    def execute_sql(self, query, values=None, commit=True, fetchmethod=None):
        conn = connect(host=self.DB_HOST, dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASSWORD, port=self.DB_PORT)
        try:
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            if fetchmethod == "fetchone":
                fetch_sql = cursor.fetchone()
            elif fetchmethod == "fetchall":
                fetch_sql = cursor.fetchall()
            else:
                fetch_sql = cursor
            conn.commit()
            conn.close()
            return fetch_sql
        except Exception as e:
            print("Error executing SQL query:", e)
            return None

# Function to create a table based on the provided definition
    def create_table(self, table_name, table_definition):
        query = f"CREATE TABLE IF NOT EXISTS {table_definition}"
        self.execute_sql(query)
        print(f"Table '{table_name}' created successfully.")

    def insert_data_to_table(self, table_name, values: tuple):
        """
        Inserts a new item into the specified SQL table.
        """
        placeholders = ', '.join(['%s'] * len(values))
        query = f"""
            INSERT INTO {table_name} 
            VALUES ({placeholders})
            ON CONFLICT DO NOTHING;
        """
        self.execute_sql(query, values)

    def create_view(self):
        """Creates a view combining movies, genres, and their relationships."""
        query = """
            CREATE OR REPLACE VIEW movie_genres_view AS
            SELECT m.id AS movie_id, m.title, m.original_title, m.vote_average, m.popularity,
                g.name AS genre_name, EXTRACT(YEAR from m.release_date ) as release_year 
            FROM top_movies AS m
            INNER JOIN genres_movies AS gm ON m.id = gm.movie_id
            INNER JOIN genres AS g ON gm.genre_id = g.id;
        """
        self.execute_sql(query)
        print("View created successfully!")

    def get_data(self, view):
        """Fetches all movies with their genres from the view."""
        query = f"""SELECT * FROM {view}; """
        data = self.execute_sql(query, fetchmethod="fetchall")
        return data