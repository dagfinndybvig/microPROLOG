# Tarski's World 3D Rendering

This directory contains multiple 3D rendering implementations for visualizing Tarski's World. Each renderer uses a different approach, progressing from complex but unstable to simple and reliable.

## Overview

The 3D rendering system allows you to visualize Tarski's World objects (tetrahedrons, cubes, and dodecahedrons) on an 8×8 checkered board from multiple viewing angles. The coordinate system matches the ASCII visualization in the parent directory.

## Files in This Directory

### Core Geometry Library
- **`geometry.py`** - Complete 3D mathematics library
  - Vector3D operations (add, subtract, cross product, dot product, normalize)
  - Matrix3D transformations (rotation matrices)
  - Projection systems (perspective and isometric)
  - PlatonicSolid implementations (Tetrahedron, Cube, Dodecahedron)
  - Uses exact golden ratio (φ) for dodecahedron vertices

- **`board.py`** - Board rendering and coordinate mapping
  - Converts world coordinates [1-8, 1-8] to 3D space
  - Generates checkered board pattern
  - Square size management

### Test and Development Files
- **`test_render.py`** - Initial test renderer
  - Uses full geometry library
  - Real-time 3D rendering with camera controls
  - Places test objects to verify geometry
  - **Status**: Works but can be unstable

### Production Renderers

#### 1. **`render_3d.py`** - Full 3D Renderer ⚠️
The original full-featured renderer using complete geometry library.

**Features:**
- Loads actual world files
- Real-time 3D rendering with lighting
- Backface culling and depth sorting
- Camera orbit controls (arrow keys, zoom)

**Issues:**
- Can crash unexpectedly
- Objects may not render consistently
- Complex rendering pipeline

**Usage:**
```bash
python render_3d.py ../world1.pl
```

#### 2. **`render_simple.py`** - Simplified Renderer ⚙️
Simplified version with basic geometric calculations.

**Features:**
- Simpler isometric projection
- Basic shape rendering (cubes, tetrahedrons, spheres)
- More stable than render_3d.py
- Dodecahedrons rendered as gradient-shaded spheres

**Issues:**
- Spheres can vary in size during rotation
- Objects may disappear at certain angles

**Usage:**
```bash
python render_simple.py ../world1.pl
```

#### 3. **`render_sprites.py`** - Sprite-based Renderer ✨
Uses pre-rendered sprites for all shapes.

**Features:**
- Beautiful pre-rendered sprites with proper shading
- Cubes: Isometric 3-face rendering
- Tetrahedrons: Isometric 3-face rendering
- Dodecahedrons: Gradient spheres with highlights
- Consistent object sizes
- Smooth real-time rotation

**Advantages:**
- More stable than render_3d.py
- Better visual quality
- Sprites stay consistent

**Usage:**
```bash
python render_sprites.py ../world1.pl
```

#### 4. **`render_views.py`** - Pre-rendered Views Renderer ⭐ **RECOMMENDED**
The most stable and performant renderer.

**Features:**
- Pre-renders entire scene at 16 different angles
- Instant view switching (no rendering lag)
- Rock-solid stability
- Perfect depth sorting every time
- All shapes rendered as high-quality sprites

**Advantages:**
- Zero rendering crashes
- Instant rotation between views
- Consistent appearance from all angles
- Perfect for demonstration and exploration

**Controls:**
- **Left/Right Arrow**: Switch between 16 pre-rendered views
- **Space**: Reset to default view
- **ESC**: Quit

**Usage:**
```bash
python render_views.py ../world1.pl
python render_views.py ../world2.pl
python render_views.py ../world3.pl
```

## Rendering Approaches Explained

### Approach 1: Real-time 3D (render_3d.py, test_render.py)
**Method:** Calculate geometry, transform vertices, project to 2D every frame

**Pros:**
- Smooth continuous rotation
- True 3D rendering

**Cons:**
- Complex rendering pipeline
- Prone to crashes
- Depth sorting issues
- Objects may not render correctly

### Approach 2: Simplified Real-time (render_simple.py)
**Method:** Simplified projection with basic shapes

**Pros:**
- More stable than full 3D
- Simpler code

**Cons:**
- Spheres still inconsistent
- Objects can disappear

### Approach 3: Sprite-based Real-time (render_sprites.py)
**Method:** Pre-render shapes as sprites, compose scene in real-time

**Pros:**
- Beautiful visual quality
- Consistent object appearance
- Still allows smooth rotation

**Cons:**
- Real-time composition still has minor stability issues
- Sprites don't rotate with view (always face camera)

### Approach 4: Pre-rendered Views (render_views.py) ⭐
**Method:** Pre-render entire scene at multiple angles at startup

**Pros:**
- Maximum stability (no crashes)
- Instant view switching
- Perfect results every time
- No runtime calculation overhead

**Cons:**
- Discrete rotation steps (16 views)
- Slightly longer startup time
- Higher memory usage

## Coordinate System

The 3D renderer matches the ASCII visualization coordinate system:

```
World Coordinates: [X, Y]
- X: 1 (left) → 8 (right)
- Y: 1 (front/bottom) → 8 (back/top)

3D Space:
- X-axis: Right (but negated for mirror correction)
- Y-axis: Up (height)
- Z-axis: Back (depth)
```

Objects are positioned at the center of their board square and lifted by half their height so they sit on the board.

## Shape Representations

- **Tetrahedron**: Isometric pyramid with 3 visible faces
- **Cube**: Isometric cube with 3 visible faces (top, left, right)
- **Dodecahedron**: Rendered as a gradient-shaded sphere with highlight

## Size Scaling

- **Small**: 0.4 units (60px sprite)
- **Medium**: 0.6 units (90px sprite)
- **Large**: 0.8 units (120px sprite)

Board squares are 1.0 unit each.

## Recommendations

**For demonstration and exploration**: Use `render_views.py` (most stable)

**For development and testing**: Use `render_simple.py` or `render_sprites.py`

**For advanced features**: Use `render_3d.py` (if you need continuous rotation and don't mind potential instability)

## Technical Details

### Dependencies
- Python 3.x
- Pygame 2.6.1
- visualize_world.py (from parent directory)

### Performance
- **render_views.py**: Pre-renders 16 views in ~2 seconds, then runs at 60 FPS
- **render_sprites.py**: Creates 27 sprites at startup, runs at 60 FPS
- **render_simple.py**: No pre-rendering, runs at 60 FPS
- **render_3d.py**: Heavy calculations every frame, may lag

### Memory Usage
- **render_views.py**: ~50MB (stores 16 full-screen images)
- **render_sprites.py**: ~5MB (27 small sprites)
- **render_simple.py**: <1MB
- **render_3d.py**: <1MB

## Future Enhancements

Possible improvements:
- Add more viewing angles (32 or 64 views)
- Implement proper dodecahedron geometry (instead of spheres)
- Add labels showing object names
- Export views as PNG images
- Animation between views for smoother transitions
- Mouse-based rotation controls

## Reference Image

See `3D.jpg` for the original inspiration image that guided this implementation.

## Integration with Main System

These renderers complement the ASCII visualization in the parent directory. While the ASCII view is great for quick inspection in the terminal, the 3D renderers provide:
- Spatial depth perception
- Size comparison visualization
- Multiple viewing angles
- Better color differentiation

Use the ASCII visualizer for quick checks and the 3D renderer for detailed exploration and presentation.

---

**Recommended Command:**
```bash
python render_views.py ../world1.pl
```

Enjoy exploring Tarski's World in 3D! 🎮✨
