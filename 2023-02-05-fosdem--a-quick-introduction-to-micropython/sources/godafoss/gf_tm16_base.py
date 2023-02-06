# ===========================================================================
#
# file     : gf_tm16_base.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the tm16_base class.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_xy import *
from godafoss.gf_color import *
from godafoss.gf_canvas import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================

class tm16_base:
    """
    interface to tm16xx chips
    
    This class provides the interface to tm16xx chips.
    """

    def __init__( 
        self, 
        sclk: [ int, pin_out, pin_in_out, pin_oc ], 
        din: [ int, pin_out, pin_in_out, pin_oc ]
    ):
        self.sclk = make_pin_out( sclk )
        self.din = make_pin_out( din )

        self.sclk.write( 1 )
        self.din.write( 1 )
        self._sleep()

    def _start( self ):
        self.din.write( 0 )
        sleep_us( 1 )
        self.sclk.write( 0 )
        sleep_us( 1 )
        
    def _write_byte( self, b: int ):
        # write 8 bits
        for i in range( 8 ):
            self.din.write( b & 0x01 )
            b = b >> 1
            sleep_us( 1 )
            self.sclk.write( 1 )
            sleep_us( 1 )
            self.sclk.write( 0 )
            sleep_us( 1 )        

    def _stop( self ):
        self.sclk.write( 1 )
        sleep_us( 1 )
        self.din.write( 1 )
        sleep_us( 1 )

    def command( self, cmd: int, data = [] ):
        """
        send command and optional data
        
        This method sends a the command and optional data
        to the chip.
        """
        
        self._start()
        self._write_byte( cmd )
        for d in data:
            self._write_byte( d )
        self._stop()
