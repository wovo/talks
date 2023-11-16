# ===========================================================================
#
# file     : gf_canvas_inverted.py
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

def _invert_ink( ink: bool | color ):
    return not ink if isinstance( ink, bool ) else - ink

# ===========================================================================

class _canvas_inverted( canvas ):
    """
    helper class that inverts a canvas    
    """
    
    def __init__( self, subject: canvas ):
        self._subject = subject
        canvas.__init__(
            self,
            subject.size,
            subject.is_color,
            _invert_ink( subject.background )
        )
        
    # =======================================================================                                                                             

    def _write_pixel_implementation(
        self,
        location: xy,
        ink: bool | color   
    ) -> None:
        self._subject.write_pixel( 
            location, 
            _invert_ink( ink ) 
        )  
        
    # =======================================================================                                                                             

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )
        
    # =======================================================================                                                                             

    def _clear_implementation(
        self,
        ink: bool | color
    ) -> None:
        self._subject.clear( _invert_ink( ink ) )       

    # =======================================================================                                                                             

# ===========================================================================
