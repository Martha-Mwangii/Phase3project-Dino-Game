#cloud.py
import pygame
import random  #generating random numbers
from constants import CLOUD_IMAGE #to locate the cloud image file

# Define the Cloud class to manage cloud objects in the game
class Cloud:
    # Initialize the Cloud object with default properties
    def __init__(self):
        # Load the cloud image from the file path specified in CLOUD_IMAGE and enable alpha transparency
        self.image = pygame.image.load(CLOUD_IMAGE).convert_alpha()
        blue = (0, 0, 255) # Define a blue color tuple for the day tint effect
        self.day_image = self.image.copy()  # Create a copy of the cloud image for day mode
        self.day_image.fill(blue, special_flags=pygame.BLEND_RGB_MULT) #Apply blueday image using RGB multiplication
        self.day_image.set_colorkey((0, 0, 0)) #Set black as the transparent color for the day image to remove unwanted edges
        self.night_image = self.image.copy() # Create a copy of the cloud image for night mode
        self.night_image.fill((100, 100, 150), special_flags=pygame.BLEND_RGB_MULT)# darker tint for night mode 
        self.night_image.set_colorkey((0, 0, 0))
        self.rect = self.day_image.get_rect()# Create a rectangle for positioning and collision detection based on the day image

        self.rect.x = 1200  # Set the initial x position of the cloud off-screen to the right
        self.rect.y = random.randint(50, 100)# Set a random y position for the cloud between 50 and 100 pixels
        self.is_night = False # Initialize the night mode flag as False (day mode is the default)

    # Update the cloud's position based on game speed
    def update(self, game_speed):
        self.rect.x -= game_speed  # Moves the cloud to the left by subtracting the game speed
        if self.rect.x < -self.rect.width:# Checks if the cloud has moved fully off the left side of the screen
            self.rect.x = 1200 #Resets the cloud's x position to 1200 (off-screen right)
            self.rect.y = random.randint(50, 100) #Generates a new random y position between 50 and 100

    # Draw the cloud on the screen
    def draw(self, screen):
        # Select the appropriate image based on the night mode flag
        image_to_draw = self.night_image if self.is_night else self.day_image
        # Blit/draw the selected image onto the screen at the cloud's rectangle position
        screen.blit(image_to_draw, self.rect)

    # Set the night mode state of the cloud
    def set_night_mode(self, is_night):
        self.is_night = is_night # Update the is_night flag to the provided value

