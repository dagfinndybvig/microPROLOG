
<img width="144" height="171" alt="skolem" src="https://github.com/user-attachments/assets/42184f92-efdf-4a17-8c3c-90502aaaeac9" /> Thoralf Skolem (1887–1963) 
<img width="144" height="171" alt="amble" src="https://github.com/user-attachments/assets/68a6e2e7-6d56-42a5-b6a2-4a4191713589" /> Tore Amble (1945-2012) 


### This project is in honour of Norwegian mathematician Thoralf Skolem who pioneered the recursive logic that lies behind PROLOG. I would also like to acknowledge the contribution to logic programming and expert systems by Tore Amble of the Norwegian University of Science and Technology, who inspired me as a very young man. I still have his book.


# microPROLOG

A simplified implementation of PROLOG (Programming in Logic) with an interactive Read-Eval-Print Loop (REPL). This implementation uses a clean prefix notation syntax and is designed for educational purposes and logic programming experiments.

A twist of fate is that the present system is implemented with the help of Github Copilot: The very artificial intelligence the creators of PROLOG worked towards but never quite achieved.

But their contribution is not forgotten!

## Table of Contents

- [What is microPROLOG?](#what-is-microprolog)
- [Key Concepts](#key-concepts)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Syntax Guide](#syntax-guide)
- [Commands](#commands)
- [Working with Files](#working-with-files)
- [Tutorial Examples](#tutorial-examples)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Built-in Predicates](#built-in-predicates)
- [Tips and Best Practices](#tips-and-best-practices)
- [Common Patterns](#common-patterns)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Learning Resources](#learning-resources)

---

## What is microPROLOG?

microPROLOG is a simplified dialect of PROLOG (PROgramming in LOGic), a declarative programming language based on formal logic. Unlike imperative languages where you tell the computer *how* to solve a problem step-by-step, in logic programming you describe *what* the problem is, and the system figures out how to solve it.
This implementation corresponds to the "core" version described in Part III of Clark/McCabe:
https://archive.org/details/microprologprogr0000clar/mode/2up

### Basic Ideas

1. **Facts**: Things that are true (e.g., "Tom is Bob's parent")
2. **Rules**: Logical implications (e.g., "X is a grandparent of Z if X is a parent of Y AND Y is a parent of Z")
3. **Queries**: Questions you ask the system (e.g., "Who are Tom's children?")
4. **Inference**: The system uses logical reasoning to derive answers from facts and rules

The system automatically handles:
- **Unification**: Matching patterns and binding variables
- **Backtracking**: Finding all possible solutions by exploring alternatives

---

## Key Concepts

### Facts

Facts are simple statements about the world. They have no conditions attached.

```
(parent tom bob)     % Tom is Bob's parent
(age tom 45)         % Tom's age is 45
```

### Rules

Rules define relationships based on conditions. They have the form:
```
((conclusion) (condition1) (condition2) ...)
```

The first element is what you conclude, and the remaining elements are conditions that must be true.

```
((grandparent X Z) (parent X Y) (parent Y Z))
% X is a grandparent of Z if:
%   - X is a parent of Y, AND
%   - Y is a parent of Z
```

### Variables

Variables represent unknown values that the system will try to find.

- **Start with uppercase**: `X`, `Y`, `Person`, `Age`
- **Or underscore**: `_`, `_temp`

**Important**: Lowercase identifiers are **atoms** (constants), not variables!
- `X` is a variable
- `x` is an atom (the constant "x")

### Queries

Queries ask questions. Prefix them with `?` in the REPL.

```
? (parent tom X)
% "Who is Tom's child?"
% Answer: X = bob

? (parent X bob)
% "Who is Bob's parent?"
% Answer: X = tom
```

### Backtracking

When multiple solutions exist, the system can find them all through backtracking.

```
? (parent tom X)
X = bob
; (press Enter for next solution)
X = mary
; (press Enter)
no more solutions
```

---

## Installation

### Requirements

- **Python 3.7 or higher** (Python 3.12 recommended)
- No external dependencies (uses only Python standard library)

### Install Python

**Windows (Microsoft Store)**:
1. Open Microsoft Store
2. Search for "Python 3.12"
3. Click "Get" or "Install"

**Other platforms**: Download from [python.org](https://www.python.org/downloads/)

### Verify Installation

```bash
python --version
```

Should show Python 3.7 or higher.

---

## Getting Started

### Starting microPROLOG

1. Open a terminal/command prompt
2. Navigate to the microPROLOG directory:
   ```bash
   cd C:\Users\YourName\Coding\microPROLOG
   ```
3. Run the system:
   ```bash
   python main.py
   ```

You should see:
```
microPROLOG v1.0
Type 'help' for commands, 'quit' to exit

&-
```

The `&-` is the prompt where you enter commands.

### Starting with a File

You can automatically load a file on startup by providing it as a command line argument:

```bash
python main.py family.pl
```

This will load the file and then start the REPL:
```
microPROLOG v1.0
Loading family.pl...

Loaded 7 clause(s) from family.pl

microPROLOG v1.0
Type 'help' for commands, 'quit' to exit

&-
```

### Your First Session

Try this simple example (type each line after the `&-` prompt):

```
&- (parent tom bob).
ok

&- (parent bob ann).
ok

&- ? (parent tom X)
X = bob
; (press Enter to continue, or type 'n' to stop)
no more solutions

&- quit
Goodbye!
```

**Note**: Facts and rules must end with a period (`.`), but queries start with `?` and don't need one.

Congratulations! You just:
1. Added two facts to the database
2. Queried to find Tom's children
3. Exited the system

---

## Syntax Guide

### General Rules

- Use **parentheses** for compound terms: `(predicate arg1 arg2 ...)`
- Use **spaces** to separate elements
- **Variables** start with uppercase or underscore: `X`, `Person`, `_temp`
- **Atoms** start with lowercase: `tom`, `parent`, `age`
- **Numbers** are recognized: `42`, `3.14`
- **Comments** start with `%`: `% This is a comment`

### Facts

Simple assertions with no conditions. **Must end with a period (`.`)**:

```
(parent tom bob).
(likes mary pizza).
(age john 25).
```

### Rules

Format: `((head) (body1) (body2) ...).` **Must end with a period (`.`)**:

```
((grandparent X Z) (parent X Y) (parent Y Z)).

((sibling X Y) (parent P X) (parent P Y)).

((ancestor X Y) (parent X Y)).
((ancestor X Z) (parent X Y) (ancestor Y Z)).
```

**Reading a rule**:
```
((grandparent X Z) (parent X Y) (parent Y Z)).
```
Means: "X is a grandparent of Z if X is a parent of Y AND Y is a parent of Z"

**Important**: The period (`.`) at the end is required to add the clause to the database.

### Queries

Start with `?` and use the same syntax as facts. **No period needed**:

```
? (parent tom X)           % Who are Tom's children?
? (parent X bob)           % Who is Bob's parent?
? (grandparent tom X)      % Who are Tom's grandchildren?
? (ancestor X mary)        % Who are Mary's ancestors?
```

**Conjunction queries** - multiple goals can be combined:

```
? (parent tom X) (parent X Y)              % Tom's grandchildren
? (parent X mary) (parent X bob)           % Who is parent of both Mary and Bob?
? (parent A B) (parent B C) (parent C D)   % Three generations
```

The system will find values for all variables that satisfy ALL the goals together.

### Lists

Lists use square brackets and support powerful pattern matching:

```
[1 2 3]              % Simple list
[]                   % Empty list
[X Y Z]              % List with variables
[H | T]              % List with head and tail (H is first element, T is rest)
[1 2 | Rest]         % Multiple elements before tail
```

**Pattern matching examples:**
```
? (= [H | T] [a b c])
H = a
T = [b c]

? (= [First Second | Rest] [1 2 3 4])
First = 1
Second = 2
Rest = [3 4]
```

---

## Commands

### Database Commands

- **Add a fact**: Type it with a period at the end
  ```
  &- (parent tom bob).
  ok
  ```

- **Add a rule**: Use the `((head) body...).` format with a period
  ```
  &- ((grandparent X Z) (parent X Y) (parent Y Z)).
  ok
  ```

- **Query**: Start with `?`
  ```
  &- ? (parent tom X)
  X = bob
  ```

- **listing**: Show all clauses in the database
  ```
  &- listing
  (parent tom bob)
  (parent bob ann)
  ((grandparent X Z) (parent X Y) (parent Y Z))
  ```

- **clear**: Remove all clauses from database
  ```
  &- clear
  Database cleared
  ```

- **consult <filename>** or **load <filename>**: Load clauses from a file
  ```
  &- consult family.pl
  Loaded 7 clause(s) from family.pl
  ```

- **save <filename>**: Save current database to a file
  ```
  &- save my_facts.pl
  Saved 7 clause(s) to my_facts.pl
  ```

### System Commands

- **help**: Show available commands
  ```
  &- help
  ```

- **quit** or **exit**: Exit microPROLOG
  ```
  &- quit
  Goodbye!
  ```

### During Queries

When a query has multiple solutions:

- **Press Enter**: Show next solution
- **Type 'n' or 'N'**: Stop showing solutions
- **Ctrl+C**: Interrupt the query

---

## Working with Files

### Creating Source Files

You can create microPROLOG source files (conventionally with `.pl` extension) in any text editor:

**Example: family.pl**
```prolog
% Family tree example
% Facts about parent relationships

(parent tom bob).
(parent tom mary).
(parent bob ann).
(parent bob pat).
(parent mary jim).

% Rules for derived relationships

((grandparent X Z) (parent X Y) (parent Y Z)).
((sibling X Y) (parent P X) (parent P Y)).
```

**Note**: In files, periods are optional but recommended for consistency with REPL usage.

### Loading Files

Use `consult` or `load` to load a file:

```
&- consult family.pl
Loaded 7 clause(s) from family.pl
```

The system will:
- Read each clause from the file
- Skip blank lines and comments (lines starting with `%`)
- Add all valid clauses to the database
- Report how many clauses were loaded

### Saving Your Work

Save your current database to a file:

```
&- save my_work.pl
Saved 10 clause(s) to my_work.pl
```

The saved file will include:
- A header comment with metadata
- All facts and rules in the current database
- Proper formatting for reloading later

### Workflow Example

1. **Start with a file:**
   ```
   &- consult family.pl
   Loaded 7 clause(s) from family.pl
   ```

2. **Add more facts interactively:**
   ```
   &- (parent pat sue).
   ok
   ```

3. **Test your queries:**
   ```
   &- ? (grandparent tom X)
   X = ann
   ; (press Enter)
   X = pat
   ```

4. **Save everything:**
   ```
   &- save family_extended.pl
   Saved 8 clause(s) to family_extended.pl
   ```

5. **Next session - reload:**
   ```
   &- consult family_extended.pl
   Loaded 8 clause(s) from family_extended.pl
   ```

---

## Tutorial Examples

### Example 1: Family Tree

Build a simple family tree and query relationships.

```
&- (parent tom bob).
ok
&- (parent tom mary).
ok
&- (parent bob ann).
ok
&- (parent bob pat).
ok
&- (parent mary jim).
ok

&- ? (parent tom X)
X = bob
; (press Enter)
X = mary
; (press Enter)
no more solutions

&- ((grandparent X Z) (parent X Y) (parent Y Z)).
ok

&- ? (grandparent tom X)
X = ann
; (press Enter)
X = pat
; (press Enter)
X = jim
; (press Enter)
no more solutions

&- ((sibling X Y) (parent P X) (parent P Y)).
ok

&- ? (sibling X Y)
X = bob
Y = bob
; (type 'n' to skip reflexive results and continue exploring...)
```

### Example 2: Ancestor Relationship

Define ancestor as a recursive relationship.

```
&- (parent alice bob).
ok
&- (parent bob charlie).
ok
&- (parent charlie diana).
ok

&- ((ancestor X Y) (parent X Y)).
ok
&- ((ancestor X Z) (parent X Y) (ancestor Y Z)).
ok

&- ? (ancestor alice X)
X = bob
; (press Enter)
X = charlie
; (press Enter)
X = diana
; (press Enter)
no more solutions

&- ? (ancestor X diana)
X = charlie
; (press Enter)
X = bob
; (press Enter)
X = alice
; (press Enter)
no more solutions
```

### Example 3: Lists with Pattern Matching

Lists support powerful pattern matching with `[H | T]` notation.

```
&- ((first L H) (= L [H | T])).
ok
&- ((rest L T) (= L [H | T])).
ok

&- ? (first [a b c] X)
X = a
; 
no more solutions

&- ? (rest [1 2 3] X)
X = [2 3]
;
no more solutions

&- ? (= [H | T] [1 2 3 4])
H = 1
T = [2 3 4]
```

---

## Project Structure

```
microPROLOG/
├── main.py                  # Entry point - run this to start
├── terms.py                 # Core data structures (Atom, Variable, Compound, List)
├── parser.py                # Tokenizer and parser for microPROLOG syntax
├── unification.py           # Unification algorithm with occurs check
├── database.py              # Clause storage and retrieval
├── inference.py             # Inference engine with SLD resolution and backtracking
├── builtin_predicates.py   # Built-in predicates (=, is, atom, number, etc.)
├── repl.py                  # Interactive Read-Eval-Print Loop
├── test_implementation.py  # Automated test suite
├── example_session.txt     # Example session walkthrough
├── PLAN.md                 # Detailed implementation plan
└── README.md               # This file
```

### File Descriptions

- **main.py**: The program entry point. Run `python main.py` to start.
- **terms.py**: Defines the internal representation of logic terms using Python dataclasses.
- **parser.py**: Converts text input into internal term structures.
- **unification.py**: Implements the pattern-matching algorithm that binds variables.
- **database.py**: Stores facts and rules, with indexing for efficient retrieval.
- **inference.py**: The core reasoning engine using SLD resolution and backtracking via Python generators.
- **builtin_predicates.py**: Built-in operations like unification (`=`) and type checking.
- **repl.py**: The interactive shell that handles user input and displays results.

---

## Technical Details

### Architecture

This implementation follows a classic Prolog architecture:

1. **Parser**: Converts text input into abstract syntax trees (terms)
2. **Unification**: Matches patterns and creates variable bindings
3. **Inference Engine**: Uses SLD resolution (Selective Linear Definite clause resolution) with depth-first search
4. **Backtracking**: Implemented using Python generators (`yield`) for lazy evaluation

### Unification Algorithm

Unification is the process of making two terms equal by finding variable bindings:

- `(parent X bob)` unifies with `(parent tom bob)` by binding `X = tom`
- Includes **occurs check** to prevent infinite structures

### SLD Resolution

The inference engine works backward from the goal:

1. Start with a query goal
2. Find a clause whose head unifies with the goal
3. Replace the goal with the clause body
4. Repeat until no goals remain (success) or no clauses match (failure)
5. Use backtracking to explore alternative clause choices

### Backtracking Implementation

Uses Python generators for efficient backtracking:

```python
def solve(goals):
    if not goals:
        yield solution  # Success
    else:
        for clause in database:
            if unifies(goal, clause.head):
                yield from solve(clause.body + remaining_goals)
```

This allows lazy evaluation - solutions are generated on-demand.

---

## Built-in Predicates

microPROLOG has 6 built-in predicates that work both in direct queries and inside rules:

- **`(= X Y)`**: Unify X and Y (pattern matching)
- **`(is X Expr)`**: Evaluate arithmetic expression (supports +, -, *, /)
- **`(atom X)`**: Check if X is an atom
- **`(number X)`**: Check if X is a number
- **`(var X)`**: Check if X is an unbound variable
- **`(nonvar X)`**: Check if X is not an unbound variable

### Examples

```
&- ? (= [1 2 3] [X Y Z])
X = 1, Y = 2, Z = 3

&- ((double X Result) (is Result (* X 2))).
ok
&- ? (double 7 X)
X = 14

&- ? (atom tom)
yes

&- ? (number 42)
yes
```


### List Operations

Lists don't require built-in predicates - they work through pattern matching:

```
&- ((member X [X | T])).
ok
&- ((member X [H | T]) (member X T)).
ok

&- ((append [] L L)).
ok
&- ((append [H | T1] L2 [H | T3]) (append T1 L2 T3)).
ok

&- ? (append [1 2] [3 4] X)
X = [1 2 3 4]
```

---

## Tips and Best practices

1. **Variable Names**: Use descriptive names for clarity
   - Good: `Person`, `Age`, `Result`
   - Less clear: `X`, `Y`, `Z` (but fine for short examples)

2. **Rule Order**: Rules are tried in the order they're defined
   - Put base cases before recursive cases
   - More specific rules before general ones

3. **Infinite Loops**: Be careful with recursive rules
   - Example of problematic rule: `((loop X) (loop X))`
   - The system has a depth limit (1000) to prevent stack overflow

4. **Testing**: Build incrementally
   - Add facts first
   - Test with simple queries
   - Then add rules
   - Test rules separately

5. **Debugging**: Use `listing` to see what's in the database

---

## Common Patterns

### Recursive Definitions

Many relationships are naturally recursive:

```
% Base case: direct parent relationship
((ancestor X Y) (parent X Y)).

% Recursive case: ancestor through intermediate
((ancestor X Z) (parent X Y) (ancestor Y Z)).
```

### Multiple Rules for Same Predicate

You can have multiple rules with the same head:

```
((sibling X Y) (parent P X) (parent P Y)).
((sibling X Y) (mother M X) (mother M Y)).
((sibling X Y) (father F X) (father F Y)).
```

The system will try all matching rules.

---

## Features

### ✅ Fully Implemented

- **Core Logic Programming**
  - Facts and rules
  - Queries with backtracking
  - Pattern matching and unification
  - SLD resolution inference engine
  - Depth-first search with occurs check

- **Data Types**
  - Atoms (strings and lowercase identifiers)
  - Numbers (integers and floats)
  - Variables (uppercase or underscore-prefixed)
  - Compound terms with arbitrary nesting
  - Lists with `[H | T]` pattern matching

- **Built-in Predicates**
  - Unification: `(= X Y)`
  - Arithmetic: `(is X Expr)` with +, -, *, /
  - Type checking: `(atom X)`, `(number X)`, `(var X)`, `(nonvar X)`
  - All built-ins work in rules and direct queries

- **File I/O**
  - Load files: `consult` or `load`
  - Save database: `save`
  - Standard `.pl` file format

- **Interactive REPL**
  - Command history
  - Solution navigation (Enter/n)
  - Database listing
  - Clear database
  - Helpful error messages

### 🔨 Future Extensions

- Arithmetic comparison operators (<, >, =<, >=)
- Assert/retract for dynamic modification
- Trace mode for debugging
- Cut (!) operator
- Negation as failure (\+)

---

## Troubleshooting

### "Parser error"
- Check your parentheses are balanced
- Ensure spaces between elements
- Variables must start with uppercase

### "No solutions" when you expect some
- Use `listing` to check what's in the database
- Verify variable names (case matters!)
- Try simpler queries first

### Query seems to hang
- Likely an infinite loop in a recursive rule
- Press Ctrl+C to interrupt
- Review your recursive rules

### ImportError on startup
- Ensure all files are in the same directory
- Check Python version is 3.7+
- Verify no files are named `builtins.py` (conflicts with Python built-in)

---

## Learning Resources

### Next Steps

1. Try the examples in this README
2. Build your own family tree or knowledge base
3. Experiment with recursive rules
4. Try modeling other relationships (friendships, hierarchies, etc.)

### Further Reading


<img width="304" height="402" alt="logic" src="https://github.com/user-attachments/assets/45d84bbf-bead-41de-9af6-5b87e5c0fd32" />

- **Logic Programming And Knowledge Engineering** by Tore Amble
- **micro-PROLOG: Programming in Logic** by Clark and McCabe
- **The Art of Prolog** by Sterling and Shapiro
- **Programming in Prolog** by Clocksin and Mellish
- **Learn Prolog Now!** (free online book)

---

## License

This is an educational implementation created for learning purposes.

---

## Contributing

This implementation can be extended with:

- Arithmetic comparison operators (<, >, =<, >=)
- Assert/retract for dynamic database modification (partially done with `clear`)
- Trace mode for debugging
- Cut (!) operator for controlling backtracking
- Negation as failure (\+)
- More sophisticated indexing for faster clause retrieval

---

## Acknowledgments

microPROLOG is based on the simplified Prolog dialect developed by Keith Clark and colleagues at Imperial College London in the 1980s. This implementation follows the educational philosophy of making logic programming accessible through clear syntax and interactive exploration.

---

**Happy Logic Programming!** 🎉

For questions or issues, refer to the code documentation in each Python file or experiment in the REPL.
