# microPROLOG Implementation Plan

## Overview
microPROLOG is a simplified dialect of PROLOG developed in the 1980s at Imperial College London. It uses a more accessible syntax than standard PROLOG, with a focus on educational use and logic programming fundamentals.

## Core Characteristics of microPROLOG

### Syntax Differences from Standard PROLOG
- **Prefix notation**: Uses `(predicate arg1 arg2 ...)` instead of `predicate(arg1, arg2, ...)`
- **Query syntax**: Uses `?` prefix for queries
- **List notation**: Uses square brackets `[...]` similar to PROLOG
- **Variables**: Start with uppercase letters or underscore
- **Atoms/constants**: Start with lowercase letters or are numeric

### Core Functionality
1. **Clause Database**: Store facts and rules
2. **Unification**: Pattern matching mechanism
3. **Backtracking**: Search through alternative solutions
4. **Built-in predicates**: Basic operations (equality, arithmetic, list operations)

## Implementation Plan

### Phase 1: Core Data Structures
- [ ] Define internal representation for terms (atoms, variables, compound terms, lists)
- [ ] Implement variable representation and management
- [ ] Create clause storage structure (fact/rule database)
- [ ] Design substitution/binding environment for variables

### Phase 2: Parser
- [ ] Implement tokenizer for microPROLOG syntax
  - [ ] Handle atoms (lowercase identifiers)
  - [ ] Handle variables (uppercase identifiers)
  - [ ] Handle numbers
  - [ ] Handle special characters: `( ) [ ] , |`
  - [ ] Handle comments
- [ ] Implement parser for terms
  - [ ] Parse atoms
  - [ ] Parse variables
  - [ ] Parse compound terms in prefix notation: `(predicate arg1 arg2 ...)`
  - [ ] Parse lists: `[head | tail]` and `[elem1 elem2 ...]`
- [ ] Parse clauses (facts and rules)
  - [ ] Facts: Simple assertions like `(parent john mary)`
  - [ ] Rules: Form `((head) (condition1) (condition2) ...)` where first term is conclusion, rest are conditions
- [ ] Parse queries: Lines starting with `?` or query commands

### Phase 3: Unification Engine
- [ ] Implement occurs check (prevents infinite structures)
- [ ] Implement term unification algorithm
  - [ ] Atom-atom unification
  - [ ] Variable-term unification
  - [ ] Compound term unification (recursive)
  - [ ] List unification
- [ ] Implement substitution composition
- [ ] Handle variable renaming (to avoid conflicts)

### Phase 4: Inference Engine
- [ ] Implement SLD resolution (backward chaining)
- [ ] Build goal stack/query processing
- [ ] Implement backtracking mechanism
  - [ ] Choice points
  - [ ] Backtrack state restoration
  - [ ] Alternative clause selection
- [ ] Implement search strategy (depth-first)
- [ ] Handle multiple solutions (yield all via backtracking)

### Phase 5: Built-in Predicates
- [ ] **Logical predicates**
  - [ ] `(= X Y)` - Unification/equality test
  - [ ] `(is X Expr)` - Arithmetic evaluation
- [ ] **Arithmetic predicates**
  - [ ] `(+ X Y Z)` - Addition
  - [ ] `(- X Y Z)` - Subtraction
  - [ ] `(* X Y Z)` - Multiplication
  - [ ] `(/ X Y Z)` - Division
  - [ ] Comparison: `(< X Y)`, `(> X Y)`, `(=< X Y)`, `(>= X Y)`
- [ ] **List predicates**
  - [ ] `(append L1 L2 L3)` - List concatenation
  - [ ] `(member X L)` - List membership
  - [ ] `(length L N)` - List length
- [ ] **Type checking predicates**
  - [ ] `(atom X)` - Check if atom
  - [ ] `(number X)` - Check if number
  - [ ] `(var X)` - Check if unbound variable
  - [ ] `(nonvar X)` - Check if bound

### Phase 6: REPL (Read-Eval-Print Loop)
- [ ] Implement command loop
- [ ] **Add clause command**: Accept facts and rules to add to database
  - [ ] Syntax: Direct entry of clauses like `(parent john mary)`
  - [ ] Store in clause database
- [ ] **Query command**: Process queries and return solutions
  - [ ] Syntax: `? (parent john X)` or similar query notation
  - [ ] Display all solutions via backtracking
  - [ ] Handle user interaction (next solution, stop)
- [ ] **Database management commands**
  - [ ] List all clauses: `listing` or `show`
  - [ ] Clear database: `clear`
  - [ ] Remove specific clauses: `retract`
