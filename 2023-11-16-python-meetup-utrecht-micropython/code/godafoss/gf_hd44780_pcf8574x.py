# ===========================================================================
#
# file     : gf_hd44780_pcf8574a.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the hd44780-over-pcf8574 character LCD driver class.
#
# ===========================================================================

from godafoss.gf_hd44780 import *
from godafoss.gf_pcf8574x import *


# ===========================================================================

def _hd44780_pcf8547x( 
    size: xy, 
    bus, 
    pcf_chip, 
    address = 0 
) -> hd44780:
    chip = pcf_chip( bus, address )
    data = chip.selection( 4, 5, 6, 7 )
    rs = chip[ 0 ]
    e = chip[ 2 ]
    rw = chip[ 1 ]
    backlight = chip[ 3 ]
    return hd44780( size, data, rs, e, rw, backlight )

def hd44780_pcf8574( 
    size, 
    bus, 
    address = 7 
):
    return _hd44780_pcf8547x( size, bus, pcf8574, address )


def hd44780_pcf8574a( 
    size, 
    bus, 
    address = 7 
):
    return _hd44780_pcf8547x( size, bus, pcf8574a, address )
     
     
# =========================================================================== 
