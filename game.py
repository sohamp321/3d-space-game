# import imgui
# import numpy as np
# from utils.graphics import Object, Camera, Shader
# from assets.shaders.shaders import object_shader, lighting_shader
# from assets.objects.objects import get_planet, get_space_station, get_transporter, rotation_matrix, get_pirates, get_laser
# import random
# from OpenGL.GL import *
# import copy
# import sys

# class Game:
#     def __init__(self, height, width, gui):
#         self.gui = gui
#         self.height = height
#         self.width = width
#         self.screen = 0              # 0 = Main Menu, 1 = Game, etc.
#         self.menu_selection = 1      # 1: New Game, 2: Exit
#         self.shaders = [Shader(lighting_shader["vertex_shader"], lighting_shader["fragment_shader"])]
#         self.objects = {}
#         self.fpp_camera = Camera(self.height, self.width)
#         # Configure default parameters if needed
#         self.fpp_camera.fov = 60
#         self.active_camera = None
#         # Laser firing control:
#         self.laser_cooldown = 0.0  # seconds before next laser can be fired
#         self.laser_lifetime = 5.0  # seconds a laser remains active (optional)

#     def InitScene(self):
#         if self.screen == 1:
#             # Set up camera
#             def setCamera():
#                 self.camera = Camera(self.height, self.width)
#                 self.camera.position = np.array([0, 0, 0], dtype=np.float32)
#                 self.camera.lookAt = np.array([0, 0, -1], dtype=np.float32)
#                 self.camera.up = np.array([0, 1, 0], dtype=np.float32)
#                 self.camera.fov = 45
#                 self.camera.near = 1.0
#                 self.camera.far = 10000.0
#             setCamera()

#             self.active_camera = self.camera
#             # Set world limits
#             def setWorldLimits():
#                 self.worldMin = np.array([-5000, -5000, -5000], dtype=np.float32)
#                 self.worldMax = np.array([5000, 5000, 5000], dtype=np.float32)
#             setWorldLimits()

#             # Initialize Planets
#             self.n_planets = 10  # example
#             self.objects["planets"] = []
#             for i in range(self.n_planets):
#                 top_color = np.random.uniform(0.7, 1.0, 3)
#                 bottom_color = np.random.uniform(0.7, 1.0, 3)
#                 planet = get_planet(bottom_color, top_color)  # should return dict with key "positions"
#                 if "normals" not in planet:
#                     n_vertices = len(planet["positions"]) // 3
#                     default_normals = np.tile(np.array([0, 0, 1], dtype=np.float32), n_vertices)
#                     planet["normals"] = default_normals

#                 pos = np.array([
#                     np.random.uniform(-50, 50),
#                     np.random.uniform(-50, 50),
#                     np.random.uniform(-150, -40)
#                 ], dtype=np.float32)
#                 planet["position"] = pos
#                 scale_val = 5.0
#                 planet["scale"] = np.array([scale_val, scale_val, scale_val], dtype=np.float32)
#                 self.objects["planets"].append(Object(None, self.shaders[0], planet))

#             # Initialize Stations
#             self.objects["stations"] = []
#             for planet_obj in self.objects.get("planets", []):
#                 station = get_space_station()
#                 if "normals" not in station:
#                     n_vertices = len(station["positions"]) // 3
#                     station["normals"] = np.tile(np.array([0, 0, 1], dtype=np.float32), n_vertices)
#                 orbit_radius = 10.0
#                 orbit_angle = random.uniform(0, 2 * np.pi)
#                 offset = np.array([
#                     orbit_radius * np.cos(orbit_angle),
#                     0,
#                     orbit_radius * np.sin(orbit_angle)
#                 ], dtype=np.float32)
#                 orbit_center = planet_obj.properties["position"].copy()
#                 station["orbitCenter"] = orbit_center.copy()
#                 station["position"] = orbit_center + offset
#                 station["rotation_radius"] = orbit_radius
#                 station["init_position"] = orbit_center.copy()
#                 station["rotation"] = np.array([0, 0, orbit_angle], dtype=np.float32)
#                 station["scale"] = np.array([0.7, 0.7, 0.7], dtype=np.float32)
#                 self.objects["stations"].append(Object(None, self.shaders[0], station))

#             # Choose a target planet/station and update its color to green.
#             if len(self.objects["planets"]) > 0:
#                 target_index = random.randint(0, len(self.objects["planets"]) - 1)
#                 print(f"Target index: {target_index}")
#                 self.target_planet = self.objects["planets"][target_index]
#                 self.target_station = self.objects["stations"][target_index]

#                 green_color = np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32)
#                 vbo_id = self.target_planet.vbo.ID
#                 num_vertices = self.target_planet.num_vertices
#                 glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
#                 for i in range(num_vertices):
#                     # Layout: [pos(3), color(4), normal(3)] → color starts at offset 3.
#                     offset = (i * 10 + 3) * 4  # bytes
#                     glBufferSubData(GL_ARRAY_BUFFER, offset, 4 * 4, green_color)
#                 if "color" in self.target_station.properties:
#                     self.target_station.properties["color"] = green_color
#                 print(f"Target planet at: {self.target_planet.properties['position']}")

#             # Initialize transporter.
#             self.objects["transporter"] = None
#             transporter = get_transporter()
#             transporter["position"] = np.array([0, -1.5, -5], dtype=np.float32)
#             transporter["scale"] = np.array([0.15, 0.15, 0.15], dtype=np.float32)
#             self.objects["transporter"] = Object(None, self.shaders[0], transporter)
            
