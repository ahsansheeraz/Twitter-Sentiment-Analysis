import sqlite3

# Define the database file name
DB_FILE = "users.db"

def setup_database():
    """Create the database and users table if they do not exist."""
    # Connect to the SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the users table if it does not already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database setup complete. Database file: {DB_FILE}")

if __name__ == "__main__":
    setup_database()
