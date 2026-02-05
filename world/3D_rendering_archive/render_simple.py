"""
Simplified 3D Renderer for Tarski's World
Uses simple geometric shapes for stability.
"""

import pygame
import sys
import math
import os

# Import world parser from parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from visualize_world import parse_world_file


class SimpleRenderer:
    """Simplified 3D renderer using basic shapes."""
    
    def __init__(self, world_file: str, width: int = 1024, height: int = 768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Tarski's World 3D - {os.path.basename(world_file)}")
        
        self.clock = pygame.time.Clock()
        self.angle_y = math.radians(45)
        self.zoom = 40
        
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
    
    def project_3d_to_2d(self, x, y, z):
        """Simple isometric projection."""
        # Rotate around Y axis
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # Isometric projection
        screen_x = (x_rot - z_rot) * self.zoom + self.width / 2
        screen_y = (x_rot + z_rot) * 0.5 * self.zoom - y * self.zoom + self.height / 2
        
        return (screen_x, screen_y, z_rot)
    
    def draw_sphere_simple(self, x, y, z, size, color):
        """Draw a sphere with 3D shading effect."""
        # Project center
        center_2d = self.project_3d_to_2d(x, y, z)
        center_x, center_y = int(center_2d[0]), int(center_2d[1])
        depth = center_2d[2]
        
        # Calculate screen-space radius consistently
        # Use vertical offset which is rotation-independent
        radius_3d = size / 2
        top_point = self.project_3d_to_2d(x, y + radius_3d, z)
        screen_radius = int(abs(top_point[1] - center_2d[1]))
        
        # Don't draw if too small or behind camera
        if screen_radius < 2 or depth < 0:
            return
        
        # Draw multiple concentric circles from dark to light (inside to outside)
        # This creates a gradient effect making it look 3D
        steps = 12
        for i in range(steps, 0, -1):
            ratio = i / steps
            radius = int(screen_radius * ratio)
            
            # Brightness increases from center (0.4) to edge (1.0)
            brightness = 0.3 + (ratio * 0.7)
            shaded_color = tuple(int(c * brightness) for c in color)
            
            if radius > 0:
                pygame.draw.circle(self.screen, shaded_color, 
                                 (center_x, center_y), radius)
        
        # Add a highlight spot for shininess (upper-left)
        highlight_offset_x = int(-screen_radius * 0.3)
        highlight_offset_y = int(-screen_radius * 0.3)
        highlight_radius = max(2, int(screen_radius * 0.25))
        highlight_color = tuple(min(255, int(c * 1.5)) for c in color)
        
        pygame.draw.circle(self.screen, highlight_color,
                         (center_x + highlight_offset_x, center_y + highlight_offset_y),
                         highlight_radius)
        
        # Draw thick black outline
        pygame.draw.circle(self.screen, (0, 0, 0), 
                         (center_x, center_y), screen_radius, 3)
    
    def draw_tetrahedron_simple(self, x, y, z, size, color):
        """Draw a simple tetrahedron."""
        s = size / 2
        
        # Define 4 vertices of tetrahedron
        # Base triangle on XZ plane, apex above
        vertices = [
            (x, y - s * 0.5, z - s * 0.577),  # 0 - front base
            (x - s, y - s * 0.5, z + s * 0.577),  # 1 - left base
            (x + s, y - s * 0.5, z + s * 0.577),  # 2 - right base
            (x, y + s * 1.2, z),  # 3 - apex
        ]
        
        # Project all vertices
        projected = [self.project_3d_to_2d(*v) for v in vertices]
        
        # Define 4 triangular faces
        faces = [
            ([0, 1, 2], 0.6),  # Base
            ([0, 1, 3], 0.8),  # Front-left
            ([1, 2, 3], 0.9),  # Back
            ([2, 0, 3], 1.0),  # Front-right
        ]
        
        # Sort faces by average depth
        face_depths = []
        for face_indices, brightness in faces:
            avg_depth = sum(projected[i][2] for i in face_indices) / len(face_indices)
            face_depths.append((avg_depth, face_indices, brightness))
        
        face_depths.sort(reverse=True)
        
        # Draw faces back to front
        for depth, face_indices, brightness in face_depths:
            points = [(projected[i][0], projected[i][1]) for i in face_indices]
            shaded_color = tuple(int(c * brightness) for c in color)
            pygame.draw.polygon(self.screen, shaded_color, points)
            pygame.draw.polygon(self.screen, (0, 0, 0), points, 2)
    
    def draw_cube_simple(self, x, y, z, size, color):
        """Draw a simple cube using rectangles."""
        s = size / 2
        
        # Define 8 vertices of cube
        vertices = [
            (x - s, y - s, z - s),  # 0
            (x + s, y - s, z - s),  # 1
            (x + s, y + s, z - s),  # 2
            (x - s, y + s, z - s),  # 3
            (x - s, y - s, z + s),  # 4
            (x + s, y - s, z + s),  # 5
            (x + s, y + s, z + s),  # 6
            (x - s, y + s, z + s),  # 7
        ]
        
        # Project all vertices
        projected = [self.project_3d_to_2d(*v) for v in vertices]
        
        # Define faces (only draw visible ones based on depth)
        faces = [
            ([0, 1, 2, 3], 0.8),  # Front
            ([4, 5, 6, 7], 0.8),  # Back
            ([0, 1, 5, 4], 0.6),  # Bottom
            ([2, 3, 7, 6], 1.0),  # Top
            ([0, 3, 7, 4], 0.7),  # Left
            ([1, 2, 6, 5], 0.7),  # Right
        ]
        
        # Sort faces by average depth
        face_depths = []
        for face_indices, brightness in faces:
            avg_depth = sum(projected[i][2] for i in face_indices) / len(face_indices)
            face_depths.append((avg_depth, face_indices, brightness))
        
        face_depths.sort(reverse=True)
        
        # Draw faces back to front
        for depth, face_indices, brightness in face_depths:
            points = [(projected[i][0], projected[i][1]) for i in face_indices]
            shaded_color = tuple(int(c * brightness) for c in color)
            pygame.draw.polygon(self.screen, shaded_color, points)
            pygame.draw.polygon(self.screen, (0, 0, 0), points, 2)
    
    def draw_shape(self, x, y, z, size, color, shape_name):
        """Draw shape based on shape_name."""
        if shape_name == 'tetrahedron':
            self.draw_tetrahedron_simple(x, y, z, size, color)
        elif shape_name == 'cube':
            self.draw_cube_simple(x, y, z, size, color)
        elif shape_name == 'dodecahedron':
            self.draw_sphere_simple(x, y, z, size, color)
        else:
            self.draw_cube_simple(x, y, z, size, color)
    
    def world_to_3d(self, world_x, world_y):
        """Convert world coordinates to 3D coordinates."""
        # World coordinates are 1-8, center at 4.5
        # Negate X so left-right matches ASCII view
        x = -(world_x - 4.5)
        z = (world_y - 4.5)
        return (x, z)
    
    def draw_board(self):
        """Draw the checkered board."""
        for i in range(8):
            for j in range(8):
                x, z = self.world_to_3d(i + 1, j + 1)
                
                # Checkerboard pattern
                if (i + j) % 2 == 0:
                    color = (220, 220, 220)
                else:
                    color = (80, 80, 80)
                
                # Draw square
                s = 0.5
                corners = [
                    (x - s, 0, z - s),
                    (x + s, 0, z - s),
                    (x + s, 0, z + s),
                    (x - s, 0, z + s),
                ]
                
                projected = [self.project_3d_to_2d(*c)[:2] for c in corners]
                pygame.draw.polygon(self.screen, color, projected)
                pygame.draw.polygon(self.screen, (50, 50, 50), projected, 1)
    
    def draw_objects(self):
        """Draw all objects from the world."""
        size_map = {'small': 0.4, 'medium': 0.6, 'large': 0.8}
        
        for name, obj in self.objects.items():
            if not obj.is_complete():
                continue
            
            world_x, world_y = obj.position
            x, z = self.world_to_3d(world_x, world_y)
            
            size = size_map.get(obj.size, 0.6)
            y = size / 2  # Lift object so it sits on board
            
            color = self.get_color_rgb(obj.color)
            
            self.draw_shape(x, y, z, size, color, obj.shape)
    
    def handle_input(self):
        """Handle keyboard input."""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.angle_y -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle_y += 0.02
        if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
            self.zoom = min(80, self.zoom + 1)
        if keys[pygame.K_MINUS]:
            self.zoom = max(20, self.zoom - 1)
        if keys[pygame.K_SPACE]:
            self.angle_y = math.radians(45)
            self.zoom = 40
    
    def draw_ui(self):
        """Draw UI overlay."""
        font = pygame.font.Font(None, 24)
        
        text = font.render(f"World: {os.path.basename(self.world_file)} | Objects: {len(self.objects)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        text = font.render("Arrow Keys: Rotate | +/-: Zoom | Space: Reset | ESC: Quit", True, (255, 255, 255))
        self.screen.blit(text, (10, self.height - 30))
    
    def run(self):
        """Main render loop."""
        running = True
        
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                
                self.handle_input()
                
                # Clear screen
                self.screen.fill((100, 150, 200))
                
                # Draw everything
                self.draw_board()
                self.draw_objects()
                self.draw_ui()
                
                pygame.display.flip()
                self.clock.tick(60)
        
        except Exception as e:
            print(f"Error during rendering: {e}")
            import traceback
            traceback.print_exc()
        finally:
            pygame.quit()


def main():
    if len(sys.argv) < 2:
        print("Usage: python render_simple.py <world_file.pl>")
        print("\nExample:")
        print("  python render_simple.py ../world1.pl")
        sys.exit(1)
    
    world_file = sys.argv[1]
    
    if not os.path.exists(world_file):
        print(f"Error: File '{world_file}' not found")
        sys.exit(1)
    
    renderer = SimpleRenderer(world_file)
    renderer.run()


if __name__ == "__main__":
    main()
