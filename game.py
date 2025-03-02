#  #game..py
# import imgui
# import numpy as np
# from utils.graphics import Object, Camera, Shader
# from assets.shaders.shaders import object_shader , lighting_shader
# from assets.objects.objects import  get_planet , get_space_station , get_transporter , rotation_matrix
# import random
# from OpenGL.GL import *
# import copy
# import sys

# class Game:
#     def __init__(self, height, width, gui):
#         self.gui = gui
#         self.height = height
#         self.width = width
#         self.screen = 0
#         self.menu_selection = 1  # 1: New Game, 2: Exit
#         self.shaders = [Shader(lighting_shader["vertex_shader"], lighting_shader["fragment_shader"])]
#         self.objects = {}

#         self.prev_key_states = {}
    

#     def InitScene(self):
#         if self.screen == 1:

#             def setCamera():
#                 self.camera = Camera(self.height, self.width)
#                 self.camera.position = np.array([0, 0, 0], dtype=np.float32)
#                 self.camera.lookAt = np.array([0, 0, -1], dtype=np.float32)
#                 self.camera.up = np.array([0, 1, 0], dtype=np.float32)
#                 self.camera.fov = 45
#                 self.camera.near = 1.0
#                 self.camera.far = 10000.0
                
#             setCamera()
#             ############################################################################

#             def setWorldLimits():
#                 self.worldMin = np.array([-5000, -5000, -5000], dtype=np.float32)
#                 self.worldMax = np.array([5000, 5000, 5000], dtype=np.float32)
#             setWorldLimits()

#             ############################################################################

            

#             ############################################################################

#             # Initialize Planets and space stations (Randomly place n planets and n spacestations within world bounds)
#             self.n_planets = 10 # for example

#             self.objects["planets"] = []
#             for i in range(self.n_planets):
#                 greyish_white = np.array([0.8, 0.8, 0.8])
#                 # bottom_color = np.array([random.random(), random.random(), random.random()])
#                 # top_color = np.array([random.random(), random.random(), random.random()])
#                 # top_color =greyish_white
#                 # bottom_color = greyish_white
#                 top_color = np.random.uniform(0.7, 1.0, 3)
#                 bottom_color = np.random.uniform(0.7, 1.0, 3)

#                 planet = get_planet(bottom_color , top_color)  # get default planet properties with gradient colors
#                 # Set a random position: x in [-300,300], y in [-300,300], z in [-150, -30]
                
#                 if "normals" not in planet:
#                     n_vertices = len(planet["vertices"]) // 3
#                     # Create a flat array of n_vertices copies of (0, 0, 1)
#                     default_normals = np.tile(np.array([0, 0, 1], dtype=np.float32), n_vertices)
#                     planet["normals"] = default_normals

#                 pos = np.array([
#                     np.random.uniform(-50, 50),
#                     np.random.uniform(-50, 50),
#                     np.random.uniform(-150, -40)
#                 ], dtype=np.float32)

#                 planet["position"] = pos
#                 # Optionally, set a random uniform scale between 0.5 and 2.0
#                 scale_val = 5.0
#                 planet["scale"] = np.array([scale_val, scale_val, scale_val], dtype=np.float32)
#                 # Create the planet object and add it to the list
#                 self.objects["planets"].append(Object(None, self.shaders[0], planet))
            

#             self.objects["stations"] = []
#             for planet_obj in self.objects.get("planets", []):
#                 station = get_space_station()

#                 if "normals" not in station:
#                     n_vertices = len(station["vertices"]) // 3
#                     station["normals"] = np.tile(np.array([0, 0, 1], dtype=np.float32), n_vertices)
                
#                 orbit_radius = 10.0  # Adjust as needed
#                 orbit_angle = random.uniform(0, 2 * np.pi)
#                 # inclination = random.uniform(-np.radians(60), np.radians(60))  # Adjust as needed
    
#                 # Compute the initial offset based on orbit_radius and orbit_angle.
#                 offset = np.array([
#                     orbit_radius * np.cos(orbit_angle) ,
#                     0,
#                     orbit_radius * np.sin(orbit_angle)  # For simplicity, keep z offset zero. Adjust if needed.
#                 ], dtype=np.float32)

#                 # Tie the station to its planet: the orbit center is the planet's position.
#                 orbit_center = planet_obj.properties["position"].copy()
                
#                 station["orbitCenter"] = planet_obj.properties["position"].copy()

#                 station["position"] = orbit_center + offset
#                 # Store the orbital properties using our custom keys.
#                 station["rotation_radius"] = orbit_radius
#                 station["init_position"] = orbit_center.copy()
#                 # Also store the current orbit angle in the Z rotation component.
#                 station["rotation"] =  np.array([0, 0, orbit_angle], dtype=np.float32)
#                 station["scale"] = np.array([0.7, 0.7, 0.7], dtype=np.float32)
#                 self.objects["stations"].append(Object(None, self.shaders[0], station))
                
#                 # Optionally, make the station smaller.
                
#                 # Create the station object and add it to our stations list.
#                 # self.objects["stations"].append(Object(None, self.shaders[0], station))
                
#             if len(self.objects["planets"]) > 0:
#                 target_index = random.randint(0, len(self.objects["planets"]) - 1)
#                 print(f"target index is {target_index}, for planet list length {len(self.objects['planets'])}, and station list length {len(self.objects['stations'])}")
#                 self.target_planet = self.objects["planets"][target_index]
#                 self.target_station = self.objects["stations"][target_index]
                
#                 # Change target planet and station color to green
#                 green_color = np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32)
                
#                 # Instead of setting the 'color' property, update the VBO data.
#                 # The interleaved layout per vertex is: [pos (3), color (4), normal (3)]
#                 # So for each vertex, the color data starts at offset 3 (floats) with a stride of 10 floats.
#                 vbo_id = self.target_planet.vbo.ID
#                 num_vertices = self.target_planet.num_vertices
#                 glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
#                 for i in range(num_vertices):
#                     offset = (i * 10 + 3) * 4  # offset in bytes (each float is 4 bytes)
#                     glBufferSubData(GL_ARRAY_BUFFER, offset, 4 * 4, green_color)    
                
