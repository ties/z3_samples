"""
Simple trick with digits.

https://www.volkskrant.nl/nieuws-achtergrond/elke-goochelaar-heeft-een-kast-vol-ongebruikte-trucs-liggen~b0aafe5a/

DE GETALLENTRUC
Laat drie toeschouwers om de beurt een willekeurig cijfer noemen (bijvoorbeeld
4, 2, 9) en schrijf die op: 429. Draai de cijfers om: 924. Trek het laagste
getal af van het hoogste: 924 – 429 = 495. Draai dat getal ook om: 594. Tel de
twee laatste getallen bij elkaar op. Welke drie eerste getallen je ook kiest,
als je het goed doet, zal de uitkomst altijd 1089 zijn, zegt Douwe Swierstra.
‘Het werkt het altijd.’

Works iff digits are distinct and > 0.
"""
import functools
from typing import Union

from z3 import And, ArithRef, Distinct, Int, If, Solver


def as_number(*digits: Union[Int, ArithRef]) -> ArithRef:
    """Return separate digits as argument as one number"""
    return functools.reduce(lambda x, y: 10*x + y, digits)


def symbolic_min(*args: Union[Int, ArithRef]) -> ArithRef:
    """Minimum of Z3 Int/ArithRef's."""
    return functools.reduce(lambda x, y: If(x < y, x, y), args)


def symbolic_max(*args: Union[Int, ArithRef]) -> ArithRef:
    """Maximumum of Z3 Int/ArithRef's"""
    return functools.reduce(lambda x, y: If(x > y, x, y), args)


def digit_at_pos(number: Union[Int, ArithRef], pos: int) -> ArithRef:
    """
    Get the digit at position `pos` in a number.

    Implicit floor division, // not available.

    pos: position, counting from the final position, starting at 0
    """
    return (number / 10**pos) % 10


def main():
    s = Solver()

    X = Int('X')
    Y = Int('Y')
    Z = Int('Z')

    # X, Y, Z: 1-9
    s.add(*[And(cur >= 1, cur <= 9) for cur in (X, Y, Z)])
    s.add(Distinct(X, Y, Z))

    given_number = as_number(X, Y, Z)
    reversed_number = as_number(Z, Y, X)

    high_min_low = symbolic_max(given_number, reversed_number) - symbolic_min(given_number, reversed_number)

    high_min_low_rev = as_number(digit_at_pos(high_min_low, 0),
                                 digit_at_pos(high_min_low, 1),
                                 digit_at_pos(high_min_low, 2))

    s.push()
    # Check that it always holds/there is no counterexample:
    total = high_min_low + high_min_low_rev
    s.add(total != 1089)
    res = s.check()

    if res.r == -1:
        print("unsat -> it holds. Example:")
        s.pop()
        s.add(total == 1089)
        s.check()

        mod = s.model()

        print(f"given number: {mod.eval(given_number)}")
        print(f"reversed: {mod.eval(reversed_number)}")
        print(f"highest - lowest: {mod.eval(high_min_low)}, reversed: {mod.eval(high_min_low_rev)}")
        print(f"sums to: {mod.eval(total)}")
    else:
        print("sat.")
        print(s.model())


if __name__ == '__main__':
    main()
