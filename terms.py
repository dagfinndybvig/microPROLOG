"""
Core data structures for microPROLOG terms.
"""
from dataclasses import dataclass
from typing import Union, List, Any


@dataclass(frozen=True)
class Atom:
    """Represents atomic values: atoms (strings) or numbers."""
    value: Union[str, int, float]
    
    def __repr__(self):
        return f"Atom({self.value!r})"
    
    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Variable:
    """Represents logical variables (uppercase names or underscore)."""
    name: str
    
    def __repr__(self):
        return f"Variable({self.name!r})"
    
    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Compound:
    """Represents compound terms: (functor arg1 arg2 ...)"""
    functor: str
    args: tuple  # Tuple of Terms for immutability
    
    def __repr__(self):
        args_repr = ", ".join(repr(arg) for arg in self.args)
        return f"Compound({self.functor!r}, ({args_repr}))"
    
    def __str__(self):
        if not self.args:
            return f"({self.functor})"
        args_str = " ".join(str(arg) for arg in self.args)
        return f"({self.functor} {args_str})"


@dataclass(frozen=True)
class List:
    """Represents lists: [] or [head|tail]"""
    elements: tuple  # Tuple of Terms
    tail: Any = None  # Can be Variable, another List, or None
    
    def __repr__(self):
        if self.tail:
            return f"List({self.elements!r}, tail={self.tail!r})"
        return f"List({self.elements!r})"
    
    def __str__(self):
        if not self.elements and not self.tail:
            return "[]"
        if self.tail:
            elements_str = " ".join(str(e) for e in self.elements)
            return f"[{elements_str} | {self.tail}]"
        elements_str = " ".join(str(e) for e in self.elements)
        return f"[{elements_str}]"


# Type alias for any term
Term = Union[Atom, Variable, Compound, List]
