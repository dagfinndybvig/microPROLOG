"""
Checkered board rendering for Tarski's World 3D visualization.
"""

from typing import List, Tuple
from geometry import Vector3D, Vector2D, Matrix3D, Projection


class Board:
    """8x8 checkered board for Tarski's World."""
    
    def __init__(self, square_size: float = 1.0):
        """
        Initialize board.
        
        Args:
            square_size: Size of each square in 3D units
        """
        self.size = 8  # 8x8 board
        self.square_size = square_size
        self.white_color = (240, 240, 240)
        self.black_color = (60, 60, 80)
    
    def get_square_vertices_3d(self, x: int, y: int) -> List[Vector3D]:
        """
        Get 3D vertices for a board square.
        
        Args:
            x: Board X coordinate (1-8)
            y: Board Y coordinate (1-8)
        
        Returns:
            List of 4 vertices defining the square
        """
        # Center board at origin
        # Convert from 1-8 to centered coordinates
        x_start = (x - 4.5) * self.square_size
        y_start = (y - 4.5) * self.square_size
        x_end = x_start + self.square_size
        y_end = y_start + self.square_size
        
        # Board is on Y=0 plane (horizontal)
        # Return vertices in counter-clockwise order when viewed from above
        return [
            (x_start, 0, y_start),  # Bottom-left
            (x_end, 0, y_start),    # Bottom-right
            (x_end, 0, y_end),      # Top-right
            (x_start, 0, y_end)     # Top-left
        ]
    
    def is_white_square(self, x: int, y: int) -> bool:
        """
        Determine if a square should be white.
        
        Args:
            x: Board X coordinate (1-8)
            y: Board Y coordinate (1-8)
        
        Returns:
            True if white, False if black
        """
        # Checkerboard pattern: (x + y) even = white
        return (x + y) % 2 == 0
    
    def get_all_squares(self) -> List[Tuple[List[Vector3D], Tuple[int, int, int]]]:
        """
        Get all board squares with their colors.
        
        Returns:
            List of (vertices, color) tuples
        """
        squares = []
        for y in range(1, self.size + 1):
            for x in range(1, self.size + 1):
                vertices = self.get_square_vertices_3d(x, y)
                color = self.white_color if self.is_white_square(x, y) else self.black_color
                squares.append((vertices, color))
        
        return squares
    
    def world_to_3d(self, world_x: int, world_y: int, height: float = 0) -> Vector3D:
        """
        Convert world coordinates [X, Y] to 3D position.
        
        Args:
            world_x: World X coordinate (1-8)
            world_y: World Y coordinate (1-8)
            height: Height above board (default: 0 = on board)
        
        Returns:
            3D position vector
        """
        # Center of the square
        x_3d = (world_x - 4.5) * self.square_size
        z_3d = (world_y - 4.5) * self.square_size
        
        return (x_3d, height, z_3d)
