# ===========================================================================
#
# file     : gf_xyz.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the xyz class.
#
# ===========================================================================

from godafoss.gf_tools import *


# ===========================================================================

class xyz( immutable ):
    """
    xyz 3d coordinates or vector

    :param x: int | float
        x value

    :param y: int | float
        y value

    :param z: int | float
        z value

    An xyz value represents a vector in a 3d space.
    Such values can for instance be used to represent the direction
    of gravity returned by an acceleration sensor.

    The x, y and z values, and the xyz tuple are available
    as attributes.

    The supported operations are addition, subtraction, negation,
    multiplication (by an integer or float), true division and floor division
    (by an integer or float), and taking the string representation.

    $macro_insert immutable

    examples::
    $insert_example( "test_xyz.py", "xyz examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        x: int | float,
        y: int | float,
        z: int | float,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.xyz = ( x, y, z )
        immutable.__init__( self )

    # =======================================================================

    def __add__(
        self,
        other: "xyz"
    ) -> "xyz":
        return xyz(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    # =======================================================================

    def __sub__(
        self,
        other: "xyz"
    ) -> "xyz":
        return xyz(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    # =======================================================================

    def __neg__( self ) -> "xyz":
        return xyz(
           - self.x,
           - self.y,
           - self.z
        )

    # =======================================================================

    def __mul__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x * other,
            self.y * other,
            self.z * other
        )

    # =======================================================================

    def __rmul__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x * other,
            self.y * other,
            self.z * other
        )

    # =======================================================================

    def __truediv__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x / other,
            self.y / other,
            self.z / other
        )

    # =======================================================================

    def __floordiv__(
        self,
        other: int | float
    ) -> "xyz":
        return xyz(
            self.x // other,
            self.y // other,
            self.z // other
        )

    # =======================================================================

    def __repr__( self ) -> str:
        return "(%d,%d,%d)" % ( self.x, self.y, self.z )

    # =======================================================================

# ===========================================================================
