# ===========================================================================
#
# file     : gf_color.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the color class.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_invertible import *


# ===========================================================================

class color( invertible, immutable ):
    """
    rgb color

    :param red: int
        red channel brightness (0..255)

    :param green: int
        green channel brightness (0..255)

    :param blue: int
        blue channel brightness (0..255)

    This is a (red, green, blue) color value.

    The red, green and blue attributes are in the range 0...255.
    Values outside this range are clamped to the nearest value
    within the range.
    The rgb attribute is the tuple of the read, green and blue
    attributes.

    The color channel values are additive
    (like light; not subtractive, like paint or filters).

    Two colors can be added or subtracted.

    Colors and be multiplied by an integer value,
    or divided by an integer value.

    Some common colors are available as attributes of the colors class.

    $macro_insert invertible

    $macro_insert immutable

    examples::
    $insert_example( "test_color.py", "color examples", 1 )
    """

    # =======================================================================

    def __init__(
        self,
        red: int,
        green: int,
        blue: int
    ) -> None:
        self.red   = clamp( red, 0, 255 )
        self.green = clamp( green, 0, 255 )
        self.blue  = clamp( blue, 0, 255 )
        invertible.__init__( self )
        immutable.__init__( self )

    # =======================================================================

    def rgb( self ):
        """
        return the 3 values read, green, blue
        """
        return self.red, self.green, self.blue

    # =======================================================================

    def __add__(
        self,
        other: "color"
    ) -> "color":
        return color(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue
        )

    # =======================================================================

    def __sub__(
        self,
        other: "color"
    ) -> "color":
        return color(
            self.red - other.red,
            self.green - other.green,
            self.blue - other.blue
        )

    # =======================================================================

    def inverted( self ) -> "color":
        """
        the complement of the color

        A color can be negated, which yields the complimentary
        :class:`~godafoss.color`.

        examples::
        $insert_example( "test_color.py", "color invert example", 2 )
        """
        return colors.white - self

    # =======================================================================

    def __mul__(
        self,
        other: int
    ) -> "color":
        return color(
            self.red * other,
            self.green * other,
            self.blue * other
        )

    # =======================================================================

    def __rmul__(
        self,
        other: int
    ) -> "color":
        return color(
            self.red * other,
            self.green * other,
            self.blue * other
        )

    # =======================================================================

    def __floordiv__(
        self,
        other: int
    ) -> "color":
        return color(
            self.red // other,
            self.green // other,
            self.blue // other
        )

    # =======================================================================

    def __repr__( self ) -> str:
        return "(%d,%d,%d)" % ( self.red, self.green, self.blue )

    # =======================================================================

# ===========================================================================


class colors:
    """
    some common color values
    """

    black   = color(    0,    0,    0 )
    white   = color( 0xFF, 0xFF, 0xFF )
    gray    = color( 0x80, 0x80, 0x80 )

    red     = color( 0xFF,    0,    0 )
    green   = color(    0, 0xFF,    0 )
    blue    = color(    0,    0, 0xFF )

    yellow  = color( 0xFF, 0xFF,    0 )
    cyan    = color(    0, 0xFF, 0xFF )
    magenta = color( 0xFF,    0, 0xFF )

    violet  = color( 0xEE, 0x82, 0xEE )
    sienna  = color( 0xA0, 0x52, 0x2D )
    purple  = color( 0x80, 0x00, 0x80 )
    pink    = color( 0xFF, 0xC8, 0xCB )
    silver  = color( 0xC0, 0xC0, 0xC0 )
    brown   = color( 0xA5, 0x2A, 0x2A )
    salmon  = color( 0xFA, 0x80, 0x72 )

# ===========================================================================
