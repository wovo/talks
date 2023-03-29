# ===========================================================================
#
# file     : gf_ft6236.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the ft6236 touch screen interface driver class.
#
# ===========================================================================

from micropython import const 

from godafoss.gf_xy import *
from godafoss.gf_touch import *


# ===========================================================================

class ft6236( touch ):
    """
    ft6236 touch screen chip driver
    
    :param i2c: machine.I2C
        i2c bus that connects to the chip, max 10 Mhz       
    
    :param size: :class:`~godafoss.xy`
        the size of the touch area in pixels        
    
    mux settling time 500 clocks???
    rotate and mirror the screen
    offsets & calibration
    general touch class for this??
    """

    # =======================================================================   

    class registers:   
        dev_mode             = const( 0x00 )
        gest_id              = const( 0x01 )
        td_status            = const( 0x02 )
        
        p1_xh                = const( 0x03 )
        p1_xl                = const( 0x04 )
        p1_yh                = const( 0x05 )
        p1_hl                = const( 0x06 )
        p1_weight            = const( 0x07 )
        p1_misc              = const( 0x08 )
        
        p2_xh                = const( 0x09 )
        p2_xl                = const( 0x0A )
        p2_yh                = const( 0x0B )
        p2_hl                = const( 0x0C )
        p2_weight            = const( 0x0D )
        p2_misc              = const( 0x0E )
        
        group                = const( 0x80 )
        th_diff              = const( 0x85 )
        ctrl                 = const( 0x86 )
        time_enter_monitor   = const( 0x87 )
        period_active        = const( 0x88 )
        period_monitor       = const( 0x89 )
        
        radian_value         = const( 0x91 )
        offset_left_right    = const( 0x92 )
        offset_up_down       = const( 0x93 )
        distance_left_right  = const( 0x94 )
        distance_up_down     = const( 0x95 )
        distance_zoom        = const( 0x96 )

        lib_ver_h            = const( 0xA1 )
        lib_ver_l            = const( 0xA2 )
        cipher               = const( 0xA3 )
        g_mode               = const( 0xA4 )
        pwr_mode             = const( 0xA5 )
        firmid               = const( 0xA6 )
        focaltech_id         = const( 0xA6 )
        release_code_id      = const( 0xA6 )
        state                = const( 0xA )

        
    # =======================================================================    

    def __init__(
        self,
        i2c: machine.I2C,
        size: xy = None,
        address: int = 0x38
    ):
        touch.__init__(
            self,
            size = size,
            span = 4096
        )
        self._i2c = i2c
        self._size = size
        self._address = address
        
    # =======================================================================        

    def touch_adcs( self ):
        
        status, x_high, x_low, y_high, y_low = \
            self._i2c.readfrom_mem( self._address, 2, 5 )
        
        if ( status & 0x03 ) == 0:
            return None, None
        
        else:
            x = ( ( x_high & 0x0F ) << 8 ) + x_low
            y = ( ( y_high & 0x0F ) << 8 ) + y_low
            return x, y
            
    # =======================================================================        

# ===========================================================================


