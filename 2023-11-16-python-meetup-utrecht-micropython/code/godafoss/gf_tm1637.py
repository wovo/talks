# ===========================================================================
#
# file     : gf_tm1637.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the tm1637 LED matrix driver class.
#
# ===========================================================================

from godafoss.gf_pins import *
from godafoss.gf_make_pins import *
from godafoss.gf_tm16xx import *
from godafoss.gf_digits import *

# ===========================================================================

class tm1637( tm16xx, digits ):
    """
    tm1637 LED display and keypad interface driver
    
    This class controls a tm1637 LED display and keypad interface chip.
    The mandatory constructor parameters are the number of digits,
    and the interface pins slk and dio.
    The optional parameters are the bightness (0..7, default is 0),
    and the order of the numerical digits.
    
    The driver is buffered: a clear() call is required to update
    the display.
    
    The tm1637 harware interface is i2c-like, but does not use
    a slave address byte.
    The driver uses an output pin for the clk (clock) pin.
    An open-collector is used for the dio pin, hence that
    pin must have a suitable pull-up resistor.
    """

    # =======================================================================

    def __init__( 
        self, 
        n: int, 
        slk: [ int, pin_out, pin_in_out, pin_oc ], 
        dio: [ int, pin_out, pin_in_out, pin_oc ], 
        background: bool = False,
        brightness = 0,
        order = None # : Iterable[ int ] = None
    ) -> None:
        
        self._slk = make_pin_out( slk )
        self._dio = make_pin_oc( dio )
        self._slk.write( 1 )
        self._dio.write( 1 )
        sleep_us( 1 )
        
        digits.__init__(
            self,
            n = n,
            order = order
        )
        
        tm16xx.__init__(
            self,          
            size = xy( n, 8 ),
            background = background,
            brightness = brightness                         
        )
       
    # =======================================================================
    
    def write_digit_segments(
        self,
        n: int,
        v: int    
    ) -> None:
        if ( n >= 0 ) and ( n < self.n ):
            self._buffer[ n ] = v
            
    # =======================================================================
    
    def _start( self ) -> None:
        self._dio.write( 0 )
        sleep_us( 1 )
        self._slk.write( 0 )
        sleep_us( 1 )
            
    # =======================================================================
        
    def _ack( self ) -> None:
        # i2c-style ack cycle 
        self._dio.write( 0 )
        sleep_us( 1 )
        self._slk.write( 1 )
        sleep_us( 1 )
        self._slk.write( 0 )
        sleep_us( 1 )
            
    # =======================================================================

    def _stop( self ) -> None:
        self._dio.write( 0 )
        sleep_us( 1 )
        self._slk.write( 1 )
        sleep_us( 1 )
        self._dio.write( 1 )
        sleep_us( 1 )
            
    # =======================================================================


# ===========================================================================
