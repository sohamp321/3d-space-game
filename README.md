# 3D Space Transport Game

A 3D space game where you pilot a transport ship through space while avoiding or fighting pirates to deliver your payload to a designated station.

## Game Overview

You are a space transport pilot tasked with delivering crucial cargo to a specific space station. The target station orbits a green-highlighted planet among various other celestial bodies. However, space pirates are actively hunting you down! You must either evade them or defend yourself with your laser weapons.

## Core Features

- Full 3D space environment with planets and orbiting stations
- Dual perspective gameplay (Third-person and First-person views)
- Combat system with laser weapons
- Dynamic enemy AI that pursues the player
- Intuitive navigation system with directional indicator
- Physics-based movement and rotation controls

## Controls

### Ship Movement

- `W` - Pitch Up
- `S` - Pitch Down
- `A` - Yaw Left
- `D` - Yaw Right
- `Q` - Roll Left
- `E` - Roll Right
- `SPACE` - Accelerate

### Combat & Camera

- `Right Click` - Toggle between Third-Person and First-Person view
- `Left Click` - Fire lasers (in First-Person view)
- `F` - Alternative fire button for lasers

## Gameplay Mechanics

### Navigation

- A minimap shows the direction to your target planet with a color-coded arrow:
  - Green: Target is at your current elevation
  - Red: Target is above you
  - Blue: Target is below you
- Distance to target is displayed in the minimap

### Combat

- Pirates will continuously pursue your ship
- Use lasers to destroy pirates
- Destroyed pirates respawn at a safe distance
- Letting pirates get too close results in game over

### Victory Conditions

- Successfully dock with the target station orbiting the green planet
- Avoid or eliminate pursuing pirates
- Stay within the world boundaries

## Code Structure

The game is built using Python with OpenGL and implements several key components:

### Main Game Class

- Handles scene initialization
- Manages game states (menu, gameplay, win/lose conditions)
- Processes user input
- Updates game objects
- Renders the scene

### Key Systems

#### Camera System

- Implements both third-person and first-person cameras
- Smooth transitions between viewing modes
- First-person mode includes a targeting reticle

#### Physics & Movement

- 3D rotation matrices for ship orientation
- Velocity-based movement
- Collision detection for objectives and threats

#### Combat System

- Laser projectile physics
- Hit detection
- Enemy respawn mechanics

#### UI Elements

- Dynamic minimap with directional guidance
- Distance indicator
- Menu systems for game states

## Technical Requirements

- Python 3.x
- OpenGL
- NumPy
- GLFW
- ImGUI

## Installation & Running

1. Install required dependencies:

```bash
pip install numpy pyopengl glfw imgui
```

3. Run the game:

```bash
python main.py
```

## Developer Notes

The game uses a component-based architecture where each object (planets, stations, ships, lasers) is managed independently but interacts through the main game loop. The shader system handles lighting and materials, while the physics system manages movement and collisions.

Key technical features include:

- Real-time 3D graphics rendering
- Dynamic object management
- Collision detection systems
- Particle effects for lasers
- UI overlay system
