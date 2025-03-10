# Import the sqlite3 module to interact with SQLite databases
import sqlite3

# Define the path to the high scores database file
DB_PATH = "high_scores.db"

# Define a function to retrieve the top N scores from the high_scores table
def get_top_scores(limit=3):
    # Establish a connection to the database file
    conn = sqlite3.connect(DB_PATH)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Execute SQL to select the top N scores, ordered descending, with a parameter for the limit
    cursor.execute("SELECT score FROM high_scores ORDER BY score DESC LIMIT ?", (limit,))
    # Fetch all matching rows from the query result
    top_scores = cursor.fetchall()
    # Close the database connection to free resources
    conn.close()
    # Extract the score value from each tuple and return as a list
    return [score[0] for score in top_scores]

# Define a function to retrieve the bottom N scores from the high_scores table
def get_bottom_scores(limit=3):
    # Establish a connection to the database file
    conn = sqlite3.connect(DB_PATH)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Execute SQL to select the bottom N scores, ordered ascending, with a parameter for the limit
    cursor.execute("SELECT score FROM high_scores ORDER BY score ASC LIMIT ?", (limit,))
    # Fetch all matching rows from the query result
    bottom_scores = cursor.fetchall()
    # Close the database connection to free resources
    conn.close()
    # Extract the score value from each tuple and return as a list
    return [score[0] for score in bottom_scores]

# Execute the following code only if this script is run directly
if __name__ == "__main__":
    # Get the 3 highest scores by calling get_top_scores
    top_3 = get_top_scores()
    # Print the list of top 3 scores to the console
    print("Top 3 Scores:", top_3)

    # Get the 3 lowest scores by calling get_bottom_scores
    bottom_3 = get_bottom_scores()
    # Print the list of bottom 3 scores to the console
    print("Bottom 3 Scores:", bottom_3)

# Improvement Suggestions:
# 1. Connection Management: Use a context manager (with statement) to handle connections automatically and ensure they close properly.
# 2. Error Handling: Add try-except blocks to handle database connection or query errors gracefully.
# 3. Parameter Validation: Add checks to ensure the limit parameter is a positive integer.
# 4. Database Integration: Consider integrating this with the game to display top/bottom scores in the menu.