#             # ### FPP Camera: When the game starts, update the FPP camera relative to the transporter.
#             # Initially, position the FPP camera in front of the transporter.
#             forward_offset = 10.0  # Distance in front of the ship for the FPP camera
#             if "orientation" not in self.objects["transporter"].properties:
#                 t_rot = self.objects["transporter"].properties.get("rotation", np.array([0,0,0], dtype=np.float32))
#                 self.objects["transporter"].properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
#             transporter_orient = self.objects["transporter"].properties["orientation"]
#             forward_vec = transporter_orient @ np.array([0, 0, -1], dtype=np.float32)
#             self.fpp_camera.position = self.objects["transporter"].properties["position"] + forward_vec * forward_offset
#             self.fpp_camera.lookAt = self.fpp_camera.position + forward_vec
#             self.fpp_camera.up = np.array([0, 1, 0], dtype=np.float32)

#             # Initialize pirates.
#             # Spawn Pirates at random positions (ensuring they are far enough from the ship).
#             self.n_pirates = 20 
#             self.objects["pirates"] = []
#             min_pirate_distance = 300
#             ship_pos = self.objects["transporter"].properties["position"]
#             for i in range(self.n_pirates):
#                 valid_spawn = False
#                 while not valid_spawn:
#                     pos = np.array([
#                         np.random.uniform(self.worldMin[0], self.worldMax[0]),
#                         np.random.uniform(self.worldMin[1], self.worldMax[1]),
#                         np.random.uniform(self.worldMin[2], self.worldMax[2])
#                     ], dtype=np.float32)
#                     if np.linalg.norm(pos - ship_pos) > min_pirate_distance:
#                         valid_spawn = True
#                 pirate = get_pirates()
#                 pirate["position"] = pos
#                 scale_val = random.uniform(10, 15)
#                 pirate["scale"] = np.array([scale_val, scale_val, scale_val], dtype=np.float32)
#                 self.objects["pirates"].append(Object(None, self.shaders[0], pirate))
#             print(f"Spawned {len(self.objects['pirates'])} pirates.")
            
#             # Initialize lasers list.
#             self.objects["lasers"] = []
#             self.laser_cooldown = 0.0
            
            
#     # def fireLaser(self):
#     #     # ### LASER CODE: Spawn a laser in FPP mode.
#     #     # Only fire if active camera is FPP.
#     #     if self.active_camera != self.fpp_camera:
#     #         return
#     #     # Get transporter info.
#     #     transporter = self.objects["transporter"]
#     #     forward_spaceship = transporter.properties["orientation"] @ np.array([0, 0, -1], dtype=np.float32)
#     #     # Laser starts a bit in front of the ship.
#     #     laser_start = transporter.properties["position"] + forward_spaceship * 5.0
#     #     laser = get_laser()
#     #     laser["position"] = laser_start
#     #     # Set laser velocity (fast).
#     #     laser_speed = 50.0
#     #     laser["velocity"] = forward_spaceship * laser_speed
#     #     # Set laser scale small.
#     #     laser["scale"] = np.array([0.5, 0.5, 0.5], dtype=np.float32)
#     #     self.objects["lasers"].append(Object(None, self.shaders[0], laser))
#     #     #Set the lifetime property
#     #     laser["lifetime"] = 0
    
#     # def fireLaser(self):
#     #     """Fires a laser from the FPP camera position through the crosshair."""
#     #     # Only fire if we're in FPP mode
#     #     if self.active_camera != self.fpp_camera:
#     #         return
            
#     #     # Calculate forward vector from camera (matches the crosshair direction)
#     #     camera_forward = self.fpp_camera.lookAt - self.fpp_camera.position
#     #     camera_forward = camera_forward / np.linalg.norm(camera_forward)
        
#     #     # Start laser exactly at the camera position
#     #     laser_start = self.fpp_camera.position.copy()
        
#     #     # Create the laser
#     #     laser = get_laser()
#     #     laser["position"] = laser_start
        
#     #     # Set laser velocity in camera's forward direction
#     #     laser_speed = 300.0
#     #     laser["velocity"] = camera_forward * laser_speed
        
#     #     # Adjust scale - make it thinner but longer for better visibility
#     #     laser["scale"] = np.array([0.05, 0.05, 2.0], dtype=np.float32)
        
#     #     # Create rotation matrix for the laser to align with firing direction
#     #     forward = camera_forward
#     #     world_up = np.array([0, 1, 0], dtype=np.float32)
        
#     #     # Handle the case where forward is parallel to world up
#     #     if abs(np.dot(forward, world_up)) > 0.999:
#     #         # If looking straight up/down, use a different reference vector
#     #         world_up = np.array([1, 0, 0], dtype=np.float32)
            
#     #     # Calculate right vector
#     #     right = np.cross(forward, world_up)
#     #     right = right / np.linalg.norm(right)
        
#     #     # Calculate actual up vector
#     #     up = np.cross(right, forward)
#     #     up = up / np.linalg.norm(up)
        
#     #     # Create rotation matrix where columns are the basis vectors
#     #     orientation = np.column_stack((right, up, -forward))
#     #     laser["orientation"] = orientation
        
#     #     # Set lifetime
#     #     laser["lifetime"] = 0
        
#     #     # Add to lasers collection
#     #     self.objects.setdefault("lasers", []).append(Object(None, self.shaders[0], laser))
        
#     #     # Print debug info
#     #     print(f"Firing laser from camera at {laser_start}")
        
        

#     #     # after the lifetime has pased
            
#     def fireLaser(self):
#         """Fires a laser from the crosshair (center of FPP view)."""
#         if self.active_camera != self.fpp_camera:
#             return

#         # Calculate the ray from the FPP camera.
#         ray_origin = self.fpp_camera.position
#         # The direction from the camera to the crosshair (center of screen) is:
#         ray_direction = self.fpp_camera.lookAt - self.fpp_camera.position
#         ray_direction = ray_direction / np.linalg.norm(ray_direction)
#         # Use the camera's near plane distance as the offset so that the laser starts at the crosshair.
#         near_offset = self.fpp_camera.near  # e.g., 1.0
#         laser_start = ray_origin + ray_direction * near_offset

