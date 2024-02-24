import os
import dotenv
from psycopg2 import connect, Error
from const import *

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

        self.create_table(TOP_MOVIES_TABLE_NAME, TOP_MOVIES_TABLE_DEFINITION)
        self.create_table(GENRES_TABLE_NAME, GENRES_TABLE_DEFINITION)
        self.create_table(GENRES_MOVIES_TABLE_NAME, GENRES_MOVIES_TABLE_DEFINITION)

    def execute_sql(self, query, values=None, commit=True, fetchmethod=None):
        conn = connect(host=self.DB_HOST, dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASSWORD)
        cursor = conn.cursor()
        if values:
            sql_execute = cursor.execute(query, values)
        else:
            sql_execute = cursor.execute(query)
        fetch_sql = sql_execute
        if fetchmethod == "fetchone":
            fetch_sql = sql_execute.fetchone()
        elif fetchmethod == "fetchall":
            fetch_sql = sql_execute.fetchall()
        conn.commit()
        conn.close()
        return fetch_sql

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

    def check_movie_by_id(self, movie_id):
        """Checks if a movie with the given ID exists in the database."""
        query = f"SELECT * FROM top_movies WHERE id = %s"
        result = self.execute_sql(query, values=(movie_id,), fetchmethod="fetchone")
        return result is not None

    def modify_column_value(self, column_name, new_value, id):
        """Updates a column value for a specific row in a table."""
        query = f"UPDATE top_movies SET {column_name} = %s WHERE id = %s"
        self.execute_sql(query, values=(new_value, id))
