% Ancestor relationships
% Demonstrates recursive rules in microPROLOG

% Base facts
(parent alice bob)
(parent bob charlie)
(parent charlie diana)

% Base case: parent is an ancestor
((ancestor X Y) (parent X Y))

% Recursive case: ancestor through intermediate
((ancestor X Z) (parent X Y) (ancestor Y Z))
