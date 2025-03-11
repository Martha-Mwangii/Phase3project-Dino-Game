#star.py
import pygame
import random
import math#Import the math module for trigonometric calculations

# Define the Star class using pygame's Sprite class to manage night mode stars
class Star(pygame.sprite.Sprite):
    # Initialize the Star object with default properties
    def __init__(self):
        super().__init__()  # Initialize the parent Sprite class
        self.size = 6  # Size of the star (diameter in pixels)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA) #Create a surface for the star with alpha support
        self.alpha = random.randint(50, 255) # Set a random initial transparency value between 50 and 255
        self.draw_star()  # Draw the star shape
        self.rect = self.image.get_rect()  # Create a rectangle for positioning
        self.rect.x = random.randint(0, 1100)# Set a random x position within the screen width (0 to 1100)
        self.rect.y = random.randint(50, 200)# Set a random y position between 50 and 200 pixels
        self.twinkle_speed = random.uniform(0.02, 0.05)# Set a random twinkling speed between 0.02 and 0.05

    # Draw the star shape on the image surface
    def draw_star(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface with transparent black
        center = self.size // 2  # Calculate the center point of the star
        radius = self.size // 2  # Calculate the radius based on size
        points = []  # List to store the star's polygon points
        for i in range(5):
            # Calculate outer points of the star
            angle = math.radians(72 * i - 90)  # Rotate by 72 degrees per point, offset by -90
            x = center + radius * math.cos(angle)  # X coordinate of outer point
            y = center + radius * math.sin(angle)  # Y coordinate of outer point
            points.append((x, y))
            # Calculate inner points to create the star shape
            angle = math.radians(72 * i - 90 + 36)  # Offset inner points by 36 degrees
            x = center + (radius / 2) * math.cos(angle)  # X coordinate of inner point
            y = center + (radius / 2) * math.sin(angle)  # Y coordinate of inner point
            points.append((x, y))
        # Draw a polygon with white color and current alpha on the image
        pygame.draw.polygon(self.image, (255, 255, 255, int(self.alpha)), points)

    # Update the star's twinkling effect
    def update(self):
        # Adjust alpha value based on twinkling speed and random direction
        self.alpha += self.twinkle_speed * random.choice([-1, 1]) * 10
        # Keep alpha within bounds (50 to 255)
        self.alpha = max(50, min(255, self.alpha))
        self.draw_star()  # Redraw the star with the updated alpha

    # Draw the star on the screen
    def draw(self, screen):
        # Blit (draw) the star image onto the screen at its rectangle position
        screen.blit(self.image, self.rect)
