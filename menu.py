# Import the pygame library for game development functionality
import pygame
# Import the os module to handle file and directory paths
import os
# Import SCREEN_WIDTH, SCREEN_HEIGHT, DINO_DIR, OTHER_DIR, FONT_PATH, and FONT_SIZE constants from the constants module
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DINO_DIR, OTHER_DIR, FONT_PATH, FONT_SIZE
# Import init_db, add_score, and get_high_score functions from the database module for score management
from database import init_db, add_score, get_high_score

# Define the menu function to display the start or game over screen
def menu(screen, death_count, points=0):
    # Initialize all pygame modules (redundant if called in main.py, kept for standalone testing)
    pygame.init()
    # Load the font for rendering text with the specified size
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
    
    # Load and scale the starting dinosaur image with alpha transparency
    DINO_START = pygame.transform.scale(pygame.image.load(os.path.join(DINO_DIR, "DinoStart.png")).convert_alpha(), (50, 60))
    # Load and scale the game over image with alpha transparency
    GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join(OTHER_DIR, "GameOver.png")).convert_alpha(), (200, 50))
    # Load and scale the reset button image with alpha transparency
    RESET = pygame.transform.scale(pygame.image.load(os.path.join(OTHER_DIR, "Reset.png")).convert_alpha(), (40, 40))

    # Initialize the high scores database
    init_db()
    # Retrieve the current high score from the database
    high_score = get_high_score()

    # Control variable for the menu loop
    run = True
    # Flag to ensure the score is recorded only once per session
    score_recorded = False
    # Print a message to the console indicating the menu loop has started
    print("Menu loop started")

    # Main menu loop
    while run:
        # Fill the screen with a white background
        screen.fill((255, 255, 255))

        # Handle all pygame events
        for event in pygame.event.get():
            # Exit the game and menu if the window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                print("Window closed, exiting menu")
                return False
            # Start or restart the game on any key press
            if event.type == pygame.KEYDOWN:
                print("Key pressed, returning True")
                return True

        # Display the initial menu if no deaths have occurred
        if death_count == 0:
            # Render the "Press any Key to Start" text in black
            text = FONT.render("Press any Key to Start", True, (0, 0, 0))
            # Create a rectangle centered on the screen for the text
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            # Draw the text on the screen
            screen.blit(text, text_rect)
            # Create a rectangle for the starting dinosaur image, offset above center
            dino_rect = DINO_START.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140))
            # Draw the starting dinosaur image on the screen
            screen.blit(DINO_START, dino_rect)
        else:
            # Record the score if points are greater than 0 and not yet recorded
            if points > 0 and not score_recorded:
                # Add the current score to the database
                add_score(points)
                # Update the high score after adding the new score
                high_score = get_high_score()
                # Set the flag to prevent further recording
                score_recorded = True

            # Create a rectangle for the game over image, centered above the middle
            game_over_rect = GAME_OVER.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            # Draw the game over image on the screen using the top-left corner of the rectangle
            screen.blit(GAME_OVER, game_over_rect.topleft)
            # Render the player's score text in black
            score_text = FONT.render(f"Your Score: {points}", True, (0, 0, 0))
            # Create a rectangle centered below the game over image for the score
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            # Draw the score text on the screen
            screen.blit(score_text, score_rect)
            # Render the high score text in black
            high_score_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
            # Create a rectangle centered below the score for the high score
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            # Draw the high score text on the screen
            screen.blit(high_score_text, high_score_rect)
            # Render the restart instruction text in black
            restart_text = FONT.render("Press any Key to Restart", True, (0, 0, 0))
            # Create a rectangle centered below the high score for the restart text
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            # Draw the restart text on the screen
            screen.blit(restart_text, restart_rect)
            # Create a rectangle for the reset image, centered below the restart text
            reset_rect = RESET.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            # Draw the reset image on the screen
            screen.blit(RESET, reset_rect)

        # Update the full display window to the screen
        pygame.display.update()

    # Return False if the loop exits without a key press (e.g., window closed)
    return False

# Improvement Suggestions:
# 1. **Remove Redundant pygame.init()**: Remove this call since main.py initializes Pygame, avoiding potential reinitialization issues.
# 2. **Constants for Positions**: Define constants for text and image positions (e.g., START_TEXT_Y) to simplify adjustments.
# 3. **Error Handling**: Add try-except for image loading to handle missing files gracefully.
# 4. **Display Top Scores**: Enhance the game over screen with the top 3 scores using a new database function.

'''import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, RUNNING, GAME_OVER_IMAGE, FONT_PATH, FONT_SIZE, DINO_DIR, OTHER_DIR

class GameState:
    def __init__(self):
        self.high_score = 0

game_state = GameState()

# ... (previous imports and GameState class remain unchanged)

def menu(screen, death_count, points=0):
    pygame.init()  # Ensure initialization (though redundant if called in main)
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
    
    # Load images inside the function
    DINO_START = pygame.image.load(os.path.join(DINO_DIR, "DinoStart.png")).convert_alpha()
    GAME_OVER = pygame.image.load(GAME_OVER_IMAGE).convert_alpha()
    RESET = pygame.image.load(os.path.join(OTHER_DIR, "Reset.png")).convert_alpha()

    # Scale images
    DINO_START = pygame.transform.scale(DINO_START, (50, 60))
    GAME_OVER = pygame.transform.scale(GAME_OVER, (200, 50))
    RESET = pygame.transform.scale(RESET, (40, 40))

    run = True
    print("Menu loop started")  # Keep this to indicate menu start

    while run:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                print("Window closed, exiting menu")  # New debug for window close
                return False
            if event.type == pygame.KEYDOWN:
                print("Key pressed, returning True")  # Keep this for key press
                return True

        if death_count == 0:
            text = FONT.render("Press any Key to Start", True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            dino_rect = DINO_START.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140))
            screen.blit(DINO_START, dino_rect)
        else:
            game_state.high_score = max(game_state.high_score, points)
            game_over_rect = GAME_OVER.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(GAME_OVER, game_over_rect.topleft)
            score_text = FONT.render(f"Score: {points}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(score_text, score_rect)
            high_score_text = FONT.render(f"High Score: {game_state.high_score}", True, (0, 0, 0))
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(high_score_text, high_score_rect)
            restart_text = FONT.render("Press any Key to Restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            screen.blit(restart_text, restart_rect)
            reset_rect = RESET.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            screen.blit(RESET, reset_rect)

        pygame.display.update()

    return False

'''