#                 # Set station colors to green
#                 if "color" in self.target_station.properties:
#                     self.target_station.properties["color"] = green_color
                    
#                 print(f"Station properties after setting color: {self.target_station.properties}")
                
#                 print(f"Target set to planet at position {self.target_planet.properties['position']}")

#             ############################################################################
#             # Initialize transporter (Randomly choose start and end planet, and initialize transporter at start planet)
            
#             self.objects["transporter"] = None
#             transporter = get_transporter()
#             transporter["position"] = np.array([0, -1.5, -5], dtype=np.float32)
#             transporter["scale"] = np.array([0.15, 0.15, 0.15], dtype=np.float32)
#             # transporter["rotation"] = np.array([0 , np.pi/2, np.pi/2], dtype=np.float32)
#             self.objects["transporter"] = Object(None, self.shaders[0], transporter)
            
#             # self.objects["transporter"] = None
#             # if len(self.objects["planets"]) > 0:
#             #     # Pick the first planet (or choose randomly).
#             #     source_planet = self.objects["planets"][0]
#             #     transporter = get_transporter()
#             #     # Position the transporter at a fixed offset from the planet (e.g., slightly above it).
#             #     transporter["position"] = source_planet.properties["position"] + np.array([0, 0, 5], dtype=np.float32)
#             #     # Set an appropriate scale for the transporter.
#             #     transporter["scale"] = np.array([2, 2.5, 2.5], dtype=np.float32)
#             #     self.objects["transporter"] = Object(None, self.shaders[0], transporter)


#             ############################################################################
#             # Initialize Pirates (Spawn at random locations within world bounds)
#             self.n_pirates = 20 # for example

#             ############################################################################
#             # Initialize minimap arrow (Need to write orthographic projection shader for it)

#             ############################################################################

#     def ProcessFrame(self, inputs, time):
#         imgui.new_frame()
#         self.DrawText(inputs)
#         self.UpdateScene(inputs, time)
#         self.DrawScene()
        
#         imgui.render()
#         self.gui.render(imgui.get_draw_data())

#     def DrawText(self, inputs=None):
#         if self.screen == 0:  # Main menu screen
#             window_w, window_h = 400, 200
#             x_pos = (self.width - window_w) / 2
#             y_pos = (self.height - window_h) / 2

#             imgui.set_next_window_position(x_pos, y_pos)
#             imgui.set_next_window_size(window_w, window_h)
#             imgui.begin("Main Menu", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)
#             # Highlight selected option.
#             if self.menu_selection == 1:
#                 imgui.text_colored("1: New Game", 0.0, 1.0, 0.0, 1.0)
#             else:
#                 imgui.text("1: New Game")
#             if self.menu_selection == 2:
#                 imgui.text_colored("2: Exit", 0.0, 1.0, 0.0, 1.0)
#             else:
#                 imgui.text("2: Exit")
                
#             imgui.spacing()
#             imgui.separator()
#             imgui.text("Press 1 or 2 to select, ENTER to confirm")
            
#             imgui.end()

#         if self.screen == 2: # YOU WON Screen
#             pass

#         if self.screen == 3: # GAME OVER Screen
#             pass
        
#     def UpdateScene(self, inputs, time):
        
#         if self.screen == 0:
#             # Debug the inputs
#             print(f"Current inputs: {inputs}")
            
#             # Get current key states
#             key_1_pressed = bool(inputs.get("1"))
#             key_2_pressed = bool(inputs.get("2"))
#             enter_pressed = bool(inputs.get("ENTER"))
            
#             # Detect key presses (pressed this frame but not last frame)
#             key_1_press = key_1_pressed and not self.prev_key_states.get("1", False)
#             key_2_press = key_2_pressed and not self.prev_key_states.get("2", False)
#             enter_press = enter_pressed and not self.prev_key_states.get("ENTER", False)
            
#             # Update menu selection
#             if key_1_press:
#                 self.menu_selection = 1
#                 print("Selected: New Game")
#             if key_2_press:
#                 self.menu_selection = 2
#                 print("Selected: Exit")
                
#             # Process selection when ENTER is pressed
#             if enter_press:
#                 print(f"ENTER pressed, selection: {self.menu_selection}")
#                 if self.menu_selection == 1:
#                     print("Starting New Game")
#                     self.screen = 1
#                     self.InitScene()
#                 elif self.menu_selection == 2:
#                     print("Exiting Game")
#                     sys.exit(0)
                    
#             # Store current key states for next frame
#             self.prev_key_states = {
#                 "1": key_1_pressed,
#                 "2": key_2_pressed,
#                 "ENTER": enter_pressed
#             }
#             return

#         if self.screen == 1: # Game screen
#             ############################################################################
#             # Update each space station's orbital motion.
#             # angular_speed = 0.5  # radians per second (adjust as needed)
#             # delta = time["deltaTime"]
#             delta = time["deltaTime"]
#             theta = 0.4 * delta  # Increment per frame.
            
#             if hasattr(self, 'target_station') and self.objects.get("transporter") is not None:
#                 arrow_window_size = 120
#                 arrow_padding = 10
#                 minimap_x = self.width - arrow_window_size - arrow_padding
#                 minimap_y = self.height - arrow_window_size - arrow_padding

#                 # Set next window position and size; don't call imgui.new_frame() here.
#                 imgui.set_next_window_position(minimap_x, minimap_y)
#                 imgui.set_next_window_size(arrow_window_size, arrow_window_size)
#                 imgui.begin("##MiniMap", False, 
#                             imgui.WINDOW_NO_TITLE_BAR | 
#                             imgui.WINDOW_NO_RESIZE | 
#                             imgui.WINDOW_NO_SCROLLBAR)
                
#                 # Calculate the center based on our known window coordinates.
#                 center_x = minimap_x + arrow_window_size / 2
#                 center_y = minimap_y + arrow_window_size / 2

