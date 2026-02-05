# 3D Rendering for Tarski's World - Implementation Plan

## Overview

Create a standalone Pygame-based 3D renderer that visualizes Tarski's World files with proper 3D geometric shapes (Platonic solids) positioned on a checkered 8×8 board, matching the coordinate system used in the ASCII visualizer.

## Reference

- `3D.jpg` - General visual style reference (checkered board, 3D perspective)
- ASCII visualizer - **Primary reference for exact coordinate system and object placement**

## Coordinate System (must match ASCII visualizer!)

From ASCII visualizer:
- **X axis**: 1-8, increases left → right
- **Y axis**: 1-8, increases front → back (bottom → top of screen)
- **Board**: 8×8 grid
- **Position format**: `[X Y]` where both are 1-8

3D coordinate mapping:
- X (1-8) → 3D X axis (horizontal, left-right)
- Y (1-8) → 3D Z axis (depth, front-back) 
- 3D Y axis → vertical (up-down) for object height

## Object Specifications

### Platonic Solids to Render

1. **Tetrahedron** (4 faces, 6 edges, 4 vertices)
   - Regular triangular pyramid
   - All faces are equilateral triangles
   
2. **Cube** (6 faces, 12 edges, 8 vertices)
   - Regular hexahedron
   - All faces are squares
   
3. **Dodecahedron** (12 faces, 30 edges, 20 vertices)
   - Regular polyhedron
   - All faces are regular pentagons

### Object Properties (from world files)

- **Size**: small, medium, large (affects scale)
- **Color**: red, yellow, purple (RGB rendering)
- **Position**: [X Y] coordinates on board

## Technical Architecture

### 1. Core Components

**File: `render_3d.py`** (main script)
- Parse world files (reuse logic from visualize_world.py)
- Initialize Pygame
- Set up 3D→2D projection
- Main rendering loop
- Camera controls

**File: `geometry.py`** (3D geometry)
- Platonic solid vertex definitions
- Face definitions (vertex indices)
- Rotation matrices
- 3D→2D projection
- Depth sorting for painter's algorithm

**File: `board.py`** (board rendering)
- 8×8 checkered board generation
- Board square positioning in 3D space
- Board rendering with perspective

### 2. 3D Rendering Pipeline

**Stage 1: World Coordinates → 3D Coordinates**
```
[X, Y] world position → [x3d, y3d, z3d] 3D position
where:
  x3d = (X - 4.5) * square_size  (center board at origin)
  z3d = (Y - 4.5) * square_size
  y3d = 0 (on board) + object_height/2
```

**Stage 2: 3D → Camera Space**
- Apply camera rotation (orbit around board)
- Apply camera translation

**Stage 3: Camera Space → Screen Space**
- Perspective projection or isometric projection
- Map to Pygame screen coordinates

