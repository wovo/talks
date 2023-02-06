# ===========================================================================
#
# file     : gf_pcf8574x.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the pcf8574x I2C I/O extender class.
#
# ===========================================================================

from machine import I2C
from godafoss.gf_tools import *
from godafoss.gf_ports import *
from godafoss.gf_port_buffers import *


# ===========================================================================

class pcf8574x( port_out_buffer ):
    """
    pcf8574 / pcf8574a I2C I/O extender
    
    This class implements an interface to a pcf8574 or pcf8574a
    I2C I/O extender chip.
    
    $insert_image( "pcf8574-pinout", 1, 300 )
    
    A pcf8574(a) is an I2C slave that provides 8 open-collector 
    input/output pins with weak pull-ups.
    The power supply range is 2.5 .. 5.5 Volt.
    
    The chip has a 7-bit slave address.
    3 bits are set by the level of 3 input pins (a0 .. a2) of the chip.
    The pcf8574 and pcf8574a are the same chips, but with different
    I2C bus addresses.
    With all address poins pulled low the 7-bit i2c address is 
    0x20 (pcf8574) or 0x38 (pcf8574a).
    
    $insert_image( "pcf8574-addresses", 1, 400 )
    
    The chip has only one register, which can be read and written.
    When written, it determines the level of the 8 output pins:
    low when the bit is 0, pulled weakly high when the bit is 1.
    When read, the level of the 8 pins determines the value:
    0 for a low pin, 1 for a high pin.
    To read the input levels, an all-1 value should first be written,
    otherwise the pins that output a 0 (low level) will dominate
    any external circuit attached to thsose pins.
    """

    def __init__( self, bus: I2C, address: int = 0 ):
        """
        create a pcf8574x interface
        
        The address must be the 7-bit I2C address.
        """
        port_out_buffer.__init__( self, 8 )
        self._bus = bus
        self._address = address

    def flush( self ):
        "write buffer to chip"
        self._bus.writeto( self._address, self._buffer )

# ===========================================================================

class pcf8574( pcf8574x ):
    
    def __init__( self, bus, address = 0 ):
        """
        create a pcf8574 interface
        
        The address must be the 3 bits formed by A0 .. A2.
        """    
        pcf8574x.__init__( self, bus, 0x20 + address )


# ===========================================================================

class pcf8574a( pcf8574x ):

    def __init__( self, bus, address = 0 ):
        """
        create a pcf8574 interface
        
        The address must be the 3 bits formed by A0 .. A2.
        """    
        pcf8574x.__init__( self, bus, 0x38 + address )


# ===========================================================================
