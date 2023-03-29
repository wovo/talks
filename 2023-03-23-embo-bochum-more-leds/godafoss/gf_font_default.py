# ===========================================================================
#
# file     : gf_font_default_font.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) adc class.
#
# ===========================================================================

from godafoss.gf_glyph import *
from godafoss.gf_font import *


# ========================================================================== =

class _font_default_image( glyph ):
    """
    glyph of the built-in 8x8 font
    """

    def __init__( self, c ):
        glyph.__init__( self, xy( 8, 8 ) )
     
        import framebuf
        buf = bytearray(( self.size.y // 8 ) * self.size.x )
        self._charbuf = framebuf.FrameBuffer( buf, 8, 8, framebuf.MONO_VLSB )
        self._charbuf.fill( 0 )
        self._charbuf.text( c, 0, 0 )   
        
    def read( 
        self, 
        location: xy 
    ) -> bool:        
        return self._charbuf.pixel( location.x, location.y )
        

# ========================================================================== =
 
class font_default( font ):
    """
    the micropython built-in 8x8 font
    """

    def __init__( self ):
        font.__init__( self, xy( 8, 8 ) )

    def read( self, c: chr ) -> glyph:
        return _font_default_image( c )
                
                
# ========================================================================== =
