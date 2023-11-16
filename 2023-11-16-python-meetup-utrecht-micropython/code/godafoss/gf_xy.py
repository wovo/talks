# ===========================================================================
#
# file     : gf_xy.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the xy class.
#
# ===========================================================================

from godafoss.gf_typing import *
from godafoss.gf_tools import *


# ===========================================================================

class xy( immutable ):
    """
    xy coordinate pair or 2d vector

    :param x: int
        x value

    :param y: int
        y value

    An xy value represents a location or displacement in a 2d integer grid.
    Such values can for instance be used for pixel or character
    cooordinates within a window.

    The x and y values, and the xy tuple are available
    as attributes.

    The supported operations are addition, subtraction, negation,
    multiplication (by an integer), integer division (by an integer),
    and taking the string representation.

    $macro_insert immutable

    examples::
    $insert_example( "test_xy.py", "xy examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        x: int,
        y: int
    ) -> None:
        self.x = x
        self.y = y
        self.xy = ( x, y )
        immutable.__init__( self )

    # =======================================================================

    def __add__(
        self,
        other: "xy"
    ) -> "xy":
        return xy(
            self.x + other.x,
            self.y + other.y
        )

    # =======================================================================

    def __sub__(
        self,
        other: "xy"
    ) -> "xy":
        return xy(
            self.x - other.x,
            self.y - other.y
        )

    # =======================================================================

    def __neg__( self ) -> "xy":
        return xy(
           - self.x,
           - self.y
        )

    # =======================================================================

    def __mul__(
        self,
        other: any
    ) -> "xy":
        if isinstance( other, int ):
            return xy(
                self.x * other,
                self.y * other
            )
        else:
            return NotImplemented

    # =======================================================================

    def __rmul__(
        self,
        other: int
    ) -> "xy":
        return xy(
            self.x * other,
            self.y * other
        )

    # =======================================================================

    def __rmatmul__(
        self,
        t: str
    ) -> "xy":
        from godafoss.gf_text import canvas_text
        return text( t ) @ self

    # ================================================================

    def __floordiv__(
        self,
        other: int
    ) -> "xy":
        return xy(
            self.x // other,
            self.y // other
        )

    # =======================================================================

    def __repr__( self ) -> "str":
        return "(%d,%d)" % ( self.x, self.y )

    # =======================================================================

# ===========================================================================