- [ ] **Control commands**
  - [ ] Exit: `quit` or `exit`
  - [ ] Help: `help`
- [ ] Error handling and user-friendly messages

### Phase 7: Testing & Refinement
- [ ] Test basic facts and queries
- [ ] Test rules with multiple clauses
- [ ] Test backtracking scenarios
- [ ] Test list operations
- [ ] Test arithmetic operations
- [ ] Test complex nested structures
- [ ] Test error cases (syntax errors, infinite loops)

## Example Usage Scenarios

### Adding Facts
```
(parent tom bob)
(parent tom liz)
(parent bob ann)
(parent bob pat)
(parent pat jim)
```

### Adding Rules
```
((grandparent X Z) (parent X Y) (parent Y Z))
((ancestor X Y) (parent X Y))
((ancestor X Z) (parent X Y) (ancestor Y Z))
```

### Querying
```
? (parent tom X)
X = bob
X = liz

? (grandparent tom X)
X = ann
X = pat

? (ancestor tom jim)
yes
```

## Technical Decisions

### Language Choice
- **Python**: Good for prototyping, easy string manipulation, dynamic typing

### Architecture Pattern
- **Interpreter pattern**: Direct execution of parsed structures
- **Modular design**: Separate parser, unifier, inference engine
- **Immutable data structures**: Easier backtracking and state management

## Notes and Considerations

1. **Syntax Flexibility**: microPROLOG has variations; clarify exact syntax expectations
2. **Performance**: Initial focus on correctness over optimization
3. **Infinite Loops**: Implement depth limit or cycle detection for safety
4. **Standard Compliance**: Focus on core features first, extend later
5. **User Experience**: Clear error messages and helpful feedback in REPL

## Resources
- Original microPROLOG was developed by Keith Clark and colleagues at Imperial College
- Syntax emphasizes readability with prefix notation
- Educational focus: simpler than full PROLOG implementations

## Next Steps
1. Choose implementation language
2. Begin with Phase 1 (data structures)
3. Implement incrementally with tests at each phase

---

## Python Implementation Outline

### Project Structure
```
microPROLOG/
├── PLAN.md
├── main.py                 # Entry point for REPL
├── terms.py                # Term representations (Atom, Variable, Compound, List)
├── parser.py               # Tokenizer and parser
├── unification.py          # Unification algorithm and substitutions
├── inference.py            # Inference engine with backtracking
├── builtins.py             # Built-in predicates
├── database.py             # Clause storage and management
├── repl.py                 # REPL implementation
└── tests/                  # Unit tests
    ├── test_terms.py
    ├── test_parser.py
    ├── test_unification.py
    └── test_inference.py
```

### Module Details

#### 1. `terms.py` - Core Data Structures
```python
# Base class for all terms
class Term:
    pass

class Atom(Term):
    """Represents atomic values: atoms, numbers"""
    def __init__(self, value):
        self.value = value

class Variable(Term):
    """Represents logical variables (uppercase names)"""
    def __init__(self, name):
        self.name = name
    
class Compound(Term):
    """Represents compound terms: (functor arg1 arg2 ...)"""
    def __init__(self, functor, args):
        self.functor = functor  # string or Atom
        self.args = args        # list of Terms

class List(Term):
    """Represents lists: [] or [head|tail]"""
    def __init__(self, elements=None, tail=None):
        self.elements = elements or []
        self.tail = tail  # Can be Variable or another List
```

**Key Python features:**
- Use `dataclasses` for cleaner term definitions
- Implement `__eq__`, `__hash__`, `__repr__` for debugging
- Use type hints for better code clarity

#### 2. `parser.py` - Tokenizer and Parser
```python
class Tokenizer:
    """Converts string input into tokens"""
    def __init__(self, text):
        self.text = text
        self.pos = 0
    
    def tokenize(self):
        """Returns list of tokens: ('LPAREN', '('), ('ATOM', 'parent'), ..."""
        tokens = []
        # Regex patterns for: identifiers, numbers, special chars
        return tokens

class Parser:
    """Converts tokens into Term objects"""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse_term(self):
        """Parse a single term (atom, variable, compound, list)"""
        pass
    
    def parse_clause(self):
        """Parse a fact or rule"""
        # Fact: single term like (parent john mary)
        # Rule: ((head) (body1) (body2) ...)
        pass
    
    def parse_query(self):
        """Parse query starting with ?"""
        pass
```

**Key Python features:**
- Use `re` module for tokenization
- Recursive descent parsing
- Generator functions for lazy parsing
- Exception handling for syntax errors

