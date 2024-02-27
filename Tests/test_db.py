from data_manipulation.sql_functions import sqlManager

def test_sql_operations():
    # Create an instance of sqlManager
    db_manager = sqlManager()

    # Test creating tables
    db_manager.create_table("test_table", "(id SERIAL PRIMARY KEY, name VARCHAR(255))")

    # Test inserting an item into the table
    db_manager.insert_item_to_table("test_table", (1, "John"))

    # Test inserting multiple items into the table
    values_list = [(2, "Alice"), (3, "Bob"), (4, "Eve")]
    db_manager.insert_data_to_table("test_table", values_list)

    # Test creating a view
    db_manager.create_view()

    # Test fetching data from the table/view
    data = db_manager.get_data_from_table("movie_genres_view")
    print("Data from view:")
    print(data)

if __name__ == "__main__":
    test_sql_operations()
