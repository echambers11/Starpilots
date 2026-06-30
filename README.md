# Starpilots
Starpilots is an action-packed 2D space shooter built in Python using Pygame. Command your starship, navigate hazardous asteroid fields, and eliminate hostile enemy forces. Take on individual custom maps or challenge yourself in full campaign modes!

![Screenshot of Starpilots Gameplay](/Images/gameplay.png)

## Features
**Intensive Physics & Movement:** Realistic inertia-based steering featuring directional thrust, acceleration, and spin mechanics.\
**Immersive Audio:** Space atmosphere with a continuous soundtrack and sound effects for lasers, asteroid impacts, and explosions.\
**Campaign Mode:** Progress through multi-level campaigns, trying to survive multiple levels in a row.\
**Highscores:** Your best scores are saved locally, so you can keep coming back to beat them!\
**Modifiable Maps:** Levels and whole campaigns can be added or modified via json files.

## Controls & How to Play
### Controls
You can review these anytime in-game via the main menu:
| Key                  | Action           |
|----------------------|------------------|
| Left Arrow           | Rotate Ship Left |
| Right Arrow          | Rotate Ship Right|
| Up Arrow             | Accelerate       |
| Down Arrow / Spacebar| Fire Lasers      |
| Escape               | Quit Match       |
### Game Rules
**Starting a Game:** Press the name of the level you want to play to start it.\
**Objective:** Defeat all enemy ships while avoiding collisions with drifting asteroids.\
**Scoring:** Your final score reduces with time. The faster and more complete your victory, the higher the final score!\
**Campaigns:** Survival is key. When playing a multi-level campaign, if you die you have to start back at the first level.\
**Leaving the Map:** If a ship or asteroid leaves the screen, it will reappear moments later at the other side.\
**Speed:** If you accelerate or turn too much you will quickly start to lose control and have trouble avoiding obstacles.\
**Your Ship:** Your ship is the maroon one below. All other ships are enemies!

![Starship 1](/Images/starship1.png)

## Getting Started
### Prerequisites
Make sure you have Python 3 installed on your system.
### Installation & Execution
**Clone the repository:**
```
  git clone https://github.com/echambers11/starpilots.git
  cd Starpilots
```
**Install dependencies:**\
This game requires pygame. You can install it via pip:
```
  pip install pygame
```
**Launch the Game:**\
Run the primary initialization file:
```
  python3 starpilots.py
```

## Built With
Python - Programming language.\
Pygame - 2D gaming framework used for graphics and audio.

## How to Make a Custom Map
### 1. File Setup
All custom map files must be saved with a .json extension inside the maps/ directory.\
**Single Level:** Save it directly as maps/your_map_name.json.\
**Campaign Level:** Create a subfolder inside maps/ and place your levels inside it ordered alphabetically or numerically (e.g., maps/my_campaign/level_1.json).

### 2. Map JSON Structure
Every map must follow this structure containing keys for "p1"(for the player), "enemies", and "asteroids":
```
{
  "p1": { "type": 1, "pos": [700, 500], "angle": 0, "dir": 0, "velo": 0, "spin": 0, "hp": 15 },
  "enemies": [
    { "type": 5, "pos": [200, 750], "angle": -45, "dir": 0, "velo": 0, "spin": 0, "hp": 5 },
    { "type": 2, "pos": [200, 200], "angle": 200, "dir": 0, "velo": 0, "spin": 0, "hp": 5 }
  ],
  "asteroids": [
    { "type": 1, "pos": [600, 300], "angle": 0, "dir": 40, "velo": 1, "spin": 5, "hp": 5 }
  ]
}
```
### 3. Entity Parameter Guide
Every object (player, enemy, asteroid) requires the exact same block of 7 parameters:\
| Parameter |    Type    |                                     Description                                    |
|-----------|------------|------------------------------------------------------------------------------------|
| "type"    | Integer    | The ID for the sprite's image (1-4 for asteroids, and 1-6 for ships).              |
| "pos"     | List [X, Y]| The starting coordinate on the screen layout array.                                |
| "angle"   | Integer    | The initial rotation angle of the entity's sprite model.                           |
| "dir"     | Integer    | The angle of the trajectory that the entity will travel along.                     |
| "velo"    | Float      | The starting forward velocity.                                                     |
| "spin"    | Integer    | How fast the object automatically rotates on its own axis over time.               |
| "hp"      | Integer    | The starting health points. When hit, this depletes until the entity is destroyed. |
### 4. Playing Your Map
Once you save your file in the maps/ directory, simply relaunch the game via python3 starpilots.py. The map manager scans the folder and it will show up as a selectable button on the menu!
