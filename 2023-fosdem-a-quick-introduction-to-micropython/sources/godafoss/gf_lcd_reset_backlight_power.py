# ===========================================================================
#
# file     : gf_lcd_rst_bl_power.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the lcd_rst_bl_power class.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_pins import *
from godafoss.gf_make_pins import *


# ===========================================================================

class lcd_reset_backlight_power:
    """
    lcd common functionality
    
    :param rst: (None, int, pin_out, pin_in_out, pin_oc)
        reset pin; active low; high for normal operation
        
    :param bl: (None, int, pin_out, pin_in_out, pin_oc)
        backlight pin; active high
        
    :param power: (None, int, pin_out, pin_in_out, pin_oc)
        power pin, active high
        
    :param reset_duration: (int)
        width of a reset pulse, in microseconds (default 1)
        
    :param reset_wait: (int)
        wait time after a reset, in microseconds (default 1)
        
    This class provides the basic functions for a typical LCD
    of having reset, backlight and power pins.
    All pins are optional, and active high.    .
    The constructor enables power and backlight, 
    and resets the lcd.
    
    $macro_start lcd_reset_backlight_power_parameters
    :param reset: ($macro_insert make_pin_out_types)
        reset pin (optional), active low, high for normal operation
        
    :param backlight: ($macro_insert make_pin_out_types)
        backlight pin (optional), active high
        
    :param power: ($macro_insert make_pin_out_types)
        power pin (optional), active high    
    $macro_end
    
    $macro_start lcd_reset_backlight_power_functionality
    This class inherits from 
    :class:`~godafoss:lcd_reset_backlight_power`, 
    which provides functions to reset, switch the power, 
    and switch the backlight
    (when the respective pins are available).
    $macro_end
    """

    # =======================================================================

    def __init__(
        self, 
        reset: [ None, int, pin_out, pin_in_out, pin_oc ],
        backlight: [ None, int, pin_out, pin_in_out, pin_oc ],
        power: [ None, int, pin_out, pin_in_out, pin_oc ],
        reset_duration: int = 1_000,
        reset_wait: int = 1_000
    ) -> None:
        self._rst = make_pin_out( reset )
        self._bl = make_pin_out( backlight )
        self._power = make_pin_out( power )
        self._reset_duration = reset_duration
        self._reset_wait = reset_wait
    
        self.power( 1 )
        self.backlight( 1 )
        self.reset()
        
    # =======================================================================

    def reset( self ) -> None:
        """
        hard-reset the display.
        """
        
        self._rst.pulse( 
            self._reset_duration, 
            self._reset_wait 
        )          
        
    # =======================================================================

    def backlight(
        self,
        state: bool
    ) -> None:
        """
        turn the backlight on (True) or off (False)
        """
        
        self._bl.write( state )
        
    # =======================================================================

    def backlight_blink(
        self,
        high_time = 500_000,
        low_time = None,        
        iterations: None = None,
        
    ):
        for _ in repeater( iterations ):
            self.backlight( 1 )
            sleep_us( high_time )
            self.backlight( 0 )
            sleep_us( first_not_none( low_time, high_time ) )        
        
    # =======================================================================

    def power(
        self,
        state: bool
    ) -> None:
        """
        turn the power on (True) or off (False)
        """
        
        self._power.write( state )       

    # =======================================================================

# ===========================================================================