#         # Create the laser using get_laser().
#         laser = get_laser()
#         laser["position"] = laser_start
#         # Set laser velocity in the ray's (forward) direction.
#         laser_speed = 300.0
#         laser["velocity"] = ray_direction * laser_speed
#         # Adjust scale: make it thin but long.
#         laser["scale"] = np.array([0.05, 0.05, 2.0], dtype=np.float32)

#         # Create a rotation matrix for the laser so it aligns with the firing direction.
#         forward = ray_direction
#         world_up = np.array([0, 1, 0], dtype=np.float32)
#         # Handle near-parallel case.
#         if abs(np.dot(forward, world_up)) > 0.999:
#             world_up = np.array([1, 0, 0], dtype=np.float32)
#         right = np.cross(forward, world_up)
#         right /= np.linalg.norm(right)
#         up = np.cross(right, forward)
#         up /= np.linalg.norm(up)
#         orientation = np.column_stack((right, up, -forward))
#         laser["orientation"] = orientation
#         # Initialize laser lifetime.
#         laser["lifetime"] = 0

#         # Add laser to the active lasers collection.
#         self.objects.setdefault("lasers", []).append(Object(None, self.shaders[0], laser))
#         print(f"Firing laser from crosshair at {laser_start}")


#     def ProcessFrame(self, inputs, time):
#         # Start a single ImGui frame.
#         imgui.new_frame()
#         self.DrawText(inputs)
#         self.UpdateScene(inputs, time)
#         self.DrawScene()
#         imgui.render()
#         self.gui.render(imgui.get_draw_data())

#     def DrawText(self, inputs=None):
#         if self.screen == 0 or self.screen == 2 or self.screen == 3:
#             window_w, window_h = 400, 200
#             x_pos = (self.width - window_w) / 2
#             y_pos = (self.height - window_h) / 2
#             imgui.set_next_window_position(x_pos, y_pos)
#             imgui.set_next_window_size(window_w, window_h)
#             if self.screen == 0:
#                 title = "Main Menu"
#             elif self.screen == 2:
#                 title = "Game Won"
#             else:
#                 title = "Game Over"
#             imgui.begin(title, False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)
#             if self.screen == 2:
#                 imgui.text_colored("Congratulations!", 0.0, 1.0, 0.0, 1.0)
#                 imgui.text("You have successfully delivered the cargo.")
#                 imgui.separator()
#             if self.screen == 3:
#                 imgui.text_colored("Game Over", 1.0, 0.0, 0.0, 1.0)
#                 imgui.text("Pirates caught you!")
#                 imgui.separator()
#             # Display options.
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
#             if self.screen == 0:
#                 imgui.text("Press 1 or 2 to select, ENTER to confirm")
#             else:
#                 imgui.text("Press ENTER to confirm your choice")
#             imgui.end()

#     def UpdateScene(self, inputs, time):
#         if self.screen == 0 or self.screen == 2 or self.screen == 3:
#             if inputs.get("1") is True:
#                 self.menu_selection = 1
#             if inputs.get("2") is True:
#                 self.menu_selection = 2
#             if inputs.get("ENTER") is True:
#                 print(f"ENTER pressed, menu selection: {self.menu_selection}")
#                 if self.menu_selection == 1:
#                     print("Starting New Game")
#                     self.screen = 1
#                     self.InitScene()
#                 elif self.menu_selection == 2:
#                     print("Exiting Game")
#                     sys.exit(0)
#             return

#         if self.screen == 1:  # Game screen updates.
#             delta = time["deltaTime"]
#             theta = 0.4 * delta

#             # Create a minimap window to show the direction to the target planet.
#             if hasattr(self, 'target_planet') and self.objects.get("transporter") is not None:
#                 # Set up minimap window
#                 arrow_window_size = 150
#                 arrow_padding = 10
#                 minimap_x = self.width - arrow_window_size - arrow_padding
#                 minimap_y = arrow_padding
#                 center_x = minimap_x + arrow_window_size / 2
#                 center_y = minimap_y + arrow_window_size / 2

#                 imgui.set_next_window_position(minimap_x, minimap_y)
#                 imgui.set_next_window_size(arrow_window_size, arrow_window_size)
#                 imgui.begin("##MiniMap", False, 
#                         imgui.WINDOW_NO_TITLE_BAR | 
#                         imgui.WINDOW_NO_RESIZE | 
#                         imgui.WINDOW_NO_SCROLLBAR)

#                 # Get transporter and target positions
#                 transporter = self.objects["transporter"]
#                 ship_pos = transporter.properties["position"]
#                 target_pos = self.target_planet.properties["position"]
                
#                 # Calculate world direction vector from ship to target
#                 direction = target_pos - ship_pos
#                 distance = np.linalg.norm(direction)
                
#                 # Get the ship's orientation
#                 if "orientation" not in transporter.properties:
#                     t_rot = transporter.properties.get("rotation", np.zeros(3, dtype=np.float32))
#                     transporter.properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
                
#                 # Get the ship's forward and up vectors in world space
#                 forward = transporter.properties["orientation"] @ np.array([0, 0, -1], dtype=np.float32)
#                 right = transporter.properties["orientation"] @ np.array([1, 0, 0], dtype=np.float32)
                
#                 # Project vectors to XY plane and normalize
#                 direction_xy = np.array([direction[0], direction[1]], dtype=np.float32)
#                 forward_xy = np.array([forward[0], forward[1]], dtype=np.float32)
                
