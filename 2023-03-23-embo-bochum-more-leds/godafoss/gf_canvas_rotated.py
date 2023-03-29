# ===========================================================================
#
# file     : gf_canvas_rotated.py
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

def _canvas_rotated( 
    self, 
    rotation: int 
) -> "canvas":
        
    from godafoss.gf_canvas_transformed import _canvas_transformed    

    if rotation == 0:
        return _canvas_transformed( 
            self, 
            self.size, 
            lambda c: xy( c.x, c.y )
        )
            
    elif rotation == 90:
        return _canvas_transformed( 
            self, 
            xy( self.size.y, self.size.x ),
            lambda c: xy( self.size.x - 1 - c.y, c.x )
        )
            
    elif rotation == 180:
        return _canvas_transformed( 
            self, 
            self.size, 
            lambda c: xy( self.size.x - 1 - c.x, self.size.y - 1 - c.y )
        )
           
    elif rotation == 270:
        return _canvas_transformed( 
            self, 
            xy( self.size.y, self.size.x ), 
            lambda c: xy( c.y, self.size.y - 1 - c.x ) 
        )    
            
    else:
        raise ValueError( "rotation must be 0, 90, 180 or 270" )                                                                                                                                                        

# ===========================================================================
