"""
3D Renderer for Tarski's World
Main renderer - loads and visualizes world files.
"""

import pygame
import sys
import math
import os
from typing import Dict, List
from geometry import *
from board import Board

# Import world parser from parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from visualize_world import parse_world_file, WorldObject


class Camera:
    """Camera with orbit controls."""
    
    def __init__(self):
        self.distance = 12  # Distance from origin
        self.angle_x = math.radians(30)  # Elevation angle
        self.angle_y = math.radians(45)  # Rotation around Y axis
        self.target = (0, 0, 0)  # Look at origin
    
    def get_position(self) -> Vector3D:
        """Calculate camera position based on angles."""
        x = self.distance * math.cos(self.angle_x) * math.sin(self.angle_y)
        y = self.distance * math.sin(self.angle_x)
        z = self.distance * math.cos(self.angle_x) * math.cos(self.angle_y)
        return (x, y, z)
    
    def transform_point(self, point: Vector3D) -> Vector3D:
        """Transform point from world space to camera space."""
        cam_pos = self.get_position()
        translated = Vector3.subtract(point, cam_pos)
        
        rot_y = Matrix3D.rotate_y(-self.angle_y)
        rotated_y = Matrix3D.apply(rot_y, translated)
        
        rot_x = Matrix3D.rotate_x(-self.angle_x)
        rotated = Matrix3D.apply(rot_x, rotated_y)
        
        return rotated


