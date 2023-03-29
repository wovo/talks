# ===========================================================================
#
# file     : gf_board_01space_rp2040_042lcd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains board-specific things.
#
# ===========================================================================

import godafoss as gf
import machine


# ===========================================================================

class board_01space_rp2040_042lcd:
    """
    `01space_rp2040_042lcd`_ board
    
    .. _01space_rp2040_042lcd: https://github.com/01Space/RP2040-0.42LCD
    
    $insert_image( "01space_rp2040_042lcd", 1, 300 )
    
    +-----------+--------------------------------------------------------+
    | uC        | RP2040                                                 |
    +-----------+--------------------------------------------------------+
    | OLED      | SSD1306 74 x 40 monochrome                             |
    +-----------+--------------------------------------------------------+
    | neopixel  | WS2812                                                 |
    +-----------+--------------------------------------------------------+
    | USB       | C                                                      |
    +-----------+--------------------------------------------------------+

    This is a very small RP2040 board with a 72 x 40 I2C oled, 
    a single neopixel, and two buttons for bootmode and reset.
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |  12 | neopixel_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  23 | i2c_scl_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  22 | i2c_sda_pin                                                    |
    +-----+----------------------------------------------------------------+
    |  21 | bootmode_pin                                                   |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board 01space_rp2040_042lcd
    """

    def __init__( self ):
        self.i2c_scl = 23
        self.i2c_sda = 22
        self.boot = 21
        self.neopixel_pin = 12
   
    def i2c( self ):
        """
        the (soft) I2C bus
        """    
        return machine.SoftI2C(
            scl = machine.Pin( self.i2c_scl, machine.Pin.OUT ),
            sda = machine.Pin( self.i2c_sda, machine.Pin.OUT )
        ) 
       
    def display( self ):
        """
        the oled display
        """    
        return gf.ssd1306_i2c( 
            size = gf.xy( 72, 40 ), 
            i2c = self.i2c 
        )
        
    def neopixel( self ):
        """
        the (single) neopixel
        """    
        return gf.ws281x( 
            pin = self.neopixel_pin, 
            n = 1
        )
    
# ===========================================================================
