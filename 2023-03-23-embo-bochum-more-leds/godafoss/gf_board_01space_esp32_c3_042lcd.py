# ===========================================================================
#
# file     : gf_board_01space_esp32_c3_042lcd.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the board object for the 01space_esp32_c3_042lcd.
#
# ===========================================================================

import godafoss as gf
import machine


# ===========================================================================

class board_01space_esp32_c3_042lcd:
    """
    `01space_esp32_c3_042lcd`_ board
    
    .. _01space_esp32_c3_042lcd: https://github.com/01Space/ESP32-C3-0.42LCD
    
    $insert_image( "01space_esp32_c3_042lcd", 1, 300 )
    
    +-----------+--------------------------------------------------------+
    | uC        | ESP32-C3                                               |
    +-----------+--------------------------------------------------------+
    | OLED      | SSD1306 74 x 40 monochrome                             |
    +-----------+--------------------------------------------------------+
    | neopixel  | WS2812                                                 |
    +-----------+--------------------------------------------------------+

    This is a very small ESP32 board with a 72 x 40 I2C oled, 
    a single neopixel, and two buttons for bootmode and reset.
    
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | Attribute name                                                 |
    +-----+----------------------------------------------------------------+
    |   2 | neopixel_pin                                                   |
    +-----+----------------------------------------------------------------+
    |   6 | i2c_scl_pin                                                    |
    +-----+----------------------------------------------------------------+
    |   5 | i2c_sda_pin                                                    |
    +-----+----------------------------------------------------------------+
    |   9 | bootmode_pin                                                   |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board 01space_esp32_c3_042lcd
    """
    
    # =======================================================================

    def __init__( self ) -> None:
        self.i2c_scl_pin = 6
        self.i2c_sda_pin = 5
        self.bootmode_pin = 9
        self.neopixel_pin = 2
   
    # =======================================================================

    def i2c( self ) -> machine.I2C:
        """
        the (soft) I2C bus
        """
        return machine.SoftI2C(
            scl = machine.Pin( self.i2c_scl_pin, machine.Pin.OUT ),
            sda = machine.Pin( self.i2c_sda_pin, machine.Pin.OUT )
        ) 
       
    # =======================================================================

    def display( self ) -> "canvas":
        """
        the oled display
        """
        return gf.ssd1306_i2c( 
            size = gf.xy( 72, 40 ), 
            i2c = self.i2c 
        )
        
    # =======================================================================

    def neopixel( self ) -> "canvas":
        """
        the (single) neopixel
        """
        return gf.ws281x( 
            pin = self.neopixel_pin_pin, 
            n = 1
        )
        
    # =======================================================================

# ===========================================================================