#                 transporter_pos = self.objects["transporter"].properties["position"]
#                 target_pos = self.target_station.properties["position"]
#                 direction = target_pos - transporter_pos
#                 direction_xy = np.array([direction[0], direction[1]])

#                 if np.linalg.norm(direction_xy) > 0.001:
#                     direction_xy = direction_xy / np.linalg.norm(direction_xy)

#                 elevation_diff = target_pos[2] - transporter_pos[2]
#                 if abs(elevation_diff) < 3.0:
#                     arrow_color = (1.0, 1.0, 1.0, 1.0)
#                 elif elevation_diff > 0:
#                     arrow_color = (1.0, 0.2, 0.2, 1.0)
#                 else:
#                     arrow_color = (0.2, 0.2, 1.0, 1.0)

#                 angle = np.arctan2(direction_xy[1], direction_xy[0])
#                 arrow_size = 30
#                 # Base arrow triangle points (centered at origin, pointing up)
#                 p1 = (0, -arrow_size / 2)
#                 p2 = (-arrow_size / 4, arrow_size / 2)
#                 p3 = (arrow_size / 4, arrow_size / 2)

#                 def rotate_point(p, angle):
#                     c = np.cos(angle - np.pi / 2)
#                     s = np.sin(angle - np.pi / 2)
#                     return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)

#                 p1r = rotate_point(p1, angle)
#                 p2r = rotate_point(p2, angle)
#                 p3r = rotate_point(p3, angle)

#                 p1_screen = (center_x + p1r[0], center_y + p1r[1])
#                 p2_screen = (center_x + p2r[0], center_y + p2r[1])
#                 p3_screen = (center_x + p3r[0], center_y + p3r[1])

#                 draw_list = imgui.get_window_draw_list()
#                 draw_list.add_triangle_filled(
#                     p1_screen[0], p1_screen[1],
#                     p2_screen[0], p2_screen[1],
#                     p3_screen[0], p3_screen[1],
#                     imgui.get_color_u32_rgba(*arrow_color)
#                 )

#                 # Optionally display the distance as text.
#                 distance = np.linalg.norm(direction)
#                 imgui.text(f"Distance: {distance:.1f}")

#                 imgui.end() 

#             for station_obj in self.objects.get("stations", []):
#                 station_obj.properties["rotation"][2] += theta
#                 radius = station_obj.properties["rotation_radius"]
#                 center = station_obj.properties["init_position"]
#                 station_obj.properties["position"][0] = center[0] + radius * np.cos(station_obj.properties["rotation"][2])
#                 station_obj.properties["position"][1] = center[1] + radius * np.sin(station_obj.properties["rotation"][2])
#                 station_obj.properties["position"][2] = center[2]

#             if self.objects.get("transporter") is not None:
#                 transporter = self.objects["transporter"]
#                 if "orientation" not in transporter.properties:
#                     t_rot = transporter.properties["rotation"]
#                     transporter.properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
                
#                 # Get current orientation.
#                 current_orient = transporter.properties["orientation"]

#                 rotation_speed = 0.5  # radians per second
#                 dR = np.eye(3, dtype=np.float32)
#                 if inputs.get("W"): dR = dR @ rotation_matrix(rotation_speed * delta, 0, 0)[:3, :3]  # pitch down
#                 if inputs.get("S"): dR = dR @ rotation_matrix(-rotation_speed * delta, 0, 0)[:3, :3]  # pitch up
#                 if inputs.get("A"): dR = dR @ rotation_matrix(0, rotation_speed * delta, 0)[:3, :3]  # yaw left
#                 if inputs.get("D"): dR = dR @ rotation_matrix(0, -rotation_speed * delta, 0)[:3, :3]  # yaw right
#                 if inputs.get("Q"): dR = dR @ rotation_matrix(0, 0, rotation_speed * delta)[:3, :3]  # roll left
#                 if inputs.get("E"): dR = dR @ rotation_matrix(0, 0, -rotation_speed * delta)[:3, :3]  # roll right

#                 new_orient = current_orient @ dR
#                 transporter.properties["orientation"] = new_orient

#                 max_speed = 10.0 

#                 forward_spaceship = new_orient @ np.array([0, 0, -1], dtype=np.float32)
#                 up_spaceship = new_orient @ np.array([0, 1, 0], dtype=np.float32)

#                 if inputs.get("SPACE"):
#                     transporter.properties["speed"] += 0.05
#                     if transporter.properties["speed"] > max_speed:
#                         transporter.properties["speed"] = max_speed

#                     transporter.properties["velocity"] = transporter.properties["speed"] * forward_spaceship
#                 else:
#                     transporter.properties["speed"] = 0.0
#                     transporter.properties["velocity"] = np.array([0, 0, 0], dtype=np.float32)

#                 transporter.properties["position"] += transporter.properties["velocity"] * delta
            
#                 self.camera.lookAt = forward_spaceship
#                 self.camera.up = up_spaceship
#                 self.camera.position = copy.deepcopy(transporter.properties["position"]) - (5*forward_spaceship) + (up_spaceship)
#             # Manage inputs 
            
#             ############################################################################
#             # Update transporter (Update velocity, position, and check for collisions)
           

#             ############################################################################
#             # Update spacestations (Update velocity and position to revolve around respective planet)
            

#             ############################################################################
#             # Update Minimap Arrow: (Set direction based on transporter velocity direction and target direction)
            

#             ############################################################################
#             # Update Lasers (Update position of any currently shot lasers, make sure to despawn them if they go too far to save computation)
           
            
#             ############################################################################
#             # Update Pirates (Write logic to update their velocity based on transporter position, and check for collision with laser or transporter)
            

#             ############################################################################
#             # Update Camera (Check for view (3rd person or 1st person) and set position and LookAt accordingly)
            

#             ############################################################################
#             pass
        
#         # elif self.screen == 0: # Example start screen
#         #     if inputs.get("1"):
#         #         self.screen = 1
#         #         self.InitScene()
                
                
        
