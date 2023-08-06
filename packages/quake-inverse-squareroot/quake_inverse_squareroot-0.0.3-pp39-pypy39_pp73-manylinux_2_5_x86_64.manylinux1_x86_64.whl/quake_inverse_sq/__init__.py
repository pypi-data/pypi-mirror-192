"""
Inverse square root implementations. (Implementation from Wikipedia and math.h)
"""

from ._sqrt import coarse_inv_sqrt as c
from ._sqrt import fined_inv_sqrt as f

def coarse_inv_sqrt(number:float) -> float:
    """
    Coarse inverse square root. (Implementation from [Wikipedia](https://en.wikipedia.org/wiki/Fast_coarse_inv_sqrt))
    """
    if number <= 0:
        raise ZeroDivisionError
    elif not isinstance(number, (float,int)):
        raise ValueError("Inappropriate argument value")
    return c(number)

def fined_inv_sqrt(number: float) -> float:
    """
    Fined inverse square root. (Implementation from math.h)
    """
    if number <= 0:
        raise ZeroDivisionError
    elif not isinstance(number, (float,int)):
        raise ValueError("Inappropriate argument value")
    return f(number)