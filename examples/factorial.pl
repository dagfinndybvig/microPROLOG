% Factorial computation using recursion
% Demonstrates arithmetic, comparison, and cut operators

% Base case: factorial of 0 is 1
% Cut prevents backtracking once we match N = 0
((fact 0 1) !).

% Recursive case: fact(N) = N * fact(N-1)
% Only tries this if N > 0 (first clause didn't match)
((fact N Result) (> N 0) (is N1 (- N 1)) (fact N1 R1) (is Result (* N R1))).

% Example queries:
% ? (fact 5 X)
% X = 120
%
% ? (fact 0 X)
% X = 1
%
% ? (fact 10 X)
% X = 3628800
