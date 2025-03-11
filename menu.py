#menu.py
import pygame
import os
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DINO_DIR, OTHER_DIR, FONT_PATH, FONT_SIZE
from database import init_db, add_score, get_high_score, clear_scores # Import these functions from database module for score management

# Define the menu function to display the start or game over screen
def menu(screen, death_count, points=0):
    # Initialize all pygame modules is redundant since is called in main.py,is kept for standalone testing
    #pygame.init()
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)#Loads the font for rendering text with the specified size
    
    # Load and scale the starting dinosaur image with alpha transparency
    DINO_START = pygame.transform.scale(pygame.image.load(os.path.join(DINO_DIR, "DinoStart.png")).convert_alpha(), (50, 60))
    #for game over image 
    GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join(OTHER_DIR, "GameOver.png")).convert_alpha(), (200, 50))
    # for reset button image   
    RESET = pygame.transform.scale(pygame.image.load(os.path.join(OTHER_DIR, "Reset.png")).convert_alpha(), (40, 40))

    init_db()# Initialize the high scores database
    high_score = get_high_score()# Retrieve the current high score from the database

    # Control variable for the menu loop
    run = True
    score_recorded = False# Flag to ensure the score is recorded only once per session
    #print("Menu loop started")# Print a message to the console indicating the menu loop has started

    # Main menu loop
    while run:
        #screen.fill((173, 216, 230))  # Light Blue
        screen.fill((255, 255, 255))# Fill the screen with a white background

        # Handle all pygame events
        for event in pygame.event.get():
            # Exit the game and menu if the window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                print("Window closed, exiting menu")
                sys.exit()  #to ensure immediate termination
                return False
            # Start or restart the game on any key press
            if event.type == pygame.KEYDOWN:
                print("Key pressed, returning True")
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                if reset_rect.collidepoint(event.pos):  # Check if reset button is clicked
                    clear_scores()  # Clear all scores
                    high_score = get_high_score()  # Update high score (should be 0)
                    print("High scores cleared!")

        # Display the initial menu if no deaths have occurred
        if death_count == 0:
            text = FONT.render("Press any Key to Start", True, (0, 0, 0))#letters are in black
            # Create a rectangle centered on the screen for the text
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)# Draw the text on the screen
            # Create a rectangle for the starting dinosaur image, sets it 50pixels above center
            dino_rect = DINO_START.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(DINO_START, dino_rect)# Draw the starting dinosaur image on the screen
            
        else:
            # Record the score if points are greater than 0 and not yet recorded
            if points > 0 and not score_recorded:
                add_score(points) # Add the current score to the database
                high_score = get_high_score()# Update the high score after adding the new score
                score_recorded = True# Set the flag to prevents the score from being recorded multiple times after the game ends

            # Create a rectangle for the game over image, centered above the middle
            game_over_rect = GAME_OVER.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            # Draw the game over image on the screen using the top-left corner of the rectangle
            screen.blit(GAME_OVER, game_over_rect.topleft)
            # Render the player's score text in black
            score_text = FONT.render(f"Your Score: {points}", True, (0, 0, 0))
            # Create a rectangle centered below the game over image for the score
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(score_text, score_rect)
            high_score_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(high_score_text, high_score_rect)
            restart_text = FONT.render("Press any Key to Restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            screen.blit(restart_text, restart_rect)
            reset_rect = RESET.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            screen.blit(RESET, reset_rect)
            reset_rect = RESET.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            screen.blit(RESET, reset_rect)

        # Update the full display window to the screen
        pygame.display.update()

    # Return False if the loop exits without a key press (e.g when window is closed)
    #safety measure in case the loop exits unexpectedly
    return False

'''import pygame
import os
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DINO_DIR, OTHER_DIR, FONT_PATH, FONT_SIZE
from database import init_db, add_score, get_high_score, clear_scores, update_score
from test_db import get_top_scores  # Import get_top_scores

def menu(screen, death_count, points=0):
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
    DINO_START = pygame.transform.scale(pygame.image.load(os.path.join(DINO_DIR, "DinoStart.png")).convert_alpha(), (50, 60))
    GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join(OTHER_DIR, "GameOver.png")).convert_alpha(), (200, 50))
    RESET = pygame.transform.scale(pygame.image.load(os.path.join(OTHER_DIR, "Reset.png")).convert_alpha(), (40, 40))

    init_db()
    high_score = get_high_score()

    run = True
    score_recorded = False
    selected_score_id = None  # Track the selected score ID for updating
    new_score_input = ""  # Buffer for new score input

    while run:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                print("Window closed, exiting menu")
                sys.exit()
                return False
            if event.type == pygame.KEYDOWN:
                if death_count == 0:
                    print("Key pressed, returning True")
                    return True
                elif selected_score_id is not None:
                    if event.key == pygame.K_RETURN:  # Submit new score
                        if new_score_input.isdigit():
                            update_score(selected_score_id, int(new_score_input))
                            high_score = get_high_score()
                            selected_score_id = None
                            new_score_input = ""
                            print(f"Updated score for id {selected_score_id} to {new_score_input}")
                        else:
                            print("Please enter a valid number")
                    elif event.key == pygame.K_BACKSPACE:
                        new_score_input = new_score_input[:-1]
                    elif event.unicode.isdigit():
                        new_score_input += event.unicode
                else:
                    print("Key pressed, returning True")
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_rect.collidepoint(event.pos):
                    clear_scores()
                    high_score = get_high_score()
                    print("High scores cleared!")
                # Check for clicks on score list
                scores = get_top_scores(5)  # Get top 5 scores
                for i, score_data in enumerate(scores):
                    score_text = FONT.render(f"ID: {i+1} Score: {score_data}", True, (0, 0, 0))
                    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 30))
                    if score_rect.collidepoint(event.pos):
                        # Fetch the actual ID from the database (simplified assumption: ID matches index + 1)
                        selected_score_id = i + 1  # Adjust based on your database indexing
                        new_score_input = ""
                        print(f"Selected score ID: {selected_score_id} for update")

        if death_count == 0:
            text = FONT.render("Press any Key to Start", True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            dino_rect = DINO_START.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(DINO_START, dino_rect)
        else:
            if points > 0 and not score_recorded:
                add_score(points)
                high_score = get_high_score()
                score_recorded = True

            game_over_rect = GAME_OVER.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(GAME_OVER, game_over_rect.topleft)
            score_text = FONT.render(f"Your Score: {points}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(score_text, score_rect)
            high_score_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(high_score_text, high_score_rect)
            restart_text = FONT.render("Press any Key to Restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            screen.blit(restart_text, restart_rect)
            reset_rect = RESET.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
            screen.blit(RESET, reset_rect)

            # Display top scores for update
            scores = get_top_scores(5)  # Show top 5 scores
            for i, score in enumerate(scores):
                score_text = FONT.render(f"ID: {i+1} Score: {score}", True, (0, 0, 0))
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 30))
                screen.blit(score_text, score_rect)

            # Display input field if a score is selected
            if selected_score_id is not None:
                input_text = FONT.render(f"Enter new score (ID {selected_score_id}): {new_score_input}", True, (0, 0, 0))
                input_rect = input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250))
                screen.blit(input_text, input_rect)

        pygame.display.update()

    return False'''


