# Chrome Dino Game 

This is a Python-based recreation of the Chrome Dino Game using Pygame, featuring a dinosaur that jumps over obstacles, ducks under birds, and tracks high scores in an SQLite database. This project includes day/night transitions, sound effects, and a star-filled night sky for added immersion.

## Features

- **Gameplay**: Control the dinosaur to jump (`UP` arrow) or duck (`DOWN` arrow) to avoid obstacles (cacti and birds).
- **Day/Night Cycle**: Transitions to night mode at 500 points with a darker background and twinkling stars.
- **Score Tracking**: Scores are saved to an SQLite database (`high_scores.db`), with the highest score displayed.
- **Audio**: Includes jump, collision, and game-over sounds, plus background music.
- **Animations**: Dinosaur running, jumping, ducking, and bird flapping animations.
- **Pause Functionality**: Press `P` to pause/resume the game.
- **Responsive Design**: Window resizes dynamically with seamless background scrolling.

## Installation

1. **Prerequisites**:
   - Python 3.8.13
   - Pygame (`pip install pygame`)
   - SQLite3 (included with Python)

2. **Clone the Repository**:
   - git clone <[repository-url](https://github.com/Martha-Mwangii/Phase3project-Dino-Game)>
   - cd chrome-dino-game

3. **Directory Structure**:
   Ensure the Assets folder is present with subfolders (Dino, Cactus, Bird, Other, Sounds) containing the required images and audio files.

4. **Run the Game**:
   python main.py

## How to Play

- **Start**: Press any key at the initial menu.
- **Controls**:
  - `UP Arrow`: Jump over obstacles.
  - `DOWN Arrow`: Duck under birds.
  - `P`: Pause/resume the game.
- **Objective**: Survive as long as possible by avoiding obstacles to achieve a high score.
- **Game Over**: Collide with an obstacle to see the menu with your score and the high score and restart by pressing any key.

## File Overview

- **`main.py`**: Entry point, initializes Pygame and the database, then starts the game loop.
- **`game.py`**: Core game logic, including background scrolling, obstacle spawning/creation, and score updates.
- **`player.py`**: Manages the dinosaur's movement and animations.
- **`obstacles.py`**: Defines cactus and bird obstacles with scaling and night tinting.
- **`cloud.py`**: Handles cloud movement and day/night visuals.
- **`star.py`**: Creates twinkling stars for night mode.
- **`menu.py`**: Displays the start screen, game-over screen, and high scores.
- **`database.py`**: Manages the SQLite database for score storage.
- **`constants.py`**: Centralizes file paths and game constants.
- **`test_db.py`**: Utility script to test database queries (e.g., top/bottom scores).

## Database

- **Schema**: The `high_scores` table stores:
  - `id` (auto-incrementing primary key)
  - `score` (integer, not null)
  - `date` (text, defaults to current timestamp)
- **Functions**:
  - `init_db()`: Creates the table if it doesn’t exist.
  - `add_score(score)`: Inserts a new score.
  - `get_high_score()`: Retrieves the highest score.
  - `clear_scores()`: Deletes all scores.

## Future Enhancements

- Add a leaderboard displaying top 3 scores in the menu.
- Implement difficulty levels (e.g., increasing obstacle frequency).
- Add more obstacle types or power-ups.

## Contributing

Feel free to fork this repository, submit issues, or create pull requests with improvements!

## Author:Martha Mwangi
 If you encounter any issues with the code or need assistance, kindly reach out through:
 - email ..<marthawanguimwangi4@gmail.com> 

## License
Copyright (c) 2024 Martha-Mwangii

Have fun!! 🚀