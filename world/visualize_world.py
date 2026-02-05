#!/usr/bin/env python3
"""
Tarski's World Board Visualizer
Displays an ASCII representation of the world board with objects.
"""

import sys
import re
from typing import Dict, Tuple, Optional


# ANSI color codes
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class WorldObject:
    """Represents an object in the world."""
    def __init__(self, name: str):
        self.name = name
        self.shape = None
        self.size = None
        self.color = None
        self.position = None
    
    def is_complete(self) -> bool:
        """Check if all properties are set."""
        return all([self.shape, self.size, self.color, self.position])
    
    def get_shape_symbol(self) -> str:
        """Get single-letter symbol for shape."""
        if self.shape == 'tetrahedron':
            return 'T'
        elif self.shape == 'cube':
            return 'C'
        elif self.shape == 'dodecahedron':
            return 'D'
        return '?'
    
    def get_color_code(self) -> str:
        """Get abbreviated color code."""
        if self.color == 'red':
            return 'R'
        elif self.color == 'yellow':
            return 'Y'
        elif self.color == 'purple':
            return 'P'
        return '?'
    
    def get_ansi_color(self) -> str:
        """Get ANSI color code for this object's color."""
        if self.color == 'red':
            return Colors.RED
        elif self.color == 'yellow':
            return Colors.YELLOW
        elif self.color == 'purple':
            return Colors.PURPLE
        return Colors.RESET
    
    def get_size_symbol(self) -> str:
        """Get size symbol."""
        if self.size == 'small':
            return 's'
        elif self.size == 'medium':
            return 'm'
        elif self.size == 'large':
            return 'L'
        return '?'


def parse_world_file(filename: str) -> Dict[str, WorldObject]:
    """Parse a microPROLOG world file and extract objects."""
    objects = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse each line
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('%'):
                continue
            
            # Remove trailing period
            if line.endswith('.'):
                line = line[:-1].strip()
            
            # Parse different fact types using regex
            
            # (object name)
            match = re.match(r'\(object\s+(\w+)\)', line)
            if match:
                name = match.group(1)
                if name not in objects:
                    objects[name] = WorldObject(name)
                continue
            
            # (shape name shape_type)
            match = re.match(r'\(shape\s+(\w+)\s+(\w+)\)', line)
            if match:
                name, shape = match.groups()
                if name not in objects:
                    objects[name] = WorldObject(name)
                objects[name].shape = shape
                continue
            
            # (size name size_type)
            match = re.match(r'\(size\s+(\w+)\s+(\w+)\)', line)
            if match:
                name, size = match.groups()
                if name not in objects:
                    objects[name] = WorldObject(name)
                objects[name].size = size
                continue
            
            # (color name color_type)
            match = re.match(r'\(color\s+(\w+)\s+(\w+)\)', line)
            if match:
                name, color = match.groups()
                if name not in objects:
                    objects[name] = WorldObject(name)
                objects[name].color = color
                continue
            
            # (position name [X Y])
            match = re.match(r'\(position\s+(\w+)\s+\[(\d+)\s+(\d+)\]\)', line)
            if match:
                name, x, y = match.groups()
                if name not in objects:
                    objects[name] = WorldObject(name)
                objects[name].position = (int(x), int(y))
                continue
        
        return objects
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)


def visualize_board(objects: Dict[str, WorldObject], show_legend: bool = True):
    """Display ASCII visualization of the board with colored names."""
    BOARD_SIZE = 8
    
    # Create empty board
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # Place objects on board
    for obj in objects.values():
        if obj.is_complete() and obj.position:
            x, y = obj.position
            # Convert to 0-indexed
            board[y-1][x-1] = obj
    
    # Print board header
    print("\n     " + "".join(f"{i+1:4}" for i in range(BOARD_SIZE)))
    print("   " + "─" * (BOARD_SIZE * 4 + 1))
    
    # Print board from top to bottom (Y=8 to Y=1)
    for y in range(BOARD_SIZE - 1, -1, -1):
        row_num = y + 1
        print(f" {row_num} │", end="")
        
        for x in range(BOARD_SIZE):
            obj = board[y][x]
            if obj:
                # Display name in color
                color = obj.get_ansi_color()
                cell = f"{color}{obj.name}{Colors.RESET}"
                # Need to account for invisible ANSI codes in spacing
                print(f" {cell} ", end="")
            else:
                print("  . ", end="")
        
        print("│")
    
    print("   " + "─" * (BOARD_SIZE * 4 + 1))
    print()
    
    # Print detailed object table
    print("Objects:")
    print(f"  {'Name':<6} {'Shape':<13} {'Size':<8} {'Color':<8} {'Position'}")
    print(f"  {'-'*6} {'-'*13} {'-'*8} {'-'*8} {'-'*8}")
    sorted_objects = sorted(objects.values(), key=lambda o: o.name)
    for obj in sorted_objects:
        if obj.is_complete():
            x, y = obj.position
            # Display name in color in the table too
            color = obj.get_ansi_color()
            print(f"  {color}{obj.name:<6}{Colors.RESET} {obj.shape:<13} {obj.size:<8} {obj.color:<8} [{x}, {y}]")


def visualize_board_detailed(objects: Dict[str, WorldObject], show_legend: bool = True):
    """Display more detailed ASCII visualization with multi-line cells."""
    BOARD_SIZE = 8
    
    # Create empty board
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # Place objects on board
    for obj in objects.values():
        if obj.is_complete() and obj.position:
            x, y = obj.position
            board[y-1][x-1] = obj
    
    # Print legend
    if show_legend:
        print("\nLegend:")
        print("  T=Tetrahedron, C=Cube, D=Dodecahedron")
        print("  R=Red, Y=Yellow, P=Purple")
        print("  s=small, m=medium, L=large")
        print()
    
    # Print board header
    print("      " + "".join(f"{i+1:7}" for i in range(BOARD_SIZE)))
    print("    " + "─" * (BOARD_SIZE * 7 + 2))
    
    # Print board from top to bottom (Y=8 to Y=1)
    for y in range(BOARD_SIZE - 1, -1, -1):
        row_num = y + 1
        
        # Two-line cells
        # Line 1: name and shape
        print(f"  {row_num} │", end="")
        for x in range(BOARD_SIZE):
            obj = board[y][x]
            if obj:
                line1 = f"{obj.name}:{obj.get_shape_symbol()}"
                print(f"{line1:^6}", end=" ")
            else:
                print("   .  ", end=" ")
        print("│")
        
        # Line 2: color and size
        print(f"    │", end="")
        for x in range(BOARD_SIZE):
            obj = board[y][x]
            if obj:
                line2 = f"{obj.get_color_code()}{obj.get_size_symbol()}"
                print(f"{line2:^6}", end=" ")
            else:
                print("      ", end=" ")
        print("│")
        
        print("    " + "─" * (BOARD_SIZE * 7 + 2))
    
    print()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python visualize_world.py <world_file.pl>")
        print("\nExample:")
        print("  python visualize_world.py world1.pl")
        print("  python visualize_world.py world2.pl")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Parse world file
    objects = parse_world_file(filename)
    
    # Check if any objects were found
    if not objects:
        print("No objects found in file")
        sys.exit(1)
    
    print(f"\nTarski's World: {filename}")
    print(f"Objects: {len(objects)}")
    
    # Visualize
    visualize_board(objects)


if __name__ == "__main__":
    main()
