# Rock Paper Scissors Battle Game

A fun pygame implementation of rock-paper-scissors where objects battle automatically in a 2D arena!

## Features

- **Automated Gameplay**: Objects spawn and battle each other without user input
- **Configurable Object Count**: Use UI controls to set how many of each object type spawn
- **Physics-Based Movement**: Objects move at 1 inch per second and bounce off walls
- **Battle Rules**: 
  - Rock beats Scissors
  - Scissors beats Paper
  - Paper beats Rock
- **Real-time Counters**: See how many of each object type remain
- **Victory Conditions**: Game ends when only one object type survives

## Setup

1. **Install Python** (3.7+ recommended)

2. **Create virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Sprites** (optional):
   - Place PNG images in `assets/sprites/` folder:
     - `rock.png` (64x64 pixels recommended)
     - `paper.png` (64x64 pixels recommended) 
     - `scissors.png` (64x64 pixels recommended)
   - If no sprites are provided, the game will use colored circles with labels

## How to Run

```bash
python game.py
```

## Controls

- **Object Count Control**: Use ▲/▼ arrows to increase/decrease the number of objects per type (1-50)
- **New Game Button**: Start a new battle with the current object count setting
- **Close Window**: Quit the game

## Game Mechanics

- Objects spawn from different corners:
  - Scissors: Bottom left
  - Paper: Bottom right  
  - Rock: Top right
- Each object moves in a random direction at spawn
- Objects bounce off screen boundaries like pool balls
- When objects collide, the winner continues moving while the loser disappears
- Game ends when only one object type remains

## Customization

You can modify these constants in `game.py`:

- `OBJECT_SIZE_RATIO`: Size of objects relative to screen (default: 1/20)
- `SPAWN_INTERVAL`: Time between spawns in seconds (default: 0.1)
- `SPEED_INCHES_PER_SEC`: Movement speed (default: 1 inch per second)
- `WINDOW_WIDTH` / `WINDOW_HEIGHT`: Game window dimensions

Enjoy the battle!
