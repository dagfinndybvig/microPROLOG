# Tarski's World for microPROLOG

A Tarski's World implementation where geometric objects (Platonic solids) with properties are placed on an 8×8 grid, and users can query about spatial relationships derived from absolute positions.

## Inspiration

This implementation is inspired by **"The Language of First-Order Logic"** by Jon Barwise and John Etchemendy, and the accompanying educational software **Tarski's World**. The program was designed to teach first-order logic through visual reasoning about geometric objects in a simple blocks world.

**Alfred Tarski** (1901-1983) was a Polish-American logician and mathematician, one of the greatest logicians of the 20th century. He made fundamental contributions to model theory, metamathematics, and the semantics of formal languages. His work on truth in formal languages and the concept of logical consequence forms the foundation of modern logic. Tarski's World honors his legacy by making abstract logical concepts concrete and accessible through visual representation.

## Quick Start

1. **Start microPROLOG** from the parent directory:
   ```bash
   cd ..
   python main.py
   ```

2. **Load the world rules**:
   ```
   &- consult world/world.pl
   ```

3. **Load an example world**:
   ```
   &- consult world/world1.pl
   ```

4. **Try a query**:
   ```
   &- ? (object X)
   X = a1
   ; (press Enter)
   X = b1
   ; (press Enter)
   ...
   ```

5. **Visualize the world** (from the world directory):
   ```bash
   python visualize_world.py world1.pl
   ```
   
   This displays the board with colored object names and a detailed table of all properties!

## What is Tarski's World?

Named after logician Alfred Tarski, Tarski's World is an educational system for teaching first-order logic using simple geometric shapes. You describe properties and relationships, then query the system using logical expressions.

## Object Properties

Each object has:
- **Name**: Lowercase letter + numeral (e.g., `a1`, `b2`, `c3`)
- **Shape**: `tetrahedron`, `cube`, or `dodecahedron` (Platonic solids)
- **Size**: `small`, `medium`, or `large`
- **Color**: `red`, `yellow`, or `purple`
- **Position**: `[X Y]` coordinates on 8×8 board (both 1-8)

### Geometric Properties

The three Platonic solids have these properties:

| Shape | Faces | Edges | Vertices |
|-------|-------|-------|----------|
| Tetrahedron | 4 | 6 | 4 |
| Cube | 6 | 12 | 8 |
| Dodecahedron | 12 | 30 | 20 |

## Available Predicates

### Basic Properties
- `(object X)` - X is an object in the world
- `(shape A S)` - Object A has shape S
- `(size A S)` - Object A has size S
- `(color A C)` - Object A has color C
- `(position A [X Y])` - Object A is at coordinates [X, Y]

### Spatial Relations (derived from positions)
- `(leftOf A B)` - A is to the left of B (A's X < B's X)
- `(rightOf A B)` - A is to the right of B (A's X > B's X)
- `(frontOf A B)` - A is in front of B (A's Y < B's Y)
- `(backOf A B)` - A is behind B (A's Y > B's Y)

### Size Relations (derived from size property)
- `(smaller A B)` - A is smaller than B
- `(larger A B)` - A is larger than B
- `(sameSize A B)` - A and B have the same size

### Property Matching
- `(sameShape A B)` - A and B have the same shape
- `(sameColor A B)` - A and B have the same color

### Geometric Properties
- `(faces S N)` - Shape S has N faces
- `(edges S N)` - Shape S has N edges
- `(vertices S N)` - Shape S has N vertices
- `(hasFaces X N)` - Object X has N faces
- `(hasEdges X N)` - Object X has N edges
- `(hasVertices X N)` - Object X has N vertices

## Example Queries

### Find all cubes
```
&- ? (shape X cube)
```

### Find small red objects
```
&- ? (size X small) (color X red)
```

### Find what's left of object a1
```
&- ? (leftOf X a1)
```

### Find objects smaller than a1
```
&- ? (smaller X a1)
```

### Complex: Find large objects to the right of small objects
```
&- ? (size X large) (size Y small) (rightOf X Y)
```

### Find objects with 12 faces (dodecahedrons)
```
&- ? (hasFaces X 12)
```

### Find objects in the back half of the board
```
&- ? (position X [XC Y]) (> Y 4)
```

See `queries.txt` for many more example queries!

## Example Session

