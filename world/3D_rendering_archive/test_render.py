"""
3D Renderer for Tarski's World
Test version - renders a simple scene with one of each shape.
"""

import pygame
import sys
import math
from geometry import *
from board import Board


class Camera:
    """Camera with orbit controls."""
    
    def __init__(self):
        self.distance = 12  # Distance from origin
        self.angle_x = math.radians(30)  # Elevation angle
        self.angle_y = math.radians(45)  # Rotation around Y axis
        self.target = (0, 0, 0)  # Look at origin
    
    def get_position(self) -> Vector3D:
        """Calculate camera position based on angles."""
        # Spherical coordinates to Cartesian
        x = self.distance * math.cos(self.angle_x) * math.sin(self.angle_y)
        y = self.distance * math.sin(self.angle_x)
        z = self.distance * math.cos(self.angle_x) * math.cos(self.angle_y)
        return (x, y, z)
    
    def transform_point(self, point: Vector3D) -> Vector3D:
        """Transform point from world space to camera space."""
        # Translate to camera position
        cam_pos = self.get_position()
        translated = Vector3.subtract(point, cam_pos)
        
        # Rotate around Y axis (horizontal rotation)
        rot_y = Matrix3D.rotate_y(-self.angle_y)
        rotated_y = Matrix3D.apply(rot_y, translated)
        
        # Rotate around X axis (vertical rotation)
        rot_x = Matrix3D.rotate_x(-self.angle_x)
        rotated = Matrix3D.apply(rot_x, rotated_y)
        
        return rotated


class Renderer:
    """Main 3D renderer."""
    
    def __init__(self, width: int = 1024, height: int = 768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tarski's World - 3D Test")
        
        self.camera = Camera()
        self.board = Board(square_size=1.0)
        self.clock = pygame.time.Clock()
        
        # Light direction (normalized)
        self.light_dir = Vector3.normalize((0.5, -1, 0.5))
    
    def project_to_screen(self, point: Vector3D) -> Vector2D:
        """Project 3D point to screen coordinates."""
        # Transform to camera space
        cam_point = self.camera.transform_point(point)
        
        # Project to 2D
        projected = Projection.perspective(cam_point, fov=500, distance=5)
        
        # Convert to screen coordinates (center of screen is origin)
        screen_x = projected[0] + self.width / 2
        screen_y = -projected[1] + self.height / 2  # Flip Y (screen Y goes down)
        
        return (screen_x, screen_y)
    
    def calculate_lighting(self, normal: Vector3D) -> float:
        """Calculate lighting intensity for a face."""
        # Simple diffuse lighting
        intensity = -Vector3.dot(normal, self.light_dir)
        intensity = max(0.2, min(1.0, intensity))  # Clamp to [0.2, 1.0]
        return intensity
    
    def apply_shading(self, color: Tuple[int, int, int], intensity: float) -> Tuple[int, int, int]:
        """Apply lighting intensity to color."""
        return (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity)
        )
    
    def draw_face(self, vertices: List[Vector3D], color: Tuple[int, int, int], face_indices: List[int]):
        """Draw a single face."""
        # Get face vertices
        face_verts = [vertices[i] for i in face_indices]
        
        # Calculate normal for lighting
        if len(face_indices) >= 3:
            v0, v1, v2 = face_verts[0], face_verts[1], face_verts[2]
            edge1 = Vector3.subtract(v1, v0)
            edge2 = Vector3.subtract(v2, v0)
            normal = Vector3.normalize(Vector3.cross(edge1, edge2))
            
            # Backface culling: only draw if normal points toward camera
            cam_pos = self.camera.get_position()
            to_camera = Vector3.normalize(Vector3.subtract(cam_pos, v0))
            if Vector3.dot(normal, to_camera) < 0:
                return  # Face is facing away
            
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
            # Draw edges
            pygame.draw.polygon(self.screen, (0, 0, 0), screen_points, 1)
    
    def draw_shape(self, shape: PlatonicSolid, position: Vector3D, color: Tuple[int, int, int]):
        """Draw a Platonic solid."""
        # Get vertices
        vertices = shape.get_scaled_vertices(1.0)
        
        # Translate to position
        translated = [Vector3.add(v, position) for v in vertices]
        
        # Sort faces by depth (painter's algorithm)
        faces_with_depth = []
        for face in shape.faces:
            center = shape.get_face_center(face, translated)
            cam_point = self.camera.transform_point(center)
            depth = cam_point[2]  # Z depth in camera space
            faces_with_depth.append((depth, face))
        
        # Sort by depth (farthest first)
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
            # Calculate center for depth sorting
            center_x = sum(v[0] for v in vertices) / 4
            center_y = sum(v[1] for v in vertices) / 4
            center_z = sum(v[2] for v in vertices) / 4
            center = (center_x, center_y, center_z)
            
            cam_point = self.camera.transform_point(center)
            depth = cam_point[2]
            squares_with_depth.append((depth, vertices, color))
        
        # Sort by depth (farthest first)
        squares_with_depth.sort(reverse=True)
        
        # Draw squares
        for depth, vertices, color in squares_with_depth:
            # Darken board slightly
            darkened = self.apply_shading(color, 0.6)
            screen_points = [self.project_to_screen(v) for v in vertices]
            if len(screen_points) >= 3:
                pygame.draw.polygon(self.screen, darkened, screen_points)
                pygame.draw.polygon(self.screen, (0, 0, 0), screen_points, 1)
    
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
    
    def run(self):
        """Main render loop."""
        # Test objects
        tetra = Tetrahedron(0.5)
        cube = Cube(0.5)
        dodeca = Dodecahedron(0.5)
        
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
            
            # Clear screen with gradient
            self.screen.fill((100, 150, 200))
            
            # Draw board
            self.draw_board()
            
            # Draw test objects
            # Red tetrahedron at [2, 2]
            pos1 = self.board.world_to_3d(2, 2, height=0.5)
            self.draw_shape(tetra, pos1, (220, 60, 60))
            
            # Yellow cube at [5, 5]
            pos2 = self.board.world_to_3d(5, 5, height=0.5)
            self.draw_shape(cube, pos2, (240, 220, 60))
            
            # Purple dodecahedron at [7, 3]
            pos3 = self.board.world_to_3d(7, 3, height=0.5)
            self.draw_shape(dodeca, pos3, (180, 80, 180))
            
            # Draw UI
            self.draw_text("Test Renderer - Arrow keys to rotate, +/- to zoom, Space to reset", 10, 10)
            self.draw_text(f"Camera: angle=({math.degrees(self.camera.angle_x):.0f}, {math.degrees(self.camera.angle_y):.0f}), dist={self.camera.distance:.1f}", 10, 35)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()


if __name__ == "__main__":
    renderer = Renderer()
    renderer.run()
