# ===========================================================================
#
# file     : gf_xpt2046.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the xpt2046 touch screen interface driver class.
#
# ===========================================================================

from micropython import const

from godafoss.gf_touch import *


# ===========================================================================

class xpt2046( touch ):
    """
    XPT2046 touch screen chip driver
    
    :param spi: (machine.SPI)
        spi bus that connects to the chip, max 10 Mhz

    :param cs: ($macro_insert make_pin_out_types )
        chip select pin (active low)        
    
    :param size: :class:`~godafoss.xy`
        the size of the touch area in pixels        
    
    mux settling time 500 clocks???
    rotate and mirror the screen
    offsets & calibration
    general touch class for this??
    """

    # =======================================================================   

    class channels:   
        x              = const( 5 )
        y              = const( 1 )
        z1             = const( 3 )
        z2             = const( 4 )
        temperature_0  = const( 0 )
        temperature_1  = const( 7 )
        battery        = const( 2 )
        auxillary      = const( 6 )
        
    # =======================================================================    

    def __init__(
        self,
        spi: machine.SPI,
        cs: [ int, pin_out, pin_in_out, pin_oc ],
        size: xy = None
    ):
        touch.__init__(
            self,
            size = size,
            span = 4095
        )
        self._spi = spi
        self._cs = make_pin_out( cs )
        self._size = size
        self._rx = bytearray( 3 )
        self._tx = bytearray( 3 )
        
    # =======================================================================        

    def touch_adcs( self ):

        a = self.command_response( channel = self.channels.x )
        b = self.command_response( channel = self.channels.y )
        
        if a == 0 or b == 0:
            return None, None
        
        else:
            return a, b
            
    # =======================================================================
    
    def command_response( 
        self, 
        channel: int = 0, 
        command: int = 0 
    ):
        """
        command / response exchange with the chip
        
        :param channel: int (default 0)
            channel number to read
               
        :param command: int (default 0)
            other command bits; default is single ended, 12 bits
        
        :result: int
            the 12 bit respons from the chip      
        This function sends a command to the chip and receives and
        returns the response. 
        The most significan bit (start bit) of the command 
        is automatically set.
        """

        self._tx[ 0 ] = 0x80 | channel << 4 | command
        self._cs.write( 0 )
        self._spi.write_readinto( self._tx, self._rx )
        self._cs.write( 1 )

        return ( self._rx[ 1 ] << 4 ) | ( self._rx[ 2 ] >> 4 )    
    
# ===========================================================================


