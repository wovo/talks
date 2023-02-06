# ===========================================================================
#
# file     : gf_tm1638.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the tm1638 LED matrix driver class.
#
# ===========================================================================

from godafoss.gf_pins import *
from godafoss.gf_make_pins import *
from godafoss.gf_port_buffers import *
from godafoss.gf_tm16xx import *
from godafoss.gf_digits import *

# ===========================================================================

class tm1638( tm16xx, digits ):
    """
    tm1638 LED display and keypad interface driver
    
    This class interfaces to the tm1638 LED display and keypad chip.
    The mandatory constructor parameters are the number of digits,
    and the interface pins slk, dio and stb.
    The optional parameters are the bightness (0..7, default is 0),
    and the order of the numerical digits.
    
    The driver is buffered: a clear() call is required to update
    the display.
    
    Multiple tm1638 chips can share slk and dio pins.
    """


    # =======================================================================

    def __init__( 
        self, 
        n: int, 
        slk: [ int, pin_out, pin_in_out, pin_oc ], 
        dio: [ int, pin_out, pin_in_out, pin_oc ], 
        stb: [ int, pin_out, pin_in_out, pin_oc ], 
        brightness = 0,
        digit_order: Iterable[ Int ] = None
    ) -> None :
        self._order = order
        
        self._slk = make_pin_out( slk )
        self._dio = make_pin_oc( dio )
        self._stb = make_pin_out( stb )
        self._stb.write( 1 )
        sleep_us( 1 )
        
        digits.__init__(
            self,
            n = n,
            digit_order = digit_order
        )
        
        self.leds = port_out_buffer( 8 )
        self.leds.flush = lambda : self.flush( True )
        
        self.buttons = port_in_buffer( 8 )
        self.buttons.refresh = lambda : self.refresh()

        tm16xx.__init__(
            self,
            size = xy( n, 16 ),
            background = False,
            brightness = brightness                            
        )
       
    # =======================================================================
    
    def write_digit_segments(
        self,
        n: int,
        v: int    
    ) -> None:
        
        if ( n >= 0 ) and ( n < self.n ):
            self._buffer[ 2 * n ] = v
                      
    # =======================================================================
    
    def write_digit_upper(
        self,
        n: int,
        v: int    
    ) -> None:
        
        if ( n >= 0 ) and ( n < self.n ):
            self._buffer[ 2 * n + 1 ] = v
                      
    # =======================================================================

    def _start( self ) -> None:
        sleep_us( 1 )
        self._stb.write( 0 )
        sleep_us( 1 )
        
    # =======================================================================
        
    def _write_byte( self, b: int ):
        # write 8 bits, LSB first
        for _ in range( 8 ):
            self._dio.write( ( b & 0x01 ) != 0 )
            b = b >> 1
            sleep_us( 1 )
            self._slk.write( 1 )
            sleep_us( 1 )
            self._slk.write( 0 )
            sleep_us( 1 )
            
    # =======================================================================

    def _stop( self ):
        sleep_us( 1 )
        self._stb.write( 1 )
        sleep_us( 1 )
        
    # =======================================================================

    def _flush_implementation( self ) -> None:
        
        # get the LED settings from our port aspect
        mask = 0x01
        for i in range( 8 ):
            self.write_digit_upper(
                i,
                0 if self.leds._value & mask == 0 else 1
            )
            mask = mask << 1
        
        tm16xx.flush( self, forced )
        
    # =======================================================================

    def refresh( self ) -> None:
        pass
        
    # =======================================================================
    
    def demo( self ) -> None:
        n = 0
        while True:
            n += 1 
            print( n, "%02X" % self.read_chip() )
            sleep_us( 200_000 )
        from godafoss.gf_pin_port_demos import kitt
        kitt( self.leds )
        while True:
            self.write_digit_upper( 0, 1 )
            self.flush()
            sleep_us( 200_000 )
            self.write_digit_upper( 0, 0 )
            self.flush()
            sleep_us( 200_000 )
                     
        
# ===========================================================================