#### 3. `unification.py` - Unification Engine
```python
class Substitution:
    """Represents variable bindings: {Variable: Term, ...}"""
    def __init__(self, bindings=None):
        self.bindings = bindings or {}
    
    def bind(self, var, term):
        """Add a new binding"""
        pass
    
    def lookup(self, var):
        """Follow binding chain for a variable"""
        pass
    
    def apply(self, term):
        """Apply substitution to a term"""
        pass

def unify(term1, term2, subst=None):
    """
    Unify two terms, returning updated Substitution or None if fails
    
    Cases:
    - Both atoms: must be equal
    - Variable and term: bind variable (occurs check!)
    - Compounds: functors must match, unify args recursively
    - Lists: unify elements, handle tail
    """
    subst = subst or Substitution()
    # Implementation here
    return subst  # or None if unification fails

def occurs_check(var, term, subst):
    """Check if variable occurs in term (prevents infinite structures)"""
    pass
```

**Key Python features:**
- Use dictionaries for substitutions
- Immutable approach: return new Substitution objects
- Pattern matching (Python 3.10+) for term type checking

#### 4. `database.py` - Clause Database
```python
class Clause:
    """Represents a fact or rule"""
    def __init__(self, head, body=None):
        self.head = head  # Term
        self.body = body or []  # List of Terms (empty for facts)
    
    def is_fact(self):
        return len(self.body) == 0

class Database:
    """Stores and retrieves clauses"""
    def __init__(self):
        self.clauses = []
        self._index = {}  # Index by functor for efficiency
    
    def add_clause(self, clause):
        """Add a fact or rule"""
        self.clauses.append(clause)
        self._update_index(clause)
    
    def get_clauses(self, goal):
        """Retrieve clauses that might unify with goal"""
        # Use index to filter by functor
        return matching_clauses
    
    def clear(self):
        """Remove all clauses"""
        pass
    
    def retract(self, pattern):
        """Remove clauses matching pattern"""
        pass
```

**Key Python features:**
- List for clause storage
- Dictionary for indexing by functor (optimization)
- Iterator protocol for clause retrieval

#### 5. `inference.py` - Inference Engine with Backtracking
```python
class InferenceEngine:
    """SLD resolution with backtracking"""
    def __init__(self, database):
        self.database = database
        self.depth_limit = 1000  # Prevent infinite recursion
    
    def solve(self, goals, subst=None, depth=0):
        """
        Generator that yields all solutions (substitutions)
        
        Args:
            goals: List of Terms to prove
            subst: Current substitution
            depth: Current recursion depth
            
        Yields:
            Substitution objects (solutions)
        """
        if depth > self.depth_limit:
            return
        
        subst = subst or Substitution()
        
        # Base case: no more goals
        if not goals:
            yield subst
            return
        
        # Take first goal
        goal = goals[0]
        remaining_goals = goals[1:]
        
        # Try to match with each clause in database
        for clause in self.database.get_clauses(goal):
            # Rename variables in clause to avoid conflicts
            renamed_clause = self._rename_variables(clause)
            
            # Try to unify goal with clause head
            new_subst = unify(goal, renamed_clause.head, subst)
            
            if new_subst is not None:
                # Add clause body to goals
                new_goals = [new_subst.apply(g) for g in renamed_clause.body] + remaining_goals
                
                # Recursively solve new goals
                yield from self.solve(new_goals, new_subst, depth + 1)
    
    def _rename_variables(self, clause):
        """Rename all variables in clause to avoid conflicts"""
        # Use counter to generate unique variable names
        pass
```

**Key Python features:**
- **Generators** (`yield from`) for lazy backtracking
- Recursion for depth-first search
- List slicing for goal management

#### 6. `builtins.py` - Built-in Predicates
```python
class BuiltinRegistry:
    """Registry of built-in predicates"""
    def __init__(self):
        self.builtins = {
            '=': self._unify,
            'is': self._arithmetic_eval,
            '+': self._add,
            # ... more builtins
        }
    
    def is_builtin(self, functor):
        """Check if functor is a built-in"""
        return functor in self.builtins
    
    def evaluate(self, goal, subst):
        """
        Evaluate built-in predicate
        
        Returns:
            Generator yielding Substitution (success) or nothing (failure)
        """
        functor = goal.functor
        if functor in self.builtins:
            yield from self.builtins[functor](goal.args, subst)
    
    def _unify(self, args, subst):
        """(= X Y) - unify X and Y"""
        if len(args) == 2:
            new_subst = unify(args[0], args[1], subst)
            if new_subst:
                yield new_subst
    
    def _arithmetic_eval(self, args, subst):
        """(is X Expr) - evaluate arithmetic expression"""
        # Evaluate right side, unify with left
        pass
```

