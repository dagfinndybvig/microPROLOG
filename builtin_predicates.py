"""
Built-in predicates for microPROLOG.
"""
from typing import Generator
from terms import Term, Atom, Variable, Compound, List as ListTerm
from unification import Substitution, unify


class BuiltinRegistry:
    """Registry of built-in predicates."""
    
    def __init__(self):
        self.builtins = {
            '=': self._unify_builtin,
            'is': self._arithmetic_eval,
            'atom': self._is_atom,
            'number': self._is_number,
            'var': self._is_var,
            'nonvar': self._is_nonvar,
            '<': self._less_than,
            '>': self._greater_than,
            '=<': self._less_or_equal,
            '>=': self._greater_or_equal,
            '<>': self._not_equal,
            '/=': self._not_unifiable,
        }
    
    def is_builtin(self, functor: str) -> bool:
        """Check if functor is a built-in predicate."""
        return functor in self.builtins
    
    def evaluate(self, goal: Term, subst: Substitution) -> Generator[Substitution, None, None]:
        """
        Evaluate built-in predicate.
        
        Yields:
            Substitution (success) or nothing (failure)
        """
        if not isinstance(goal, Compound):
            return
        
        functor = goal.functor
        if functor in self.builtins:
            yield from self.builtins[functor](goal.args, subst)
    
    def _unify_builtin(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(= X Y) - unify X and Y"""
        if len(args) != 2:
            return
        
        new_subst = unify(args[0], args[1], subst)
        if new_subst is not None:
            yield new_subst
    
    def _arithmetic_eval(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(is X Expr) - evaluate arithmetic expression and unify with X"""
        if len(args) != 2:
            return
        
        try:
            # Evaluate the expression
            expr = subst.apply(args[1])
            result = self._eval_arithmetic(expr, subst)
            
            # Unify with first argument
            new_subst = unify(args[0], Atom(result), subst)
            if new_subst is not None:
                yield new_subst
        except:
            pass  # Evaluation failed
    
    def _eval_arithmetic(self, expr: Term, subst: Substitution) -> float:
        """Evaluate an arithmetic expression."""
        expr = subst.apply(expr)
        
        if isinstance(expr, Atom):
            if isinstance(expr.value, (int, float)):
                return expr.value
            raise ValueError(f"Not a number: {expr}")
        
        elif isinstance(expr, Compound):
            if expr.functor == '+' and len(expr.args) == 2:
                left = self._eval_arithmetic(expr.args[0], subst)
                right = self._eval_arithmetic(expr.args[1], subst)
                return left + right
            
            elif expr.functor == '-' and len(expr.args) == 2:
                left = self._eval_arithmetic(expr.args[0], subst)
                right = self._eval_arithmetic(expr.args[1], subst)
                return left - right
            
            elif expr.functor == '*' and len(expr.args) == 2:
                left = self._eval_arithmetic(expr.args[0], subst)
                right = self._eval_arithmetic(expr.args[1], subst)
                return left * right
            
            elif expr.functor == '/' and len(expr.args) == 2:
                left = self._eval_arithmetic(expr.args[0], subst)
                right = self._eval_arithmetic(expr.args[1], subst)
                if right == 0:
                    raise ValueError("Division by zero")
                return left / right
            
            raise ValueError(f"Unknown operator: {expr.functor}")
        
        raise ValueError(f"Cannot evaluate: {expr}")
    
    def _is_atom(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(atom X) - check if X is an atom"""
        if len(args) != 1:
            return
        
        term = subst.apply(args[0])
        if isinstance(term, Atom) and isinstance(term.value, str):
            yield subst
    
    def _is_number(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(number X) - check if X is a number"""
        if len(args) != 1:
            return
        
        term = subst.apply(args[0])
        if isinstance(term, Atom) and isinstance(term.value, (int, float)):
            yield subst
    
    def _is_var(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(var X) - check if X is an unbound variable"""
        if len(args) != 1:
            return
        
        term = subst.apply(args[0])
        if isinstance(term, Variable):
            yield subst
    
    def _is_nonvar(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(nonvar X) - check if X is not an unbound variable"""
        if len(args) != 1:
            return
        
        term = subst.apply(args[0])
        if not isinstance(term, Variable):
            yield subst
    
    def _less_than(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(< X Y) - check if X is less than Y"""
        if len(args) != 2:
            return
        
        try:
            left = self._eval_arithmetic(args[0], subst)
            right = self._eval_arithmetic(args[1], subst)
            if left < right:
                yield subst
        except:
            pass  # Evaluation failed
    
    def _greater_than(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(> X Y) - check if X is greater than Y"""
        if len(args) != 2:
            return
        
        try:
            left = self._eval_arithmetic(args[0], subst)
            right = self._eval_arithmetic(args[1], subst)
            if left > right:
                yield subst
        except:
            pass  # Evaluation failed
    
    def _less_or_equal(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(=< X Y) - check if X is less than or equal to Y"""
        if len(args) != 2:
            return
        
        try:
            left = self._eval_arithmetic(args[0], subst)
            right = self._eval_arithmetic(args[1], subst)
            if left <= right:
                yield subst
        except:
            pass  # Evaluation failed
    
    def _greater_or_equal(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(>= X Y) - check if X is greater than or equal to Y"""
        if len(args) != 2:
            return
        
        try:
            left = self._eval_arithmetic(args[0], subst)
            right = self._eval_arithmetic(args[1], subst)
            if left >= right:
                yield subst
        except:
            pass  # Evaluation failed
    
    def _not_equal(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(<> X Y) - check if X is arithmetically not equal to Y"""
        if len(args) != 2:
            return
        
        try:
            left = self._eval_arithmetic(args[0], subst)
            right = self._eval_arithmetic(args[1], subst)
            if left != right:
                yield subst
        except:
            pass  # Evaluation failed
    
    def _not_unifiable(self, args: tuple, subst: Substitution) -> Generator[Substitution, None, None]:
        """(/= X Y) - check if X and Y cannot be unified"""
        if len(args) != 2:
            return
        
        new_subst = unify(args[0], args[1], subst)
        if new_subst is None:
            # Unification failed - they are not unifiable
            yield subst
