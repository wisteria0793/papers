import sqlite3

def check_local_database(db_path='papers.db'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a query to retrieve all records from the 'papers' table
    cursor.execute("SELECT * FROM papers")

    # Fetch all results
    rows = cursor.fetchall()

    # Display the results
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

# Call the function to check the database
check_local_database()
