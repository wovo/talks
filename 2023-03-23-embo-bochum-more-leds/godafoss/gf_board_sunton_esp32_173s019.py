# ===========================================================================
#
# file     : gf_board_sunton_esp32_173s019.py
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

from micropython import const

import godafoss as gf
import machine


# ===========================================================================

class board_sunton_esp32_173s019:

    """
    sunton_sp32_173s019 board
    
    
    $insert_image( "sunton_esp32_173s019_front", 1, 200, width = 45 )
    $insert_image( "sunton_esp32_173s019_back", 1, 200, width = 45 )
    [MicroPython image](https://micropython.org/download/GENERIC_S3_SPIRAM_OCT/)
    
    +-----------+--------------------------------------------------------+
    | uC        | ESP32-S3 with SPIRAM (octal)                           |
    +-----------+--------------------------------------------------------+
    | Image     | ST7789 170 x 320 color                                 |
    +-----------+--------------------------------------------------------+
    | LCD       | ST7789 170 x 320 color                                 |
    +-----------+--------------------------------------------------------+
    | USB       | micro, CH340, boot & reset circuit,                    |
    |           | linear regulator                                       |
    +-----------+--------------------------------------------------------+
    | buttons   | boot, reset                                            |
    +-----------+--------------------------------------------------------+
    | misc.     | boot & reset buttons, SD card,                         |
    |           | connector, single-wire connector                       |
    +-----------+--------------------------------------------------------+

    This is an ESP32-S3 board with a color LCD 
    simple charge circuit (with linear regulators), a speaker interface,
    
    The names in the table below are available as attributes.
    
    +-----+----------------------------------------------------------------+
    | Pin | name                                                           |
    +-----+----------------------------------------------------------------+
    |   0 | boot_mode_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  12 | lcd_sclk_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  13 | lcd_mosi_pin                                                   |
    +-----+----------------------------------------------------------------+
    |  11 | lcd_rs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |  10 | lcd_cs_pin                                                     |
    +-----+----------------------------------------------------------------+
    |   1 | lcd_reset_pin                                                  |
    +-----+----------------------------------------------------------------+
    |  14 | lcd_backlight_pin                                              |
    +-----+----------------------------------------------------------------+
    
    $macro_insert board sunton_esp32_173s019
    
    http://www.jczn1688.com/zlxz
    """
    
    boot_mode_pin      = const(  0 )
        
    lcd_sclk_pin       = const( 12 )
    lcd_mosi_pin       = const( 13 )
    lcd_rs_pin         = const( 11 )
    lcd_cs_pin         = const( 10 )
    lcd_reset_pin      = const(  1 )
    lcd_backlight_pin  = const( 14 )      

    def __init__( self ):
        pass
           
    def display( self ):
        spi = gf.spi(
            id = 1,
            frequency = 30_000_000,
            sck = self.lcd_sclk_pin,
            mosi = self.lcd_mosi_pin,
            miso = 15 # dummy
        )        
        return gf.lcd(
            chip = "st7789",
            size = gf.xy( 170, 320 ), 
            spi = spi,
            data_command = self.lcd_rs_pin,
            chip_select = self.lcd_cs_pin,
            reset = self.lcd_reset_pin,
            backlight = self.lcd_backlight_pin,
            invert = True,
            offset = gf.xy( 35, 0 )
        )
        
# ===========================================================================
