#player.py
import pygame
from constants import RUNNING, JUMPING, DUCKING, DEAD, JUMP_SOUND

# Define the Dinosaur class using pygame's Sprite class to manage the player character
class Dinosaur(pygame.sprite.Sprite):
    X_POS = 80# Define the initial x position of the dinosaur
    Y_POS = 320# Define the initial y position (standing)
    Y_POS_DUCK = 340# Define the y position when ducking
    JUMP_VEL = 8.5# Define the initial jump velocity
    DUCK_OFFSET = 10# used to slightly adjust the position of the dinosaur when it's ducking

    # Initialize the Dinosaur object with a clock and audio status
    def __init__(self, clock, has_audio=False):
        super().__init__()  # Initialize the parent Sprite class
        # Load and convert all running animation images with alpha transparency
        self.run_img = [pygame.image.load(path).convert_alpha() for path in RUNNING]
        self.jump_img = pygame.image.load(JUMPING).convert_alpha()#jumping 
        self.duck_img = [pygame.image.load(path).convert_alpha() for path in DUCKING]# all ducking animation images 
        self.dead_img = pygame.image.load(DEAD).convert_alpha()#dead image 

        # Calculate a scale factor based on desired sprite dimensions (50x60)
        scale_factor = 50 / 60
        # Scale all running images to 50x60 pixels
        self.run_img = [pygame.transform.scale(img, (50, 60)) for img in self.run_img]
        self.jump_img = pygame.transform.scale(self.jump_img, (50, 60))
        self.duck_img = [pygame.transform.scale(img, (50, 60)) for img in self.duck_img]
        self.dead_img = pygame.transform.scale(self.dead_img, (50, 60))

        # Initialize day and night versions of images
        self.day_run_img = self.run_img.copy()  # Store copies of day running images
        self.day_jump_img = self.jump_img.copy()  # Store a copy of day jumping image
        self.day_duck_img = self.duck_img.copy()  # Store copies of day ducking images
        # Apply night tint to all running images and store copies
        self.night_run_img = [self.apply_night_tint(img.copy()) for img in self.run_img]
        self.night_jump_img = self.apply_night_tint(self.jump_img.copy())
        self.night_duck_img = [self.apply_night_tint(img.copy()) for img in self.duck_img]

        # Initialize jump sound variable
        self.jump_sound = None
        # Load and configure jump sound if audio is enabled
        if has_audio:
            try:
                self.jump_sound = pygame.mixer.Sound(JUMP_SOUND)
                self.jump_sound.set_volume(0.5)
            except pygame.error:
                # Print a warning if the jump sound fails to load
                print("Warning: Failed to load jump sound. Continuing without it.")
                self.jump_sound = None

        # Initialize state flags
        self.dino_duck = False  # Flag for ducking state
        self.dino_run = True  # Flag for running state
        self.dino_jump = False  # Flag for jumping state
        self.dino_dead = False  # Flag for dead state
        self.jump_vel = self.JUMP_VEL  # Set initial jump velocity
        self.image = self.day_run_img[0]  # Set the initial image to the first running frame
        self.rect = self.image.get_rect()  # Create a rectangle for collision detection
        self.rect.x = self.X_POS  # Set the x position
        self.rect.y = self.Y_POS  # Set the y position
        self.run_index = 0  # Index for running animation frames
        self.duck_index = 0  # Index for ducking animation frames
        self.animation_time = 0  # Timer for animation frame updates
        self.clock = clock  # Store the pygame clock for timing
        self.last_jump_time = 0  # Timestamp of the last jump
        self.duck_offset = 0  # Offset for ducking movement
        self.is_night = False  # Track night mode state

    # Apply a night tint to the image
    def apply_night_tint(self, image):
        night_image = image.copy()  # Create a copy of the original image
        # Apply a dark blue tint for night mode
        night_image.fill((100, 100, 150), special_flags=pygame.BLEND_RGB_MULT)
        night_image.set_colorkey((0, 0, 0))  # Set black as transparent
        return night_image

    # Update the dinosaur's state based on user input
    def update(self, user_input):
        # Return early if the dinosaur is dead
        if self.dino_dead:
            return
        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump(current_time)
        # Update ducking animation if in duck state
        if self.dino_duck:
            self.duck(current_time)

        # Handle jump action with a 500ms cooldown
        if user_input[pygame.K_UP] and not self.dino_jump and (current_time - self.last_jump_time > 200):
            self.dino_duck = False  # Disable ducking
            self.dino_run = False  # Disable running
            self.dino_jump = True  # Enable jumping
            if self.jump_sound:
                self.jump_sound.play()  # Play jump sound if available
            self.last_jump_time = current_time  # Update last jump time
        # Handle duck action
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True  # Enable ducking
            self.dino_run = False  # Disable running
            self.dino_jump = False  # Disable jumping
        # Handle return to running state
        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_duck = False  # Disable ducking
            self.dino_run = True  # Enable running
            self.dino_jump = False  # Disable jumping
            self.duck_offset = 0  # Reset duck offset

    # Handle the running animation and position
    def run(self):
        self.rect.y = self.Y_POS  # Set the y position to standing height
        self.update_animation()  # Update the animation frame

    # Handle the jumping physics
    def jump(self, current_time):
        if self.dino_jump:
            # Calculate elapsed time in seconds since the last jump
            elapsed_time = (current_time - self.last_jump_time) / 1000
            # Update y position based on jump velocity and time
            self.rect.y -= self.jump_vel * 4 * elapsed_time
            # Decrease jump velocity to simulate gravity
            self.jump_vel -= 0.8 * elapsed_time
            # Reset jump state when velocity falls below negative initial velocity
            if self.jump_vel < -self.JUMP_VEL:
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL

    # Handle the ducking animation and position
    def duck(self, current_time):
        # Calculate a dynamic offset for ducking movement (oscillates between -5 and 5)
        self.duck_offset = max(-5, min(5, self.duck_offset + (pygame.time.get_ticks() % 200 - 100) / 50))
        # Set the y position with the duck offset
        self.rect.y = self.Y_POS_DUCK + self.duck_offset
        self.update_animation()  # Update the animation frame

    # Update the animation frame based on time
    def update_animation(self):
        # Increment the animation timer by the time elapsed since the last frame
        self.animation_time += self.clock.get_time()
        # Set animation speed dynamically based on frame rate (minimum 50ms)
        animation_speed = 100 #max(50, 150 - (self.clock.get_fps() * 2))
        if self.animation_time >= animation_speed:
            self.animation_time = 0  # Reset the timer
            if self.dino_run:
                # Cycle through running animation frames
                self.run_index = (self.run_index + 1) % len(self.run_img)
                # Select the appropriate image based on night mode
                self.image = (self.night_run_img if self.is_night else self.day_run_img)[self.run_index]
            elif self.dino_duck:
                # Cycle through ducking animation frames
                self.duck_index = (self.duck_index + 1) % len(self.duck_img)
                # Select the appropriate image based on night mode
                self.image = (self.night_duck_img if self.is_night else self.day_duck_img)[self.duck_index]

    # Draw the dinosaur on the screen
    def draw(self, SCREEN, is_night):
        if self.dino_dead:
            self.image = self.dead_img  # Set image to dead if the dinosaur is dead
        elif self.dino_jump:
            # Set image to jump image based on night mode
            self.image = self.night_jump_img if is_night else self.day_jump_img
        self.is_night = is_night  # Update night mode state
        # Draw the current image on the screen at the rectangle position
        SCREEN.blit(self.image, self.rect)

