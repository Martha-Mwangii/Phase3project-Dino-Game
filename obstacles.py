#obstacles.py
import random
import pygame
from constants import SCREEN_WIDTH #from the constants module for obstacle placement/appearance/creation

# Define a function to scale an image to specified dimensions while preserving transparency
def scale_image(image, width, height):
    """Scale an image to the specified dimensions while preserving transparency."""
    return pygame.transform.scale(image, (width, height))

# Define the base class for all obstacles (cacti, birds) using pygame's Sprite class
class Obstacle(pygame.sprite.Sprite):
    """Base class for all obstacles (cacti, birds) in the game."""
    # Initialize the Obstacle object with images and optional scaling
    def __init__(self, images, is_night=False, scale_width=None, scale_height=None):
        super().__init__()  # Initialize the parent Sprite class
        self.images = images  # List of images for the obstacle (e.g., different cactus types)
        if scale_width and scale_height:
            # Scale all images to the specified dimensions if provided
            self.images = [scale_image(img, scale_width, scale_height) for img in self.images]
        # Randomly select a type (e.g., cactus variant) if multiple images are available
        self.type = random.randint(0, len(images) - 1) if len(images) > 1 else 0
        self.image = self.images[self.type]  # Set the initial image based on the selected type
        self.rect = self.image.get_rect()  # Create a rectangle for collision detection
        self.rect.x = SCREEN_WIDTH  # Position the obstacle off-screen to the right
        self.is_night = is_night  # Track whether the game is in night mode
        self.day_image = self.image.copy()  # Store a copy of the day image
        self.night_image = self.apply_night_tint(self.image.copy())  # Precompute the night image

    # Apply a night tint to the image with adjusted color and alpha blending
    def apply_night_tint(self, image):
        """Apply a night tint to the image with adjusted color and alpha blending for better visibility."""
        night_image = image.copy()  # Create a copy of the original image
        # Adjusted tint: Lighter bluish tone for better contrast against the night background (10, 20, 40)
        tint_color = (80, 120, 140) 
        # Apply alpha blending with an alpha value of 200 to let some original colors show through
        night_image.fill((*tint_color, 200), special_flags=pygame.BLEND_RGBA_MULT)
        night_image.set_colorkey((0, 0, 0))  # Set black as transparent (for sprite edges)
        return night_image

    # Update the obstacle's position and remove it if it moves off-screen
    def update(self, game_speed, obstacles):
        """Update the obstacle's position and remove it if it moves off-screen."""
        self.rect.x -= game_speed  # Move the obstacle to the left based on game speed
        if self.rect.x < -self.rect.width:  # Check if the obstacle is fully off-screen
            obstacles.remove(self)  # Remove the obstacle from the sprite group

    # Draw the obstacle on the screen using precomputed day or night images
    def draw(self, SCREEN, is_night):
        """Draw the obstacle on the screen using precomputed day or night images."""
        self.image = self.night_image if is_night else self.day_image  # Select the appropriate image
        SCREEN.blit(self.image, self.rect)  # Draw the image at its current position

# Define the class for small cactus obstacles
class SmallCactus(Obstacle):
    """Class for small cactus obstacles."""
    # Initialize the SmallCactus object with specific dimensions
    def __init__(self, images, is_night=False):
        # Initialize the parent Obstacle class with specific dimensions for small cacti
        super().__init__(images, is_night, scale_width=30, scale_height=60)
        # Set a random y position for variation (close to the ground)
        self.rect.y = random.randint(300, 340)

# Define the class for large cactus obstacles
class LargeCactus(Obstacle):
    """Class for large cactus obstacles."""
    # Initialize the LargeCactus object with specific dimensions
    def __init__(self, images, is_night=False):
        # Initialize the parent Obstacle class with specific dimensions for large cacti
        super().__init__(images, is_night, scale_width=40, scale_height=80)
        # Set a random y position for variation (slightly above small cacti)
        self.rect.y = random.randint(280, 320)

# Define the class for bird obstacles with animation
class Bird(Obstacle):
    """Class for bird obstacles with animation."""
    # Initialize the Bird object with specific dimensions
    def __init__(self, images, is_night=False):
        # Initialize the parent Obstacle class with specific dimensions for birds
        super().__init__(images, is_night, scale_width=50, scale_height=40)
        # Set a random y position for birds (higher up in the air)
        self.rect.y = random.randint(200, 280)
        self.index = 0  # Index for animation frames
        self.frame_count = 0  # Counter for animation timing
        # Precompute day and night images for all animation frames
        self.day_images = [img.copy() for img in self.images]  # Store copies of day images
        self.night_images = [self.apply_night_tint(img.copy()) for img in self.images]  # Precompute night images
        self.image = self.day_images[self.index]  # Set the initial image

    # Apply a night tint specific to birds with adjusted color and alpha blending
    def apply_night_tint(self, image):
        """Apply a night tint specific to birds with adjusted color and alpha blending."""
        night_image = image.copy()  # Create a copy of the original image
        # Adjusted tint: Slightly Light Greyish White for better visibility
        tint_color = (230, 230, 230)  
        # Apply alpha blending with an alpha value of 180 for a softer effect
        night_image.fill((*tint_color, 180), special_flags=pygame.BLEND_RGBA_MULT)
        night_image.set_colorkey((0, 0, 0))  # Set black as transparent
        return night_image

    # Update the bird's position and animation using precomputed images
    def update(self, game_speed, obstacles):
        """Update the bird's position and animation using precomputed images."""
        self.rect.x -= game_speed  # Move the bird to the left
        if self.rect.x < -self.rect.width:  # Remove the bird if it moves off-screen
            obstacles.remove(self)
        self.frame_count += 1  # Increment frame counter for animation timing
        # Adjust animation speed based on game speed (faster at higher speeds)
        animation_speed = max(5, 15 - (game_speed // 2))
        if self.frame_count >= animation_speed: #Update animation frame when threshold is reachedi.ehow many frames to wait before switching images
            self.frame_count = 0  # Reset frame counter
            self.index = (self.index + 1) % len(self.day_images)  #Cycle through animation frames i.eSwitch to the next bird image
            self.image = self.night_images[self.index] if self.is_night else self.day_images[self.index]

    # Draw the bird on the screen using precomputed images
    def draw(self, SCREEN, is_night):
        """Draw the bird on the screen using precomputed images."""
        self.is_night = is_night  # Update night mode state
        SCREEN.blit(self.image, self.rect)  # the Image is already set in update(),so its just drawn
