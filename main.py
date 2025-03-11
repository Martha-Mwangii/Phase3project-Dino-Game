#main.py
import pygame
from menu import menu# Import the menu function from the menu module to handle the game menu
from game import game #to run the main game loop
from constants import SCREEN_WIDTH, SCREEN_HEIGHT # for window size
from database import init_db # function from the database module to initialize the high scores database
import sys  # Add this import for sys.exit()

# Define the main function for the game startup
def main():
    pygame.init()#Initialize all pygame modules
    init_db()# Ensure the high scores database is initialized and ready
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#Create the gamwindow with the specified width and height
    # Show the menu and start the game if the menu returns True
    # Check the return value of menu and exit if False
    if not menu(SCREEN, 0):
        pygame.quit()
        sys.exit()  # Explicitly exit the Python process
    game()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

