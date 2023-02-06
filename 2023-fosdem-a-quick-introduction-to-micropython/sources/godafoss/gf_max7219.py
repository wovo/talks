# ===========================================================================
#
# file     : gf_max7219.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the max7219 LED matrix driver class.
#
# ===========================================================================

from micropython import const
import framebuf

from godafoss.gf_xy import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *
from godafoss.gf_canvas import *


# ===========================================================================

class max7219( canvas ):
    """
    max7219 LED matrix driver
    
    The max7219 is a LED matrix driver that is commonly used to drive
    either an 8x8 LED matrix, or up to 8 7-segment LED displays.
    Max7219 chips can be chained to drive a larger LED matrix.
    
    The 
    """

    # =======================================================================    

    class _commands: 
        NOOP          = const( 0x00 )
        DIGIT_ZERO    = const( 0x01 ) # + digit (y) number 0..7
        DECODE_MODE   = const( 0x09 ) # data: 0bxxxx_xxxx mode of each digit
        INTENSITY     = const( 0x0A ) # data: 0bxxxx duty cycle
        SCAN_LIMIT    = const( 0x0B ) # data: 0bxxx 0-7 for 1-8 displays
        SHUT_DOWN     = const( 0x0C ) # data: 0b1 = normal, 0b0 = shutdown
        DISPLAY_TEST  = const( 0x0F ) # data: 0b0 = normal, 0b1 = test
    
    # =======================================================================    

    def __init__( 
        self, 
        n, 
        spi, 
        chip_select : [ int, pin_out, pin_in_out, pin_oc ], 
        background = False, 
        brightness = 0, 
        enable = True 
    ):
        self._n = n
        self._spi = spi
        self._chip_select = make_pin_out( chip_select )
        
        canvas.__init__(
            self,
            size = xy( 8 * self._n, 8 ),
            is_color = False,            
            background = background
        )
        
        self.buffer = bytearray(( self.size.y // 8 ) * self.size.x )
        self.framebuf = framebuf.FrameBuffer(
            self.buffer, self.size.x, self.size.y, framebuf.MONO_HLSB 
        )      

        self.write_command(  self._commands.DISPLAY_TEST, 0 ),
        self.write_command(  self._commands.SCAN_LIMIT, 7 ),
        self.write_command(  self._commands.DECODE_MODE, 0 ),

        self.brightness( brightness )
        self.enable( enable )
       
    # =======================================================================    

    def enable( self, v ):
        self.write_command(
            self._commands.SHUT_DOWN,
            0x01 if v else 0x00
        )
        
    # =======================================================================    

    def brightness( self, v ):
        self.write_command(
            self._commands.INTENSITY,
            clamp( v, 0, 7 )
        )
        
    # =======================================================================    

    def _write_pixel_implementation( 
        self, 
        location: xy, 
        ink: bool | None = True
    ) -> None:        
        self.framebuf.pixel( 
            location.x, 
            location.y, 
            ink
        )

    # =======================================================================    

    def write_command(
        self,
        command,
        data
    ) -> None:
        self._chip_select.write( 0 )
        for m in range( self._n ):
            self._spi.write( bytearray( [ command, data ] ) )
        self._chip_select.write( 1 )    
        
    # =======================================================================    

    def _flush_implementation( self ) -> None:
        
        for y in range( 8 ):
            self._chip_select.write( 0 )
            for x8 in range( self._n ):
                self._spi.write( bytearray( [
                    self._commands.DIGIT_ZERO + y ,
                    self.buffer[ ( y * self._n ) + x8 ]
                ] ) )
            self._chip_select.write( 1 )

    # =======================================================================    

# ===========================================================================
