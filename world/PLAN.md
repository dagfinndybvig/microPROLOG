# Tarski's World Implementation Plan

## Overview

Implement a Tarski's World-style blocks world domain in microPROLOG where geometric objects with properties (shape, size, color) are placed on an 8×8 grid, and users can query about spatial relationships derived from absolute positions.

## Object Model

### Object Properties

Each object has:
- **Name**: lowercase letter + numeral (e.g., `a1`, `b2`, `c3`)
- **Shape**: `tetrahedron`, `dodecahedron`, or `cube`
- **Size**: `small`, `medium`, or `large`
- **Color**: `red`, `yellow`, or `purple`
- **Position**: `[X Y]` coordinates on 8×8 board (X: 1-8, Y: 1-8)

### Geometric Properties (for reference)

- **Tetrahedron**: 4 faces, 6 edges, 4 vertices
- **Cube**: 6 faces, 12 edges, 8 vertices
- **Dodecahedron**: 12 faces, 30 edges, 20 vertices

## Data Representation

### Facts (stored in database)

```prolog
% Object identity
(object a1)

% Properties
(shape a1 cube)
(size a1 small)
(color a1 red)

% Absolute position
(position a1 [3 5])
```

### Rules (derive relations from facts)

#### Spatial Relations (binary)
- `(leftOf A B)` - A's X < B's X
- `(rightOf A B)` - A's X > B's X
- `(backOf A B)` - A's Y > B's Y (higher Y = back of board)
- `(frontOf A B)` - A's Y < B's Y (lower Y = front of board)

#### Size Relations (binary)
- `(smaller A B)` - A's size < B's size
- `(larger A B)` - A's size > B's size
- `(sameSize A B)` - A's size = B's size

#### Spatial Ordering (ternary)
- `(between A B C)` - A is spatially between B and C (on same line)

## Implementation Steps

### 1. Create Basic World File (`world.pl`)

Define the rule set for deriving spatial and size relations:

```prolog
% Spatial relations - left/right (compare X coordinates)
((leftOf A B) 
  (position A [XA Y]) 
  (position B [XB Y]) 
  (< XA XB))

((rightOf A B) 
  (position A [XA Y]) 
  (position B [XB Y]) 
  (> XA XB))

% Spatial relations - front/back (compare Y coordinates)
((frontOf A B) 
  (position A [X YA]) 
  (position B [X YB]) 
  (< YA YB))

((backOf A B) 
  (position A [X YA]) 
  (position B [X YB]) 
  (> YA YB))

% Size comparisons
((smaller A B) (size A small) (size B medium))
((smaller A B) (size A small) (size B large))
((smaller A B) (size A medium) (size B large))

((larger A B) (size A large) (size B medium))
((larger A B) (size A large) (size B small))
((larger A B) (size A medium) (size B small))

((sameSize A B) (size A S) (size B S))

% Same shape
((sameShape A B) (shape A S) (shape B S))

% Same color
((sameColor A B) (color A C) (color B C))
```

### 2. Create World Generator (`generate_world.py`)

Python script to generate random worlds:

**Features:**
- Generate N objects (configurable, default 5-10)
- Random assignment of:
  - Names (a1, b2, c3, etc.)
  - Shapes (tetrahedron/dodecahedron/cube)
  - Sizes (small/medium/large)
  - Colors (red/yellow/purple)
  - Positions (ensure no collisions on 8×8 grid)
- Output as microPROLOG `.pl` file

**Functions:**
- `generate_object_name(index)` → unique name
- `random_property(options)` → random choice from list
- `random_position(taken_positions)` → random free position
- `generate_world(num_objects)` → complete world
- `save_world(objects, filename)` → write to `.pl` file

### 3. Create Example Worlds

Generate 2-3 example world files:
- `world1.pl` - Simple world (3-4 objects)
- `world2.pl` - Medium world (6-8 objects)
- `world3.pl` - Complex world (10-12 objects)

### 4. Create Query Examples (`queries.txt`)

Example queries to demonstrate the system:

```prolog
% Find all objects
? (object X)

% Find cubes
? (shape X cube)

% Find small red objects
? (size X small) (color X red)

% Find what's left of a1
? (leftOf X a1)

% Find what's behind b2
? (backOf X b2)

% Find objects smaller than a1
? (smaller X a1)

% Find objects with same shape as a1
? (sameShape X a1)

% Complex: small red cubes to the left of something large
? (shape X cube) (size X small) (color X red) (leftOf X Y) (size Y large)
```

### 5. Create README (`README.md`)

Document:
- How to load worlds
- How to query spatial relations
- Example session walkthrough
- How to generate new worlds
- Complete list of available predicates

### 6. Testing Plan

**Manual Tests:**
1. Load `world.pl` rules
2. Load example world (e.g., `world1.pl`)
3. Run query examples from `queries.txt`
4. Verify spatial relations match positions
5. Test edge cases (objects at boundaries)

**Validation:**
- All objects have unique positions
- Spatial relations are consistent (if A leftOf B, then B rightOf A)
- Size relations follow ordering (small < medium < large)

## File Structure

```
world/
├── PLAN.md                 # This file
├── README.md              # User documentation
├── world.pl               # Core rules for spatial/size relations
├── generate_world.py      # Python script to generate random worlds
├── world1.pl              # Example world (simple)
├── world2.pl              # Example world (medium)
├── world3.pl              # Example world (complex)
├── queries.txt            # Example queries
└── tarski.jpg            # Reference image
```

## Extension Ideas (Future)

- Geometric property queries (faces, edges, vertices)
- Distance calculations (Manhattan distance on grid)
- Path finding (objects between two points)
- Visual board display (ASCII art)
- Interactive world builder
- Euler's formula validation for Platonic solids

## Notes

- Position format: `[X Y]` where both X and Y are 1-8
- Board orientation: X increases left→right, Y increases front→back
- No two objects can occupy same position
- Spatial relations (leftOf, rightOf, etc.) are based purely on coordinates
- Object names are for identity only, not encoding position
