#!/usr/bin/env python3
"""
Tarski's World Generator
Generates random worlds with geometric objects on an 8x8 grid.
"""

import random
import sys
from typing import List, Tuple, Set

# Configuration
SHAPES = ['tetrahedron', 'cube', 'dodecahedron']
SIZES = ['small', 'medium', 'large']
COLORS = ['red', 'yellow', 'purple']
BOARD_SIZE = 8  # 8x8 grid
DEFAULT_NUM_OBJECTS = 6


class WorldObject:
    """Represents a single object in the world."""
    
    def __init__(self, name: str, shape: str, size: str, color: str, position: Tuple[int, int]):
        self.name = name
        self.shape = shape
        self.size = size
        self.color = color
        self.position = position
    
    def to_prolog(self) -> List[str]:
        """Convert object to microPROLOG facts."""
        x, y = self.position
        return [
            f"(object {self.name})",
            f"(shape {self.name} {self.shape})",
            f"(size {self.name} {self.size})",
            f"(color {self.name} {self.color})",
            f"(position {self.name} [{x} {y}])"
        ]


def generate_object_name(index: int) -> str:
    """Generate unique object name (a1, b2, c3, etc.)."""
    letter = chr(ord('a') + (index % 26))
    number = (index // 26) + 1
    return f"{letter}{number}"


def random_position(taken_positions: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """Generate a random free position on the board."""
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(1, BOARD_SIZE)
        y = random.randint(1, BOARD_SIZE)
        pos = (x, y)
        if pos not in taken_positions:
            return pos
    
    # Fallback: find first free position
    for x in range(1, BOARD_SIZE + 1):
        for y in range(1, BOARD_SIZE + 1):
            pos = (x, y)
            if pos not in taken_positions:
                return pos
    
    raise ValueError("Board is full!")


def generate_world(num_objects: int = DEFAULT_NUM_OBJECTS) -> List[WorldObject]:
    """Generate a random world with specified number of objects."""
    if num_objects > BOARD_SIZE * BOARD_SIZE:
        raise ValueError(f"Cannot place {num_objects} objects on {BOARD_SIZE}x{BOARD_SIZE} board")
    
    objects = []
    taken_positions = set()
    
    for i in range(num_objects):
        name = generate_object_name(i)
        shape = random.choice(SHAPES)
        size = random.choice(SIZES)
        color = random.choice(COLORS)
        position = random_position(taken_positions)
        taken_positions.add(position)
        
        obj = WorldObject(name, shape, size, color, position)
        objects.append(obj)
    
    return objects


def save_world(objects: List[WorldObject], filename: str):
    """Save world to a microPROLOG file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("% Tarski's World - Generated World\n")
        f.write(f"% Contains {len(objects)} objects on an 8x8 board\n")
        f.write("% Load this file after loading world.pl\n\n")
        
        for i, obj in enumerate(objects):
            if i > 0:
                f.write("\n")
            
            # Write all facts for this object
            for fact in obj.to_prolog():
                f.write(fact + ".\n")
    
    print(f"Generated world with {len(objects)} objects: {filename}")
    
    # Print summary
    print("\nObjects:")
    for obj in objects:
        x, y = obj.position
        print(f"  {obj.name}: {obj.size} {obj.color} {obj.shape} at [{x}, {y}]")


def print_board(objects: List[WorldObject]):
    """Print ASCII representation of the board."""
    # Create empty board
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # Place objects (use first letter of name)
    for obj in objects:
        x, y = obj.position
        board[y-1][x-1] = obj.name[0]  # Use first character of name
    
    print("\nBoard Layout (Y increases upward, X increases rightward):")
    print("  " + " ".join(str(i+1) for i in range(BOARD_SIZE)))
    
    # Print from top to bottom (high Y to low Y)
    for y in range(BOARD_SIZE - 1, -1, -1):
        row = board[y]
        print(f"{y+1} " + " ".join(row))


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        try:
            num_objects = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [num_objects]")
            sys.exit(1)
    else:
        num_objects = DEFAULT_NUM_OBJECTS
    
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    else:
        filename = "generated_world.pl"
    
    # Set random seed for reproducibility (optional)
    # random.seed(42)
    
    try:
        objects = generate_world(num_objects)
        save_world(objects, filename)
        print_board(objects)
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
