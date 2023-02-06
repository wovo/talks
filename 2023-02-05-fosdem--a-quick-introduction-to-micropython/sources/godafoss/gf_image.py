# ===========================================================================
#
# file     : gf_image.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) image class.
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_drawable import *


# ===========================================================================

class image( drawable ):
    """
    a rectangualar area of colored pixels
    """

    # =======================================================================

    def __init__( self, size ):
        self.size = size
        drawable.__init__( self )

    # =======================================================================

    def read( self, location: xy ) -> color:
        """the color of the pixel at the location"""
        raise NotImplementedError

    # =======================================================================

    def draw_implementation( self, canvas, offset, ink ):
        for x in range( self.size.x ): 
            for y in range( self.size.y ):
                c =  self.read( xy( x, y ) )
                canvas.draw( offset + xy( x, y ), c )

        
# ===========================================================================
        