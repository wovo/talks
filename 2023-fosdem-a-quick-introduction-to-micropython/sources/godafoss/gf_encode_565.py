# ===========================================================================
#
# file     : gf_st7789.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the st7789 LCD driver class.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_color import *


# ===========================================================================

class encode_565:
    """
    encode a color into a 16-bit word
    
    :param order: str
        color order, must be a permutation of "RGB"
    
    :param reverse: bool
        whether the bits of each color must be reversed (default: False)
        
    This class provides the _encode function that encodes
    a :class:`color` into a 16-bit value using the 565 format,
    using the colors in the order specified in the order parameter.
    To speed things up a little, the lowest bit ofd the middle color
    (the '6' in 565) is always 0.
    
    When reverse is True, the biits of each color value are reversed:
    the least significat bit is at the highest position.
    The seems to be required for the st7789.
    """

    def __init__( 
        self,
        order: str,
        reverse: bool = False        
    ):
        
        order = order.upper()
        if order == "RGB":
            self._encode = self._encode_rgb
        elif order == "RBG":
            self._encode = self._encode_rbg        
        elif order == "GRB":
            self._encode = self._encode_grb
        elif order == "GBR":
            self._encode = self._encode_gbr        
        elif order == "BRG":
            self._encode = self._encode_brg        
        elif order == "BGR":
            self._encode = self._encode_bgr
        else:
            raise ValueError( "unsupported color order '%s'" % order )       
            
        if reversed:
            self._reverse5 = lambda x: mirror_bits( 5, x )
            self._reverse6 = lambda x: mirror_bits( 6, x )
        else:
            self._reverse5 = unity
            self._reverse6 = unity
    
    # =======================================================================
    
    def _rgb555( self, c: color ):
        r, g, b = c.rgb()
        if self._reverse:
            r = lambda x: mirror_bits( 6, r )
            g = lambda x: mirror_bits( 6, g )
            b = lambda x: mirror_bits( 6, b )
        else:
            r = r >> 3
            g = g >> 3
            b = b >> 3            
        return r, g, b
     
    # =======================================================================
     
    def _encode_rgb( self, c: color ):
        red, green, blue = self._rgb555( c )
        return (
              ( red   << 11 )
            | ( green <<  5 )
            | ( blue  <<  0 )
        )        
        
    # =======================================================================
    
    def _encode_rbg( self, c ):
        red, green, blue = self._rgb555( c )
        return (
              ( red   << 11 )
            | ( blue  <<  5 )
            | ( green <<  0 )
        )      
        
    # =======================================================================

    def _encode_brg( self, c ):
        red, green, blue = self._rgb555( c )
        return (
              ( blue  << 11 )
            | ( red   <<  5 )
            | ( green <<  0 )
        )      
        
    # =======================================================================

    def _encode_bgr( self, c ):
        red, green, blue = self._rgb555( c )
        return (
              ( blue  << 11 )
            | ( green <<  5 )
            | ( red   <<  0 )
        )      
        
    # =======================================================================

    def _encode_gbr( self, c ):
        red, green, blue = self._rgb555( c )
        return (
              ( green << 11 )
            | ( blue  <<  5 )
            | ( red   <<  0 )
        )      
        
    # =======================================================================

    def _encode_grb( self, c ):
        red, green, blue = self._rgb555( c )
        return (
              ( green << 11 )
            | ( red   <<  5 )
            | ( blue  <<  0 )
        )      
        
    # =======================================================================
    
# ===========================================================================
 