#                 # Normalize if possible
#                 dir_norm = np.linalg.norm(direction_xy)
#                 if dir_norm > 0.001:
#                     direction_xy /= dir_norm
#                 else:
#                     direction_xy = np.array([0, 1], dtype=np.float32)
                    
#                 fwd_norm = np.linalg.norm(forward_xy)
#                 if fwd_norm > 0.001:
#                     forward_xy /= fwd_norm
#                 else:
#                     forward_xy = np.array([0, 1], dtype=np.float32)
                
#                 # Calculate angle between forward and direction vectors using dot and cross products
#                 dot_product = np.dot(forward_xy, direction_xy)
#                 cross_product = np.cross([forward_xy[0], forward_xy[1], 0], [direction_xy[0], direction_xy[1], 0])[2]
                
#                 # Use atan2 to get the angle (-π to π)
#                 error_angle = np.arctan2(cross_product, dot_product)
                
#                 # Display debug info
#                 imgui.text(f"Distance: {distance:.1f}")
#                 imgui.text(f"Angle: {error_angle:.2f} rad")
                
#                 # Define arrow geometry (pointing up by default)
#                 arrow_size = 50
#                 p1 = (0, -arrow_size / 2)      # Tip
#                 p2 = (-arrow_size / 3, arrow_size / 2)  # Bottom left
#                 p3 = (arrow_size / 3, arrow_size / 2)   # Bottom right
                
#                 # Rotate by error angle
#                 def rotate_point(p, angle):
#                     c, s = np.cos(angle), np.sin(angle)
#                     return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)
                
#                 p1r = rotate_point(p1, error_angle)
#                 p2r = rotate_point(p2, error_angle)
#                 p3r = rotate_point(p3, error_angle)
                
#                 # Convert to screen coordinates
#                 p1_screen = (center_x + p1r[0], center_y + p1r[1])
#                 p2_screen = (center_x + p2r[0], center_y + p2r[1])
#                 p3_screen = (center_x + p3r[0], center_y + p3r[1])
                
#                 # Draw background
#                 draw_list = imgui.get_window_draw_list()
                
#                 # Draw background circle
#                 draw_list.add_circle_filled(
#                     center_x, center_y, 
#                     arrow_window_size/2 - 10,
#                     imgui.get_color_u32_rgba(0.1, 0.1, 0.1, 0.8)
#                 )
                
#                 # Draw center reference dot
#                 draw_list.add_circle_filled(
#                     center_x, center_y, 
#                     5, 
#                     imgui.get_color_u32_rgba(0.7, 0.7, 0.7, 0.7)
#                 )
                
#                 # Set arrow color based on altitude difference
#                 elevation_diff = target_pos[2] - ship_pos[2]
#                 if abs(elevation_diff) < 5.0:
#                     # Target is at same level (green)
#                     arrow_color = (0.0, 1.0, 0.0, 1.0)
#                 elif elevation_diff > 0:
#                     # Target is above (red)
#                     arrow_color = (1.0, 0.2, 0.2, 1.0)
#                 else:
#                     # Target is below (blue)
#                     arrow_color = (0.2, 0.2, 1.0, 1.0)
                
#                 # Draw arrow
#                 draw_list.add_triangle_filled(
#                     p1_screen[0], p1_screen[1],
#                     p2_screen[0], p2_screen[1],
#                     p3_screen[0], p3_screen[1],
#                     imgui.get_color_u32_rgba(*arrow_color)
#                 )
                
#                 # Draw arrow outline
#                 draw_list.add_triangle(
#                     p1_screen[0], p1_screen[1],
#                     p2_screen[0], p2_screen[1],
#                     p3_screen[0], p3_screen[1],
#                     imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0),
#                     1.5
#                 )
                
#                 # Show distance as text
#                 draw_list.add_text(
#                     center_x - 20, 
#                     center_y + arrow_window_size/2 - 20,
#                     imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0), 
#                     f"{int(distance)}u"
#                 )
                
#                 imgui.end()
                
                
#             # GAME WON : Check if transporter has reached the target planet.
#             transporter_pos = self.objects["transporter"].properties["position"]
#             target_pos = self.target_station.properties["position"]
#             if np.linalg.norm(transporter_pos - target_pos) < 5:  # threshold distance
#                 print("Game Won! Transporter has reached the target station.")
#                 self.screen = 2  # Switch to Game Won screen
#                 return
            
#             # GAME OVER : Check if transporter has been caught by a pirate.
#             ship_pos = transporter_pos
#             for pirate_obj in self.objects.get("pirates", []):
#                 pirate_pos = pirate_obj.properties["position"]
#                 if np.linalg.norm(pirate_pos - ship_pos) < 5:
#                     print("Game Over! A pirate has caught you.")
#                     self.screen = 3
#                     return

#             # Update station orbits.
#             for station_obj in self.objects.get("stations", []):
#                 station_obj.properties["rotation"][2] += theta
#                 radius = station_obj.properties["rotation_radius"]
#                 center = station_obj.properties["init_position"]
#                 station_obj.properties["position"][0] = center[0] + radius * np.cos(station_obj.properties["rotation"][2])
#                 station_obj.properties["position"][1] = center[1] + radius * np.sin(station_obj.properties["rotation"][2])
#                 station_obj.properties["position"][2] = center[2]

