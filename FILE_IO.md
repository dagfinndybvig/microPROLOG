# File I/O Features - Quick Reference

## Commands

### Loading Files
```
consult <filename>    % Load clauses from file
load <filename>       % Same as consult
```

### Saving Files
```
save <filename>       % Save current database to file
```

## File Format

microPROLOG source files use `.pl` extension (Prolog standard).

### Example file content:
```prolog
% This is a comment

(parent tom bob)
(parent bob ann)

((grandparent X Z) (parent X Y) (parent Y Z))
```

### File conventions:
- Comments start with `%`
- One clause per line
- Blank lines are ignored
- Facts: `(predicate arg1 arg2)`
- Rules: `((head) (body1) (body2) ...)`

## Usage Examples

### Example 1: Load existing knowledge base
```
&- consult family.pl
Loaded 7 clause(s) from family.pl

&- ? (parent tom X)
X = bob
```

### Example 2: Build and save
```
&- (parent tom bob)
ok
&- (parent bob ann)
ok
&- ((grandparent X Z) (parent X Y) (parent Y Z))
ok

&- save my_rules.pl
Saved 3 clause(s) to my_rules.pl
```

### Example 3: Extend existing file
```
&- consult family.pl
Loaded 7 clause(s) from family.pl

&- (parent pat sue)
ok

&- save family_extended.pl
Saved 8 clause(s) to family_extended.pl
```

## Example Files Included

- **family.pl** - Family tree with grandparent rules
- **examples/ancestors.pl** - Recursive ancestor relationships

## Tips

1. **Always save before quitting** if you want to preserve your work
2. **Use descriptive filenames** like `family.pl`, `rules.pl`
3. **Add comments** to document your logic
4. **One database at a time**: Loading a new file adds to current database
5. **Use `clear` first**: If you want to replace database completely:
   ```
   &- clear
   &- consult new_file.pl
   ```
