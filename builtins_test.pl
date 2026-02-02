% Built-in Predicates Test Suite for microPROLOG
% Load this file with: consult builtins_test.pl
% Then run the test queries shown below

% ===== Test Data =====

% Some facts for testing
(value five 5)
(value ten 10)
(name person tom)
(name person mary)

% ===== Test Rules Using Built-ins =====

% Rule 1: Check if something is a valid number value
((isNumberValue X) (value X Y) (number Y))

% Rule 2: Check if something is a name
((isName X) (name person X) (atom X))

% Rule 3: Compute double of a number
((double X Result) (is Result (* X 2)))

% Rule 4: Compute sum of two stored values
((sumOf Name1 Name2 Result) 
 (value Name1 V1) 
 (value Name2 V2) 
 (is Result (+ V1 V2)))

% Rule 5: Check if result of calculation is bound
((calcBound X Result)
 (is Result (+ X 10))
 (nonvar Result))

% Rule 6: Check if input is unbound variable
((testVar X) (var X))

% ===== TESTS TO RUN IN REPL =====

% After loading this file, try these queries:

% TEST 1: Unification (=)
% &- ? (= 5 5)
% Expected: yes

% &- ? (= X tom)
% Expected: X = tom

% &- ? (= (parent X bob) (parent tom Y))
% Expected: X = tom, Y = bob

% TEST 2: Arithmetic (is)
% &- ? (is X (+ 3 4))
% Expected: X = 7

% &- ? (is Result (* 5 6))
% Expected: Result = 30

% &- ? (is Z (- 20 8))
% Expected: Z = 12

% &- ? (is W (/ 15 3))
% Expected: W = 5

% &- ? (is Complex (+ (* 3 4) (- 10 5)))
% Expected: Complex = 17

% TEST 3: Using arithmetic in rules
% &- ? (double 7 X)
% Expected: X = 14

% &- ? (sumOf five ten X)
% Expected: X = 15

% TEST 4: Type checking - atom
% &- ? (atom tom)
% Expected: yes

% &- ? (atom 42)
% Expected: no

% &- ? (isName tom)
% Expected: yes

% TEST 5: Type checking - number
% &- ? (number 42)
% Expected: yes

% &- ? (number 3.14)
% Expected: yes

% &- ? (number tom)
% Expected: no

% &- ? (isNumberValue five)
% Expected: yes

% TEST 6: Variable checking - var
% &- ? (var X)
% Expected: yes

% &- ? (var 5)
% Expected: no

% &- ? (testVar X)
% Expected: yes

% &- ? (testVar tom)
% Expected: no

% TEST 7: Variable checking - nonvar
% &- ? (nonvar tom)
% Expected: yes

% &- ? (nonvar 42)
% Expected: yes

% &- ? (nonvar X)
% Expected: no

% &- ? (calcBound 5 X)
% Expected: X = 15

% TEST 8: Nested arithmetic
% &- ? (is X (/ (+ 10 20) (- 6 3)))
% Expected: X = 10

% TEST 9: All built-ins together
% &- ((testAll X Y Z) 
%     (= X 10) 
%     (is Y (+ X 5)) 
%     (number Y) 
%     (nonvar Y) 
%     (is Z (* Y 2)))
% ok
% &- ? (testAll X Y Z)
% Expected: X = 10, Y = 15, Z = 30
