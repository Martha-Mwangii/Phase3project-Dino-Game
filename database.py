#database.py
import sqlite3 # to interact with SQLite databases

# Define the path to the high scores database file
DB_PATH = "high_scores.db"

# Initialize the database by creating the high_scores table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_PATH) #Establishes a connection to the database file
    cursor = conn.cursor()#Create a cursor object to execute SQL commands
    # Execute SQL to create the high_scores table with id, score, and date columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()# Commit the changes to the database
    conn.close()# Close the database connection 

# Add a new score to the high_scores table
def add_score(score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Execute SQL to insert the score into the high_scores table
    cursor.execute("INSERT INTO high_scores (score) VALUES (?)", (score,))
    conn.commit()
    conn.close()

# Retrieve the highest score from the high_scores table
def get_high_score():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(score) FROM high_scores")
    high_score = cursor.fetchone()[0]# Fetch the first result(max score)
    conn.close()# Close the database connection
    return high_score if high_score is not None else 0#Returns the high score or a zero if no score exists
def delete_score(score_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM high_scores WHERE id = ?", (score_id,))
    conn.commit()
    conn.close()

# In database.py
def clear_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS high_scores")  # Drop the table
    cursor.execute('''
        CREATE TABLE high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')  # Recreate the table
    conn.commit()
    conn.close()
    print("High scores cleared and table reset")

# Update a score for a specific ID
def update_score(score_id, new_score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE high_scores SET score = ? WHERE id = ?", (new_score, score_id))
        if cursor.rowcount == 0:
            print(f"Warning: No score found with id {score_id}")
        else:
            conn.commit()
            print(f"Successfully updated score for id {score_id} to {new_score}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
        
'''def delete_score(score_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM high_scores WHERE id = ?", (score_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Warning: No score found with id {score_id}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()'''



'''def clear_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM high_scores")
    conn.commit()
    conn.close()
'''

