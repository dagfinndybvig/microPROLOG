% Family tree example
% Facts about parent relationships

(parent tom bob)
(parent tom mary)
(parent bob ann)
(parent bob pat)
(parent mary jim)

% Rules for derived relationships

((grandparent X Z) (parent X Y) (parent Y Z))
((sibling X Y) (parent P X) (parent P Y))
