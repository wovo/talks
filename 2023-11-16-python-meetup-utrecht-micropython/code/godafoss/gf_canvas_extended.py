# ===========================================================================
#
# file     : gf_canvas_extended.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains a helper function and class for the canvas class.
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *

# ===========================================================================

def _canvas_extended( 
    self, 
    other: "canvas", 
    direction: str
) -> "canvas":

    if len( direction ) != 2:
        raise ValueError( "direction must be 2 characters" )
            
    direction, alignment = direction            
            
    # which canvas comes first    
    if direction in "SE":
        a, b = self, other
    elif direction in "NW":
        a, b = other, self
    else:
       raise ValueError( "direction[ 0 ] is invalid" ) 
           
    # size depends on extension direction: x or y
    # shift depends on both extension direction and alignment
    if direction in "EW":
        size = xy( 
            self.size.x + other.size.x,
            max( self.size.y, other.size.y ) )

        if alignment == "S":
            a_shift = xy( 0,        size.y - a.size.y )
            b_shift = xy( a.size.x, size.y - b.size.y )
                
        elif alignment == "N":
            a_shift = xy( 0,        0 )
            b_shift = xy( a.size.x, 0 )
                
        else:
            raise ValueError( "direction[ 1 ] is invalid" )
                
    elif direction in "NS":
        size = xy( 
            max( self.size.x, other.size.x ),
            self.size.y + other.size.y )

        if alignment == "E":
            a_shift = xy( b.size.x - a.size.x, 0 )
            #b_shift = xy( a.size.x, 0 )
                
        elif alignment == "W":
            a_shift = xy( 0, 0 )
            b_shift = xy( 0, a.size.y )
                
        else:
            raise ValueError( "direction[ 1 ] is invalid" )           
        
    return _canvas_extended_class( a, b, size, - a_shift, - b_shift ) 

# ===========================================================================

class _canvas_extended_class( canvas ):
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
