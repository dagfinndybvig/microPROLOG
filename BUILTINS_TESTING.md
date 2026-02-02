# Built-in Predicates Test Guide

## Status

✅ **Built-in predicates now work both in direct queries AND inside rules!** The inference engine has been updated to evaluate built-ins during goal resolution.

## How to Test Built-in Predicates in the REPL

Start the REPL: `python main.py`

## TEST 1: Unification `(=)`

```
&- ? (= 5 5)
Expected: yes

&- ? (= tom tom)
Expected: yes

&- ? (= tom mary)
Expected: no
```

## TEST 2: Arithmetic Evaluation `(is)`

**Note**: The `(is)` predicate shows "yes" but doesn't display the result. This is a limitation in how built-ins are displayed.

```
&- ? (is X (+ 3 4))
Expected: yes (X is bound to 7, but not displayed)

&- ? (is Result (* 5 6))
Expected: yes (Result = 30)

&- ? (is Z (- 20 8))
Expected: yes (Z = 12)

&- ? (is W (/ 15 3))
Expected: yes (W = 5)
```

### Nested arithmetic:
```
&- ? (is X (+ (* 3 4) (- 10 5)))
Expected: yes (X = 17: 3*4=12, 10-5=5, 12+5=17)

&- ? (is Y (/ (+ 10 20) (- 6 3)))
Expected: yes (Y = 10: 10+20=30, 6-3=3, 30/3=10)
```

## TEST 3: Type Checking `(atom)`

```
&- ? (atom tom)
Expected: yes

&- ? (atom mary)
Expected: yes

&- ? (atom 42)
Expected: no (42 is a number, not an atom)

&- ? (atom X)
Expected: no (X is a variable)
```

## TEST 4: Type Checking `(number)`

```
&- ? (number 42)
Expected: yes

&- ? (number 3.14)
Expected: yes

&- ? (number tom)
Expected: no (tom is an atom)

&- ? (number X)
Expected: no (X is a variable)
```

## TEST 5: Variable Testing `(var)`

```
&- ? (var X)
Expected: yes (X is unbound)

&- ? (var tom)
Expected: no (tom is an atom)

&- ? (var 5)
Expected: no (5 is a number)
```

## TEST 6: Non-Variable Testing `(nonvar)`

```
&- ? (nonvar tom)
Expected: yes

&- ? (nonvar 42)
Expected: yes

&- ? (nonvar X)
Expected: no (X is unbound)
```

## Examples

### ✅ Built-ins Work in Rules

This now works correctly:
```
&- ((double X Result) (is Result (* X 2)))
ok
&- ? (double 5 X)
X = 10  ← Works! Built-ins are evaluated in rules
```

Complex example chaining predicates:
```
&- (value five 5)
ok
&- ((doubleValue X Y) (value X V) (double V Y))
ok
&- ? (doubleValue five X)
X = 10  ← Chains normal predicates with built-ins
```

### ✅ Built-ins Work Directly

Direct queries also work:
```
&- ? (is X (* 5 2))
yes  ← X is bound to 10 internally
```

## Summary of Built-ins

| Predicate | Purpose | Example |
|-----------|---------|---------|
| `(= X Y)` | Unify X and Y | `? (= tom tom)` |
| `(is X Expr)` | Evaluate arithmetic | `? (is X (+ 3 4))` |
| `(atom X)` | Check if atom | `? (atom tom)` |
| `(number X)` | Check if number | `? (number 42)` |
| `(var X)` | Check if unbound variable | `? (var X)` |
| `(nonvar X)` | Check if not unbound variable | `? (nonvar tom)` |

## Operators Supported in `(is)`

- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division

All operators are binary (take exactly 2 arguments).
