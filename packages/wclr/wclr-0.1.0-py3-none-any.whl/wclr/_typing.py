import decimal
import fractions
import numbers
import sys
from typing import Union

if sys.version_info < (3, 9):
    from typing import Iterator  # noqa: F401
    from typing import Tuple
else:
    from builtins import tuple as Tuple
    from collections.abc import Iterator  # noqa: F401


FractionLike = Union[numbers.Rational, float, decimal.Decimal, str]

ThreeTupleColor = Tuple[
    fractions.Fraction,
    fractions.Fraction,
    fractions.Fraction]
FourTupleColor = Tuple[
    fractions.Fraction,
    fractions.Fraction,
    fractions.Fraction,
    fractions.Fraction]
