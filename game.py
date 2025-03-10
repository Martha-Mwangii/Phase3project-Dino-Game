
#game.py
# Import the pygame library for game development functionality
import pygame
# Import the random module for generating random numbers
import random
# Import the os module to handle file and directory paths
import os
# Import constants from the constants module for screen dimensions, asset paths, etc.
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG, SMALL_CACTUS, LARGE_CACTUS, BIRD, FONT_PATH, FONT_SIZE, JUMP_SOUND, COLLISION_SOUND, GAMEOVER_SOUND, BACKGROUND_MUSIC, OTHER_DIR
# Import the Dinosaur class from the player module to manage the player character
from player import Dinosaur
# Import the Cloud class from the cloud module to manage background clouds
from cloud import Cloud
# Import obstacle classes from the obstacles module to manage game obstacles
from obstacles import SmallCactus, LargeCactus, Bird
# Import the menu function from the menu module to handle the game menu
from menu import menu
# Import the get_high_score function from the database module to retrieve high scores
from database import get_high_score
# Import the Star class from the star module to manage night mode stars
from star import Star

# Define the main game function
def game():
    # Initialize all pygame modules
    pygame.init()
    # Create the game window with the specified width and height
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Create a clock object to control the game frame rate
    clock = pygame.time.Clock()

    # Load the track image for the background and enable alpha transparency
    track_image = pygame.image.load(BG).convert_alpha()
    # Create a surface for the day background base
    bg_base = pygame.Surface((SCREEN_WIDTH, 20))
    # Fill the base with white to represent day background
    bg_base.fill((255, 255, 255))
    # Blit the track image onto the base surface
    bg_base.blit(track_image, (0, 0))
    # Scale the day background to fit the screen width
    BG_IMAGE = pygame.transform.scale(bg_base, (SCREEN_WIDTH, 20))
    # Create a surface for the night background base
    night_bg_base = pygame.Surface((SCREEN_WIDTH, 20))
    # Fill the base with dark gray to represent night background
    night_bg_base.fill((50, 50, 50))
    # Blit the track image onto the night base surface
    night_bg_base.blit(track_image, (0, 0))
    # Scale the night background to fit the screen width
    NIGHT_IMAGE = pygame.transform.scale(night_bg_base, (SCREEN_WIDTH, 20))
    # Load and convert all small cactus images with alpha transparency
    SMALL_CACTUS_IMAGES = [pygame.image.load(path).convert_alpha() for path in SMALL_CACTUS]
    # Load and convert all large cactus images with alpha transparency
    LARGE_CACTUS_IMAGES = [pygame.image.load(path).convert_alpha() for path in LARGE_CACTUS]
    # Load and convert all bird images with alpha transparency
    BIRD_IMAGES = [pygame.image.load(path).convert_alpha() for path in BIRD]
    # Load the font for rendering text with the specified size
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

    # Initialize audio system with error handling
    has_audio = True
    try:
        # Initialize the pygame mixer for sound
        pygame.mixer.init()
        # Load and configure the jump sound effect
        jump_sound = pygame.mixer.Sound(JUMP_SOUND)
        jump_sound.set_volume(0.5)
        # Load and configure the collision sound effect
        collision_sound = pygame.mixer.Sound(COLLISION_SOUND)
        collision_sound.set_volume(0.7)
        # Load and configure the game over sound effect
        gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND)
        gameover_sound.set_volume(0.6)
        # Load and configure the background music
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.set_volume(0.3)
        # Play the background music on loop
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        # Print a warning if audio initialization fails and continue without sound
        print(f"Warning: Audio initialization failed ({e}). Continuing without sound.")
        has_audio = False

    # Initialize game state variables
    game_running = True  # Main game loop control
    is_night = False  # Flag for day/night mode
    transition_start = None  # Timestamp for starting the day/night transition
    transition_duration = 1000  # Duration of the transition in milliseconds (1 second)
    background_color = [255, 255, 255]  # Initial background color (white for day)
    night_background_color = [10, 20, 40]  # Background color for night mode (dark navy blue)
    paused = False  # Flag to pause the game
    # Render the pause text to display when paused
    pause_text = FONT.render("Paused - Press P to Resume", True, (0, 0, 0))
    # Create a sprite group for stars in night mode
    stars = pygame.sprite.Group()
    # Add 20 star objects to the group for night mode decoration
    for _ in range(20):
        stars.add(Star())

    # Main game loop
    while game_running:
        # Create a new dinosaur player instance with the clock and audio status
        player = Dinosaur(clock, has_audio)
        # Create a sprite group containing the player
        player_group = pygame.sprite.Group(player)
        # Create a new cloud instance for the background
        cloud = Cloud()
        # Set the initial game speed
        game_speed = 20
        # Initial x position for the background scrolling
        x_pos_bg = 0
        # Initial y position for the background
        y_pos_bg = 380
        # Initialize the player's score
        points = 0
        # Create a sprite group for obstacles
        obstacles = pygame.sprite.Group()
        # Initialize the death counter
        death_count = 0
        # Control variable for the active game state
        game_active = True

        # Create two copies of the background image for seamless scrolling
        bg_images = [BG_IMAGE.copy(), BG_IMAGE.copy()]
        # Create two copies of the night background image
        night_images = [NIGHT_IMAGE.copy(), NIGHT_IMAGE.copy()]

        # Inner game loop
        while game_active:
            # Handle all pygame events
            for event in pygame.event.get():
                # Exit the game if the window is closed
                if event.type == pygame.QUIT:
                    print("Window closed, exiting game")
                    game_active = False
                    game_running = False
                # Resize the window if the user resizes it
                elif event.type == pygame.VIDEORESIZE:
                    SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    # Update the day background image to match the new width
                    BG_IMAGE = pygame.transform.scale(bg_base, (event.w, 20))
                    # Update the night background image to match the new width
                    NIGHT_IMAGE = pygame.transform.scale(night_bg_base, (event.w, 20))
                    # Recreate background images for scrolling
                    bg_images = [BG_IMAGE.copy(), BG_IMAGE.copy()]
                    night_images = [NIGHT_IMAGE.copy(), NIGHT_IMAGE.copy()]
                # Handle key presses
                elif event.type == pygame.KEYDOWN:
                    # Toggle pause state on 'P' key press
                    if event.key == pygame.K_p:
                        paused = not paused

            # Display pause screen if game is paused
            if paused:
                # Calculate the center position for the pause text
                pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                # Draw the pause text on the screen
                SCREEN.blit(pause_text, pause_rect)
                # Update the display to show the pause screen
                pygame.display.update()
                # Skip the rest of the loop iteration
                continue

            # Trigger night mode transition at 500 points
            if points == 500 and not is_night:
                # Switch to night mode
                is_night = True
                # Update cloud to night mode
                cloud.set_night_mode(True)
                # Record the start time of the transition
                transition_start = pygame.time.get_ticks()
                # Print a message to the console
                print("Switched to night mode!")

            # Handle the day to night transition animation
            if transition_start is not None:
                # Calculate the time elapsed since the transition started
                elapsed = pygame.time.get_ticks() - transition_start
                # Perform the transition if it hasn't completed
                if elapsed < transition_duration:
                    # Calculate the transition progress (0 to 1)
                    progress = elapsed / transition_duration
                    # Interpolate the background color from day to night
                    background_color = [
                        int(255 + (night_background_color[0] - 255) * progress),
                        int(255 + (night_background_color[1] - 255) * progress),
                        int(255 + (night_background_color[2] - 255) * progress)
                    ]
                else:
                    # Set the background to full night color when transition is complete
                    background_color = night_background_color
                    # Reset the transition start time
                    transition_start = None

            # Fill the screen with the current background color
            SCREEN.fill(background_color if not is_night else night_background_color)
            # Get the current state of all keyboard keys
            user_input = pygame.key.get_pressed()

            # Update the background scrolling position
            x_pos_bg = background(SCREEN, bg_images if not is_night else night_images, x_pos_bg, game_speed, y_pos_bg)

            # Draw and update the cloud
            cloud.draw(SCREEN)
            cloud.update(game_speed)

            # Update and draw stars in night mode
            if is_night:
                stars.update()
                for star in stars:
                    star.draw(SCREEN)

            # Update and draw the player
            player_group.update(user_input)
            player_group.draw(SCREEN, is_night)

            # Determine the spawn threshold for obstacles (decreases as points increase)
            spawn_threshold = max(20, 200 - (points // 50))
            # Spawn a new obstacle based on random chance
            if not obstacles or random.randint(0, spawn_threshold) == 0:
                # Randomly choose the type of obstacle
                choice = random.randint(0, 2)
                if choice == 0:
                    # Add a small cactus to the obstacles group
                    obstacles.add(SmallCactus(SMALL_CACTUS_IMAGES, is_night))
                elif choice == 1:
                    # Add a large cactus to the obstacles group
                    obstacles.add(LargeCactus(LARGE_CACTUS_IMAGES, is_night))
                else:
                    # Add a bird to the obstacles group
                    obstacles.add(Bird(BIRD_IMAGES, is_night))

            # Update and draw all obstacles
            obstacles.update(game_speed, obstacles)
            obstacles.draw(SCREEN, is_night)

            # Check for collisions between the player and obstacles
            collisions = pygame.sprite.spritecollide(player, obstacles, False)
            if collisions:
                # Play collision and game over sounds if audio is enabled
                if has_audio:
                    collision_sound.play()
                    gameover_sound.play()
                # Set the player's dead state
                player.dino_dead = True
                # Delay for 2 seconds to show the death animation
                pygame.time.delay(2000)
                # Increment the death counter
                death_count += 1
                # Print a message to the console
                print("Collision detected, showing menu")
                # Show the menu and check if the game should continue
                if not menu(SCREEN, death_count, points):
                    # Exit the game if the menu returns False
                    game_active = False
                    game_running = False
                else:
                    # Reset game state for a new game
                    player = Dinosaur(clock, has_audio)
                    player_group = pygame.sprite.Group(player)
                    obstacles.empty()
                    game_speed = 20
                    x_pos_bg = 0
                    points = 0
                    is_night = False
                    background_color = [255, 255, 255]
                    transition_start = None
                    stars.empty()
                    for _ in range(20):
                        stars.add(Star())
                # Break the inner loop to restart the game
                break

            # Update the score and game speed
            points, game_speed = score(SCREEN, FONT, points, game_speed, is_night)

            # Handle jump action with sound if audio is enabled
            if user_input[pygame.K_UP] and not player.dino_jump and has_audio:
                jump_sound.play()
                print("Jump action detected")
            # Handle duck action (no sound required)
            if user_input[pygame.K_DOWN] and not player.dino_jump:
                print("Duck action detected")

            # Limit the game to 30 frames per second
            clock.tick(30)
            # Update the full display window to the screen
            pygame.display.update()

# Define a function to handle background scrolling
def background(screen, bg_images, x_pos_bg, game_speed, y_pos_bg):
    # Get the width of the background image
    image_width = bg_images[0].get_width()
    # Draw the first background image at the current x position
    screen.blit(bg_images[0], (x_pos_bg, y_pos_bg))
    # Draw a second background image to create a seamless loop
    screen.blit(bg_images[0], (x_pos_bg + image_width, y_pos_bg))
    # Move the background to the left based on game speed
    x_pos_bg -= game_speed
    # Reset the x position if the background has scrolled fully off-screen
    if x_pos_bg <= -image_width:
        x_pos_bg = 0
    # Return the updated x position
    return x_pos_bg

# Define a function to update and display the score
def score(screen, font, points, game_speed, is_night):
    # Increment the player's score by 1
    points += 1
    # Increase game speed every 100 points
    if points % 100 == 0:
        game_speed += 1
    # Retrieve the current high score from the database
    high_score = get_high_score()
    # Render the score text with appropriate color based on day/night mode
    text = font.render(f"Points: {points}  HI: {high_score}", True, (0, 0, 0) if not is_night else (200, 200, 200))
    # Create a rectangle for the text
    text_rect = text.get_rect()
    # Position the text 20 pixels from the right edge
    text_rect.right = screen.get_width() - 20
    # Position the text 40 pixels from the top
    text_rect.top = 40
    # Draw the text on the screen
    screen.blit(text, text_rect)
    # Return the updated points and game speed
    return points, game_speed

# Run the game if this script is executed directly
if __name__ == "__main__":
    game()

# Improvement Suggestions:
# 1. **Audio Error Recovery**: Add a fallback sound system or log errors to a file.
# 2. **Transition Smoothness**: Interpolate sprite tints (e.g., in obstacles.py) to match the background fade.
# 3. **Pause Menu Enhancement**: Add options (e.g., resume, quit) with a simple UI using buttons.
# 4. **Performance Optimization**: Use pygame.sprite.Sprite for the background to leverage group updates.