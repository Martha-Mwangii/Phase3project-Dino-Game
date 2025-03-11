#test_db.py
import sqlite3

# Define the path to the high scores database file
DB_PATH = "high_scores.db"

# Define a function to retrieve the top N scores from the high_scores table
def get_top_scores(limit=3):
    conn = sqlite3.connect(DB_PATH)# Establish a connection to the database file
    cursor = conn.cursor()# Create a cursor object to execute SQL commands
    # Execute SQL to select the top N scores, ordered descending, with a parameter for the limit
    cursor.execute("SELECT score FROM high_scores ORDER BY score DESC LIMIT ?", (limit,))
    top_scores = cursor.fetchall()# Fetch all matching rows from the query result
    conn.close()# Close the database connection 
    return [score[0] for score in top_scores]# Extract the score value from each tuple and return as a list

# Define a function to retrieve the bottom N scores from the high_scores table
def get_bottom_scores(limit=3):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM high_scores ORDER BY score ASC LIMIT ?", (limit,))# bottom scores, ordered ascending
    bottom_scores = cursor.fetchall()
    conn.close()
    return [score[0] for score in bottom_scores]

# Execute the following code only if this script is run directly
if __name__ == "__main__":
    top_3 = get_top_scores()#Get the 3 highest scores by calling get_top_scores
    print("Top 3 Scores:", top_3)# Print the list of top 3 scores to the console

    bottom_3 = get_bottom_scores()
    print("Bottom 3 Scores:", bottom_3)
