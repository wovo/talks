# ===========================================================================
#
# file     : gf_font.py
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

from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_glyph import *


# ===========================================================================

class font:
    """
    a character font
    
    :param size: (:class:`~godafoss.xy`)
        the size of a glyph
    
    A character font defines a 
    :class:`~godafoss.glyph` 
    (monochrome image) for each character in the font.
    Each font has a fixed character height, equal to size.y.
    A proportional font has a size.x == 0. 
    For a fixed width font size.x is the witdh of each character.
    """

    # =======================================================================

    def __init__( 
        self, 
        size: xy
    ):
        self.size = size

    # =======================================================================

    def read( 
        self, 
        c: chr 
    ) -> glyph:
        """
        the :class:`~godafoss.glyph` for the specified character
        
        :param c: (chr)
            the char for which the :class:`~godafoss.glyph` is retrieved     
        """
        raise NotImplementedError


# ========================================================================== =

class _default_font_image( glyph ):
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
 
class default_font( font ):
    """
    the micropython built-in 8x8 font
    """

    def __init__( self ):
        font.__init__( self, xy( 8, 8 ) )

    def read( self, c: chr ) -> glyph:
        return _default_font_image( c )
                
                
# ========================================================================== =
