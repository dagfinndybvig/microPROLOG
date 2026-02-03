% Alternative factorial without cut but with guard
% Demonstrates that guards can replace cut for deterministic predicates

% Base case: factorial of 0 is 1
% No cut needed - the guard in recursive case prevents overlap
((fact2 0 1)).

% Recursive case: fact2(N) = N * fact2(N-1) for N > 0
% Guard (> N 0) ensures this only applies when N is positive
((fact2 N Result)
  (> N 0)
  (is N1 (- N 1))
  (fact2 N1 R1)
  (is Result (* N R1))).

% Example queries:
% ? (fact2 5 X)
% X = 120
%
% ? (fact2 0 X)
% X = 1
%
% ? (fact2 10 X)
% X = 3628800
%
% This version is more declarative than using cut
% The guard makes the logic explicit rather than relying on clause ordering
