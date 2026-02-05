"""
3D Geometry and Math for Tarski's World Renderer
Defines Platonic solids and 3D transformation operations.
"""

import math
from typing import List, Tuple

# Type aliases
Vector3D = Tuple[float, float, float]
Vector2D = Tuple[float, float]
Face = List[int]  # List of vertex indices


class Vector3:
    """3D Vector operations."""
    
    @staticmethod
    def add(v1: Vector3D, v2: Vector3D) -> Vector3D:
        """Add two vectors."""
        return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])
    
    @staticmethod
    def subtract(v1: Vector3D, v2: Vector3D) -> Vector3D:
        """Subtract v2 from v1."""
        return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])
    
    @staticmethod
    def scale(v: Vector3D, s: float) -> Vector3D:
        """Scale vector by scalar."""
        return (v[0] * s, v[1] * s, v[2] * s)
    
    @staticmethod
    def cross(v1: Vector3D, v2: Vector3D) -> Vector3D:
        """Cross product of two vectors."""
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        )
    
    @staticmethod
    def dot(v1: Vector3D, v2: Vector3D) -> float:
        """Dot product of two vectors."""
        return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    
    @staticmethod
    def length(v: Vector3D) -> float:
        """Length (magnitude) of vector."""
        return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    
    @staticmethod
    def normalize(v: Vector3D) -> Vector3D:
        """Normalize vector to unit length."""
        length = Vector3.length(v)
        if length == 0:
            return (0, 0, 0)
        return (v[0] / length, v[1] / length, v[2] / length)


class Matrix3D:
    """3D transformation matrices."""
    
    @staticmethod
    def rotate_x(angle: float) -> List[List[float]]:
        """Rotation matrix around X axis."""
        c = math.cos(angle)
        s = math.sin(angle)
        return [
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ]
    
    @staticmethod
    def rotate_y(angle: float) -> List[List[float]]:
        """Rotation matrix around Y axis."""
        c = math.cos(angle)
        s = math.sin(angle)
        return [
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ]
    
    @staticmethod
    def rotate_z(angle: float) -> List[List[float]]:
        """Rotation matrix around Z axis."""
        c = math.cos(angle)
        s = math.sin(angle)
        return [
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ]
    
    @staticmethod
    def apply(matrix: List[List[float]], v: Vector3D) -> Vector3D:
        """Apply matrix transformation to vector."""
        x = matrix[0][0] * v[0] + matrix[0][1] * v[1] + matrix[0][2] * v[2]
        y = matrix[1][0] * v[0] + matrix[1][1] * v[1] + matrix[1][2] * v[2]
        z = matrix[2][0] * v[0] + matrix[2][1] * v[1] + matrix[2][2] * v[2]
        return (x, y, z)


class Projection:
    """3D to 2D projection."""
    
    @staticmethod
    def perspective(v: Vector3D, fov: float = 500, distance: float = 5) -> Vector2D:
        """Perspective projection."""
        # Simple perspective: scale by distance
        z = v[2] + distance
        if z <= 0:
            z = 0.1  # Avoid division by zero
        
        factor = fov / z
        x = v[0] * factor
        y = v[1] * factor
        return (x, y)
    
    @staticmethod
    def isometric(v: Vector3D, scale: float = 50) -> Vector2D:
        """Isometric projection (no perspective distortion)."""
        # Standard isometric projection angles
        angle_x = math.radians(30)
        angle_y = math.radians(30)
        
        x = (v[0] - v[2]) * math.cos(angle_x) * scale
        y = (v[0] + v[2]) * math.sin(angle_y) * scale - v[1] * scale
        return (x, y)


class PlatonicSolid:
    """Base class for Platonic solids."""
    
    def __init__(self, size: float = 1.0):
        self.size = size
        self.vertices: List[Vector3D] = []
        self.faces: List[Face] = []
    
    def get_scaled_vertices(self, scale: float) -> List[Vector3D]:
        """Get vertices scaled by given factor."""
        return [Vector3.scale(v, scale * self.size) for v in self.vertices]
    
    def get_face_normal(self, face: Face, vertices: List[Vector3D]) -> Vector3D:
        """Calculate normal vector for a face."""
        # Use first three vertices to calculate normal
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]
        
        # Two edges of the face
        edge1 = Vector3.subtract(v1, v0)
        edge2 = Vector3.subtract(v2, v0)
        
        # Cross product gives normal
        normal = Vector3.cross(edge1, edge2)
        return Vector3.normalize(normal)
    
    def get_face_center(self, face: Face, vertices: List[Vector3D]) -> Vector3D:
        """Calculate center point of a face (for depth sorting)."""
        sum_x = sum(vertices[i][0] for i in face)
        sum_y = sum(vertices[i][1] for i in face)
        sum_z = sum(vertices[i][2] for i in face)
        n = len(face)
        return (sum_x / n, sum_y / n, sum_z / n)


