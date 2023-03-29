# ===========================================================================
#
# file     : gf_fraction.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the fraction class.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_invertible import *


# ===========================================================================

class fraction( invertible, immutable ):
    """
    a fractional value

    :param value: int
        the value, interpreted as a fraction of the maximum

    :param maximum: int
        the value is interpreted on the scale [0..maximum]

    A fraction is conceptually a value in the range 0.0 ... 1.0.
    It is stored as a maximum (must be >0) and a value
    (will be 0 ... maximum).

    A fraction represents for instance the result of an ADC reading
    (like 512 out of 1023 for a 10-bit ADC for half the maximum voltage),
    or a setpoint for a servo
    (100 out of 400 would be 1/4 of full travel).

    The value and maximum are available as attributes.
    The scaled method returns the fraction of the interval (minimum
    and maximum).

    $macro_insert invertible
    For a fraction, the inverse is the complement of its value.

    A fraction can be converted to a string representation.

    $macro_insert immutable

    examples::
    $insert_example( "test_fraction.py", "fraction examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        value: int,
        maximum: int
    ):
        self.value = clamp( value, 0, maximum )
        self.maximum = maximum
        self.value_maximum = ( self.value, self.maximum )
        invertible.__init__( self )
        immutable.__init__( self )

    # =======================================================================

    def scaled(
        self,
        minimum: int | float,
        maximum: int | float
    ) -> int | float:
        """
        the fraction, scaled to an interval

        :param minimum: int | float
            the real part (default 0.0)

        :param maximum: int | float
            the imaginary part (default 0.0)

        :result: int | float
            the franctional value,
            scaled to the interval [minimum...maximum]

        The scaled method is usefull to scale a fraction to an
        interval, which is specified by the minimum and maximum parameters.
        When those parameters are integers, the result will be an integer.
        When one or both are floats, the result is a float.

        examples::
        $insert_example( "test_fraction.py", "fraction scaled examples", 2 )
        """

        span = ( maximum - minimum )
        if isinstance( maximum, int ) and isinstance( minimum, int ):
            return minimum + span * self.value // self.maximum
        else:
            return minimum + span * self.value / self.maximum

    # =======================================================================

    def inverted( self ) -> "fraction":
        """
        complement of the fraction

        The inverted (negative) of a fraction is its complement.
        For instance, the complement of 3-out-of-10 is 7-out-of-10.

        examples::
        $insert_example( "test_fraction.py", "fraction invert examples", 2 )
        """

        return fraction( self.maximum - self.value, self.maximum )

    # =======================================================================

    def __repr__( self ) -> str:
        return "(%d/%d)" % ( self.value, self.maximum )

    # =======================================================================

# ===========================================================================
