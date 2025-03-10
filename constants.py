
#constants.py
# Import the os module to handle file and directory paths
import os

# Define the screen height as a constant (600 pixels)
SCREEN_HEIGHT = 600
# Define the screen width as a constant (1100 pixels)
SCREEN_WIDTH = 1100

# Define the base directory for all assets
ASSETS_DIR = "Assets"
# Define the directory for dinosaur-related assets
DINO_DIR = os.path.join(ASSETS_DIR, "Dino")
# Define the directory for cactus-related assets
CACTUS_DIR = os.path.join(ASSETS_DIR, "Cactus")
# Define the directory for bird-related assets
BIRD_DIR = os.path.join(ASSETS_DIR, "Bird")
# Define the directory for other miscellaneous assets
OTHER_DIR = os.path.join(ASSETS_DIR, "Other")
# Define the directory for sound assets
SOUNDS_DIR = os.path.join(ASSETS_DIR, "Sounds")

# Define a list of file paths for running dinosaur animation frames
RUNNING = [os.path.join(DINO_DIR, "DinoRun1.png"), os.path.join(DINO_DIR, "DinoRun2.png")]
# Define the file path for the jumping dinosaur image
JUMPING = os.path.join(DINO_DIR, "DinoJump.png")
# Define a list of file paths for ducking dinosaur animation frames
DUCKING = [os.path.join(DINO_DIR, "DinoDuck1.png"), os.path.join(DINO_DIR, "DinoDuck2.png")]
# Define the file path for the dead dinosaur image
DEAD = os.path.join(DINO_DIR, "DinoDead.png")

# Define a list of file paths for small cactus images
SMALL_CACTUS = [os.path.join(CACTUS_DIR, f"SmallCactus{i}.png") for i in range(1, 4)]
# Define a list of file paths for large cactus images
LARGE_CACTUS = [os.path.join(CACTUS_DIR, f"LargeCactus{i}.png") for i in range(1, 4)]
# Define a list of file paths for bird animation frames
BIRD = [os.path.join(BIRD_DIR, f"Bird{i}.png") for i in range(1, 3)]

# Define the file path for the cloud image
CLOUD_IMAGE = os.path.join(OTHER_DIR, "Cloud.png")
# Define the file path for the background track image
BG = os.path.join(OTHER_DIR, "Track.png")
# Define the file path for the game over image
GAME_OVER_IMAGE = os.path.join(OTHER_DIR, "GameOver.png")

# Define the file path for the jump sound effect
JUMP_SOUND = os.path.join(SOUNDS_DIR, "jump.wav")
# Define the file path for the collision sound effect
COLLISION_SOUND = os.path.join(SOUNDS_DIR, "collision.wav")
# Define the file path for the game over sound effect
GAMEOVER_SOUND = os.path.join(SOUNDS_DIR, "gameover.wav")
# Define the file path for the background music
BACKGROUND_MUSIC = os.path.join(SOUNDS_DIR, "background_music.mp3")

# Define the file path for the font to use in the game
FONT_PATH = "freesansbold.ttf"
# Define the font size for text rendering
FONT_SIZE = 20

# Improvement Suggestions:
# 1. **Validation**: Add runtime checks to ensure files exist using os.path.exists().
# 2. **Config File**: Move constants to a JSON or INI file for easier editing outside the code.
# 3. **Dynamic Paths**: Use os.path.abspath() or pathlib.Path for cross-platform compatibility.