class Tetrahedron(PlatonicSolid):
    """Regular tetrahedron (4 faces, 4 vertices, 6 edges)."""
    
    def __init__(self, size: float = 1.0):
        super().__init__(size)
        
        # Regular tetrahedron centered at origin
        # Height calculation for regular tetrahedron
        h = math.sqrt(2.0 / 3.0)  # Height from base to apex
        r = 1.0 / math.sqrt(3.0)  # Radius of base circle
        
        # Vertices: apex at top, three base vertices
        self.vertices = [
            (0, h * 0.75, 0),                    # Apex (centered, pointing up)
            (-r, -h * 0.25, r),                  # Base vertex 1
            (r, -h * 0.25, r),                   # Base vertex 2
            (0, -h * 0.25, -r * 1.5)             # Base vertex 3
        ]
        
        # Faces (4 triangular faces)
        self.faces = [
            [0, 2, 1],  # Front face
            [0, 3, 2],  # Right face
            [0, 1, 3],  # Left face
            [1, 2, 3]   # Bottom face
        ]


class Cube(PlatonicSolid):
    """Regular cube/hexahedron (6 faces, 8 vertices, 12 edges)."""
    
    def __init__(self, size: float = 1.0):
        super().__init__(size)
        
        # Cube centered at origin
        s = 0.5  # Half-size
        
        # 8 vertices
        self.vertices = [
            (-s, -s, -s),  # 0: back-bottom-left
            (s, -s, -s),   # 1: back-bottom-right
            (s, s, -s),    # 2: back-top-right
            (-s, s, -s),   # 3: back-top-left
            (-s, -s, s),   # 4: front-bottom-left
            (s, -s, s),    # 5: front-bottom-right
            (s, s, s),     # 6: front-top-right
            (-s, s, s)     # 7: front-top-left
        ]
        
        # 6 faces (each is a square - 4 vertices)
        self.faces = [
            [0, 1, 2, 3],  # Back face
            [4, 5, 6, 7],  # Front face
            [0, 4, 7, 3],  # Left face
            [1, 5, 6, 2],  # Right face
            [0, 1, 5, 4],  # Bottom face
            [3, 2, 6, 7]   # Top face
        ]


class Dodecahedron(PlatonicSolid):
    """Regular dodecahedron (12 faces, 20 vertices, 30 edges)."""
    
    def __init__(self, size: float = 1.0):
        super().__init__(size)
        
        # Golden ratio
        phi = (1 + math.sqrt(5)) / 2
        
        # Scale factor to normalize size
        scale = 0.5
        
        # 20 vertices using golden ratio relationships
        # 8 vertices of a cube
        self.vertices = [
            (scale, scale, scale),
            (scale, scale, -scale),
            (scale, -scale, scale),
            (scale, -scale, -scale),
            (-scale, scale, scale),
            (-scale, scale, -scale),
            (-scale, -scale, scale),
            (-scale, -scale, -scale),
            # 4 vertices on XY plane
            (0, scale * phi, scale / phi),
            (0, scale * phi, -scale / phi),
            (0, -scale * phi, scale / phi),
            (0, -scale * phi, -scale / phi),
            # 4 vertices on YZ plane
            (scale / phi, 0, scale * phi),
            (scale / phi, 0, -scale * phi),
            (-scale / phi, 0, scale * phi),
            (-scale / phi, 0, -scale * phi),
            # 4 vertices on XZ plane
            (scale * phi, scale / phi, 0),
            (scale * phi, -scale / phi, 0),
            (-scale * phi, scale / phi, 0),
            (-scale * phi, -scale / phi, 0)
        ]
        
        # 12 pentagonal faces
        self.faces = [
            [0, 16, 2, 12, 8],
            [0, 8, 4, 18, 16],
            [0, 16, 17, 1, 9],
            [0, 9, 8, 4, 18],
            [1, 9, 5, 15, 13],
            [1, 13, 3, 17, 16],
            [2, 12, 14, 6, 10],
            [2, 10, 3, 17, 16],
            [3, 17, 1, 13, 11],
            [3, 11, 7, 19, 15],
            [4, 14, 6, 19, 18],
            [5, 15, 7, 19, 6]
        ]


def get_shape(shape_name: str, size_name: str) -> PlatonicSolid:
    """
    Factory function to create a shape with appropriate size.
    
    Args:
        shape_name: 'tetrahedron', 'cube', or 'dodecahedron'
        size_name: 'small', 'medium', or 'large'
    
    Returns:
        PlatonicSolid instance
    """
    # Size scaling factors
    size_map = {
        'small': 0.3,
        'medium': 0.5,
        'large': 0.7
    }
    
    size = size_map.get(size_name, 0.5)
    
    # Shape factory
    if shape_name == 'tetrahedron':
        return Tetrahedron(size)
    elif shape_name == 'cube':
        return Cube(size)
    elif shape_name == 'dodecahedron':
        return Dodecahedron(size)
    else:
        # Default to cube
        return Cube(size)
