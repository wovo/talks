# ===========================================================================
#
# file     : gf_circle.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the circle class
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_shape import *
from godafoss.gf_line import *

             
# ===========================================================================
  
class circle( shape ):   
    """
    circle shape
    
    :param radius: (int)
        the radius of the circle   
        
    :param fill: (bool)
        whether the circle is outline (False, default) or filled (True)     
        
    $insert_image( "circles", 1, 300 )

    Without any offset, a circle has its centre at the origin 
    (xy(0,0), the top-left pixel of the sheet).
    
    $macro_insert shape
    """    

    def __init__( 
        self, 
        radius: int, 
        fill = False
    ):
        self._radius = radius
        self._fill = fill
        shape.__init__( self )
    
    def write( 
        self, 
        sheet: "sheet",
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ):
        """
        write the circle to the sheet
       
        $macro_insert shape_write 
        """
    
        # don't draw anything when the size would be 0 
        if self._radius < 1:
            return
         
        # http://en.wikipedia.org/wiki/Midpoint_circle_algorithm
   
        fx = 1 - self._radius
        ddFx = 1
        ddFy = -2 * self._radius
        x = 0
        y = self._radius
    
        while x < y + 1:
        
            self._draw_circle_part( sheet, offset, x,  y, ink )
            self._draw_circle_part( sheet, offset, x, -y, ink )
            self._draw_circle_part( sheet, offset, y,  x, ink )
            self._draw_circle_part( sheet, offset, y, -x, ink )    

            # calculate next outer circle point
            if fx >= 0:
                y -= 1
                ddFy += 2
                fx += ddFy
           
            x += 1
            ddFx += 2
            fx += ddFx     

    def _draw_circle_part(
        self,
        sheet,
        offset,
        x,
        y,
        ink
    ):
        sheet.write_pixel( offset + xy( - x, y ) )    
        sheet.write_pixel( offset + xy( + x, y ) )    
        if self._fill:
            sheet.write( line( 2 * xy( x, 0 ) ), xy( -x,  y ) + offset, ink )
            
              
# ===========================================================================