class WorldRenderer:
    """Main 3D renderer for Tarski's World."""
    
    def __init__(self, world_file: str, width: int = 1024, height: int = 768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Tarski's World 3D - {os.path.basename(world_file)}")
        
        self.camera = Camera()
        self.board = Board(square_size=1.0)
        self.clock = pygame.time.Clock()
        
        # Light direction (normalized)
        self.light_dir = Vector3.normalize((0.5, -1, 0.5))
        
        # Load world
        self.world_file = world_file
        self.objects = parse_world_file(world_file)
        
        if not self.objects:
            print(f"Error: No objects found in {world_file}")
            sys.exit(1)
        
        print(f"Loaded {len(self.objects)} objects from {world_file}")
    
    def get_color_rgb(self, color_name: str) -> tuple:
        """Convert color name to RGB."""
        colors = {
            'red': (220, 60, 60),
            'yellow': (240, 220, 60),
            'purple': (180, 80, 180)
        }
        return colors.get(color_name, (128, 128, 128))
    
    def project_to_screen(self, point: Vector3D) -> Vector2D:
        """Project 3D point to screen coordinates."""
        cam_point = self.camera.transform_point(point)
        projected = Projection.perspective(cam_point, fov=500, distance=5)
        
        screen_x = projected[0] + self.width / 2
        screen_y = -projected[1] + self.height / 2
        
        return (screen_x, screen_y)
    
    def calculate_lighting(self, normal: Vector3D) -> float:
        """Calculate lighting intensity for a face."""
        intensity = -Vector3.dot(normal, self.light_dir)
        intensity = max(0.2, min(1.0, intensity))
        return intensity
    
    def apply_shading(self, color: tuple, intensity: float) -> tuple:
        """Apply lighting intensity to color."""
        return (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity)
        )
    
    def draw_face(self, vertices: List[Vector3D], color: tuple, face_indices: List[int]):
        """Draw a single face."""
        face_verts = [vertices[i] for i in face_indices]
        
        # Calculate normal for lighting
        if len(face_indices) >= 3:
            v0, v1, v2 = face_verts[0], face_verts[1], face_verts[2]
            edge1 = Vector3.subtract(v1, v0)
            edge2 = Vector3.subtract(v2, v0)
            normal = Vector3.normalize(Vector3.cross(edge1, edge2))
            
            # Backface culling
            cam_pos = self.camera.get_position()
            to_camera = Vector3.normalize(Vector3.subtract(cam_pos, v0))
            if Vector3.dot(normal, to_camera) < 0:
                return
            
            # Apply lighting
            intensity = self.calculate_lighting(normal)
            shaded_color = self.apply_shading(color, intensity)
        else:
            shaded_color = color
        
        # Project vertices to screen
        screen_points = [self.project_to_screen(v) for v in face_verts]
        
        # Draw polygon
        if len(screen_points) >= 3:
            pygame.draw.polygon(self.screen, shaded_color, screen_points)
            pygame.draw.polygon(self.screen, (0, 0, 0), screen_points, 1)
    
    def draw_shape(self, shape: PlatonicSolid, position: Vector3D, color: tuple):
        """Draw a Platonic solid."""
        vertices = shape.get_scaled_vertices(1.0)
        translated = [Vector3.add(v, position) for v in vertices]
        
        # Sort faces by depth (painter's algorithm)
        faces_with_depth = []
        for face in shape.faces:
            center = shape.get_face_center(face, translated)
            cam_point = self.camera.transform_point(center)
            depth = cam_point[2]
            faces_with_depth.append((depth, face))
        
        faces_with_depth.sort(reverse=True)
        
        # Draw faces
        for depth, face in faces_with_depth:
            self.draw_face(translated, color, face)
    
    def draw_board(self):
        """Draw the checkered board."""
        squares = self.board.get_all_squares()
        
        # Sort squares by depth
        squares_with_depth = []
        for vertices, color in squares:
            center_x = sum(v[0] for v in vertices) / 4
            center_y = sum(v[1] for v in vertices) / 4
            center_z = sum(v[2] for v in vertices) / 4
            center = (center_x, center_y, center_z)
            
            cam_point = self.camera.transform_point(center)
            depth = cam_point[2]
            squares_with_depth.append((depth, vertices, color))
        
        squares_with_depth.sort(reverse=True)
        
        # Draw squares
        for depth, vertices, color in squares_with_depth:
            darkened = self.apply_shading(color, 0.6)
            screen_points = [self.project_to_screen(v) for v in vertices]
            if len(screen_points) >= 3:
                pygame.draw.polygon(self.screen, darkened, screen_points)
                pygame.draw.polygon(self.screen, (0, 0, 0), screen_points, 1)
    
    def draw_world_objects(self):
        """Draw all objects from the loaded world."""
        for name, obj in self.objects.items():
            if not obj.is_complete():
                continue
            
            # Get shape (get_shape handles size scaling internally)
            shape = get_shape(obj.shape, obj.size)
            
            # Get position (center of square, lifted so object sits on board)
            x, y = obj.position
            size_scale = {'small': 0.3, 'medium': 0.5, 'large': 0.7}
            scale = size_scale.get(obj.size, 0.5)
            height = scale * 0.5  # Lift based on object size
            position = self.board.world_to_3d(x, y, height)
            
            # Get color
            color = self.get_color_rgb(obj.color)
            
            # Draw the shape
            self.draw_shape(shape, position, color)
    
    def handle_input(self):
        """Handle keyboard input."""
        keys = pygame.key.get_pressed()
        
        rotation_speed = 0.02
        zoom_speed = 0.2
        
        if keys[pygame.K_LEFT]:
            self.camera.angle_y -= rotation_speed
        if keys[pygame.K_RIGHT]:
            self.camera.angle_y += rotation_speed
        if keys[pygame.K_UP]:
            self.camera.angle_x += rotation_speed
        if keys[pygame.K_DOWN]:
            self.camera.angle_x -= rotation_speed
        
        if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
            self.camera.distance = max(5, self.camera.distance - zoom_speed)
        if keys[pygame.K_MINUS]:
            self.camera.distance = min(30, self.camera.distance + zoom_speed)
        
        if keys[pygame.K_SPACE]:
            # Reset camera
            self.camera.angle_x = math.radians(30)
            self.camera.angle_y = math.radians(45)
            self.camera.distance = 12
    
    def draw_text(self, text: str, x: int, y: int, color=(255, 255, 255)):
        """Draw text on screen."""
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_ui(self):
        """Draw UI overlay."""
        # Title
        self.draw_text(f"World: {os.path.basename(self.world_file)}", 10, 10)
        self.draw_text(f"Objects: {len(self.objects)}", 10, 35)
        
        # Controls
        y_offset = self.height - 90
        self.draw_text("Controls:", 10, y_offset)
        self.draw_text("  Arrow Keys: Rotate camera", 10, y_offset + 20)
        self.draw_text("  +/- : Zoom in/out", 10, y_offset + 40)
        self.draw_text("  Space: Reset view", 10, y_offset + 60)
    
    def run(self):
        """Main render loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Handle input
            self.handle_input()
            
            # Clear screen with gradient background
            self.screen.fill((100, 150, 200))
            
            # Draw everything
            self.draw_board()
            self.draw_world_objects()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python render_3d.py <world_file.pl>")
        print("\nExample:")
        print("  python render_3d.py ../world1.pl")
        print("  python render_3d.py ../world2.pl")
        sys.exit(1)
    
    world_file = sys.argv[1]
    
    if not os.path.exists(world_file):
        print(f"Error: File '{world_file}' not found")
        sys.exit(1)
    
    renderer = WorldRenderer(world_file)
    renderer.run()


if __name__ == "__main__":
    main()
