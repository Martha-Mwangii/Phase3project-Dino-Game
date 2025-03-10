#main.py
# Import the pygame library for game development functionality
import pygame

# Import the menu function from the menu module to handle the game menu
from menu import menu

# Import the game function from the game module to run the main game loop
from game import game

# Import SCREEN_WIDTH and SCREEN_HEIGHT constants from the constants module for window size
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Import the init_db function from the database module to initialize the high scores database
from database import init_db

# Define the main function to orchestrate the game startup
def main():
    # Initialize all pygame modules
    pygame.init()
    # Ensure the high scores database is initialized and ready
    init_db()
    # Create the game window with the specified width and height
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Show the menu and start the game if the menu returns True
    if menu(SCREEN, 0):
        game()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

# Improvement Suggestions:
# 1. Error Handling: Wrap the main logic in a try-except block to catch and log errors.
# 2. Window Caption: Set a window title using pygame.display.set_caption("Dino Game").
# 3. Menu Integration: Add a main menu with options (e.g., start, quit) before calling menu().

# Improvement Suggestions:
# 1. **Error Handling**: Wrap the main logic in a try-except block to catch and log errors.
# 2. **Window Caption**: Set a window title using pygame.display.set_caption("Dino Game").
# 3. **Menu Integration**: Add a main menu with options (e.g., start, quit) before calling menu().

'''#main.py
import pygame
from menu import menu
from game import game

def main():
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Initialize display here
    if menu(SCREEN, 0):  # Pass SCREEN to menu
        game()

if __name__ == "__main__":
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # Import here to use SCREEN_WIDTH and SCREEN_HEIGHT
    main()'''