#constants.py
import os # to handle file and directory paths

SCREEN_HEIGHT = 600 # Define the screen height as a constant of 600 pixels
SCREEN_WIDTH = 1100 # constant of 1100 pixels for screen width

ASSETS_DIR = "Assets"# Define the base directory for all assets
DINO_DIR = os.path.join(ASSETS_DIR, "Dino")# Define the directory for dinosaur-related assets
CACTUS_DIR = os.path.join(ASSETS_DIR, "Cactus")#cactus-related assets
BIRD_DIR = os.path.join(ASSETS_DIR, "Bird")
OTHER_DIR = os.path.join(ASSETS_DIR, "Other")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")

# Define a list of file paths for running dinosaur animation frames
RUNNING = [os.path.join(DINO_DIR, "DinoRun1.png"), os.path.join(DINO_DIR, "DinoRun2.png")]
JUMPING = os.path.join(DINO_DIR, "DinoJump.png")#Define the file path for the jumping dinosaur image
DUCKING = [os.path.join(DINO_DIR, "DinoDuck1.png"), os.path.join(DINO_DIR, "DinoDuck2.png")]# list for ducking dinosaur
DEAD = os.path.join(DINO_DIR, "DinoDead.png")#Define the file path for the dead dinosaur image

# Define a list of file paths for small cactus images
SMALL_CACTUS = [os.path.join(CACTUS_DIR, f"SmallCactus{i}.png") for i in range(1, 4)]
LARGE_CACTUS = [os.path.join(CACTUS_DIR, f"LargeCactus{i}.png") for i in range(1, 4)]#large cactus images
BIRD = [os.path.join(BIRD_DIR, f"Bird{i}.png") for i in range(1, 3)]#Bird images

# Define the file path for the cloud image
CLOUD_IMAGE = os.path.join(OTHER_DIR, "Cloud.png")
BG = os.path.join(OTHER_DIR, "Track.png")#for the background track image
GAME_OVER_IMAGE = os.path.join(OTHER_DIR, "GameOver.png")#for the game over image

# Define the file path for the jump sound effect
JUMP_SOUND = os.path.join(SOUNDS_DIR, "jump.wav")
COLLISION_SOUND = os.path.join(SOUNDS_DIR, "collision.wav")#for the collision sound effect
GAMEOVER_SOUND = os.path.join(SOUNDS_DIR, "gameover.wav")#for the game over sound effect
BACKGROUND_MUSIC = os.path.join(SOUNDS_DIR, "background_music.mp3")# for the background music

FONT_PATH = "freesansbold.ttf"# Defines the file path for the font to use in the game
FONT_SIZE = 25 # Defines the font size for text rendering

