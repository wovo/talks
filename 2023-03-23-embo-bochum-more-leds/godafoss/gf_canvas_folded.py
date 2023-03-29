# ===========================================================================
#
# file     : gf_canvas_folded.py
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

class _canvas_folded( canvas ):
    """
    helper class that folds a canvas    
    """
    
    def __init__(
        self,
        subject: canvas,
        n: int,
        zigzag: bool
    ) -> None:
        self._subject = subject
        self._n = n
        self._zigzag = zigzag
        canvas.__init__(
            self,
            xy( subject.size.x // n, subject.size.y * n ),
            is_color = subject.is_color,
            background = subject.background
        )
        
    # =======================================================================

    def _write_pixel_implementation(
        self,
        location: xy,
        ink: bool | color        
    ) -> None:
        x, y = location.x, location.y
        if self._zigzag and ( ( y % 2 ) == 1 ):
            x = self.size.x - ( x + 1 )
        x = x + self.size.x * ( y // self._subject.size.y )
        y = y % self._subject.size.y
        self._subject.write_pixel( xy( x, y ), ink )  
               
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
        self._subject.clear( ink )       

    # =======================================================================                                                                             

# ===========================================================================   
