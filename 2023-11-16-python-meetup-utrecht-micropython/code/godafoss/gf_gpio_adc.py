# ===========================================================================
#
# file     : gf_gpio_adc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the gpio_adc class.
#
# ===========================================================================

from godafoss.gf_fraction import *
from godafoss.gf_adc import *


# ===========================================================================
        
class gpio_adc( adc ):
    """
    analog input pin of the target chip
    
    :param pin_nr: int
        target chip pin number

    This class abstracts an ADC (Analog to Digital Converter)
    input pin of the target chip.    
    
    $macro_insert invertible    
    For the inverted version, the read() method returns
    the complement of the value that would be retruned by the
    original adc.
    """

    # =======================================================================

    def __init__( 
        self, 
        pin_nr: int 
    ):
        import machine
        self._adc = machine.ADC( machine.Pin( pin_nr ) )

    # =======================================================================

    def read( self ):
        return fraction( self._adc.read_u16(), 65535 )
        
    # =======================================================================

# ===========================================================================
