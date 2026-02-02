"""
Unification algorithm and substitution management for microPROLOG.
"""
from typing import Optional, Dict
from terms import Term, Atom, Variable, Compound, List as ListTerm


class Substitution:
    """Represents variable bindings."""
    
    def __init__(self, bindings: Optional[Dict[str, Term]] = None):
        self.bindings = bindings if bindings is not None else {}
    
    def bind(self, var_name: str, term: Term) -> 'Substitution':
        """Create a new substitution with an additional binding."""
        new_bindings = self.bindings.copy()
        new_bindings[var_name] = term
        return Substitution(new_bindings)
    
    def lookup(self, var_name: str) -> Optional[Term]:
        """Look up a variable, following the binding chain."""
        if var_name not in self.bindings:
            return None
        
        term = self.bindings[var_name]
        
        # Follow chain of variable bindings
        while isinstance(term, Variable) and term.name in self.bindings:
            term = self.bindings[term.name]
        
        return term
    
    def apply(self, term: Term) -> Term:
        """Apply substitution to a term."""
        if isinstance(term, Atom):
            return term
        
        elif isinstance(term, Variable):
            bound = self.lookup(term.name)
            if bound is not None:
                return self.apply(bound)  # Recursively apply
            return term
        
        elif isinstance(term, Compound):
            new_args = tuple(self.apply(arg) for arg in term.args)
            return Compound(term.functor, new_args)
        
        elif isinstance(term, ListTerm):
            new_elements = tuple(self.apply(elem) for elem in term.elements)
            new_tail = self.apply(term.tail) if term.tail else None
            return ListTerm(new_elements, new_tail)
        
        return term
    
    def __repr__(self):
        return f"Substitution({self.bindings})"
    
    def __str__(self):
        items = [f"{var} = {term}" for var, term in self.bindings.items()]
        return "{" + ", ".join(items) + "}"


def occurs_check(var: Variable, term: Term, subst: Substitution) -> bool:
    """
    Check if variable occurs in term (prevents infinite structures).
    Returns True if var occurs in term.
    """
    # Apply substitution first
    term = subst.apply(term)
    
    if isinstance(term, Variable):
        return var.name == term.name
    
    elif isinstance(term, Compound):
        return any(occurs_check(var, arg, subst) for arg in term.args)
    
    elif isinstance(term, ListTerm):
        for elem in term.elements:
            if occurs_check(var, elem, subst):
                return True
        if term.tail:
            return occurs_check(var, term.tail, subst)
        return False
    
    return False


def unify(term1: Term, term2: Term, subst: Optional[Substitution] = None) -> Optional[Substitution]:
    """
    Unify two terms, returning updated Substitution or None if unification fails.
    """
    if subst is None:
        subst = Substitution()
    
    # Apply current substitution to both terms
    term1 = subst.apply(term1)
    term2 = subst.apply(term2)
    
    # Both are atoms
    if isinstance(term1, Atom) and isinstance(term2, Atom):
        if term1.value == term2.value:
            return subst
        return None
    
    # term1 is a variable
    elif isinstance(term1, Variable):
        if isinstance(term2, Variable) and term1.name == term2.name:
            return subst  # Same variable
        if occurs_check(term1, term2, subst):
            return None  # Occurs check fails
        return subst.bind(term1.name, term2)
    
    # term2 is a variable
    elif isinstance(term2, Variable):
        if occurs_check(term2, term1, subst):
            return None  # Occurs check fails
        return subst.bind(term2.name, term1)
    
    # Both are compounds
    elif isinstance(term1, Compound) and isinstance(term2, Compound):
        # Functors must match
        if term1.functor != term2.functor:
            return None
        
        # Arity must match
        if len(term1.args) != len(term2.args):
            return None
        
        # Unify arguments
        for arg1, arg2 in zip(term1.args, term2.args):
            subst = unify(arg1, arg2, subst)
            if subst is None:
                return None
        
        return subst
    
    # Both are lists
    elif isinstance(term1, ListTerm) and isinstance(term2, ListTerm):
        # Empty lists
        if not term1.elements and not term1.tail and not term2.elements and not term2.tail:
            return subst
        
        # One empty, one not
        if (not term1.elements and not term1.tail) or (not term2.elements and not term2.tail):
            return None
        
        # Unify elements
        min_len = min(len(term1.elements), len(term2.elements))
        
        for i in range(min_len):
            subst = unify(term1.elements[i], term2.elements[i], subst)
            if subst is None:
                return None
        
        # Handle remaining elements and tails
        remaining1 = term1.elements[min_len:]
        remaining2 = term2.elements[min_len:]
        
        # Construct tail for term1
        if remaining1:
            tail1 = ListTerm(remaining1, term1.tail)
        else:
            tail1 = term1.tail if term1.tail else ListTerm(tuple())
        
        # Construct tail for term2
        if remaining2:
            tail2 = ListTerm(remaining2, term2.tail)
        else:
            tail2 = term2.tail if term2.tail else ListTerm(tuple())
        
        # Unify tails
        return unify(tail1, tail2, subst)
    
    # Different types - cannot unify
    return None
