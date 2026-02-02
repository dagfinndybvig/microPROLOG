"""
Clause database for storing and retrieving facts and rules.
"""
from typing import List, Optional
from terms import Term, Compound


class Clause:
    """Represents a fact or rule."""
    
    def __init__(self, head: Term, body: Optional[List[Term]] = None):
        self.head = head
        self.body = body if body is not None else []
    
    def is_fact(self) -> bool:
        """Check if this is a fact (no body)."""
        return len(self.body) == 0
    
    def __repr__(self):
        if self.is_fact():
            return f"Clause({self.head!r})"
        return f"Clause({self.head!r}, body={self.body!r})"
    
    def __str__(self):
        if self.is_fact():
            return str(self.head)
        body_str = " ".join(str(term) for term in self.body)
        return f"({self.head} {body_str})"


class Database:
    """Stores and retrieves clauses."""
    
    def __init__(self):
        self.clauses: List[Clause] = []
        self._index: dict = {}  # Index by functor for efficiency
    
    def add_clause(self, clause: Clause):
        """Add a fact or rule to the database."""
        self.clauses.append(clause)
        self._update_index(clause)
    
    def _update_index(self, clause: Clause):
        """Update the functor index."""
        functor = self._get_functor(clause.head)
        if functor:
            if functor not in self._index:
                self._index[functor] = []
            self._index[functor].append(clause)
    
    def _get_functor(self, term: Term) -> Optional[str]:
        """Get the functor of a term."""
        if isinstance(term, Compound):
            return term.functor
        return None
    
    def get_clauses(self, goal: Term) -> List[Clause]:
        """Retrieve clauses that might unify with goal."""
        functor = self._get_functor(goal)
        
        if functor and functor in self._index:
            return self._index[functor]
        
        # If no functor or not indexed, return all clauses
        return self.clauses
    
    def clear(self):
        """Remove all clauses from the database."""
        self.clauses.clear()
        self._index.clear()
    
    def retract(self, pattern: Term) -> bool:
        """Remove first clause matching pattern. Returns True if removed."""
        from unification import unify, Substitution
        
        for i, clause in enumerate(self.clauses):
            if unify(clause.head, pattern, Substitution()) is not None:
                removed_clause = self.clauses.pop(i)
                self._rebuild_index()
                return True
        
        return False
    
    def _rebuild_index(self):
        """Rebuild the functor index."""
        self._index.clear()
        for clause in self.clauses:
            self._update_index(clause)
    
    def __len__(self):
        return len(self.clauses)
    
    def __iter__(self):
        return iter(self.clauses)
