"""
Inference engine with SLD resolution and backtracking.
"""
from typing import List, Generator
from terms import Term, Variable, Compound
from database import Database, Clause
from unification import Substitution, unify
from builtin_predicates import BuiltinRegistry


class InferenceEngine:
    """SLD resolution with backtracking."""
    
    def __init__(self, database: Database):
        self.database = database
        self.depth_limit = 1000  # Prevent infinite recursion
        self._var_counter = 0  # Counter for variable renaming
        self.builtins = BuiltinRegistry()  # Built-in predicates
    
    def solve(self, goals: List[Term], subst: Substitution = None, depth: int = 0) -> Generator[Substitution, None, None]:
        """
        Generator that yields all solutions (substitutions) for given goals.
        
        Args:
            goals: List of Terms to prove
            subst: Current substitution
            depth: Current recursion depth
            
        Yields:
            Substitution objects (solutions)
        """
        if depth > self.depth_limit:
            return
        
        if subst is None:
            subst = Substitution()
        
        # Base case: no more goals - success!
        if not goals:
            yield subst
            return
        
        # Take first goal
        goal = subst.apply(goals[0])
        remaining_goals = goals[1:]
        
        # Check if goal is a built-in predicate
        if isinstance(goal, Compound) and self.builtins.is_builtin(goal.functor):
            # Evaluate built-in predicate
            for new_subst in self.builtins.evaluate(goal, subst):
                # Continue with remaining goals
                yield from self.solve(remaining_goals, new_subst, depth + 1)
        else:
            # Try to match with each clause in database
            for clause in self.database.get_clauses(goal):
                # Rename variables in clause to avoid conflicts
                renamed_clause = self._rename_variables(clause)
                
                # Try to unify goal with clause head
                new_subst = unify(goal, renamed_clause.head, subst)
                
                if new_subst is not None:
                    # Add clause body to goals (prepend to remaining goals)
                    new_goals = renamed_clause.body + remaining_goals
                    
                    # Recursively solve new goals
                    yield from self.solve(new_goals, new_subst, depth + 1)
    
    def _rename_variables(self, clause: Clause) -> Clause:
        """Rename all variables in a clause to avoid conflicts."""
        self._var_counter += 1
        suffix = f"_{self._var_counter}"
        
        rename_map = {}
        
        def rename_term(term: Term) -> Term:
            """Recursively rename variables in a term."""
            from terms import Atom, Variable, Compound, List as ListTerm
            
            if isinstance(term, Atom):
                return term
            
            elif isinstance(term, Variable):
                if term.name not in rename_map:
                    rename_map[term.name] = Variable(term.name + suffix)
                return rename_map[term.name]
            
            elif isinstance(term, Compound):
                new_args = tuple(rename_term(arg) for arg in term.args)
                return Compound(term.functor, new_args)
            
            elif isinstance(term, ListTerm):
                new_elements = tuple(rename_term(elem) for elem in term.elements)
                new_tail = rename_term(term.tail) if term.tail else None
                return ListTerm(new_elements, new_tail)
            
            return term
        
        # Rename head and body
        new_head = rename_term(clause.head)
        new_body = [rename_term(goal) for goal in clause.body]
        
        return Clause(new_head, new_body)
    
    def query(self, goal: Term) -> Generator[Substitution, None, None]:
        """
        Query the database with a single goal.
        Convenience method that wraps solve().
        """
        yield from self.solve([goal])
