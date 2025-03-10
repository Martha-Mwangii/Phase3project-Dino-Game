#cloud.py
# Import the pygame library for game development functionality
import pygame
# Import the random module for generating random numbers
import random
# Import the CLOUD_IMAGE constant from the constants module to locate the cloud image file
from constants import CLOUD_IMAGE

# Define the Cloud class to manage cloud objects in the game
class Cloud:
    # Initialize the Cloud object with default properties
    def __init__(self):
        # Load the cloud image from the file path specified in CLOUD_IMAGE and enable alpha transparency
        self.image = pygame.image.load(CLOUD_IMAGE).convert_alpha()
        # Define a blue color tuple for the day tint effect
        blue = (0, 0, 255)
        # Create a copy of the cloud image for day mode
        self.day_image = self.image.copy()
        # Apply a blue tint to the day image using RGB multiplication
        self.day_image.fill(blue, special_flags=pygame.BLEND_RGB_MULT)
        # Set black as the transparent color for the day image to remove unwanted edges
        self.day_image.set_colorkey((0, 0, 0))
        # Create a copy of the cloud image for night mode
        self.night_image = self.image.copy()
        # Apply a darker tint for night mode using RGB multiplication
        self.night_image.fill((100, 100, 150), special_flags=pygame.BLEND_RGB_MULT)
        # Set black as the transparent color for the night image
        self.night_image.set_colorkey((0, 0, 0))
        # Create a rectangle for positioning and collision detection based on the day image
        self.rect = self.day_image.get_rect()
        # Set the initial x position of the cloud off-screen to the right
        self.rect.x = 1200
        # Set a random y position for the cloud between 50 and 100 pixels
        self.rect.y = random.randint(50, 100)
        # Initialize the night mode flag as False (day mode by default)
        self.is_night = False

    # Update the cloud's position based on game speed
    def update(self, game_speed):
        # Move the cloud to the left by subtracting the game speed
        self.rect.x -= game_speed
        # Check if the cloud has moved fully off the left side of the screen
        if self.rect.x < -self.rect.width:
            # Reset the cloud's x position to 1200 (off-screen right)
            self.rect.x = 1200
            # Generate a new random y position between 50 and 100
            self.rect.y = random.randint(50, 100)

    # Draw the cloud on the screen
    def draw(self, screen):
        # Select the appropriate image based on the night mode flag
        image_to_draw = self.night_image if self.is_night else self.day_image
        # Blit (draw) the selected image onto the screen at the cloud's rectangle position
        screen.blit(image_to_draw, self.rect)

    # Set the night mode state of the cloud
    def set_night_mode(self, is_night):
        # Update the is_night flag to the provided value
        self.is_night = is_night

# Improvement Suggestions:
# 1. **Multiple Clouds**: Add a group of clouds with varying speeds for a richer background (e.g., use pygame.sprite.Group).
# 2. **Tint Variety**: Introduce random tint variations for day/night clouds to enhance visual diversity.
# 3. **Precomputed Images**: Since images are already precomputed in __init__, consider moving tint application to game startup if multiple clouds are added.