#             # Update transporter.
#             if self.objects.get("transporter") is not None:
#                 transporter = self.objects["transporter"]
#                 if "orientation" not in transporter.properties:
#                     t_rot = transporter.properties["rotation"]
#                     transporter.properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
#                 current_orient = transporter.properties["orientation"]
#                 rotation_speed = 0.5
#                 dR = np.eye(3, dtype=np.float32)
#                 if inputs.get("W"): dR = dR @ rotation_matrix(rotation_speed * delta, 0, 0)[:3, :3]
#                 if inputs.get("S"): dR = dR @ rotation_matrix(-rotation_speed * delta, 0, 0)[:3, :3]
#                 if inputs.get("A"): dR = dR @ rotation_matrix(0, rotation_speed * delta, 0)[:3, :3]
#                 if inputs.get("D"): dR = dR @ rotation_matrix(0, -rotation_speed * delta, 0)[:3, :3]
#                 if inputs.get("Q"): dR = dR @ rotation_matrix(0, 0, rotation_speed * delta)[:3, :3]
#                 if inputs.get("E"): dR = dR @ rotation_matrix(0, 0, -rotation_speed * delta)[:3, :3]
#                 new_orient = current_orient @ dR
#                 transporter.properties["orientation"] = new_orient
#                 max_speed = 15.0
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
#                 self.camera.position = copy.deepcopy(transporter.properties["position"]) - (5 * forward_spaceship) + up_spaceship
                
#                 # Switch between cameras
#                 if inputs.get("R_CLICK") is True:
#                     # Use FPP camera.
#                     forward_offset = 10.0  # distance in front of ship
#                     self.fpp_camera.position = transporter.properties["position"] + forward_spaceship * forward_offset
#                     self.fpp_camera.lookAt = self.fpp_camera.position + forward_spaceship
#                     self.fpp_camera.up = np.array([0, 1, 0], dtype=np.float32)
#                     self.active_camera = self.fpp_camera
#                 else:
#                     self.active_camera = self.camera
                    
#                 if self.laser_cooldown > 0:
#                     self.laser_cooldown -= delta
#                 if self.active_camera == self.fpp_camera:
#     # Update cooldown timer
#                     if self.laser_cooldown > 0:
#                         self.laser_cooldown -= delta
                    
#                     # Only fire if L_CLICK or F key is pressed AND cooldown has expired
#                     is_firing = inputs.get("L_CLICK") or inputs.get("F")
#                     if is_firing and self.laser_cooldown <= 0:
#                         self.fireLaser()
#                         self.laser_cooldown = 0.2  # Reduced cooldown for more rapid fire when holding
#                         print("Firing laser - button pressed")
            
#             # Update pirates.
#             if "pirates" in self.objects:
#                 pirate_speed = 50.0  # adjust speed as needed
#                 ship_pos = self.objects["transporter"].properties["position"]
#                 for pirate_obj in self.objects["pirates"]:
#                     pirate_pos = pirate_obj.properties["position"]
#                     direction = ship_pos - pirate_pos
#                     dist = np.linalg.norm(direction)
#                     if dist > 1e-3:
#                         direction /= dist
#                     else:
#                         direction = np.zeros_like(direction)
#                     # Move pirate toward ship
#                     pirate_obj.properties["position"] += direction * pirate_speed * delta
                    
#                 if "lasers" in self.objects:
#                     lasers_to_remove = []
#                     for laser_obj in self.objects["lasers"]:
#                         # Simple update: position += velocity * delta
#                         if "velocity" in laser_obj.properties:
#                             laser_obj.properties["position"] += laser_obj.properties["velocity"] * delta
#                             # Optionally remove lasers after a certain lifetime or distance.
#                             # For now, if laser is beyond a distance threshold, mark for removal.
#                             if np.linalg.norm(laser_obj.properties["position"]) > 6000:
#                                 lasers_to_remove.append(laser_obj)
#                         laser_obj.properties["lifetime"] += delta
#                         if laser_obj.properties["lifetime"] > self.laser_lifetime:
#                             lasers_to_remove.append(laser_obj)
#                     for l in lasers_to_remove:
#                         self.objects["lasers"].remove(l)

#         elif self.screen in (2, 3):
#             # Additional screens (YOU WON, GAME OVER) go here.
#             pass
        
#     # def fireLaser(self):
#         """Fires a laser from the FPP camera position through the crosshair."""
#         # Only fire if we're in FPP mode
#         if self.active_camera != self.fpp_camera:
#             return
            
#         # Calculate forward vector from camera (matches the crosshair direction)
#         camera_forward = self.fpp_camera.lookAt - self.fpp_camera.position
#         camera_forward = camera_forward / np.linalg.norm(camera_forward)
        
#         # Start laser exactly at the camera position
#         laser_start = self.fpp_camera.position.copy()
        
#         # Create the laser
#         laser = get_laser()
#         laser["position"] = laser_start
        
#         # Set laser velocity in camera's forward direction
#         laser_speed = 300.0
#         laser["velocity"] = camera_forward * laser_speed
        
#         # Adjust scale - make it thinner but longer for better visibility
#         laser["scale"] = np.array([0.05, 0.05, 2.0], dtype=np.float32)
        
#         # Create rotation matrix for the laser to align with firing direction
#         forward = camera_forward
#         world_up = np.array([0, 1, 0], dtype=np.float32)
        
#         # Handle the case where forward is parallel to world up
#         if abs(np.dot(forward, world_up)) > 0.999:
#             # If looking straight up/down, use a different reference vector
#             world_up = np.array([1, 0, 0], dtype=np.float32)
            
#         # Calculate right vector
#         right = np.cross(forward, world_up)
#         right = right / np.linalg.norm(right)
        
#         # Calculate actual up vector
#         up = np.cross(right, forward)
#         up = up / np.linalg.norm(up)
        
#         # Create rotation matrix where columns are the basis vectors
#         orientation = np.column_stack((right, up, -forward))
#         laser["orientation"] = orientation
        
#         # Set lifetime
#         laser["lifetime"] = 0
        
#         # Add to lasers collection
#         self.objects.setdefault("lasers", []).append(Object(None, self.shaders[0], laser))
        
