"""
REPL (Read-Eval-Print Loop) for microPROLOG.
"""
from typing import Optional
from terms import Term, Variable, Compound, List as ListTerm
from parser import parse_text, parse_query
from database import Database, Clause
from inference import InferenceEngine
from builtin_predicates import BuiltinRegistry
from unification import Substitution


class REPL:
    """Interactive REPL for microPROLOG."""
    
    def __init__(self):
        self.database = Database()
        self.engine = InferenceEngine(self.database)
        self.builtins = BuiltinRegistry()
    
    def run(self):
        """Main REPL loop."""
        print("microPROLOG v1.0")
        print("Type 'help' for commands, 'quit' to exit")
        print()
        
        while True:
            try:
                line = input("&- ").strip()
                
                if not line:
                    continue
                
                # Handle commands (single-line only)
                if line in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                elif line == 'help':
                    self._show_help()
                elif line == 'listing':
                    self._show_database()
                elif line == 'clear':
                    self.database.clear()
                    print("Database cleared")
                # Load from file
                elif line.startswith('consult ') or line.startswith('load '):
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2:
                        filename = parts[1].strip()
                        self._load_file(filename)
                    else:
                        print("Usage: consult <filename> or load <filename>")
                # Save to file
                elif line.startswith('save '):
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2:
                        filename = parts[1].strip()
                        self._save_file(filename)
                    else:
                        print("Usage: save <filename>")
                # Show visualization
                elif line.startswith('show '):
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2:
                        filename = parts[1].strip()
                        self._show_visualization(filename)
                    else:
                        print("Usage: show <filename>")
                # Query (starts with ?)
                elif line.startswith('?'):
                    self._handle_query(line[1:].strip())
                # Clause (fact or rule) - check if complete
                elif line.startswith('('):
                    # Accumulate lines until we get a period
                    clause_lines = [line]
                    
                    while not clause_lines[-1].endswith('.'):
                        try:
                            continuation = input("... ").strip()
                            if continuation:
                                clause_lines.append(continuation)
                        except (EOFError, KeyboardInterrupt):
                            print("\nInput cancelled")
                            clause_lines = []
                            break
                    
                    if clause_lines:
                        # Join all lines and remove the period
                        full_clause = ' '.join(clause_lines)[:-1].strip()
                        self._handle_clause(full_clause)
                else:
                    print(f"Unknown command: {line}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\nInterrupted")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_help(self):
        """Display help message."""
        print("microPROLOG Commands:")
        print("  (fact args...).         - Add a fact (note the period!)")
        print("  ((head) (body)...).     - Add a rule (note the period!)")
        print("  ? (query args...)       - Query the database")
        print("  listing                 - Show all clauses")
        print("  clear                   - Clear database")
        print("  consult <file>          - Load clauses from file")
        print("  load <file>             - Load clauses from file (same as consult)")
        print("  save <file>             - Save database to file")
        print("  show <file>             - Visualize world file (Tarski's World only)")
        print("  help                    - Show this message")
        print("  quit / exit             - Exit microPROLOG")
        print()
        print("Examples:")
        print("  (parent tom bob).")
        print("  ((grandparent X Z) (parent X Y) (parent Y Z)).")
        print("  ? (parent tom X)")
        print("  consult family.pl")
        print("  save my_facts.pl")
        print("  show world/world1.pl")
    
    def _show_database(self):
        """Display all clauses in the database."""
        if len(self.database) == 0:
            print("Database is empty")
            return
        
        for clause in self.database:
            if clause.is_fact():
                print(str(clause.head))
            else:
                # Print rule in the form: ((head) (body1) (body2) ...)
                parts = [str(clause.head)] + [str(goal) for goal in clause.body]
                print(f"({' '.join(parts)})")
    
    def _handle_clause(self, clause_text: str):
        """Parse and add a clause to the database."""
        try:
            term = parse_text(clause_text)
            
            # Check if it's a rule: ((head) (body1) (body2) ...)
            if isinstance(term, Compound) and len(term.args) > 0:
                # First argument is head, rest are body
                first_arg = term.args[0]
                
                # If first arg is a compound, this might be a rule
                if isinstance(first_arg, Compound) and term.functor == "":
                    # This is a rule (empty functor means rule syntax)
                    head = first_arg
                    body = list(term.args[1:])  # Body might be empty
                    clause = Clause(head, body)
                else:
                    # This is a fact
                    clause = Clause(term)
            else:
                # This is a fact
                clause = Clause(term)
            
            self.database.add_clause(clause)
            print("ok")
            
        except Exception as e:
            print(f"Error parsing clause: {e}")
    
    def _handle_query(self, query_text: str):
        """Process a query and display solutions."""
        try:
            goals = parse_query(query_text)
            
            if not goals:
                print("Error: Empty query")
                return
            
            # Single goal - check if it's a builtin
            if len(goals) == 1 and isinstance(goals[0], Compound) and self.builtins.is_builtin(goals[0].functor):
                self._handle_builtin_query(goals[0])
            else:
                # Multiple goals or non-builtin - use regular query
                self._handle_regular_query(goals)
                
        except Exception as e:
            print(f"Error processing query: {e}")
    
    def _handle_builtin_query(self, goal: Term):
        """Handle a built-in predicate query."""
        # Collect all variables in the goal
        variables = self._collect_variables(goal)
        
        solution_count = 0
        
        for subst in self.builtins.evaluate(goal, Substitution()):
            solution_count += 1
            
            # Display variable bindings
            if variables:
                self._display_solution(variables, subst)
            else:
                print("yes")
            
            # Ask if user wants more solutions
            if not self._continue_search():
                break
        
        if solution_count == 0:
            print("no")
    
    def _handle_regular_query(self, goals):
        """Handle a regular database query (single goal or conjunction)."""
        # Collect all variables in all goals
        variables = []
        for goal in goals:
            variables.extend(self._collect_variables(goal))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_vars = []
        for var in variables:
            if var.name not in seen:
                seen.add(var.name)
                unique_vars.append(var)
        variables = unique_vars
        
        solution_count = 0
        
        # Query with all goals
        for subst in self.engine.solve(goals):
            solution_count += 1
            
            # Display variable bindings
            if variables:
                self._display_solution(variables, subst)
            else:
                print("yes")
            
            # Ask if user wants more solutions
            if not self._continue_search():
                break
        
        if solution_count == 0:
            print("no")
        else:
            print("no more solutions")
    
    def _collect_variables(self, term: Term) -> list:
        """Collect all unique variables in a term."""
        variables = []
        seen = set()
        
        def collect(t: Term):
            if isinstance(t, Variable):
                if t.name not in seen:
                    seen.add(t.name)
                    variables.append(t)
            elif isinstance(t, Compound):
                for arg in t.args:
                    collect(arg)
            elif isinstance(t, ListTerm):
                for elem in t.elements:
                    collect(elem)
                if t.tail:
                    collect(t.tail)
        
        collect(term)
        return variables
    
    def _display_solution(self, variables: list, subst: Substitution):
        """Display variable bindings for a solution."""
        for var in variables:
            bound_term = subst.apply(var)
            print(f"{var.name} = {bound_term}")
    
    def _continue_search(self) -> bool:
        """Ask user if they want to continue searching for solutions."""
        try:
            response = input("; ").strip().lower()
            # Return continues, 'n' or 'N' stops
            return response != 'n'
        except (EOFError, KeyboardInterrupt):
            return False
    
    def _load_file(self, filename: str):
        """Load clauses from a file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by lines and accumulate until we find a complete clause
            lines = content.split('\n')
            clause_count = 0
            current_clause = []
            start_line = None
            
            for line_num, line in enumerate(lines, 1):
                # Strip whitespace but preserve the line for accumulation
                stripped = line.strip()
                
                # Skip empty lines and comments when not in a clause
                if not current_clause and (not stripped or stripped.startswith('%')):
                    continue
                
                # Skip comment lines even within clauses
                if stripped.startswith('%'):
                    continue
                
                # If we have content, accumulate it
                if stripped:
                    if not current_clause:
                        start_line = line_num
                    current_clause.append(stripped)
                
                # Check if this line completes a clause (ends with period)
                if stripped.endswith('.'):
                    # Join all accumulated lines and remove the period
                    clause_text = ' '.join(current_clause)[:-1].strip()
                    
                    try:
                        # Parse and add the clause
                        term = parse_text(clause_text)
                        
                        # Check if it's a rule or fact
                        if isinstance(term, Compound) and len(term.args) > 0:
                            first_arg = term.args[0]
                            if isinstance(first_arg, Compound) and term.functor == "":
                                # This is a rule (empty functor means rule syntax)
                                head = first_arg
                                body = list(term.args[1:])
                                clause = Clause(head, body)
                            else:
                                # This is a fact
                                clause = Clause(term)
                        else:
                            # This is a fact
                            clause = Clause(term)
                        
                        self.database.add_clause(clause)
                        clause_count += 1
                        
                    except Exception as e:
                        print(f"Warning: Error on line {start_line}: {e}")
                    
                    # Reset for next clause
                    current_clause = []
                    start_line = None
            
            # Warn if there's an incomplete clause at end of file
            if current_clause:
                print(f"Warning: Incomplete clause at end of file (starting line {start_line})")
            
            print(f"Loaded {clause_count} clause(s) from {filename}")
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def _save_file(self, filename: str):
        """Save database to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("% microPROLOG database\n")
                f.write(f"% Saved clauses: {len(self.database)}\n\n")
                
                for clause in self.database:
                    if clause.is_fact():
                        f.write(str(clause.head) + '\n')
                    else:
                        # Write rule in the form: ((head) (body1) (body2) ...)
                        parts = [str(clause.head)] + [str(goal) for goal in clause.body]
                        f.write(f"({' '.join(parts)})\n")
            
            print(f"Saved {len(self.database)} clause(s) to {filename}")
            
        except Exception as e:
            print(f"Error saving file: {e}")
    
    def _show_visualization(self, filename: str):
        """Display visualization of a world file (read-only, doesn't load)."""
        import sys
        import os
        
        # Import the visualizer from world directory if available
        try:
            # Try to import from world subdirectory
            world_dir = os.path.join(os.path.dirname(__file__), 'world')
            if os.path.exists(world_dir):
                sys.path.insert(0, world_dir)
            
            from visualize_world import parse_world_file, visualize_board
            
            # Parse and visualize
            objects = parse_world_file(filename)
            
            if not objects:
                print("No objects found in file (not a Tarski's World file?)")
                return
            
            print(f"\nTarski's World: {filename}")
            print(f"Objects: {len(objects)}")
            visualize_board(objects)
            
        except ImportError:
            print("Error: Visualization requires world/visualize_world.py")
            print("This command only works for Tarski's World files.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error visualizing file: {e}")
        finally:
            # Clean up sys.path
            if world_dir in sys.path:
                sys.path.remove(world_dir)