**Stage 4: Rendering**
- Sort faces by depth (painter's algorithm)
- Draw board
- Draw objects (back to front)
- Edge highlighting/wireframe (optional)

### 3. Pygame Implementation

**Window Setup**
- Resolution: 1024×768 (configurable)
- Background: Gradient blue (like reference image)
- Title: "Tarski's World - 3D Visualization"

**Camera System**
- Default view: Isometric-style angle (30° elevation, 45° rotation)
- Interactive controls:
  - Arrow keys: Rotate camera around board
  - +/- keys: Zoom in/out
  - Space: Reset to default view
  - Mouse: Optional click-drag rotation

**Rendering Order**
1. Clear screen (gradient background)
2. Render checkered board
3. Render all objects (depth-sorted)
4. Render UI overlay (object info, controls help)
5. Flip display

### 4. Geometry Definitions

**Coordinate Systems**
- Right-handed coordinate system
- Y-up convention (Y is vertical)
- Object origins at center

**Vertex Scaling**
- Base unit: 1.0 = one board square
- Small: 0.3 scale
- Medium: 0.5 scale  
- Large: 0.7 scale

**Tetrahedron Vertices** (centered, pointing up)
```python
vertices = [
    (0, height, 0),           # apex
    (-base/2, 0, base/2),     # base vertex 1
    (base/2, 0, base/2),      # base vertex 2
    (0, 0, -base)             # base vertex 3
]
faces = [(0,1,2), (0,2,3), (0,3,1), (1,3,2)]  # triangular faces
```

**Cube Vertices** (centered)
```python
s = size/2
vertices = [
    (-s,-s,-s), (s,-s,-s), (s,s,-s), (-s,s,-s),  # back face
    (-s,-s,s), (s,-s,s), (s,s,s), (-s,s,s)        # front face
]
faces = [(0,1,2,3), (4,5,6,7), (0,4,7,3), (1,5,6,2), (0,1,5,4), (2,3,7,6)]
```

**Dodecahedron Vertices** (use golden ratio φ = (1+√5)/2)
```python
# 20 vertices using golden ratio relationships
# Complex but standard definition
# Faces: 12 pentagonal faces
```

### 5. Color System

**Color Mapping**
- Red: (220, 60, 60)
- Yellow: (240, 220, 60)
- Purple: (180, 80, 180)

**Shading**
- Basic ambient + diffuse lighting
- Light direction: from top-front
- Face shading based on normal vector angle
- Darker faces = facing away from light

**Board Colors**
- White squares: (240, 240, 240)
- Black squares: (60, 60, 80)
- Alternating pattern

### 6. File Integration

**Input: World Files**
- Read from parent directory: `../world1.pl`, `../world2.pl`, etc.
- Parse using same logic as `visualize_world.py`
- Extract: object name, shape, size, color, position [X Y]

**Command Line Usage**
```bash
python render_3d.py ../world1.pl
python render_3d.py ../world2.pl
```

### 7. UI Overlays

**On-Screen Display**
- Top-left: World filename
- Top-right: Object count
- Bottom-left: Camera controls help
- Bottom-right: Current view angle

**Object Inspection (optional enhancement)**
- Hover over objects to highlight
- Show object properties in overlay

## Implementation Steps

### Phase 1: Core Setup
- [x] Create directory structure
- [ ] Install Pygame: `pip install pygame`
- [ ] Create `geometry.py` with basic 3D math
  - Vector operations
  - Rotation matrices
  - Projection functions
- [ ] Create `board.py` with board generation
- [ ] Test basic rendering: rotate a cube

### Phase 2: Geometry Implementation
- [ ] Implement tetrahedron vertices and faces
- [ ] Implement cube vertices and faces
- [ ] Implement dodecahedron vertices and faces
- [ ] Test rendering each shape independently
- [ ] Implement depth sorting (painter's algorithm)
- [ ] Add basic lighting/shading

### Phase 3: World Integration
- [ ] Import world file parser from parent directory
- [ ] Map world coordinates to 3D positions
- [ ] Position objects on board
- [ ] Scale objects by size property
- [ ] Color objects by color property
- [ ] Test with world1.pl

### Phase 4: Camera & Controls
- [ ] Implement camera orbit system
- [ ] Add keyboard controls (arrows, zoom)
- [ ] Add mouse controls (optional)
- [ ] Implement smooth transitions
- [ ] Test camera from multiple angles

### Phase 5: Polish
- [ ] Add gradient background
- [ ] Add UI overlays
- [ ] Add board labels (X, Y coordinates)
- [ ] Optimize rendering performance
- [ ] Add command-line argument parsing
- [ ] Test with world1, world2, world3

### Phase 6: Documentation
- [ ] Create README.md with usage instructions
- [ ] Document controls
- [ ] Add screenshots
- [ ] Update main world README

## Technical Challenges & Solutions

### Challenge 1: Pygame doesn't have 3D
**Solution**: Implement software 3D rendering
- Define vertices in 3D space
- Project to 2D using perspective/isometric projection
- Use painter's algorithm for depth

### Challenge 2: Dodecahedron complexity
**Solution**: Use golden ratio formulas
- Well-documented vertex positions
- 20 vertices, 12 pentagonal faces
- Can simplify to low-poly if needed

### Challenge 3: Coordinate system mapping
**Solution**: Explicit mapping from world to 3D
- World [X,Y] → 3D [x, 0, z]
- Center board at 3D origin
- Maintain right-handed system

### Challenge 4: Performance with many objects
**Solution**: Optimize rendering
- Only render visible faces (backface culling)
- Batch similar operations
- Limit redraw rate to 60 FPS

## Expected Output

When running `python render_3d.py ../world1.pl`:
- Opens Pygame window
- Shows 3D checkered board
- Displays 4 objects from world1:
  - a1: large red cube at [4, 8]
  - b1: small yellow cube at [3, 8]
  - c1: large purple dodecahedron at [5, 1]
  - d1: small purple dodecahedron at [3, 7]
- Interactive camera rotation
- Clean, professional visualization

## File Structure

```
3D_rendering/
├── PLAN.md              # This file
├── 3D.jpg              # Reference image
├── render_3d.py        # Main renderer
├── geometry.py         # 3D geometry & math
├── board.py            # Board rendering
├── README.md           # Usage documentation
└── screenshots/        # Example renders (optional)
```

## Dependencies

- **Pygame**: `pip install pygame`
- **Python 3.7+**: Standard library only otherwise
- **Parent modules**: Import parse logic from `../visualize_world.py`

## Testing Strategy

1. Test basic Pygame window
2. Test single cube rendering
3. Test all three shapes
4. Test board rendering
5. Test coordinate mapping with world1.pl
6. Test camera controls
7. Test all three example worlds
8. Verify coordinates match ASCII visualizer

## Future Enhancements (Optional)

- Export rendered frames as images
- Animation (rotating objects)
- Shadows on board
- Better lighting model (Phong shading)
- Texture mapping
- Anti-aliasing
- Object labels
- Click-to-select objects
- Multiple viewports

---

**Next Step**: Implement Phase 1 (Core Setup)
