
#database.py
# Import the sqlite3 module to interact with SQLite databases
import sqlite3

# Define the path to the high scores database file
DB_PATH = "high_scores.db"

# Initialize the database by creating the high_scores table if it doesn't exist
def init_db():
    # Establish a connection to the database file
    conn = sqlite3.connect(DB_PATH)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Execute SQL to create the high_scores table with id, score, and date columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Commit the changes to the database
    conn.commit()
    # Close the database connection to free resources
    conn.close()

# Add a new score to the high_scores table
def add_score(score):
    # Establish a connection to the database file
    conn = sqlite3.connect(DB_PATH)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Execute SQL to insert the score into the high_scores table
    cursor.execute("INSERT INTO high_scores (score) VALUES (?)", (score,))
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()

# Retrieve the highest score from the high_scores table
def get_high_score():
    # Establish a connection to the database file
    conn = sqlite3.connect(DB_PATH)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Execute SQL to select the maximum score from the high_scores table
    cursor.execute("SELECT MAX(score) FROM high_scores")
    # Fetch the first result (the maximum score)
    high_score = cursor.fetchone()[0]
    # Close the database connection
    conn.close()
    # Return the high score, or 0 if no score exists
    return high_score if high_score is not None else 0

# Improvement Suggestions:
# 1. Connection Management: Use a context manager (with statement) to handle connections automatically.
# 2. Error Handling: Add try-except blocks to handle database errors gracefully.
# 3. Top N Scores: Add a function to retrieve the top N scores for display in the game.

# Improvement Suggestions:
# 1. **Connection Management**: Use a context manager (with statement) to handle connections automatically.
# 2. **Error Handling**: Add try-except blocks to handle database errors gracefully.
# 3. **Top N Scores**: Add a function to retrieve the top N scores for display in the game.