#         # Print debug info
#         print(f"Firing laser from camera at {laser_start}")

#     def DrawScene(self):
#         if self.screen == 1:
#             # for shader in self.shaders:
#             #     self.camera.Update(shader)
#             #     lightPosLocation = glGetUniformLocation(shader.ID, "lightPos".encode('utf-8'))
#             #     glUniform3f(lightPosLocation, 100.0, 100.0, 100.0)
#             #     viewPosLocation = glGetUniformLocation(shader.ID, "viewPos".encode('utf-8'))
#             #     glUniform3f(viewPosLocation, self.camera.position[0], self.camera.position[1], self.camera.position[2])
#             #     glUniform1f(glGetUniformLocation(shader.ID, "ambientStrength".encode('utf-8')), 0.3)
#             #     glUniform1f(glGetUniformLocation(shader.ID, "specularStrength".encode('utf-8')), 0.8)
#             #     glUniform1f(glGetUniformLocation(shader.ID, "shininess".encode('utf-8')), 64.0)
#             # for planet_obj in self.objects.get("planets", []):
#             #     planet_obj.Draw()
#             # for station_obj in self.objects.get("stations", []):
#             #     station_obj.Draw()
#             # if self.objects.get("transporter") is not None:
#             #     self.objects["transporter"].Draw()
#             # for pirate_obj in self.objects.get("pirates", []):
#             #     pirate_obj.Draw()
#             for shader in self.shaders:
#                 self.active_camera.Update(shader)
#                 lightPosLocation = glGetUniformLocation(shader.ID, "lightPos".encode('utf-8'))
#                 glUniform3f(lightPosLocation, 100.0, 100.0, 100.0)
#                 viewPosLocation = glGetUniformLocation(shader.ID, "viewPos".encode('utf-8'))
#                 glUniform3f(viewPosLocation, self.active_camera.position[0], self.active_camera.position[1], self.active_camera.position[2])
#                 glUniform1f(glGetUniformLocation(shader.ID, "ambientStrength".encode('utf-8')), 0.3)
#                 glUniform1f(glGetUniformLocation(shader.ID, "specularStrength".encode('utf-8')), 0.8)
#                 glUniform1f(glGetUniformLocation(shader.ID, "shininess".encode('utf-8')), 64.0)
#             for planet_obj in self.objects.get("planets", []):
#                 planet_obj.Draw()
#             for station_obj in self.objects.get("stations", []):
#                 station_obj.Draw()
#             if self.objects.get("transporter") is not None:
#                 self.objects["transporter"].Draw()
#             for pirate_obj in self.objects.get("pirates", []):
#                 pirate_obj.Draw()
#             if "lasers" in self.objects:
#                 for laser_obj in self.objects["lasers"]:
#                     laser_obj.Draw()
#             # ### FPP Crosshair: If using FPP camera, draw a crosshair overlay.
#             if self.active_camera == self.fpp_camera:
#                 self.DrawCrosshair()

#     def DrawCrosshair(self):
#         # Draw a simple crosshair in the center of the screen.
#         draw_list = imgui.get_foreground_draw_list()
#         center_x = self.width / 2
#         center_y = self.height / 2
#         size = 10  # half-length of crosshair lines
#         color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0)  # white
#         thickness = 2.0
#         # Horizontal line.
#         draw_list.add_line(center_x - size, center_y, center_x + size, center_y, color, thickness)
#         # Vertical line.
#         draw_list.add_line(center_x, center_y - size, center_x, center_y + size, color, thickness)


import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader, lighting_shader
from assets.objects.objects import get_planet, get_space_station, get_transporter, rotation_matrix, get_pirates, get_laser
import random
from OpenGL.GL import *
import copy
import sys

