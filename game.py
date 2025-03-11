#game.py
import pygame #library for game development functionality
import random
import os #to handle file and directory paths.
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG, SMALL_CACTUS, LARGE_CACTUS, BIRD, FONT_PATH, FONT_SIZE, JUMP_SOUND, COLLISION_SOUND, GAMEOVER_SOUND, BACKGROUND_MUSIC, OTHER_DIR
from player import Dinosaur
from cloud import Cloud
from obstacles import SmallCactus, LargeCactus, Bird
from menu import menu
from database import get_high_score
from star import Star
import sys

# Define the main game function
def game():
    pygame.init()# Initialize all pygame modules
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))# Create the game window with given dimensions
    clock = pygame.time.Clock()# Create a clock object to control the game frame rate

    # Load the track image for the background and enable alpha transparency
    track_image = pygame.image.load(BG).convert_alpha()
    bg_base = pygame.Surface((SCREEN_WIDTH, 20))# Create a surface for the day background base
    bg_base.fill((255, 255, 255))# Fill the base with white to represent day background
    bg_base.blit(track_image, (0, 0))# Blit the track image onto the base surface
    BG_IMAGE = pygame.transform.scale(bg_base, (SCREEN_WIDTH, 20))# Scale the day background to fit the screen width
    night_bg_base = pygame.Surface((SCREEN_WIDTH, 20))# Create a surface for the night background base
    night_bg_base.fill((50, 50, 50))# Fill the base with dark gray to represent night background
    night_bg_base.blit(track_image, (0, 0))
    NIGHT_IMAGE = pygame.transform.scale(night_bg_base, (SCREEN_WIDTH, 20))

    # Load and convert all small cactus images with alpha transparency
    SMALL_CACTUS_IMAGES = [pygame.image.load(path).convert_alpha() for path in SMALL_CACTUS]
    LARGE_CACTUS_IMAGES = [pygame.image.load(path).convert_alpha() for path in LARGE_CACTUS]
    BIRD_IMAGES = [pygame.image.load(path).convert_alpha() for path in BIRD]
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
        player = Dinosaur(clock, has_audio)# Create a new dinosaur player instance with the clock and audio status
        player_group = pygame.sprite.Group(player)# Create a sprite group containing the player
        cloud = Cloud()# Create a new cloud instance for the background
        game_speed = 7# Set the initial game speed
        x_pos_bg = 0# Initial x position for the background scrolling
        y_pos_bg = 380# Initial y position for the background
        points = 0# Initialize the player's score
        obstacles = pygame.sprite.Group()# Create a sprite group for obstacles
        death_count = 0 # Initialize the death counter
        
        game_active = True# Control variable for the active game state
        bg_images = [BG_IMAGE.copy(), BG_IMAGE.copy()]#Create two copies of the background image for seamless scrolling
        night_images = [NIGHT_IMAGE.copy(), NIGHT_IMAGE.copy()]# Create two copies of the night background image

        # Inner game loop
        while game_active:
            # Handle all pygame events
            for event in pygame.event.get():
                # Exit the game if the window is closed
                if event.type == pygame.QUIT:
                    print("Window closed, exiting game")
                    game_active = False
                    game_running = False
                if not game_running:
                    pygame.quit()
                    sys.exit()
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
                SCREEN.blit(pause_text, pause_rect)# Draw the pause text on the screen
                pygame.display.update()# Update the display to show the pause screen
                # Skip the rest of the loop iteration
                continue

            # Trigger night mode transition at 500 points
            if points == 500 and not is_night:
                is_night = True# Switch to night mode
                cloud.set_night_mode(True)# Update cloud to night mode
                transition_start = pygame.time.get_ticks()# Record the start time of the transition
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
                choice = random.randint(0, 2)  # Randomly choose the type of obstacle
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
                player.dino_dead = True# Set the player's dead state
                pygame.time.delay(2000)# Delay for 2 seconds to show the death animation
                death_count += 1 # Increment the death counter
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
                #print("Jump action detected")
            # Handle duck action (no sound required)
            if user_input[pygame.K_DOWN] and not player.dino_jump:
                #print("Duck action detected")

             clock.tick(30)# Limit the game to 30 frames per second
            pygame.display.update() # Update the full display window to the screen

# Define a function to handle background scrolling
def background(screen, bg_images, x_pos_bg, game_speed, y_pos_bg):
    image_width = bg_images[0].get_width()# Get the width of the background image
    screen.blit(bg_images[0], (x_pos_bg, y_pos_bg))# Draw the first background image at the current x position
    screen.blit(bg_images[0], (x_pos_bg + image_width, y_pos_bg))# Draw a second background image to create a seamless loop
    x_pos_bg -= game_speed# Move the background to the left based on game speed

    # Reset the x position if the background has scrolled fully off-screen
    if x_pos_bg <= -image_width:
        x_pos_bg = 0
    return x_pos_bg# Return the updated x position

# Define a function to update and display the score
def score(screen, font, points, game_speed, is_night):
    points += 1# Increment the player's score by 1
    # Increase game speed every 100 points
    if points % 100 == 0:
        game_speed += 1
    
    high_score = get_high_score()# Retrieve the current high score from the database
    # Render the score text with appropriate color based on day/night mode
    text = font.render(f"Points: {points}  HI: {high_score}", True, (0, 0, 0) if not is_night else (200, 200, 200))
    text_rect = text.get_rect()# Create a rectangle for the text
    text_rect.right = screen.get_width() - 20# Position the text 20 pixels from the right edge
    text_rect.top = 40# Position the text 40 pixels from the top
    screen.blit(text, text_rect)# Draw the text on the screen
    return points, game_speed# Return the updated points and game speed

# Run the game if this script is executed directly
if __name__ == "__main__":
    game()
