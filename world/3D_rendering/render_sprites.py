"""
Sprite-based 3D Renderer for Tarski's World
Pre-renders shapes as sprites for better performance and appearance.
"""

import pygame
import sys
import math
import os

# Import world parser from parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from visualize_world import parse_world_file


class ShapeSprites:
    """Pre-rendered shape sprites."""
    
    def __init__(self):
        self.sprites = {}
        self._create_all_sprites()
    
    def _create_all_sprites(self):
        """Create sprites for all shape/size/color combinations."""
        shapes = ['tetrahedron', 'cube', 'dodecahedron']
        sizes = {'small': 60, 'medium': 90, 'large': 120}
        colors = {
            'red': (220, 60, 60),
            'yellow': (240, 220, 60),
            'purple': (180, 80, 180)
        }
        
        for shape in shapes:
            for size_name, size_px in sizes.items():
                for color_name, color_rgb in colors.items():
                    key = (shape, size_name, color_name)
                    if shape == 'tetrahedron':
                        self.sprites[key] = self._create_tetrahedron_sprite(size_px, color_rgb)
                    elif shape == 'cube':
                        self.sprites[key] = self._create_cube_sprite(size_px, color_rgb)
                    elif shape == 'dodecahedron':
                        self.sprites[key] = self._create_sphere_sprite(size_px, color_rgb)
    
    def _create_sphere_sprite(self, size, color):
        """Create a sphere sprite with 3D shading."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        radius = size // 2 - 4
        
        # Draw gradient circles for 3D effect
        steps = 15
        for i in range(steps, 0, -1):
            ratio = i / steps
            circle_radius = int(radius * ratio)
            brightness = 0.3 + (ratio * 0.7)
            shaded_color = tuple(int(c * brightness) for c in color)
            pygame.draw.circle(surface, shaded_color, (center, center), circle_radius)
        
        # Highlight
        highlight_x = center - int(radius * 0.3)
        highlight_y = center - int(radius * 0.3)
        highlight_radius = max(3, int(radius * 0.25))
        highlight_color = tuple(min(255, int(c * 1.5)) for c in color)
        pygame.draw.circle(surface, highlight_color, (highlight_x, highlight_y), highlight_radius)
        
        # Outline
        pygame.draw.circle(surface, (0, 0, 0), (center, center), radius, 3)
        
        return surface
    
    def _create_cube_sprite(self, size, color):
        """Create an isometric cube sprite."""
        surface = pygame.Surface((size, int(size * 1.2)), pygame.SRCALPHA)
        
        # Isometric cube dimensions
        w = size * 0.7
        h = w * 0.5
        d = w * 0.866
        
        center_x = size // 2
        bottom_y = int(size * 1.1)
        
        # Top face
        top_points = [
            (center_x, bottom_y - d),
            (center_x - w/2, bottom_y - d - h/2),
            (center_x, bottom_y - d - h),
            (center_x + w/2, bottom_y - d - h/2)
        ]
        top_color = tuple(min(255, int(c * 1.0)) for c in color)
        pygame.draw.polygon(surface, top_color, top_points)
        pygame.draw.polygon(surface, (0, 0, 0), top_points, 2)
        
        # Left face
        left_points = [
            (center_x, bottom_y),
            (center_x - w/2, bottom_y - h/2),
            (center_x - w/2, bottom_y - d - h/2),
            (center_x, bottom_y - d)
        ]
        left_color = tuple(int(c * 0.7) for c in color)
        pygame.draw.polygon(surface, left_color, left_points)
        pygame.draw.polygon(surface, (0, 0, 0), left_points, 2)
        
        # Right face
        right_points = [
            (center_x, bottom_y),
            (center_x + w/2, bottom_y - h/2),
            (center_x + w/2, bottom_y - d - h/2),
            (center_x, bottom_y - d)
        ]
        right_color = tuple(int(c * 0.85) for c in color)
        pygame.draw.polygon(surface, right_color, right_points)
        pygame.draw.polygon(surface, (0, 0, 0), right_points, 2)
        
        return surface
    
    def _create_tetrahedron_sprite(self, size, color):
        """Create an isometric tetrahedron sprite."""
        surface = pygame.Surface((size, int(size * 1.2)), pygame.SRCALPHA)
        
        w = size * 0.7
        h = w * 0.866
        
        center_x = size // 2
        bottom_y = int(size * 1.05)
        apex_y = bottom_y - h
        
        # Back face
        back_points = [
            (center_x - w/3, bottom_y - h/3),
            (center_x + w/3, bottom_y - h/3),
            (center_x, apex_y)
        ]
        back_color = tuple(int(c * 0.7) for c in color)
        pygame.draw.polygon(surface, back_color, back_points)
        pygame.draw.polygon(surface, (0, 0, 0), back_points, 2)
        
        # Left face
        left_points = [
            (center_x, bottom_y),
            (center_x - w/3, bottom_y - h/3),
            (center_x, apex_y)
        ]
        left_color = tuple(int(c * 0.85) for c in color)
        pygame.draw.polygon(surface, left_color, left_points)
        pygame.draw.polygon(surface, (0, 0, 0), left_points, 2)
        
        # Right face
        right_points = [
            (center_x, bottom_y),
            (center_x + w/3, bottom_y - h/3),
            (center_x, apex_y)
        ]
        right_color = tuple(min(255, int(c * 1.0)) for c in color)
        pygame.draw.polygon(surface, right_color, right_points)
        pygame.draw.polygon(surface, (0, 0, 0), right_points, 2)
        
        return surface
    
    def get(self, shape, size, color):
        """Get a sprite for the given shape/size/color."""
        return self.sprites.get((shape, size, color))


class SpriteRenderer:
    """Sprite-based 3D renderer."""
    
    def __init__(self, world_file: str, width: int = 1024, height: int = 768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Tarski's World 3D - {os.path.basename(world_file)}")
        
        self.clock = pygame.time.Clock()
        self.angle_y = math.radians(45)
        self.zoom = 60  # Increased from 40 for bigger board
        
        # Load sprites
        print("Creating sprites...")
        self.sprites = ShapeSprites()
        
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
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        screen_x = (x_rot - z_rot) * self.zoom + self.width / 2
        screen_y = (x_rot + z_rot) * 0.5 * self.zoom - y * self.zoom + self.height / 2
        
        return (screen_x, screen_y, z_rot)
    
    def world_to_3d(self, world_x, world_y):
        """Convert world coordinates to 3D coordinates."""
        x = -(world_x - 4.5)
        z = (world_y - 4.5)
        return (x, z)
    
    def draw_board(self):
        """Draw the checkered board."""
        for i in range(8):
            for j in range(8):
                x, z = self.world_to_3d(i + 1, j + 1)
                
                if (i + j) % 2 == 0:
                    color = (220, 220, 220)
                else:
                    color = (80, 80, 80)
                
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
        """Draw all objects using sprites."""
        # Collect objects with their depths for sorting
        objects_with_depth = []
        
        for name, obj in self.objects.items():
            if not obj.is_complete():
                continue
            
            world_x, world_y = obj.position
            x, z = self.world_to_3d(world_x, world_y)
            
            size_map = {'small': 0.4, 'medium': 0.6, 'large': 0.8}
            size_3d = size_map.get(obj.size, 0.6)
            y = size_3d / 2
            
            # Project position
            screen_x, screen_y, depth = self.project_3d_to_2d(x, y, z)
            
            objects_with_depth.append((depth, obj, screen_x, screen_y))
        
        # Sort by depth (back to front)
        objects_with_depth.sort(key=lambda item: item[0], reverse=True)
        
        # Draw objects
        for depth, obj, screen_x, screen_y in objects_with_depth:
            sprite = self.sprites.get(obj.shape, obj.size, obj.color)
            if sprite:
                # Center the sprite
                rect = sprite.get_rect()
                rect.centerx = int(screen_x)
                rect.bottom = int(screen_y)
                self.screen.blit(sprite, rect)
    
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
            self.zoom = 60
    
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
        print("Usage: python render_sprites.py <world_file.pl>")
        print("\nExample:")
        print("  python render_sprites.py ../world1.pl")
        sys.exit(1)
    
    world_file = sys.argv[1]
    
    if not os.path.exists(world_file):
        print(f"Error: File '{world_file}' not found")
        sys.exit(1)
    
    renderer = SpriteRenderer(world_file)
    renderer.run()


if __name__ == "__main__":
    main()