**Key Python features:**
- Dictionary dispatch for builtins
- Generators for consistency with inference engine
- `eval()` for arithmetic (with safety checks)

#### 7. `repl.py` - Read-Eval-Print Loop
```python
class REPL:
    """Interactive REPL for microPROLOG"""
    def __init__(self):
        self.database = Database()
        self.engine = InferenceEngine(self.database)
        self.parser = None
    
    def run(self):
        """Main REPL loop"""
        print("microPROLOG v1.0")
        print("Type 'help' for commands, 'quit' to exit")
        
        while True:
            try:
                line = input("?- ").strip()
                
                if not line:
                    continue
                
                # Handle commands
                if line in ['quit', 'exit']:
                    break
                elif line == 'help':
                    self._show_help()
                elif line == 'listing':
                    self._show_database()
                elif line == 'clear':
                    self.database.clear()
                # Query (starts with ?)
                elif line.startswith('?'):
                    self._handle_query(line[1:].strip())
                # Clause (fact or rule)
                else:
                    self._handle_clause(line)
                    
            except KeyboardInterrupt:
                print("\nInterrupted")
            except Exception as e:
                print(f"Error: {e}")
    
    def _handle_query(self, query_text):
        """Process a query and display solutions"""
        query = self.parser.parse_query(query_text)
        
        solution_count = 0
        for subst in self.engine.solve([query]):
            solution_count += 1
            self._display_solution(query, subst)
            
            # Ask if user wants more solutions
            if not self._continue_search():
                break
        
        if solution_count == 0:
            print("no")
    
    def _handle_clause(self, clause_text):
        """Parse and add a clause to database"""
        clause = self.parser.parse_clause(clause_text)
        self.database.add_clause(clause)
        print("ok")
```

**Key Python features:**
- `input()` for interactive input
- Exception handling for user errors
- String methods for command parsing

#### 8. `main.py` - Entry Point
```python
#!/usr/bin/env python3
from repl import REPL

def main():
    repl = REPL()
    repl.run()

if __name__ == "__main__":
    main()
```

### Implementation Strategy

**Phase-by-Phase Approach:**

1. **Phase 1 (Timeslot 1)**: Implement `terms.py`
   - Define all term classes with proper `__repr__` for debugging
   - Write unit tests for term creation

2. **Phase 2 (Timeslots 2-3)**: Implement `parser.py`
   - Start with tokenizer
   - Add parser for atoms, variables, compounds
   - Add list parsing
   - Test with example inputs

3. **Phase 3 (Timeslots 3-4)**: Implement `unification.py`
   - Core unification algorithm
   - Occurs check
   - Substitution management
   - Extensive testing (this is critical!)

4. **Phase 4 (Timeslots 4-5)**: Implement `database.py` and basic `inference.py`
   - Clause storage
   - Simple fact queries (no rules yet)
   - Add backtracking for multiple solutions

5. **Phase 5 (Timeslots 5-6)**: Complete `inference.py` with rules
   - SLD resolution
   - Variable renaming
   - Full backtracking

6. **Phase 6 (Timeslot 6)**: Implement `builtins.py`
   - Start with `=` (unification)
   - Add arithmetic predicates
   - Add list predicates

7. **Phase 7 (Timeslot 7)**: Implement `repl.py` and `main.py`
   - Interactive loop
   - Command handling
   - User experience polish

8. **Phase 8 (Ongoing)**: Testing and refinement
   - Integration tests
   - Example programs (family tree, lists, arithmetic)
   - Bug fixes and optimizations

### Python-Specific Best Practices

- **Type Hints**: Use throughout for clarity
  ```python
  def unify(term1: Term, term2: Term, subst: Substitution = None) -> Optional[Substitution]:
  ```

- **Dataclasses**: Use for term definitions
  ```python
  from dataclasses import dataclass
  
  @dataclass(frozen=True)
  class Atom:
      value: Union[str, int, float]
  ```

- **String Representations**: Implement `__repr__` and `__str__`
  ```python
  def __repr__(self):
      return f"Atom({self.value!r})"
  ```

- **Testing**: Use `pytest` for unit tests
  ```python
  def test_unify_atoms():
      a1 = Atom("john")
      a2 = Atom("john")
      result = unify(a1, a2)
      assert result is not None
  ```

- **Immutability**: Use frozen dataclasses, return new substitutions
  
- **Generators**: Essential for backtracking - use `yield` extensively