```
$ python main.py
microPROLOG v1.0
Type 'help' for commands, 'quit' to exit

&- consult world/world.pl
Loaded 25 clause(s) from world/world.pl

&- consult world/world1.pl
Loaded 20 clause(s) from world/world1.pl

&- ? (object X)
X = a1
; 
X = b1
; 
X = c1
; 
X = d1
; 
no more solutions

&- ? (shape a1 S)
S = cube
; 
no more solutions

&- ? (leftOf X a1)
X = b1
; 
no more solutions

&- ? (smaller b1 a1)
yes
; 
no more solutions

&- quit
Goodbye!
```

## Provided World Files

- **world1.pl** - Simple world with 4 objects
- **world2.pl** - Medium world with 7 objects
- **world3.pl** - Complex world with 10 objects

Each world is randomly generated with different configurations of shapes, sizes, colors, and positions.

## Visualizing Worlds

Use the `visualize_world.py` script to display an ASCII representation of the board:

```bash
python visualize_world.py world1.pl
```

The visualizer shows:
- **Board**: 8×8 grid with object names displayed in their actual colors
- **Table**: Complete object details (shape, size, color, position)

Colors are rendered using ANSI codes:
- Red objects appear in red
- Yellow objects appear in yellow  
- Purple objects appear in purple

Example output:
```
        1   2   3   4   5   6   7   8
   ─────────────────────────────────
 8 │  .   .  b1  a1   .   .   .   . │
 7 │  .   .  d1   .   .   .   .   . │
 ...

Objects:
  Name   Shape         Size     Color    Position
  ------ ------------- -------- -------- --------
  a1     cube          large    red      [4, 8]
  b1     cube          small    yellow   [3, 8]
  ...
```

## Generating New Worlds

Use the `generate_world.py` script to create random worlds:

```bash
# Generate a world with 6 objects (default)
python generate_world.py

# Generate a world with specific number of objects
python generate_world.py 8 my_world.pl

# This creates my_world.pl with 8 randomly placed objects
```

The generator:
- Randomly assigns shapes, sizes, and colors
- Places objects at random free positions on the 8×8 board
- Ensures no two objects occupy the same position
- Creates properly formatted microPROLOG facts

## Board Coordinate System

The board is an 8×8 grid:
- **X axis**: 1-8, increases left → right
- **Y axis**: 1-8, increases front → back (bottom → top)
- Position `[1 1]` is front-left corner
- Position `[8 8]` is back-right corner

```
Y
8  [back]
7
6
5
4
3
2
1  [front]
   1 2 3 4 5 6 7 8  X
   [left] → [right]
```

## Tips

1. **Load order matters**: Always load `world.pl` before loading a specific world
2. **Press Enter** to see next solution, or type `n` to stop
3. **Variables are uppercase**: Use `X`, `Y`, `S` (not `x`, `y`, `s`)
4. **Combine conditions**: Use multiple goals in one query for complex questions
5. **Use `/=` for inequality**: Find objects that DON'T match a property

## Advanced Queries

### Find objects that share properties
```
&- ? (sameColor X Y) (sameShape X Y) (/= X Y)
```
Finds pairs of objects with both same color AND same shape.

### Find objects between coordinates
```
&- ? (position X [XC Y]) (>= XC 3) (=< XC 6)
```
Finds objects with X coordinate between 3 and 6.

### Find specific configurations
```
&- ? (shape X cube) (color X red) (leftOf X Y) (shape Y dodecahedron)
```
Finds red cubes that are to the left of dodecahedrons.

## Extensions

Future ideas to enhance the system:
- Distance calculations (Manhattan distance)
- Path finding (objects between two points)
- Visual board display (ASCII art with colors)
- Interactive world builder
- More complex spatial relations (diagonal, near, far)
- Euler's formula validation for Platonic solids

## Files

- `world.pl` - Core rules for spatial and size relations
- `world1.pl`, `world2.pl`, `world3.pl` - Example worlds
- `generate_world.py` - Python script to generate random worlds
- `visualize_world.py` - ASCII board visualization tool
- `queries.txt` - Example queries to try
- `README.md` - This file
- `PLAN.md` - Implementation plan and design notes
- `tarski.jpg` - Reference image

## Learning Resources

Tarski's World was created as a teaching tool for first-order logic. This implementation demonstrates:
- How to represent facts (object properties)
- How to define rules (spatial relations derived from positions)
- How to query knowledge bases (finding objects meeting criteria)
- How to use logical operators (conjunction, negation)

Perfect for learning both logic programming and Prolog!

### Recommended Reading

- **The Language of First-Order Logic** by Jon Barwise and John Etchemendy - The original textbook that introduced Tarski's World as an educational tool
- **Tarski's World** software - The companion program for visual logic learning (now available as Tarski's World 2.0)

---

**Happy exploring!** 🎲
