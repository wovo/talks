# ===========================================================================
#
# file     : gf_glyph.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) glyph class.
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_canvas import *
from godafoss.gf_shape import *


# ===========================================================================

class glyph( shape ):
    """
    rectangualar area of monochrome pixels, can be drawn to a 
    :class:`~godafoss.sheet` 
    
    :param size: :class:`~godafoss.xy`
        the size of a glyph    
    """

    # =======================================================================

    def __init__( 
        self, 
        size: xy 
    ) -> None:
        self.size = size
        shape.__init__( self )

    # =======================================================================

    def read( 
        self, 
        location: xy
    ) -> bool:
        """
        the 'color' of the pixel at the location
        
        :param location: :class:`~godafoss.xy`
            the location within the glyph for which the pixel is retrieved
        """
        raise NotImplementedError

    # =======================================================================

    def write( 
        self, 
        sheet: "sheet", 
        offset: xy = xy( 0, 0 ),
        ink: bool | color = True
    ) -> None:
        """
        write the glyph to the sheet
        
        :param sheet: :class:`~godafoss.canvas`
            the canvas to which the glyph is written
            
        :param offset: :class:`~godafoss.xy`
            the location within the sheet where the glyph is written
        """
        for x in range( self.size.x ): 
            for y in range( self.size.y ):
                if self.read( xy( x, y ) ):
                    sheet.write_pixel( offset + xy( x, y ), ink )

    # =======================================================================
        
# ===========================================================================
        