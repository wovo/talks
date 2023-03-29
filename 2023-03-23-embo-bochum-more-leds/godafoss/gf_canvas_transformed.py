# ===========================================================================
#
# file     : gf_canvas_transformed.py
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

class _canvas_transformed( canvas ):
    """
    helper class that is a transformed version of the canvas
    """
    
    def __init__( self, subject, size, transform_location ):
        self._subject = subject
        self._transform_location = transform_location
        canvas.__init__(
            self,
            size = size,
            is_color = subject.is_color,
            background = subject.background
        )

    def write_pixel(
        self,
        location: xy,
        ink: bool | None = True        
    ) -> None:
        p = self._transform_location( location )
        if self._subject.within( p ):        
            self._subject.write_pixel( p, ink )      
       
    # =======================================================================                                                                             

    def flush( self, forced: bool = False ) -> None:
        self._subject.flush( forced )
        
    # =======================================================================                                                                             

    def clear( self, ink: bool = False ) -> None:
        self._subject.clear( ink )    
        
    # =======================================================================                                                                                                                                                       

# ===========================================================================
