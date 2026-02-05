% Tarski's World - Core Rules
% This file defines rules for deriving spatial and size relations
% from absolute positions and object properties

% =============================================================================
% SPATIAL RELATIONS - Based on coordinate comparison
% =============================================================================

% leftOf: A is to the left of B (lower X coordinate)
((leftOf A B) 
  (position A [XA YA]) 
  (position B [XB YB]) 
  (< XA XB)).

% rightOf: A is to the right of B (higher X coordinate)
((rightOf A B) 
  (position A [XA YA]) 
  (position B [XB YB]) 
  (> XA XB)).

% frontOf: A is in front of B (lower Y coordinate)
((frontOf A B) 
  (position A [XA YA]) 
  (position B [XB YB]) 
  (< YA YB)).

% backOf: A is behind B (higher Y coordinate)
((backOf A B) 
  (position A [XA YA]) 
  (position B [XB YB]) 
  (> YA YB)).

% =============================================================================
% SIZE RELATIONS - Based on size property
% =============================================================================

% smaller: A is smaller than B
((smaller A B) (size A small) (size B medium)).
((smaller A B) (size A small) (size B large)).
((smaller A B) (size A medium) (size B large)).

% larger: A is larger than B
((larger A B) (size A large) (size B medium)).
((larger A B) (size A large) (size B small)).
((larger A B) (size A medium) (size B small)).

% sameSize: A and B have the same size
((sameSize A B) (size A S) (size B S)).

% =============================================================================
% PROPERTY RELATIONS - Same shape/color
% =============================================================================

% sameShape: A and B have the same shape
((sameShape A B) (shape A S) (shape B S)).

% sameColor: A and B have the same color
((sameColor A B) (color A C) (color B C)).

% =============================================================================
% GEOMETRIC PROPERTIES - Platonic solid properties
% =============================================================================

% faces: Number of faces for each shape
((faces tetrahedron 4)).
((faces cube 6)).
((faces dodecahedron 12)).

% edges: Number of edges for each shape
((edges tetrahedron 6)).
((edges cube 12)).
((edges dodecahedron 30)).

% vertices: Number of vertices for each shape
((vertices tetrahedron 4)).
((vertices cube 8)).
((vertices dodecahedron 20)).

% hasFaces: Object A has N faces (derived from shape)
((hasFaces A N) (shape A S) (faces S N)).

% hasEdges: Object A has N edges (derived from shape)
((hasEdges A N) (shape A S) (edges S N)).

% hasVertices: Object A has N vertices (derived from shape)
((hasVertices A N) (shape A S) (vertices S N)).
