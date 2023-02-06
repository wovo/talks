# ===========================================================================
#
# file     : gf_rectangle.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the concrete rectangle class
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_shape import *
from godafoss.gf_line import *

              
# ===========================================================================

class rectangle( shape ):  
    """
    rectangle shape 
        
    :param span: (:class:`godafoss.xy`)
        the far end of the rectangle, as offset from the start
        
    $insert_image( "rectangles", 1, 300 )

    Without any offset, a rectangle starts at the origin 
    (xy(0,0), the top-left pixel of the sheet).
    
    $macro_insert shape
    """  
    
    def __init__( 
        self, 
        span: xy, 
        fill = False
    ):
        self._span = span
        self._fill = fill
        shape.__init__( self )
                
    def write( 
        self, 
        s: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ):
        """
        write the line to the sheet
       
        $macro_insert shape_write 
        """    
        
        if self._fill:
            for dx in range( 0, self._span.x ):
                for dy in range( 0, self._span.y ):
                    s.write_pixel( offset + xy( dx, dy ), ink )
        else:
            h = line( xy( self._span.x, 0 ) )
            v = line( xy( 0, self._span.y ) )
            h.write( s, offset,                             ink )
            h.write( s, offset + xy( 0, self._span.y - 1 ), ink )
            v.write( s, offset,                             ink )
            v.write( s, offset + xy( self._span.x - 1, 0 ), ink )
            
    
# ===========================================================================
