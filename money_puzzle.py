"""
SEND + MORE = MONEY puzzle

http://mathforum.org/library/drmath/view/60417.html
"""
from z3 import *
from typing import Dict

s = Solver()

# Dictionary from char to Z3 int
chars = { k: Int(k) for k in set('SENDMOREMONEY') }

def str_to_var(char_mapping: Dict[string, Int], chars: str) -> Int:
    """
    Return the z3 Int's for the given charaters, to the power implied by their
	position in the string

	(Using reverse iterator by [::-1] slice
    """
    for idx, c in enumerate(chars[::-1]):
        yield (10**idx) * char_mapping[c]

# Instantiate the z3 optimizer
s = Optimize()
# All chars are in range 0...9
s.add(*[And(0 <= k, k <= 9) for k in chars.values()])
# S & M > 0
s.add(chars['S'] > 0)
s.add(chars['M'] > 0)
# All variables are different
s.add(Distinct(*chars.values()))

# Add the calculation
s.add(Sum(*str_to_var(chars, 'SEND'))
    + Sum(*str_to_var(chars, 'MORE'))
  == Sum(*str_to_var(chars, 'MONEY'))
)

# Lowest total assignment
s.minimize(Sum(*str_to_var(chars, 'MONEY')))

# Satisfiable?
if s.check():
    print(s.model())
