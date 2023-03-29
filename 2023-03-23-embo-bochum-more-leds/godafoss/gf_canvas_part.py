# ===========================================================================
#
# file     : gf_canvas_part.py
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

class _canvas_part( canvas ):
    """
    helper class that is part of a canvas
    """
    
    def __init__( self, subject, start, size ):
        self._subject = subject
        self._start = start
        canvas.__init__(
            self,
            size,
            subject.is_color,
            subject.background
        )

    # =======================================================================                                                                             

    def _write_pixel_implementation(
        self,
        location: xy,
        ink: bool | None = True       
    ) -> None:
        self._subject.write_pixel( self._start + location, ink )      
       
    # =======================================================================                                                                             

    def _flush_implementation(
        self,
        forced: bool
    ) -> None:
        self._subject.flush( forced )
        
    # =======================================================================                                                                             

    # can't use the subject clear() method, because that
    # would clear all of the subject, and with our background
        
    # =======================================================================                                                                             
        
# ===========================================================================   
