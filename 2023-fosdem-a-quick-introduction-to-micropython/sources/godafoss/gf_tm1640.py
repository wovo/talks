# ===========================================================================
#
# file     : gf_tm1640.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the tm1640 LED matrix driver class.
#
# ===========================================================================

from godafoss.gf_xy import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *
from godafoss.gf_tm16xx import *
from godafoss.gf_canvas import *


# ===========================================================================

class tm1640( tm16xx, canvas ):
    """
    tm1640 LED matrix display interface driver
    
    This class controls a tm1640 LED matrix display interface chip.
    The mandatory constructor parameters are the size of the
    display, and the interface pins sclk and dio.
    The optional parameters are the background (default is False == disabled)
    and the bightness (0..7, default is 0)
    
    The driver is buffered: a clear() call is required to update
    the display.
    
    The tm1637 hardware interface is i2c-like, but it is not
    meant for multiple chips as it does not use
    a slave address byte or ack bits.
    The driver uses output pins for  the sclk and din pins,
    hence no pull-up resistors are needed.
    """

    # =======================================================================

    def __init__( 
        self, 
        size: xy,
        sclk: [ int, pin_out, pin_in_out, pin_oc ], 
        din: [ int, pin_out, pin_in_out, pin_oc ], 
        background: bool = False,
        brightness: int = 0
    ) -> None:

        self._sclk = make_pin_out( sclk )
        self._din = make_pin_out( din )
        self._sclk.write( 1 )
        self._din.write( 1 ) 
        sleep_us( 1 )
        
        canvas.__init__(
            self,
            size = size,
            is_color = False,
            background = background
        )
        
        tm16xx.__init__(
            self,
            size = size,
            brightness = brightness
        )
       
    # =======================================================================

    def _write_pixel_implementation( 
        self, 
        location: xy, 
        ink: bool
    ) -> None:       
        self._framebuf.pixel( 
            location.x, 
            location.y, 
            ink
        )
            
    # =======================================================================    

    def _clear_implementation( self ) -> None:
        self._framebuf.fill( 0xFF if ink else 0x00 )             
            
    # =======================================================================
            
            
    def _start( self ) -> None:
        self._din.write( 0 )
        sleep_us( 1 )
        self._sclk.write( 0 )
        sleep_us( 1 )

        
    # =======================================================================

    def _stop( self ) -> None:
        self._din.write( 0 )
        sleep_us( 1 )
        self._sclk.write( 1 )
        sleep_us( 1 )
        self._din.write( 1 )
        sleep_us( 1 )
        
    # =======================================================================
        
    def _write_byte(
        self,
        b: int
    ) -> None:
        # write 8 bits, LSB first
        for _ in range( 8 ):
            self._din.write( ( b & 0x01 ) != 0 )
            b = b >> 1
            sleep_us( 1 )
            self._sclk.write( 1 )
            sleep_us( 1 )
            self._sclk.write( 0 )
            sleep_us( 1 )
            
    # =======================================================================
         
        
# ===========================================================================