#         elif self.screen == 2: # YOU WON
#             pass
#         elif self.screen == 3: # GAME OVER
#             pass
    
#     def DrawScene(self):
#         if self.screen == 1: 
#             ######################################################
#             # Example draw statements
            
#             for shader in (self.shaders):
#                 self.camera.Update(shader)
#                 lightPosLocation = glGetUniformLocation(shader.ID, "lightPos".encode('utf-8'))
#                 glUniform3f(lightPosLocation, 100.0, 100.0, 100.0)
#                 viewPosLocation = glGetUniformLocation(shader.ID, "viewPos".encode('utf-8'))
#                 glUniform3f(viewPosLocation, self.camera.position[0], self.camera.position[1], self.camera.position[2])
#                 glUniform1f(glGetUniformLocation(shader.ID, "ambientStrength".encode('utf-8')), 0.3)
#                 glUniform1f(glGetUniformLocation(shader.ID, "specularStrength".encode('utf-8')), 0.8)
#                 glUniform1f(glGetUniformLocation(shader.ID, "shininess".encode('utf-8')), 64.0)

#             for planet_obj in self.objects.get("planets", []):
#                 planet_obj.Draw()
            
#             for station_obj in self.objects.get("stations", []):
#                 station_obj.Draw()
            
#             if self.objects.get("transporter") is not None:
#                 self.objects["transporter"].Draw()

#             # self.gameState["transporter"].Draw()
#             # self.gameState["stars"].Draw()
#             # self.gameState["arrow"].Draw()

#             # if self.gameState["transporter"].properties["view"] == 2: # Conditionally draw crosshair
#             #     self.gameState["crosshair"].Draw()

#             # for laser in self.gameState["lasers"]:
#             #     laser.Draw()
#             # for planet in self.gameState["planets"]:
#             #     planet.Draw()
#             # for spaceStation in self.gameState["spaceStations"]:
#             #     spaceStation.Draw()
#             # for pirate in self.gameState["pirates"]:
#             #     pirate.Draw()
#             ######################################################
#             pass

import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader, lighting_shader
from assets.objects.objects import get_planet, get_space_station, get_transporter, rotation_matrix
import random
from OpenGL.GL import *
import copy
import sys

