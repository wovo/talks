# ===========================================================================
#
# file     : gf_canvas_add.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains a helper class for the canvas class.
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *


# ===========================================================================


class _canvas_add( canvas ):
    """
    helper class that adds two canvasses
    """

    # =======================================================================                                                                             

    def __init__( 
        self, 
        a: canvas, 
        b: canvas 
    ):
        self._a = a
        self._b = b
        canvas.__init__(
            self,
            xy( 
                max( self._a.size.x, self._b.size.x ),
                max( self._a.size.y, self._b.size.y ) 
            ),
            a.is_color and b.is_color,
            a.background
        )
        
    # =======================================================================                                                                             

    def _write_pixel_implementation(
        self,
        location: xy,
        ink: color | bool | None = True     
    ) -> None:
        self._a.write_pixel( location, ink )
        self._b.write_pixel( location, ink )
        
    # =======================================================================                                                                             

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._a.flush( forced )       
        self._b.flush( forced )
        
    # =======================================================================                                                                             

    def _clear_implementation( 
        self, 
        ink: color | bool = False 
    ) -> None:
        self._a.clear( ink )
        self._b.clear( ink )
 
    # =======================================================================                                                                             

# ===========================================================================