class Game:
    def __init__(self, height, width, gui):
        self.gui = gui
        self.height = height
        self.width = width
        self.screen = 0              # 0 = Main Menu, 1 = Game, 2 = Game Won, 3 = Game Over
        self.menu_selection = 1      # 1: New Game, 2: Exit
        self.shaders = [Shader(lighting_shader["vertex_shader"], lighting_shader["fragment_shader"])]
        self.objects = {}
        # Create the first-person (FPP) camera.
        self.fpp_camera = Camera(self.height, self.width)
        self.fpp_camera.fov = 60
        self.active_camera = None
        # Laser firing control:
        self.laser_cooldown = 0.0  # seconds before next laser can be fired
        self.laser_lifetime = 5.0  # seconds a laser remains active

    def InitScene(self):
        if self.screen == 1:
            # Set up the normal (third-person) camera.
            def setCamera():
                self.camera = Camera(self.height, self.width)
                self.camera.position = np.array([0, 0, 0], dtype=np.float32)
                self.camera.lookAt = np.array([0, 0, -1], dtype=np.float32)
                self.camera.up = np.array([0, 1, 0], dtype=np.float32)
                self.camera.fov = 45
                self.camera.near = 1.0
                self.camera.far = 10000.0
            setCamera()
            self.active_camera = self.camera

            # Set world limits.
            def setWorldLimits():
                self.worldMin = np.array([-5000, -5000, -5000], dtype=np.float32)
                self.worldMax = np.array([5000, 5000, 5000], dtype=np.float32)
            setWorldLimits()

            # Initialize Planets.
            self.n_planets = 10
            self.objects["planets"] = []
            for i in range(self.n_planets):
                top_color = np.random.uniform(0.7, 1.0, 3)
                bottom_color = np.random.uniform(0.7, 1.0, 3)
                planet = get_planet(bottom_color, top_color)
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

            # Initialize Stations.
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
                    offset = (i * 10 + 3) * 4
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
            
            # FPP Camera: Position the FPP camera in front of the transporter.
            forward_offset = 10.0
            if "orientation" not in self.objects["transporter"].properties:
                t_rot = self.objects["transporter"].properties.get("rotation", np.array([0, 0, 0], dtype=np.float32))
                self.objects["transporter"].properties["orientation"] = rotation_matrix(t_rot[0], t_rot[1], t_rot[2])
            transporter_orient = self.objects["transporter"].properties["orientation"]
            forward_vec = transporter_orient @ np.array([0, 0, -1], dtype=np.float32)
            self.fpp_camera.position = self.objects["transporter"].properties["position"] + forward_vec * forward_offset
            self.fpp_camera.lookAt = self.fpp_camera.position + forward_vec
            self.fpp_camera.up = np.array([0, 1, 0], dtype=np.float32)

            # Spawn Pirates at random positions.
            self.n_pirates = 20 
            self.objects["pirates"] = []
            min_pirate_distance = 300
            ship_pos = self.objects["transporter"].properties["position"]
            for i in range(self.n_pirates):
                valid_spawn = False
                while not valid_spawn:
                    pos = np.array([
                        np.random.uniform(self.worldMin[0], self.worldMax[0]),
                        np.random.uniform(self.worldMin[1], self.worldMax[1]),
                        np.random.uniform(self.worldMin[2], self.worldMax[2])
                    ], dtype=np.float32)
                    if np.linalg.norm(pos - ship_pos) > min_pirate_distance:
                        valid_spawn = True
                pirate = get_pirates()
                pirate["position"] = pos
                scale_val = random.uniform(10, 15)
                pirate["scale"] = np.array([scale_val, scale_val, scale_val], dtype=np.float32)
                self.objects["pirates"].append(Object(None, self.shaders[0], pirate))
            print(f"Spawned {len(self.objects['pirates'])} pirates.")
            
            # Initialize lasers list.
            self.objects["lasers"] = []
            self.laser_cooldown = 0.0

    def fireLaser(self):
        """Fires a laser from the crosshair (center of FPP view)."""
        if self.active_camera != self.fpp_camera:
            return

        # Calculate the forward direction from the FPP camera.
        ray_origin = self.fpp_camera.position
        ray_direction = self.fpp_camera.lookAt - self.fpp_camera.position
        ray_direction = ray_direction / np.linalg.norm(ray_direction)
        # Use the camera's near plane distance as the offset so the laser starts at the crosshair.
        near_offset = self.fpp_camera.near
        laser_start = ray_origin + ray_direction * near_offset

        # Create the laser.
        laser = get_laser()
        laser["position"] = laser_start
        laser_speed = 300.0
        laser["velocity"] = ray_direction * laser_speed
        # Adjust scale to be thin and long.
        laser["scale"] = np.array([0.05, 0.05, 2.0], dtype=np.float32)

        # Create a rotation matrix so that the laser aligns with the firing direction.
        forward = ray_direction
        world_up = np.array([0, 1, 0], dtype=np.float32)
        if abs(np.dot(forward, world_up)) > 0.999:
            world_up = np.array([1, 0, 0], dtype=np.float32)
        right = np.cross(forward, world_up)
        right = right / np.linalg.norm(right)
        up = np.cross(right, forward)
        up = up / np.linalg.norm(up)
        orientation = np.column_stack((right, up, -forward))
        laser["orientation"] = orientation

        laser["lifetime"] = 0
        self.objects.setdefault("lasers", []).append(Object(None, self.shaders[0], laser))
        print(f"Firing laser from crosshair at {laser_start}")

    def ProcessFrame(self, inputs, time):
        imgui.new_frame()
        self.DrawText(inputs)
        self.UpdateScene(inputs, time)
        self.DrawScene()
        imgui.render()
        self.gui.render(imgui.get_draw_data())

    def DrawText(self, inputs=None):
        if self.screen == 0 or self.screen == 2 or self.screen == 3:
            window_w, window_h = 400, 200
            x_pos = (self.width - window_w) / 2
            y_pos = (self.height - window_h) / 2
            imgui.set_next_window_position(x_pos, y_pos)
            imgui.set_next_window_size(window_w, window_h)
            if self.screen == 0:
                title = "Main Menu"
            elif self.screen == 2:
                title = "Game Won"
            else:
                title = "Game Over"
            imgui.begin(title, False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)
            if self.screen == 2:
                imgui.text_colored("Congratulations!", 0.0, 1.0, 0.0, 1.0)
                imgui.text("You have successfully delivered the cargo.")
                imgui.separator()
            if self.screen == 3:
                imgui.text_colored("Game Over", 1.0, 0.0, 0.0, 1.0)
                imgui.text("Pirates caught you!")
                imgui.separator()
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
            if self.screen == 0:
                imgui.text("Press 1 or 2 to select, ENTER to confirm")
            else:
                imgui.text("Press ENTER to confirm your choice")
            imgui.end()

    def UpdateScene(self, inputs, time):
        if self.screen == 0 or self.screen == 2 or self.screen == 3:
            if inputs.get("1") is True:
                self.menu_selection = 1
            if inputs.get("2") is True:
                self.menu_selection = 2
            if inputs.get("ENTER") is True:
                print(f"ENTER pressed, menu selection: {self.menu_selection}")
                if self.menu_selection == 1:
                    print("Starting New Game")
                    self.screen = 1
                    self.InitScene()
                elif self.menu_selection == 2:
                    print("Exiting Game")
                    sys.exit(0)
            return

        if self.screen == 1:
            delta = time["deltaTime"]
            theta = 0.4 * delta

            # Check collision: if transporter is close to target station, game won.
            transporter_pos = self.objects["transporter"].properties["position"]
            target_pos = self.target_station.properties["position"]
            if np.linalg.norm(transporter_pos - target_pos) < 20:
                print("Game Won! Transporter has reached the target station.")
                self.screen = 2
                return

            # Check collision: if any pirate touches the ship, game over.
            for pirate_obj in self.objects.get("pirates", []):
                pirate_pos = pirate_obj.properties["position"]
                if np.linalg.norm(pirate_pos - transporter_pos) < 20:
                    print("Game Over! A pirate has caught you.")
                    self.screen = 3
                    return

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
                max_speed = 15.0
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

                # Toggle camera based on right mouse button.
                if inputs.get("R_CLICK") is True:
                    forward_offset = 10.0
                    self.fpp_camera.position = transporter.properties["position"] + forward_spaceship * forward_offset
                    self.fpp_camera.lookAt = self.fpp_camera.position + forward_spaceship
                    self.fpp_camera.up = np.array([0, 1, 0], dtype=np.float32)
                    self.active_camera = self.fpp_camera
                else:
                    self.active_camera = self.camera

                # Laser firing: Check if LMB or F key is pressed.
                if self.laser_cooldown > 0:
                    self.laser_cooldown -= delta
                if self.active_camera == self.fpp_camera and (inputs.get("L_CLICK") or inputs.get("F")):
                    if self.laser_cooldown <= 0:
                        self.fireLaser()
                        self.laser_cooldown = 0.5

            # Update pirates.
            if "pirates" in self.objects:
                pirate_speed = 50.0
                ship_pos = self.objects["transporter"].properties["position"]
                for pirate_obj in self.objects["pirates"]:
                    pirate_pos = pirate_obj.properties["position"]
                    direction = ship_pos - pirate_pos
                    dist = np.linalg.norm(direction)
                    if dist > 1e-3:
                        direction /= dist
                    else:
                        direction = np.zeros_like(direction)
                    pirate_obj.properties["position"] += direction * pirate_speed * delta

                if "lasers" in self.objects:
                    lasers_to_remove = []
                    for laser_obj in self.objects["lasers"]:
                        if "velocity" in laser_obj.properties:
                            laser_obj.properties["position"] += laser_obj.properties["velocity"] * delta
                            if np.linalg.norm(laser_obj.properties["position"]) > 6000:
                                lasers_to_remove.append(laser_obj)
                        laser_obj.properties["lifetime"] += delta
                        if laser_obj.properties["lifetime"] > self.laser_lifetime:
                            lasers_to_remove.append(laser_obj)
                    for l in lasers_to_remove:
                        self.objects["lasers"].remove(l)

        elif self.screen in (2, 3):
            # Additional screens (Game Won, Game Over)
            pass

    def fireLaser(self):
        """Fires a laser from the crosshair (center of FPP view)."""
        if self.active_camera != self.fpp_camera:
            return

        # Calculate forward direction from FPP camera.
        ray_origin = self.fpp_camera.position
        ray_direction = self.fpp_camera.lookAt - self.fpp_camera.position
        ray_direction = ray_direction / np.linalg.norm(ray_direction)
        # Use the camera's near plane as offset.
        near_offset = self.fpp_camera.near
        laser_start = ray_origin + ray_direction * near_offset

        laser = get_laser()
        laser["position"] = laser_start
        laser_speed = 300.0
        laser["velocity"] = ray_direction * laser_speed
        laser["scale"] = np.array([0.05, 0.05, 2.0], dtype=np.float32)

        forward = ray_direction
        world_up = np.array([0, 1, 0], dtype=np.float32)
        if abs(np.dot(forward, world_up)) > 0.999:
            world_up = np.array([1, 0, 0], dtype=np.float32)
        right = np.cross(forward, world_up)
        right /= np.linalg.norm(right)
        up = np.cross(right, forward)
        up /= np.linalg.norm(up)
        orientation = np.column_stack((right, up, -forward))
        laser["orientation"] = orientation
        laser["lifetime"] = 0

        self.objects.setdefault("lasers", []).append(Object(None, self.shaders[0], laser))
        print(f"Firing laser from crosshair at {laser_start}")

    def DrawScene(self):
        if self.screen == 1:
            for shader in self.shaders:
                self.active_camera.Update(shader)
                lightPosLocation = glGetUniformLocation(shader.ID, "lightPos".encode('utf-8'))
                glUniform3f(lightPosLocation, 100.0, 100.0, 100.0)
                viewPosLocation = glGetUniformLocation(shader.ID, "viewPos".encode('utf-8'))
                glUniform3f(viewPosLocation, self.active_camera.position[0], self.active_camera.position[1], self.active_camera.position[2])
                glUniform1f(glGetUniformLocation(shader.ID, "ambientStrength".encode('utf-8')), 0.3)
                glUniform1f(glGetUniformLocation(shader.ID, "specularStrength".encode('utf-8')), 0.8)
                glUniform1f(glGetUniformLocation(shader.ID, "shininess".encode('utf-8')), 64.0)
            for planet_obj in self.objects.get("planets", []):
                planet_obj.Draw()
            for station_obj in self.objects.get("stations", []):
                station_obj.Draw()
            if self.objects.get("transporter") is not None:
                self.objects["transporter"].Draw()
            for pirate_obj in self.objects.get("pirates", []):
                pirate_obj.Draw()
            if "lasers" in self.objects:
                for laser_obj in self.objects["lasers"]:
                    laser_obj.Draw()
            if self.active_camera == self.fpp_camera:
                self.DrawCrosshair()

    def DrawCrosshair(self):
        draw_list = imgui.get_foreground_draw_list()
        center_x = self.width / 2
        center_y = self.height / 2
        size = 10
        color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0)
        thickness = 2.0
        draw_list.add_line(center_x - size, center_y, center_x + size, center_y, color, thickness)
        draw_list.add_line(center_x, center_y - size, center_x, center_y + size, color, thickness)