class Game:
    def __init__(self, height, width, gui):
        self.gui = gui
        self.height = height
        self.width = width
        self.screen = 0              # 0 = Main Menu, 1 = Game, etc.
        self.menu_selection = 1      # 1: New Game, 2: Exit
        self.shaders = [Shader(lighting_shader["vertex_shader"], lighting_shader["fragment_shader"])]
        self.objects = {}

    def InitScene(self):
        if self.screen == 1:
            # Set up camera
            def setCamera():
                self.camera = Camera(self.height, self.width)
                self.camera.position = np.array([0, 0, 0], dtype=np.float32)
                self.camera.lookAt = np.array([0, 0, -1], dtype=np.float32)
                self.camera.up = np.array([0, 1, 0], dtype=np.float32)
                self.camera.fov = 45
                self.camera.near = 1.0
                self.camera.far = 10000.0
            setCamera()

            # Set world limits
            def setWorldLimits():
                self.worldMin = np.array([-5000, -5000, -5000], dtype=np.float32)
                self.worldMax = np.array([5000, 5000, 5000], dtype=np.float32)
            setWorldLimits()

            # Initialize Planets
            self.n_planets = 10  # example
            self.objects["planets"] = []
            for i in range(self.n_planets):
                top_color = np.random.uniform(0.7, 1.0, 3)
                bottom_color = np.random.uniform(0.7, 1.0, 3)
                planet = get_planet(bottom_color, top_color)  # should return dict with key "positions"
                if "normals" not in planet:
                    n_vertices = len(planet["positions"]) // 3
                    default_normals = np.tile(np.array([0, 0, 1], dtype=np.float32), n_vertices)
                    planet["normals"] = default_normals

                pos = np.array([
                    np.random.uniform(-50, 50),
                    np.random.uniform(-50, 50),
                    np.random.uniform(-150, -40)
                ], dtype=np.float32)
                planet["position"] = pos
                scale_val = 5.0
                planet["scale"] = np.array([scale_val, scale_val, scale_val], dtype=np.float32)
                self.objects["planets"].append(Object(None, self.shaders[0], planet))

            # Initialize Stations
            self.objects["stations"] = []
            for planet_obj in self.objects.get("planets", []):
                station = get_space_station()
                if "normals" not in station:
                    n_vertices = len(station["positions"]) // 3
                    station["normals"] = np.tile(np.array([0, 0, 1], dtype=np.float32), n_vertices)
                orbit_radius = 10.0
                orbit_angle = random.uniform(0, 2 * np.pi)
                offset = np.array([
                    orbit_radius * np.cos(orbit_angle),
                    0,
                    orbit_radius * np.sin(orbit_angle)
                ], dtype=np.float32)
                orbit_center = planet_obj.properties["position"].copy()
                station["orbitCenter"] = orbit_center.copy()
                station["position"] = orbit_center + offset
                station["rotation_radius"] = orbit_radius
                station["init_position"] = orbit_center.copy()
                station["rotation"] = np.array([0, 0, orbit_angle], dtype=np.float32)
                station["scale"] = np.array([0.7, 0.7, 0.7], dtype=np.float32)
                self.objects["stations"].append(Object(None, self.shaders[0], station))

            # Choose a target planet/station and update its color to green.
            if len(self.objects["planets"]) > 0:
                target_index = random.randint(0, len(self.objects["planets"]) - 1)
                print(f"Target index: {target_index}")
                self.target_planet = self.objects["planets"][target_index]
                self.target_station = self.objects["stations"][target_index]

                green_color = np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32)
                vbo_id = self.target_planet.vbo.ID
                num_vertices = self.target_planet.num_vertices
                glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
                for i in range(num_vertices):
                    # Layout: [pos(3), color(4), normal(3)] → color starts at offset 3.
                    offset = (i * 10 + 3) * 4  # bytes
                    glBufferSubData(GL_ARRAY_BUFFER, offset, 4 * 4, green_color)
                if "color" in self.target_station.properties:
                    self.target_station.properties["color"] = green_color
                print(f"Target planet at: {self.target_planet.properties['position']}")

            # Initialize transporter.
            self.objects["transporter"] = None
            transporter = get_transporter()
            transporter["position"] = np.array([0, -1.5, -5], dtype=np.float32)
            transporter["scale"] = np.array([0.15, 0.15, 0.15], dtype=np.float32)
            self.objects["transporter"] = Object(None, self.shaders[0], transporter)

            # (Additional initialization like Pirates, minimap arrow, etc.)
            self.n_pirates = 20  # example

    def ProcessFrame(self, inputs, time):
        # Start a single ImGui frame.
        imgui.new_frame()
        self.DrawText(inputs)
        self.UpdateScene(inputs, time)
        self.DrawScene()
        imgui.render()
        self.gui.render(imgui.get_draw_data())

    def DrawText(self, inputs=None):
        if self.screen == 0:  # Main menu screen
            window_w, window_h = 400, 200
            x_pos = (self.width - window_w) / 2
            y_pos = (self.height - window_h) / 2

            imgui.set_next_window_position(x_pos, y_pos)
            imgui.set_next_window_size(window_w, window_h)
            imgui.begin("Main Menu", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

            # Display and highlight menu options.
            if self.menu_selection == 1:
                imgui.text_colored("1: New Game", 0.0, 1.0, 0.0, 1.0)
            else:
                imgui.text("1: New Game")
            if self.menu_selection == 2:
                imgui.text_colored("2: Exit", 0.0, 1.0, 0.0, 1.0)
            else:
                imgui.text("2: Exit")
            imgui.spacing()
            imgui.separator()
            imgui.text("Press 1 or 2 to select, ENTER to confirm")
            imgui.end()

        # (You can add other screens such as YOU WON or GAME OVER here.)

    def UpdateScene(self, inputs, time):
        if self.screen == 0:
            # Update menu selection from inputs.
            if inputs.get("1") is True:
                self.menu_selection = 1
                # print("Menu: New Game selected")
            if inputs.get("2") is True:
                self.menu_selection = 2
                # print("Menu: Exit selected")
            # Confirm selection on ENTER.
            if inputs.get("ENTER") is True:
                print(f"ENTER pressed, menu selection: {self.menu_selection}")
                if self.menu_selection == 1:
                    print("Starting New Game")
                    self.screen = 1
                    self.InitScene()
                elif self.menu_selection == 2:
                    print("Exiting Game")
                    sys.exit(0)
            return  # Do not update game objects when in main menu.

        if self.screen == 1:  # Game screen updates.
            delta = time["deltaTime"]
            theta = 0.4 * delta

                # Draw minimap arrow.
            # Draw minimap arrow.
            # if hasattr(self, 'target_station') and self.objects.get("transporter") is not None:
            #     # Set up minimap window parameters.
            #     arrow_window_size = 150
            #     arrow_padding = 10
            #     minimap_x = self.width - arrow_window_size - arrow_padding
            #     minimap_y = self.height - arrow_window_size - arrow_padding - 100  # Adjust vertical offset as needed

            #     # We compute center from the known minimap values.
            #     center_x = minimap_x + arrow_window_size / 2
            #     center_y = minimap_y + arrow_window_size / 2

            #     imgui.set_next_window_position(minimap_x, minimap_y)
            #     imgui.set_next_window_size(arrow_window_size, arrow_window_size)
            #     imgui.begin("##MiniMap", False, 
            #                 imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR)

            #     # Get positions from transporter and target.
            #     transporter_pos = self.objects["transporter"].properties["position"]
            #     target_pos = self.target_planet.properties["position"]
            #     direction = target_pos - transporter_pos

            #     # Debug: show raw direction components.
            #     imgui.text(f"Dir: {direction[0]:.1f}, {direction[1]:.1f}, {direction[2]:.1f}")

            #     # Compute XY projection.
            #     direction_xy = np.array([direction[0], direction[1]])
            #     norm = np.linalg.norm(direction_xy)
            #     imgui.text(f"Norm: {norm:.2f}")
            #     if norm > 0.001:
            #         direction_xy = direction_xy / norm
            #     else:
            #         direction_xy = np.array([0.0, -1.0])  # Default to up if too close

            #     # Compute angle from the positive X axis.
            #     raw_angle = np.arctan2(direction_xy[1], direction_xy[0])
            #     # Adjust the angle so that the arrow (which by default points upward, i.e. along (0, -1)) rotates correctly.
            #     arrow_rotation = raw_angle + np.pi/2

            #     imgui.text(f"Angle: {arrow_rotation:.2f}")

            #     # Set arrow color based on elevation difference.
            #     elevation_diff = target_pos[2] - transporter_pos[2]
            #     if abs(elevation_diff) < 3.0:
            #         arrow_color = (0.0, 1.0, 0.0, 1.0)  # Bright green
            #     elif elevation_diff > 0:
            #         arrow_color = (1.0, 0.0, 0.0, 1.0)  # Bright red
            #     else:
            #         arrow_color = (0.0, 0.0, 1.0, 1.0)  # Bright blue

            #     # Define a larger arrow.
            #     arrow_size = 50

            #     # Define arrow triangle in local coordinates (default arrow points upward).
            #     # p1 is the tip, p2 and p3 are the base vertices.
            #     p1 = (0, -arrow_size / 2)
            #     p2 = (-arrow_size / 3, arrow_size / 2)
            #     p3 = (arrow_size / 3, arrow_size / 2)

            #     def rotate_point(p, angle):
            #         c = np.cos(angle)
            #         s = np.sin(angle)
            #         return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)

            #     # Rotate each point by the adjusted angle.
            #     p1r = rotate_point(p1, arrow_rotation)
            #     p2r = rotate_point(p2, arrow_rotation)
            #     p3r = rotate_point(p3, arrow_rotation)

            #     # Translate the rotated points to screen coordinates.
            #     p1_screen = (center_x + p1r[0], center_y + p1r[1])
            #     p2_screen = (center_x + p2r[0], center_y + p2r[1])
            #     p3_screen = (center_x + p3r[0], center_y + p3r[1])

            #     # Debug: print arrow vertices.
            #     imgui.text(f"P1: {p1_screen[0]:.1f}, {p1_screen[1]:.1f}")
            #     imgui.text(f"P2: {p2_screen[0]:.1f}, {p2_screen[1]:.1f}")
            #     imgui.text(f"P3: {p3_screen[0]:.1f}, {p3_screen[1]:.1f}")

            #     # Draw a circular background for the minimap.
            #     draw_list = imgui.get_window_draw_list()
            #     draw_list.add_circle_filled(center_x, center_y, arrow_window_size/2 - 10, 
            #                                 imgui.get_color_u32_rgba(0.2, 0.2, 0.2, 0.7))
            #     # Draw a dot at the center.
            #     draw_list.add_circle_filled(center_x, center_y, 5, 
            #                                 imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0))
            #     # Draw the arrow.
            #     draw_list.add_triangle_filled(
            #         p1_screen[0], p1_screen[1],
            #         p2_screen[0], p2_screen[1],
            #         p3_screen[0], p3_screen[1],
            #         imgui.get_color_u32_rgba(*arrow_color)
            #     )
            #     # Draw the arrow outline.
            #     draw_list.add_triangle(
            #         p1_screen[0], p1_screen[1],
            #         p2_screen[0], p2_screen[1],
            #         p3_screen[0], p3_screen[1],
            #         imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0),
            #         2.0
            #     )

            #     # Display the distance.
            #     distance = np.linalg.norm(direction)
            #     imgui.text(f"Distance: {distance:.1f}")

            #     imgui.end()
            
            
            def DrawMinimapArrow(self):
                """
                Draw a 2D arrow on the background (top–right corner) pointing toward the target,
                calculated in the transporter's local space.
                """
                # Ensure we have both transporter and target
                if self.objects.get("transporter") is None or not hasattr(self, "target_planet"):
                    return

                # Get positions
                transporter = self.objects["transporter"]
                player_pos = transporter.properties["position"]
                destination_pos = self.target_planet.properties["position"]
                
                # Ensure transporter orientation is available.
                if "orientation" not in transporter.properties:
                    # You might want to update it here if not already set.
                    t_rot = transporter.properties.get("rotation", np.array([0,0,0], dtype=np.float32))
                    transporter.properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
                orientation = transporter.properties["orientation"]

                # Compute the local orientation axes from the transporter's orientation matrix.
                # (Assuming standard basis: forward is (0,0,-1), right is (1,0,0), up is (0,1,0))
                forward_dir = orientation @ np.array([0, 0, -1], dtype=np.float32)
                right_dir   = orientation @ np.array([1, 0, 0], dtype=np.float32)
                up_dir      = orientation @ np.array([0, 1, 0], dtype=np.float32)

                # Calculate vector from player to destination (world space)
                world_direction = destination_pos - player_pos
                distance = np.linalg.norm(world_direction)
                if distance < 10:
                    return  # Skip arrow drawing if too close
                if distance > 0:
                    world_direction = world_direction / distance

                # Transform world direction to transporter's local space via dot products.
                local_forward = np.dot(world_direction, forward_dir)
                local_right   = np.dot(world_direction, right_dir)
                local_up      = np.dot(world_direction, up_dir)

                # Calculate angle in player's local XY plane (forward-right plane).
                # Using -local_right so that a positive forward gives 0 radians (pointing up).
                angle = np.arctan2(-local_right, local_forward)

                # Fixed screen position (top–right corner)
                pos_x = self.width - 80
                pos_y = 80

                # Get the background draw list (drawn behind all windows)
                draw_list = imgui.get_background_draw_list()

                # Draw background circle
                circle_radius = 50
                bg_color = imgui.get_color_u32_rgba(0.0, 0.0, 0.0, 0.5)  # Semi-transparent black
                draw_list.add_circle_filled(pos_x, pos_y, circle_radius, bg_color)
                border_color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 0.7)  # White border
                draw_list.add_circle(pos_x, pos_y, circle_radius, border_color, 16, 1.5)

                # Draw forward indicator (always points up to indicate player's forward)
                forward_length = 15.0
                forward_color = imgui.get_color_u32_rgba(0.7, 0.7, 0.7, 0.6)
                draw_list.add_line(pos_x, pos_y, pos_x, pos_y - forward_length, forward_color, 1.0)
                draw_list.add_text(pos_x - 5, pos_y - forward_length - 12, forward_color, "F")

                # Arrow dimensions (from reference code)
                arrow_length = 35.0  # Total length of arrow
                head_length = 15.0   # Length of arrow head
                arrow_width = 8.0    # Width of arrow shaft
                head_width = 18.0    # Width of arrow head at its base

                # Calculate arrow points based on angle.
                sin_angle = np.sin(angle)
                cos_angle = np.cos(angle)

                # Arrow tip (head point)
                tip_x = pos_x + arrow_length * sin_angle
                tip_y = pos_y - arrow_length * cos_angle  # screen Y increases downward

                # Base of arrow head (where it meets the shaft)
                head_base_x = pos_x + (arrow_length - head_length) * sin_angle
                head_base_y = pos_y - (arrow_length - head_length) * cos_angle

                # Arrow shaft start point (tail)
                tail_x = pos_x - 0.5 * (arrow_length/3 * sin_angle)
                tail_y = pos_y + 0.5 * (arrow_length/3 * cos_angle)

                # Calculate perpendicular direction for width
                perp_x = cos_angle
                perp_y = sin_angle

                # Points for arrow head (triangle)
                left_corner_x = head_base_x + head_width/2 * perp_x
                left_corner_y = head_base_y + head_width/2 * perp_y
                right_corner_x = head_base_x - head_width/2 * perp_x
                right_corner_y = head_base_y - head_width/2 * perp_y

                # Points for arrow shaft (rectangle)
                shaft_left_top_x = head_base_x + arrow_width/2 * perp_x
                shaft_left_top_y = head_base_y + arrow_width/2 * perp_y
                shaft_right_top_x = head_base_x - arrow_width/2 * perp_x
                shaft_right_top_y = head_base_y - arrow_width/2 * perp_y
                shaft_left_bottom_x = tail_x + arrow_width/2 * perp_x
                shaft_left_bottom_y = tail_y + arrow_width/2 * perp_y
                shaft_right_bottom_x = tail_x - arrow_width/2 * perp_x
                shaft_right_bottom_y = tail_y - arrow_width/2 * perp_y

                # For arrow color, mimic reference logic (using local_forward to choose color)
                if local_forward > 0:
                    # Destination is in front of player: green to yellow.
                    g = min(1.0, 0.8 + 0.2 * local_forward)
                    r = min(1.0, (1.0 - local_forward) + distance / 10000.0)
                    b = 0.2
                else:
                    # Destination is behind player: blue to purple.
                    b = min(1.0, 0.8 - 0.2 * local_forward)
                    r = min(1.0, abs(local_forward) + distance / 10000.0)
                    g = 0.2
                arrow_color = imgui.get_color_u32_rgba(r, g, b, 1.0)

                # Draw the arrow head (triangle)
                draw_list.add_triangle_filled(
                    tip_x, tip_y,
                    left_corner_x, left_corner_y,
                    right_corner_x, right_corner_y,
                    arrow_color
                )
                # Draw the arrow shaft (rectangle)
                draw_list.add_quad_filled(
                    shaft_left_top_x, shaft_left_top_y,
                    shaft_right_top_x, shaft_right_top_y,
                    shaft_right_bottom_x, shaft_right_bottom_y,
                    shaft_left_bottom_x, shaft_left_bottom_y,
                    arrow_color
                )
                # Draw outlines for better visibility
                outline_color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 0.7)
                draw_list.add_triangle(
                    tip_x, tip_y,
                    left_corner_x, left_corner_y,
                    right_corner_x, right_corner_y,
                    outline_color, 1.0
                )
                draw_list.add_quad(
                    shaft_left_top_x, shaft_left_top_y,
                    shaft_right_top_x, shaft_right_top_y,
                    shaft_right_bottom_x, shaft_right_bottom_y,
                    shaft_left_bottom_x, shaft_left_bottom_y,
                    outline_color, 1.0
                )

                # Display distance text below the minimap.
                draw_list.add_text(pos_x - 20, pos_y + circle_radius + 5, 
                       imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0), f"{int(distance)}u")
                
                
            # DrawMinimapArrow(self)
            
            # Draw minimap arrow using error angle between target direction and ship's look.
            if hasattr(self, 'target_planet') and self.objects.get("transporter") is not None:
                # Set up minimap window
                arrow_window_size = 150
                arrow_padding = 10
                minimap_x = self.width - arrow_window_size - arrow_padding
                minimap_y = arrow_padding
                center_x = minimap_x + arrow_window_size / 2
                center_y = minimap_y + arrow_window_size / 2

                imgui.set_next_window_position(minimap_x, minimap_y)
                imgui.set_next_window_size(arrow_window_size, arrow_window_size)
                imgui.begin("##MiniMap", False, 
                        imgui.WINDOW_NO_TITLE_BAR | 
                        imgui.WINDOW_NO_RESIZE | 
                        imgui.WINDOW_NO_SCROLLBAR)

                # Get transporter and target positions
                transporter = self.objects["transporter"]
                ship_pos = transporter.properties["position"]
                target_pos = self.target_planet.properties["position"]
                
                # Calculate world direction vector from ship to target
                direction = target_pos - ship_pos
                distance = np.linalg.norm(direction)
                
                # Get the ship's orientation
                if "orientation" not in transporter.properties:
                    t_rot = transporter.properties.get("rotation", np.zeros(3, dtype=np.float32))
                    transporter.properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
                
                # Get the ship's forward and up vectors in world space
                forward = transporter.properties["orientation"] @ np.array([0, 0, -1], dtype=np.float32)
                right = transporter.properties["orientation"] @ np.array([1, 0, 0], dtype=np.float32)
                
                # Project vectors to XY plane and normalize
                direction_xy = np.array([direction[0], direction[1]], dtype=np.float32)
                forward_xy = np.array([forward[0], forward[1]], dtype=np.float32)
                
                # Normalize if possible
                dir_norm = np.linalg.norm(direction_xy)
                if dir_norm > 0.001:
                    direction_xy /= dir_norm
                else:
                    direction_xy = np.array([0, 1], dtype=np.float32)
                    
                fwd_norm = np.linalg.norm(forward_xy)
                if fwd_norm > 0.001:
                    forward_xy /= fwd_norm
                else:
                    forward_xy = np.array([0, 1], dtype=np.float32)
                
                # Calculate angle between forward and direction vectors using dot and cross products
                dot_product = np.dot(forward_xy, direction_xy)
                cross_product = np.cross([forward_xy[0], forward_xy[1], 0], [direction_xy[0], direction_xy[1], 0])[2]
                
                # Use atan2 to get the angle (-π to π)
                error_angle = np.arctan2(cross_product, dot_product)
                
                # Display debug info
                imgui.text(f"Distance: {distance:.1f}")
                imgui.text(f"Angle: {error_angle:.2f} rad")
                
                # Define arrow geometry (pointing up by default)
                arrow_size = 50
                p1 = (0, -arrow_size / 2)      # Tip
                p2 = (-arrow_size / 3, arrow_size / 2)  # Bottom left
                p3 = (arrow_size / 3, arrow_size / 2)   # Bottom right
                
                # Rotate by error angle
                def rotate_point(p, angle):
                    c, s = np.cos(angle), np.sin(angle)
                    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)
                
                p1r = rotate_point(p1, error_angle)
                p2r = rotate_point(p2, error_angle)
                p3r = rotate_point(p3, error_angle)
                
                # Convert to screen coordinates
                p1_screen = (center_x + p1r[0], center_y + p1r[1])
                p2_screen = (center_x + p2r[0], center_y + p2r[1])
                p3_screen = (center_x + p3r[0], center_y + p3r[1])
                
                # Draw background
                draw_list = imgui.get_window_draw_list()
                
                # Draw background circle
                draw_list.add_circle_filled(
                    center_x, center_y, 
                    arrow_window_size/2 - 10,
                    imgui.get_color_u32_rgba(0.1, 0.1, 0.1, 0.8)
                )
                
                # Draw center reference dot
                draw_list.add_circle_filled(
                    center_x, center_y, 
                    5, 
                    imgui.get_color_u32_rgba(0.7, 0.7, 0.7, 0.7)
                )
                
                # Set arrow color based on altitude difference
                elevation_diff = target_pos[2] - ship_pos[2]
                if abs(elevation_diff) < 5.0:
                    # Target is at same level (green)
                    arrow_color = (0.0, 1.0, 0.0, 1.0)
                elif elevation_diff > 0:
                    # Target is above (red)
                    arrow_color = (1.0, 0.2, 0.2, 1.0)
                else:
                    # Target is below (blue)
                    arrow_color = (0.2, 0.2, 1.0, 1.0)
                
                # Draw arrow
                draw_list.add_triangle_filled(
                    p1_screen[0], p1_screen[1],
                    p2_screen[0], p2_screen[1],
                    p3_screen[0], p3_screen[1],
                    imgui.get_color_u32_rgba(*arrow_color)
                )
                
                # Draw arrow outline
                draw_list.add_triangle(
                    p1_screen[0], p1_screen[1],
                    p2_screen[0], p2_screen[1],
                    p3_screen[0], p3_screen[1],
                    imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0),
                    1.5
                )
                
                # Show distance as text
                draw_list.add_text(
                    center_x - 20, 
                    center_y + arrow_window_size/2 - 20,
                    imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0), 
                    f"{int(distance)}u"
                )
                
                imgui.end()

            # Update station orbits.
            for station_obj in self.objects.get("stations", []):
                station_obj.properties["rotation"][2] += theta
                radius = station_obj.properties["rotation_radius"]
                center = station_obj.properties["init_position"]
                station_obj.properties["position"][0] = center[0] + radius * np.cos(station_obj.properties["rotation"][2])
                station_obj.properties["position"][1] = center[1] + radius * np.sin(station_obj.properties["rotation"][2])
                station_obj.properties["position"][2] = center[2]

            # Update transporter.
            if self.objects.get("transporter") is not None:
                transporter = self.objects["transporter"]
                if "orientation" not in transporter.properties:
                    t_rot = transporter.properties["rotation"]
                    transporter.properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
                current_orient = transporter.properties["orientation"]
                rotation_speed = 0.5
                dR = np.eye(3, dtype=np.float32)
                if inputs.get("W"): dR = dR @ rotation_matrix(rotation_speed * delta, 0, 0)[:3, :3]
                if inputs.get("S"): dR = dR @ rotation_matrix(-rotation_speed * delta, 0, 0)[:3, :3]
                if inputs.get("A"): dR = dR @ rotation_matrix(0, rotation_speed * delta, 0)[:3, :3]
                if inputs.get("D"): dR = dR @ rotation_matrix(0, -rotation_speed * delta, 0)[:3, :3]
                if inputs.get("Q"): dR = dR @ rotation_matrix(0, 0, rotation_speed * delta)[:3, :3]
                if inputs.get("E"): dR = dR @ rotation_matrix(0, 0, -rotation_speed * delta)[:3, :3]
                new_orient = current_orient @ dR
                transporter.properties["orientation"] = new_orient
                max_speed = 10.0
                forward_spaceship = new_orient @ np.array([0, 0, -1], dtype=np.float32)
                up_spaceship = new_orient @ np.array([0, 1, 0], dtype=np.float32)
                if inputs.get("SPACE"):
                    transporter.properties["speed"] += 0.05
                    if transporter.properties["speed"] > max_speed:
                        transporter.properties["speed"] = max_speed
                    transporter.properties["velocity"] = transporter.properties["speed"] * forward_spaceship
                else:
                    transporter.properties["speed"] = 0.0
                    transporter.properties["velocity"] = np.array([0, 0, 0], dtype=np.float32)
                transporter.properties["position"] += transporter.properties["velocity"] * delta
                self.camera.lookAt = forward_spaceship
                self.camera.up = up_spaceship
                self.camera.position = copy.deepcopy(transporter.properties["position"]) - (5 * forward_spaceship) + up_spaceship

        elif self.screen in (2, 3):
            # Additional screens (YOU WON, GAME OVER) go here.
            pass

    def DrawScene(self):
        if self.screen == 1:
            for shader in self.shaders:
                self.camera.Update(shader)
                lightPosLocation = glGetUniformLocation(shader.ID, "lightPos".encode('utf-8'))
                glUniform3f(lightPosLocation, 100.0, 100.0, 100.0)
                viewPosLocation = glGetUniformLocation(shader.ID, "viewPos".encode('utf-8'))
                glUniform3f(viewPosLocation, self.camera.position[0], self.camera.position[1], self.camera.position[2])
                glUniform1f(glGetUniformLocation(shader.ID, "ambientStrength".encode('utf-8')), 0.3)
                glUniform1f(glGetUniformLocation(shader.ID, "specularStrength".encode('utf-8')), 0.8)
                glUniform1f(glGetUniformLocation(shader.ID, "shininess".encode('utf-8')), 64.0)
            for planet_obj in self.objects.get("planets", []):
                planet_obj.Draw()
            for station_obj in self.objects.get("stations", []):
                station_obj.Draw()
            if self.objects.get("transporter") is not None:
                self.objects["transporter"].Draw()
