% Simple test file for built-ins in rules
% Each rule must be on a single line

(value five 5)
(value ten 10)

((double X Result) (is Result (* X 2)))
((add X Y Result) (is Result (+ X Y)))
((isEven X) (is Remainder (- X (* (/ X 2) 2))) (= Remainder 0))
