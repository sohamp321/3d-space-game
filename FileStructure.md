
```
3d-game-main/
├── assets/
│   ├── objects/
│   │   ├── __init__.py
│   │   └── objects.py         # Contains 3D model definitions
│   └── shaders/
│       ├── __init__.py
│       └── shaders.py         # Contains shader code (vertex & fragment)
├── utils/
│   ├── __init__.py
│   └── graphics.py            # Core graphics utilities (Object, Camera, Shader classes)
├── game.py                    # Main game logic
└── main.py                    # Entry point
```

### Key Components:

1. **game.py**
   - Main game logic
   - Scene management
   - Input handling
   - Object updates
   - Collision detection
   - Rendering pipeline

2. **utils/graphics.py**
   - Core graphics classes:
     - Object: 3D object management
     - Camera: View/projection handling
     - Shader: OpenGL shader management

3. **assets/objects/objects.py**
   - 3D model definitions for:
     - Planets
     - Space stations
     - Transport ship
     - Pirates
     - Lasers
   - Rotation matrix calculations

4. **assets/shaders/shaders.py**
   - Vertex and fragment shaders
   - Lighting calculations
   - Material properties

5. **main.py**
   - Program entry point
   - Window creation
   - Game loop
   - Input processing
