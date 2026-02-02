"""
Test script to validate microPROLOG implementation without running REPL.
This simulates the example session from example_session.txt.
"""
from terms import Atom, Variable, Compound
from parser import parse_text
from database import Database, Clause
from inference import InferenceEngine
from unification import Substitution

def test_basic_functionality():
    """Test basic facts, rules, and queries."""
    
    print("=== Testing microPROLOG Implementation ===\n")
    
    # Initialize database and engine
    db = Database()
    engine = InferenceEngine(db)
    
    # Test 1: Add a fact - (parent tom bob)
    print("Test 1: Adding fact (parent tom bob)")
    fact1 = parse_text("(parent tom bob)")
    db.add_clause(Clause(fact1))
    print(f"  Parsed: {fact1}")
    print(f"  Database size: {len(db)}")
    print("  ✓ OK\n")
    
    # Test 2: Add another fact - (parent bob ann)
    print("Test 2: Adding fact (parent bob ann)")
    fact2 = parse_text("(parent bob ann)")
    db.add_clause(Clause(fact2))
    print(f"  Parsed: {fact2}")
    print(f"  Database size: {len(db)}")
    print("  ✓ OK\n")
    
    # Test 3: Query - ? (parent tom X)
    print("Test 3: Query (parent tom X)")
    query1 = parse_text("(parent tom X)")
    print(f"  Query: {query1}")
    solutions = list(engine.query(query1))
    print(f"  Solutions found: {len(solutions)}")
    for i, subst in enumerate(solutions):
        x_value = subst.apply(Variable("X"))
        print(f"    Solution {i+1}: X = {x_value}")
    assert len(solutions) == 1
    assert str(subst.apply(Variable("X"))) == "bob"
    print("  ✓ OK\n")
    
    # Test 4: Add a rule - ((grandparent X Z) (parent X Y) (parent Y Z))
    print("Test 4: Adding rule ((grandparent X Z) (parent X Y) (parent Y Z))")
    rule_term = parse_text("((grandparent X Z) (parent X Y) (parent Y Z))")
    print(f"  Parsed: {rule_term}")
    
    # Parse as rule: first arg is head, rest are body
    head = rule_term.args[0]
    body = list(rule_term.args[1:])
    rule = Clause(head, body)
    db.add_clause(rule)
    print(f"  Head: {head}")
    print(f"  Body: {body}")
    print(f"  Database size: {len(db)}")
    print("  ✓ OK\n")
    
    # Test 5: Query using rule - ? (grandparent tom X)
    print("Test 5: Query (grandparent tom X)")
    query2 = parse_text("(grandparent tom X)")
    print(f"  Query: {query2}")
    solutions = list(engine.query(query2))
    print(f"  Solutions found: {len(solutions)}")
    for i, subst in enumerate(solutions):
        x_value = subst.apply(Variable("X"))
        print(f"    Solution {i+1}: X = {x_value}")
    assert len(solutions) == 1
    assert str(subst.apply(Variable("X"))) == "ann"
    print("  ✓ OK\n")
    
    # Test 6: Add more facts for multiple solutions
    print("Test 6: Adding more facts")
    fact3 = parse_text("(parent tom mary)")
    fact4 = parse_text("(parent bob jane)")
    db.add_clause(Clause(fact3))
    db.add_clause(Clause(fact4))
    print(f"  Added: {fact3}")
    print(f"  Added: {fact4}")
    print(f"  Database size: {len(db)}")
    print("  ✓ OK\n")
    
    # Test 7: Query with multiple solutions
    print("Test 7: Query (grandparent tom X) - should have 2 solutions")
    query3 = parse_text("(grandparent tom X)")
    solutions = list(engine.query(query3))
    print(f"  Solutions found: {len(solutions)}")
    for i, subst in enumerate(solutions):
        x_value = subst.apply(Variable("X"))
        print(f"    Solution {i+1}: X = {x_value}")
    assert len(solutions) == 2
    results = [str(subst.apply(Variable("X"))) for subst in solutions]
    assert "ann" in results
    assert "jane" in results
    print("  ✓ OK\n")
    
    # Test 8: Listing database
    print("Test 8: Listing database")
    print("  Clauses in database:")
    for clause in db:
        if clause.is_fact():
            print(f"    {clause.head}")
        else:
            parts = [str(clause.head)] + [str(goal) for goal in clause.body]
            print(f"    ({' '.join(parts)})")
    print("  ✓ OK\n")
    
    # Test 9: Query that fails
    print("Test 9: Query (parent ann X) - should fail")
    query4 = parse_text("(parent ann X)")
    solutions = list(engine.query(query4))
    print(f"  Solutions found: {len(solutions)}")
    assert len(solutions) == 0
    print("  Result: no")
    print("  ✓ OK\n")
    
    print("=== All tests passed! ===")

if __name__ == "__main__":
    test_basic_functionality()
