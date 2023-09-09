#
# Math olympiad question:
# find integers a, b, c so that
#     a*b + c == 2020
# and a + b*c == 2021
# hold.
# 
# https://www.youtube.com/watch?v=is1vWnLsXJc
#
from z3 import And, ArithRef, Distinct, Int, If, Solver

a,  b, c = Int('a'), Int('b'), Int('c')

s = Solver()
s.add(a*b + c == 2020)
s.add(a + b*c == 2021)
res = s.check()

print(res)
model = s.model()
print(model)

# Now remove the trivial/current solution

s.add(And(a !=model[a], b != model[b], c != model[c]))
print(s.check())
model = s.model()
print(model)

# No further solutions
s.add(And(a !=model[a], b != model[b], c != model[c]))
print(s.check())